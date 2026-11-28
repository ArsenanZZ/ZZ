/* Rich-text export for the marathon articles. */
(() => {
  'use strict';
  const button = document.getElementById('copy-wechat');
  const status = document.getElementById('copy-status');
  const article = document.querySelector('main[data-edition]');
  if (!button || !status || !article) return;

  // Keep the bytes, photo order and captions for the page the reader actually opened.
  // Detached HTML documents also let link-mode exports serialize images without fetching them.
  const clipboardDocument = document.implementation.createHTMLDocument('');
  const snapshot = clipboardDocument.importNode(article, true);
  const children = Array.from(snapshot.children);
  const useDisplayed = snapshot.hasAttribute('data-copy-displayed');
  const fullLinks = snapshot.hasAttribute('data-copy-full-links');
  const chunkTarget = 9500000;
  const oversizedFullExport = 512 * 1024 * 1024;

  function exportImages(node) {
    const selector = 'img, .down';
    const images = Array.from(node.querySelectorAll(selector));
    if (node.matches(selector)) images.unshift(node);
    return images.filter(el => !el.closest('.masthead, .byline, .chapter-number, script, style, button') &&
      !(el.tagName === 'IMG' && el.closest('.down') !== null && !el.matches('.down')));
  }

  function encodedImageBytes(node, mode = 'embedded') {
    return exportImages(node).reduce((sum, image) => {
      const bytes = mode === 'displayed' ? image.dataset.displayBytes ?? image.dataset.copyBytes : image.dataset.copyBytes;
      return sum + 4 * Math.ceil(Number(bytes || 0) / 3);
    }, 0);
  }

  function splitLargeFigure(figure) {
    const photos = Array.from(figure.querySelectorAll('img'));
    if (figure.tagName !== 'FIGURE' || photos.length < 2) return [figure];
    const caption = figure.querySelector('figcaption');
    const captionText = caption ? caption.textContent : '';
    const parts = captionText.split('；');
    const labels = photos.map(img => img.getAttribute('alt'));
    const grouped = captionText.startsWith(labels.join('；') + ' · 摄影 / ');
    const individual = parts.length === photos.length &&
      parts.every((line, i) => line.startsWith(labels[i] + ' · 摄影 / '));
    return photos.map((img, i) => {
      const unit = figure.cloneNode(false);
      unit.append(img.cloneNode(true));
      if (grouped || individual) {
        const credit = caption.cloneNode(false);
        credit.textContent = individual ? parts[i] : labels[i] + captionText.slice(labels.join('；').length);
        unit.append(credit);
      } else if (caption && i === photos.length - 1) {
        // Keep a free-form caption intact with the group's final picture.
        unit.append(caption.cloneNode(true));
      }
      return unit;
    });
  }

  function originalChunks(nodes) {
    const chunks = [];
    let current = {nodes: [], bytes: 0};
    for (const node of nodes) {
      const units = encodedImageBytes(node) + 12000 > chunkTarget ? splitLargeFigure(node) : [node];
      for (const unit of units) {
        const bytes = 12000 + encodedImageBytes(unit);
        if (current.nodes.length && current.bytes + bytes > chunkTarget) {
          chunks.push(current);
          current = {nodes: [], bytes: 0};
        }
        current.nodes.push(unit);
        current.bytes += bytes;
      }
    }
    if (current.nodes.length) chunks.push(current);
    return chunks;
  }

  const starts = [0, ...children.flatMap((el, i) => el.classList.contains('chapter') || el.classList.contains('ending') ? [i] : [])];
  const chunks = snapshot.hasAttribute('data-copy-chunks') ? originalChunks(children) : [];
  const scopes = new Map([['all', children]]);
  const scope = document.createElement('select');
  scope.setAttribute('aria-label', '选择全文或分段复制');
  scope.style.cssText = 'max-width:180px;padding:9px 6px;font-size:13px;color:inherit;background:transparent;border:1px solid #888;border-radius:4px;';
  scope.add(new Option('全文复制', 'all'));
  starts.forEach((start, i) => {
    const key = String(i);
    scopes.set(key, children.slice(start, starts[i + 1] ?? children.length));
    const title = i === 0 ? '分段：开篇' : children[start].classList.contains('ending') ? '分段：结尾和署名' : `分段：第 ${i} 章`;
    scope.add(new Option(title, key));
  });
  chunks.forEach((chunk, i) => {
    const key = 'part-' + i;
    scopes.set(key, chunk.nodes);
    const size = (chunk.bytes / 1000000).toFixed(1);
    const note = chunk.bytes > 10000000 ? '，超 10 MB' : '';
    scope.add(new Option(`原图小段 ${i + 1}/${chunks.length}（约 ${size} MB${note}）`, key));
  });
  button.before(scope);
  const imageMode = document.createElement('select');
  imageMode.setAttribute('aria-label', '图片复制方式');
  imageMode.style.cssText = scope.style.cssText;
  if (useDisplayed) imageMode.add(new Option('正文图片（与网页一致）', 'displayed'));
  imageMode.add(new Option('原始大图（不压缩）', 'embedded'));
  imageMode.add(new Option('带原图链接（不嵌入）', 'links'));
  const defaultMode = useDisplayed ? 'displayed' : fullLinks ? 'links' : 'embedded';
  imageMode.value = defaultMode;
  button.before(imageMode);
  function showEstimate() {
    status.textContent = '';
    if (!useDisplayed) return;
    if (imageMode.value === 'links') {
      status.textContent = '仅复制图片链接，粘贴后需联网加载。';
      return;
    }
    const selected = scopes.get(scope.value);
    const total = selected.reduce((sum, node) => sum + encodedImageBytes(node, imageMode.value), 0);
    const mb = (total / 1000000).toFixed(1);
    status.textContent = imageMode.value === 'displayed'
      ? `所选正文图片嵌入后约 ${mb} MB，复制时保留网页画质。`
      : `所选原始大图嵌入后约 ${mb} MB。`;
  }
  scope.addEventListener('change', () => {
    if (scope.value.startsWith('part-')) imageMode.value = 'embedded';
    else if (scope.value === 'all') imageMode.value = defaultMode;
    showEstimate();
  });
  imageMode.addEventListener('change', showEstimate);
  showEstimate();
  const themeButtons = document.querySelectorAll('[data-theme-choice]');
  function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    document.querySelectorAll('.brand-intro [data-light-src]').forEach(el => el.setAttribute(el.tagName === 'SOURCE' ? 'srcset' : 'src', el.getAttribute('data-' + theme + '-src')));
    themeButtons.forEach(el => el.setAttribute('aria-pressed', String(el.dataset.themeChoice === theme)));
    showEstimate();
  }
  themeButtons.forEach(el => el.addEventListener('click', () => setTheme(el.dataset.themeChoice)));
  const canonical = 'https://zhennanzhang.com' + location.pathname;
  async function buildClipboard() {
    const selected = scopes.get(scope.value);
    if (!selected) throw new Error('请选择要复制的范围');
    if ((fullLinks || useDisplayed) && scope.value === 'all' && imageMode.value === 'embedded'
        && selected.reduce((sum, node) => sum + encodedImageBytes(node), 0) > oversizedFullExport) {
      const message = useDisplayed
        ? '请选择“正文图片（与网页一致）”一次复制全部图文；如需原始大图，可选择“原图小段”。'
        : '请选择原图小段按顺序粘贴，或选择带原图链接复制全文。';
      throw new Error('全文嵌入原始大图会超过 512 MiB。' + message);
    }
    const expectedImages = selected.flatMap(exportImages);
    const dark = document.documentElement.dataset.theme === 'dark';
    const theme = dark ? 'dark' : 'light';
    const ink = dark ? '#ece9e2' : '#262626';
    const muted = dark ? '#aaaaaa' : '#888888';
    const base = 'https://zhennanzhang.com/assets/louisiana-wechat-copy/';
    const wrapper = clipboardDocument.createElement('section');
    wrapper.exportImageCount = expectedImages.length;
    wrapper.exportPhotoCount = expectedImages.filter(el => el.hasAttribute('data-photo-id')).length;
    wrapper.style.cssText = `padding:0 4px 16px;background-color:${dark ? '#191919' : '#ffffff'};color:${ink};font-size:15px;line-height:1.95;text-align:left;font-family:Arial,"Microsoft YaHei",sans-serif;`;
    function convert(node) {
      if (node.nodeType === Node.TEXT_NODE) return clipboardDocument.createTextNode(node.textContent);
      if (node.nodeType !== Node.ELEMENT_NODE) return clipboardDocument.createTextNode('');
      const tag = node.tagName.toLowerCase();
      if (node.classList.contains('masthead') || node.classList.contains('byline')) return clipboardDocument.createTextNode('');
      if (['script','style','source','button'].includes(tag)) return clipboardDocument.createTextNode('');
      const number = node.classList.contains('chapter-number');
      const down = node.classList.contains('down');
      // Native text survives WeChat dark mode without a full-width image background.
      if (number) {
        const p = clipboardDocument.createElement('p');
        p.textContent = node.textContent.trim();
        p.style.cssText = 'font-family:Arial,sans-serif;font-size:74px;line-height:1.15;color:' + ink + ';background-color:transparent;margin:0 0 14px;padding:0;font-weight:400;text-align:left;';
        return p;
      }
      if (tag === 'img' || down) {
        const img = clipboardDocument.createElement('img');
        let url;
        if (down) url = base + 'arrows-' + theme + '.png';
        else {
          // The article builder publishes one 1600w display asset per photograph.
          const preview = imageMode.value === 'displayed' ? node.getAttribute('srcset')?.split(',')[0].trim().split(/\s+/)[0] : null;
          const src = node.getAttribute('data-' + theme + '-src') || preview || node.getAttribute('data-copy-src') || node.getAttribute('src');
          url = new URL(src, canonical).href;
        }
        img.src = url;
        img.alt = down ? '向下' : node.getAttribute('alt') || '';
        img.style.cssText = `display:block;width:100%;max-width:100%;height:auto;margin:${down ? '24px 0 30px' : '0'};border:0;`;
        if (node.closest('.poster-window')) img.style.cssText='display:block;width:104%;max-width:none;height:auto;margin:-2%;border:0;';
        if (node.closest('.brand-intro')) {
          img.width = 96;
          img.height = 120;
          img.style.cssText = 'display:inline-block;width:96px;max-width:96px;height:auto;margin:0;border:0;vertical-align:middle;';
        }
        return img;
      }
      const inline = ['strong','b','em','i','u','span','a'].includes(tag);
      const outputTag = tag === 'h2' && node.closest('.ending') ? 'p' : ['p','br','strong','b','em','i','u','span','a','h1','h2'].includes(tag) ? tag : tag === 'figcaption' ? 'p' : 'section';
      const out = clipboardDocument.createElement(outputTag);
      if (inline) {
        if (node.hasAttribute('data-cn-tone')) {
          const palette = dark ? ['#f09589','#85c9a6','#91bce8','#e8c481'] : ['#ac4336','#237953','#306eaa','#9a681c'];
          out.style.color = palette[Number(node.getAttribute('data-cn-tone'))] || palette[2];
          out.style.fontWeight = '800';
          if (node.getAttribute('data-cn-emphasis') === 'underline') {
            out.style.textDecoration = 'underline';
            out.style.textUnderlineOffset = '4px';
          }
        }

        if (tag === 'strong' || tag === 'b') out.style.fontWeight = '800';
        if (tag === 'em' || tag === 'i') out.style.fontStyle = 'italic';
        if (tag === 'u') out.style.textDecoration = 'underline';
        if (tag === 'a' && node.hasAttribute('href')) out.href = new URL(node.getAttribute('href'), canonical).href;
      } else if (tag !== 'br') {
        out.style.cssText = 'margin:0;padding:0;font-size:15px;line-height:1.95;text-align:left;';
        if (tag === 'p') out.style.marginBottom = '22px';
        if (node.classList.contains('prose') || node.closest('.intro')) out.style.textAlign = 'justify';
        if (tag === 'h1') out.style.cssText = 'margin:0 0 18px;font-size:25px;line-height:1.6;text-align:center;font-weight:700;';
        if (tag === 'h2') out.style.cssText = 'margin:0;font-size:20px;line-height:1.65;text-align:left;font-weight:700;';
        if (tag === 'figure') out.style.margin = '32px 0 36px';
        if (node.classList.contains('poster-window')) out.style.cssText='overflow:hidden;border:1px solid #b7a77d;margin:0;padding:0;';
        if (node.classList.contains('cover')) out.style.margin = '0 0 24px';
        if (tag === 'figcaption' || node.classList.contains('byline') || node.classList.contains('credits')) out.style.cssText = `margin:10px 0 22px;font-size:12px;line-height:1.9;text-align:center;color:${muted};`;
        if (node.classList.contains('chapter')) out.style.margin = '58px 0 34px';
        if (node.classList.contains('chapter-label')) out.style.cssText = `margin:18px 0 10px;font-size:11px;line-height:1.8;text-align:left;color:${muted};`;
        if (node.classList.contains('intro')) out.style.marginBottom = '54px';
        if (node.classList.contains('brand-intro')) out.style.cssText = 'margin:0 0 4px;padding:0;font-size:12px;line-height:1.5;text-align:center;';
        if (node.classList.contains('ending')) out.style.cssText = 'margin:64px 0 0;padding:32px 0 0;border-top:1px solid #888;font-size:14px;line-height:1.95;text-align:center;';
        if (node.closest('.ending')) {
          out.style.textAlign = 'center';
          out.setAttribute('align', 'center');
          if (tag === 'h2') out.style.cssText = 'margin:0;padding:0;font-size:24px;line-height:1.65;text-align:center;font-weight:700;';
          if (node.classList.contains('closing')) out.style.cssText = 'margin:0;padding:24px 0 0;font-size:13px;line-height:1.9;text-align:center;';
          if (node.classList.contains('credits')) out.style.marginTop = '36px';
        }
      }
      for (const child of node.childNodes) out.append(convert(child));
      return out;
    }
    for (const node of selected) wrapper.append(convert(node));
    const images = Array.from(wrapper.querySelectorAll('img'));
    if (images.length !== wrapper.exportImageCount ||
        (scope.value === 'all' && snapshot.hasAttribute('data-copy-photo-count') &&
         wrapper.exportPhotoCount !== Number(snapshot.dataset.copyPhotoCount))) {
      throw new Error('当前文章图片不完整，请刷新后再复制。');
    }
    if (imageMode.value !== 'links') {
      const abort = new AbortController();
      let next = 0, completed = 0;
      const readImage = blob => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(new Error('读取图片失败，请重试。'));
        reader.readAsDataURL(blob);
      });
      async function embedImages() {
        while (next < images.length && !abort.signal.aborted) {
          const img = images[next++];
          const url = new URL(img.src);
          const response = await fetch(url.pathname + url.search, {signal: abort.signal});
          if (!response.ok) throw new Error('图片加载失败：' + (img.alt || url.pathname));
          const blob = await response.blob();
          if (!blob.size || !blob.type.startsWith('image/')) {
            throw new Error('未能读取图片：' + (img.alt || url.pathname));
          }
          const src = await readImage(blob);
          if (abort.signal.aborted) return;
          img.src = src;
          status.textContent = `正在准备图片 ${++completed}/${images.length}…`;
        }
      }
      try {
        await Promise.all(Array.from({length: Math.min(4, images.length)}, embedImages));
      } finally {
        abort.abort();
      }
    }
    return wrapper;
  }

  async function preparePayload() {
    const wrapper = await buildClipboard();
    const html = wrapper.outerHTML;
    const text = wrapper.textContent;
    return {
      html, text,
      htmlBlob: new Blob([html], {type: 'text/html'}),
      textBlob: new Blob([text], {type: 'text/plain'}),
      photos: wrapper.exportPhotoCount,
      images: wrapper.exportImageCount
    };
  }

  function writeCopyEvent(event, payload) {
    if (!event.clipboardData) return false;
    event.preventDefault();
    event.clipboardData.setData('text/html', payload.html);
    event.clipboardData.setData('text/plain', payload.text);
    return true;
  }

  function copySelection(payload) {
    // The copy event supplies the HTML. Selecting a short placeholder keeps the images
    // out of the live document and avoids a second set of downloads in link mode.
    const holder = document.createElement('span');
    holder.style.cssText = 'position:fixed;left:-10000px;top:0';
    holder.textContent = '复制图文';
    document.body.append(holder);
    const selection = window.getSelection();
    const previous = selection.rangeCount ? selection.getRangeAt(0).cloneRange() : null;
    let handled = false;
    function onCopy(event) {
      handled = writeCopyEvent(event, payload);
    }
    document.addEventListener('copy', onCopy);
    try {
      const range = document.createRange();
      range.selectNodeContents(holder);
      selection.removeAllRanges();
      selection.addRange(range);
      return document.execCommand('copy') && handled;
    } catch {
      return false;
    } finally {
      document.removeEventListener('copy', onCopy);
      holder.remove();
      selection.removeAllRanges();
      if (previous) selection.addRange(previous);
    }
  }

  function writeOnClick(preparing) {
    if (!navigator.clipboard || !window.ClipboardItem) return null;
    // Safari requires write() during the click, even if preparing the image bytes takes time.
    const html = preparing.then(payload => payload.htmlBlob);
    const text = preparing.then(payload => payload.textBlob);
    // A browser may reject the operation before inspecting either promised representation.
    html.catch(() => {});
    text.catch(() => {});
    try {
      return navigator.clipboard.write([new ClipboardItem({'text/html': html, 'text/plain': text})])
        .then(() => true, () => false);
    } catch {
      return null;
    }
  }

  function reportCopied(payload) {
    const size = payload.htmlBlob.size + payload.textBlob.size;
    const mb = (size / 1000000).toFixed(2);
    const title = scope.value === 'all' ? '全文' : scope.selectedOptions[0].text.split('（')[0];
    const count = payload.photos ? `含 ${payload.photos} 张照片` : `含 ${payload.images} 幅配图`;
    const mode = {
      displayed: '正文图片已嵌入',
      embedded: '原图已嵌入',
      links: '图片使用原图链接'
    }[imageMode.value];
    status.textContent = `${title}已复制，${count}，${mode}（${mb} MB）。` +
      (imageMode.value === 'embedded' && size >= 10000000 ? '如粘贴失败，可选择较小的分段。' : '');
  }

  // A user-initiated keyboard copy can still write rich text in browsers that block
  // both programmatic clipboard APIs. Only handle a copy from this selected field.
  function offerKeyboardCopy(payload) {
    const field = document.createElement('input');
    field.readOnly = true;
    field.value = '按 ⌘C 或 Ctrl+C 复制图文';
    field.setAttribute('aria-label', field.value);
    field.addEventListener('copy', event => {
      if (writeCopyEvent(event, payload)) {
        retry = null;
        reportCopied(payload);
      }
    });
    status.append(' ', field);
    field.focus({preventScroll: true});
    field.select();
  }

  let retry = null;
  async function copyArticle() {
    const key = [scope.value, imageMode.value, document.documentElement.dataset.theme].join('|');
    const cached = retry && retry.key === key ? retry.payload : null;
    retry = null;
    button.disabled = true;
    scope.disabled = imageMode.disabled = true;
    themeButtons.forEach(el => { el.disabled = true; });
    status.textContent = '正在准备图文…';
    try {
      const preparing = cached ? Promise.resolve(cached) : preparePayload();
      const selectedCopy = cached && copySelection(cached);
      const writing = selectedCopy ? null : writeOnClick(preparing);
      const payload = await preparing;
      if (!selectedCopy && !(writing && await writing) && !copySelection(payload)) {
        retry = {key, payload};
        throw new Error('浏览器未允许自动复制。可再点一次，或用下方快捷键复制。');
      }
      reportCopied(payload);
    } catch (error) {
      status.textContent = error.message || '复制未成功，请重试。';
      if (retry) offerKeyboardCopy(retry.payload);
    } finally {
      button.disabled = false;
      scope.disabled = imageMode.disabled = false;
      themeButtons.forEach(el => { el.disabled = false; });
    }
  }
  button.addEventListener('click', copyArticle);
})();
