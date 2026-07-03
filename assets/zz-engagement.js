(function () {
  var BUSUANZI_SRC = "https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js";
  var SUPABASE_SRC = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2";

  function ready(callback) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback);
    } else {
      callback();
    }
  }

  function loadScript(src, marker) {
    if (marker && document.querySelector("script[data-zz-script='" + marker + "']")) {
      return Promise.resolve();
    }

    return new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      script.src = src;
      script.async = true;
      script.defer = true;
      if (marker) script.dataset.zzScript = marker;
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  function isRun50StoryPage() {
    var path = window.location.pathname.toLowerCase();
    if (!/\/run50\/(stories\/(chinese|english)|facebook)\//.test(path)) return false;
    if (/\/index\.html$/.test(path) || /\/$/.test(path)) return false;
    return /\.html$/.test(path);
  }

  function getStoredStoryTheme() {
    try {
      return window.localStorage.getItem("run50-story-theme");
    } catch (error) {
      return "";
    }
  }

  function storeStoryTheme(theme) {
    try {
      window.localStorage.setItem("run50-story-theme", theme);
    } catch (error) {
      return;
    }
  }

  function applyStoryTheme(theme) {
    document.documentElement.dataset.run50Theme = theme === "light" ? "light" : "dark";
  }

  function setInitialRun50StoryTheme() {
    if (!isRun50StoryPage()) return false;
    applyStoryTheme(getStoredStoryTheme() === "light" ? "light" : "dark");
    return true;
  }

  function injectRun50StoryTheme() {
    if (!isRun50StoryPage()) return;
    if (document.querySelector("[data-run50-theme-style]")) return;

    var style = document.createElement("style");
    style.dataset.run50ThemeStyle = "true";
    style.textContent = [
      "html[data-run50-theme='dark']{color-scheme:dark;background:#090d13;}",
      "html[data-run50-theme='dark'] body{background:linear-gradient(180deg,#101820 0,#090d13 340px)!important;color:#e7edf4!important;}",
      "html[data-run50-theme='dark'] a{color:#8fd3ff!important;}",
      "html[data-run50-theme='dark'] .story-nav,html[data-run50-theme='dark'] .page-footer,html[data-run50-theme='dark'] .meta,html[data-run50-theme='dark'] .byline,html[data-run50-theme='dark'] .section-nav{color:#a8b3c2!important;}",
      "html[data-run50-theme='dark'] h1,html[data-run50-theme='dark'] h2,html[data-run50-theme='dark'] h3,html[data-run50-theme='dark'] .wordmark,html[data-run50-theme='dark'] .article-body h2,html[data-run50-theme='dark'] .article-body h3,html[data-run50-theme='dark'] .zz-engagement h2{color:#f5f7fb!important;}",
      "html[data-run50-theme='dark'] .dek,html[data-run50-theme='dark'] .article-shell p,html[data-run50-theme='dark'] .article-shell li,html[data-run50-theme='dark'] .article-body p,html[data-run50-theme='dark'] .article-body li,html[data-run50-theme='dark'] .copy p,html[data-run50-theme='dark'] .copy li,html[data-run50-theme='dark'] .brief p{color:#d6dee8!important;}",
      "html[data-run50-theme='dark'] .article-shell,html[data-run50-theme='dark'] .site-head,html[data-run50-theme='dark'] .summary-box,html[data-run50-theme='dark'] .brief,html[data-run50-theme='dark'] .rail-card,html[data-run50-theme='dark'] .zz-engagement-card{background:#111820!important;border-color:#283442!important;box-shadow:0 24px 60px rgba(0,0,0,.38)!important;}",
      "html[data-run50-theme='dark'] .hero,html[data-run50-theme='dark'] figure,html[data-run50-theme='dark'] .copy figure,html[data-run50-theme='dark'] .zz-engagement-shell,html[data-run50-theme='dark'] .zz-comment-item{background:#111820!important;border-color:#283442!important;}",
      "html[data-run50-theme='dark'] .run50-global-tabs a{background:rgba(17,24,39,.78)!important;border-color:#344257!important;color:#e7edf4!important;box-shadow:none!important;}",
      "html[data-run50-theme='dark'] .run50-global-tabs a.active,html[data-run50-theme='dark'] .run50-global-tabs a[aria-current='page']{background:#263241!important;color:#ffffff!important;}",
      "html[data-run50-theme='dark'] .meta span,html[data-run50-theme='dark'] .meta a,html[data-run50-theme='dark'] .zz-engagement-stat{background:#151f2a!important;border-color:#2d3b4b!important;color:#b8c3d0!important;}",
      "html[data-run50-theme='dark'] .article-body figure img,html[data-run50-theme='dark'] .copy figure img,html[data-run50-theme='dark'] .lead-media img,html[data-run50-theme='dark'] .cover{background:#16212d!important;box-shadow:0 18px 48px rgba(0,0,0,.42)!important;}",
      "html[data-run50-theme='dark'] figcaption,html[data-run50-theme='dark'] .caption-line,html[data-run50-theme='dark'] .zz-engagement-note,html[data-run50-theme='dark'] .zz-engagement-status,html[data-run50-theme='dark'] .zz-comments-actions span,html[data-run50-theme='dark'] .zz-comment-meta span{color:#9caabd!important;}",
      "html[data-run50-theme='dark'] .zz-engagement-status{background:#151f2a!important;border-color:#2d3b4b!important;}",
      "html[data-run50-theme='dark'] .zz-comments-form label,html[data-run50-theme='dark'] .zz-comment-meta strong,html[data-run50-theme='dark'] .zz-comment-item p,html[data-run50-theme='dark'] .zz-comments-empty,html[data-run50-theme='dark'] .zz-engagement-stat strong{color:#e7edf4!important;}",
      "html[data-run50-theme='dark'] .zz-comments-form input,html[data-run50-theme='dark'] .zz-comments-form textarea{background:#0d141c!important;border-color:#2d3b4b!important;color:#e7edf4!important;}",
      "html[data-run50-theme='dark'] .site-head,html[data-run50-theme='dark'] .breaking{box-shadow:none!important;}",
      ".run50-story-cover-figure{margin:0 0 26px!important;border-radius:18px;overflow:hidden;border:1px solid rgba(15,23,42,.1);background:#ffffff;box-shadow:0 22px 54px rgba(15,23,42,.12);}",
      ".run50-story-cover-figure img{display:block;width:100%;height:auto;max-height:none;object-fit:contain;background:#0b0f14;}",
      ".run50-story-cover-figure figcaption{margin:0;padding:9px 12px;font:600 12px/1.4 -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;color:#64748b;background:rgba(248,250,252,.96);}",
      "html[data-run50-theme='dark'] .run50-story-cover-figure{background:#111820!important;border-color:#283442!important;box-shadow:0 24px 60px rgba(0,0,0,.38)!important;}",
      "html[data-run50-theme='dark'] .run50-story-cover-figure figcaption{background:#0f1721!important;color:#9caabd!important;}",
      ".run50-theme-toggle{position:fixed;z-index:9999;top:14px;right:14px;display:inline-flex;align-items:center;gap:8px;min-height:38px;padding:0 13px;border:1px solid rgba(17,24,39,.18);border-radius:999px;background:rgba(255,255,255,.86);color:#111827;font:700 13px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;letter-spacing:0;box-shadow:0 12px 34px rgba(15,23,42,.16);backdrop-filter:blur(14px);cursor:pointer;}",
      ".run50-theme-toggle::before{content:'';width:15px;height:15px;border-radius:50%;background:#111827;box-shadow:inset 5px -2px 0 #ffffff;}",
      ".run50-theme-toggle:hover{transform:translateY(-1px);}",
      "html[data-run50-theme='dark'] .run50-theme-toggle{border-color:rgba(255,255,255,.18);background:rgba(14,21,30,.82);color:#f5f7fb;box-shadow:0 14px 34px rgba(0,0,0,.34);}",
      "html[data-run50-theme='dark'] .run50-theme-toggle::before{background:#f8d66d;box-shadow:0 0 0 4px rgba(248,214,109,.12);}",
      ".run50-language-toggle{position:fixed;z-index:9999;top:58px;right:14px;display:inline-flex;align-items:center;justify-content:center;min-height:34px;padding:0 12px;border:1px solid rgba(17,24,39,.18);border-radius:999px;background:rgba(255,255,255,.86);color:#111827!important;text-decoration:none!important;font:800 13px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;letter-spacing:0;box-shadow:0 12px 34px rgba(15,23,42,.14);backdrop-filter:blur(14px);}",
      ".run50-language-toggle:hover{transform:translateY(-1px);}",
      "html[data-run50-theme='dark'] .run50-language-toggle{border-color:rgba(255,255,255,.18);background:rgba(14,21,30,.82);color:#f5f7fb!important;box-shadow:0 14px 34px rgba(0,0,0,.34);}",
      "@media (max-width:640px){.run50-theme-toggle{top:10px;right:10px;min-height:34px;padding:0 11px;font-size:12px;}.run50-language-toggle{top:50px;right:10px;min-height:32px;padding:0 11px;font-size:12px;}.run50-story-cover-figure{border-radius:14px;}}"
    ].join("\n");
    document.head.appendChild(style);
  }

  function initRun50StoryThemeToggle() {
    if (!isRun50StoryPage()) return;
    injectRun50StoryTheme();
    if (document.querySelector("[data-run50-theme-toggle]")) return;

    var button = document.createElement("button");
    button.type = "button";
    button.className = "run50-theme-toggle";
    button.dataset.run50ThemeToggle = "true";
    button.setAttribute("aria-live", "polite");

    function syncButton() {
      var isDark = document.documentElement.dataset.run50Theme !== "light";
      button.textContent = isDark ? "Light" : "Dark";
      button.setAttribute("aria-label", isDark ? "Switch to light theme" : "Switch to dark theme");
    }

    button.addEventListener("click", function () {
      var next = document.documentElement.dataset.run50Theme === "light" ? "dark" : "light";
      applyStoryTheme(next);
      storeStoryTheme(next);
      syncButton();
    });

    syncButton();
    document.body.appendChild(button);
  }

  function absoluteUrl(value) {
    if (!value) return "";
    try {
      return new URL(value, window.location.href).href;
    } catch (error) {
      return "";
    }
  }

  function equivalentImageUrl(first, second) {
    var a = absoluteUrl(first);
    var b = absoluteUrl(second);
    if (!a || !b) return false;
    try {
      var left = new URL(a);
      var right = new URL(b);
      return left.pathname.replace(/\/+/g, "/") === right.pathname.replace(/\/+/g, "/");
    } catch (error) {
      return a.split("?")[0] === b.split("?")[0];
    }
  }

  function getRun50StoryCoverUrl() {
    var meta = document.querySelector("meta[property='og:image'],meta[name='twitter:image']");
    return meta ? absoluteUrl(meta.getAttribute("content")) : "";
  }

  function findStoryContentRoot() {
    return document.querySelector(".article-shell") ||
      document.querySelector("article") ||
      document.querySelector(".article-body") ||
      document.querySelector(".copy") ||
      document.querySelector("main");
  }

  function insertRun50StoryCover() {
    if (!isRun50StoryPage()) return;
    if (document.querySelector("[data-run50-auto-cover]")) return;

    var coverUrl = getRun50StoryCoverUrl();
    var root = findStoryContentRoot();
    if (!coverUrl || !root) return;

    var firstImage = root.querySelector("img");
    if (firstImage && equivalentImageUrl(firstImage.currentSrc || firstImage.src, coverUrl)) return;

    var figure = document.createElement("figure");
    figure.className = "run50-story-cover-figure";
    figure.dataset.run50AutoCover = "true";

    var image = document.createElement("img");
    image.className = "run50-story-cover";
    image.src = coverUrl;
    image.alt = document.querySelector("h1") ? document.querySelector("h1").textContent.trim() : "Run50 story cover";
    image.loading = "eager";
    image.decoding = "async";

    var caption = document.createElement("figcaption");
    caption.textContent = "Cover";

    figure.appendChild(image);
    figure.appendChild(caption);
    root.insertBefore(figure, root.firstElementChild || root.firstChild);
  }

  function getRun50LanguageTarget() {
    var path = window.location.pathname;
    var lower = path.toLowerCase();
    var marker = lower.indexOf("/run50/");
    if (marker < 0) return null;

    var prefix = path.slice(0, marker);
    var englishMatch = lower.match(/\/run50\/stories\/english\/([^\/]+\.html)$/);
    var facebookMatch = lower.match(/\/run50\/facebook\/([^\/]+\.html)$/);
    var slug = englishMatch ? englishMatch[1] : (facebookMatch ? facebookMatch[1] : "");
    if (!slug) return null;

    return {
      href: prefix + "/run50/stories/chinese/" + slug,
      label: "中文"
    };
  }

  function initRun50LanguageToggle() {
    if (!isRun50StoryPage()) return;
    if (document.querySelector("[data-run50-language-toggle]")) return;

    var target = getRun50LanguageTarget();
    if (!target) return;

    var link = document.createElement("a");
    link.className = "run50-language-toggle";
    link.dataset.run50LanguageToggle = "true";
    link.href = target.href;
    link.textContent = target.label;
    link.setAttribute("aria-label", "Open Chinese version");
    document.body.appendChild(link);
  }

  function localeText(section, zh, en) {
    return section.dataset.locale === "zh-CN" ? zh : en;
  }

  function getSupabaseConfig() {
    var config = window.ZZ_ENGAGEMENT_CONFIG || {};
    return config.supabase || {};
  }

  function escapeHtml(value) {
    return String(value || "").replace(/[&<>"']/g, function (char) {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
      }[char];
    });
  }

  function formatTime(value, isZh) {
    try {
      return new Intl.DateTimeFormat(isZh ? "zh-CN" : "en", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
      }).format(new Date(value));
    } catch (error) {
      return value || "";
    }
  }

  function renderComments(section, list, comments) {
    var isZh = section.dataset.locale === "zh-CN";
    if (!comments.length) {
      list.innerHTML = '<p class="zz-comments-empty">' +
        localeText(section, "\u8fd8\u6ca1\u6709\u7559\u8a00\uff0c\u6765\u5199\u7b2c\u4e00\u6761\u5427\u3002", "No comments yet. Be the first to write one.") +
        "</p>";
      return;
    }

    list.innerHTML = comments.map(function (comment) {
      return [
        '<article class="zz-comment-item">',
        '<div class="zz-comment-meta">',
        '<strong>' + escapeHtml(comment.name) + '</strong>',
        '<span>' + escapeHtml(formatTime(comment.created_at, isZh)) + '</span>',
        '</div>',
        '<p>' + escapeHtml(comment.body).replace(/\n/g, "<br>") + '</p>',
        '</article>'
      ].join("");
    }).join("");
  }

  function buildCommentUi(section, mount) {
    mount.innerHTML = [
      '<form class="zz-comments-form" data-zz-comments-form>',
      '<div class="zz-comments-fields">',
      '<label><span>' + localeText(section, "\u6635\u79f0", "Name") + '</span><input name="name" maxlength="80" autocomplete="name" required></label>',
      '<label class="zz-comments-hp"><span>Company</span><input name="company" tabindex="-1" autocomplete="off"></label>',
      '</div>',
      '<label><span>' + localeText(section, "\u7559\u8a00", "Comment") + '</span><textarea name="body" maxlength="1200" rows="5" required></textarea></label>',
      '<div class="zz-comments-actions">',
      '<button type="submit">' + localeText(section, "\u53d1\u5e03\u7559\u8a00", "Post comment") + '</button>',
      '<span data-zz-comments-message></span>',
      '</div>',
      '</form>',
      '<div class="zz-comments-list" data-zz-comments-list></div>'
    ].join("");
  }

  function initComments(section) {
    var mount = section.querySelector("[data-zz-supabase-comments]");
    var status = section.querySelector("[data-zz-engagement-status]");
    if (!mount || !status) return;

    var config = getSupabaseConfig();
    if (!config.url || !config.anonKey) {
      mount.hidden = true;
      status.hidden = false;
      status.textContent = localeText(
        section,
        "Supabase \u7559\u8a00\u533a\u6b63\u5728\u63a5\u5165\u4e2d\u3002\u914d\u597d URL \u548c anon key \u540e\uff0c\u8bfb\u8005\u4e0d\u7528\u767b\u5f55\u5c31\u80fd\u76f4\u63a5\u7559\u8a00\u3002",
        "Supabase comments are being connected. Once the URL and anon key are set, readers can comment without logging in."
      );
      return;
    }

    var table = config.table || "story_comments";
    var pageKey = section.dataset.pageKey || window.location.pathname;
    var pageUrl = section.dataset.pageUrl || (window.location.origin + window.location.pathname);
    var pageTitle = section.dataset.pageTitle || document.title;

    mount.hidden = false;
    buildCommentUi(section, mount);

    var list = mount.querySelector("[data-zz-comments-list]");
    var form = mount.querySelector("[data-zz-comments-form]");
    var message = mount.querySelector("[data-zz-comments-message]");

    function setMessage(text, isError) {
      message.textContent = text || "";
      message.classList.toggle("is-error", !!isError);
    }

    function loadComments() {
      status.hidden = false;
      status.textContent = localeText(section, "\u7559\u8a00\u52a0\u8f7d\u4e2d...", "Loading comments...");
      return window.supabase
        .createClient(config.url, config.anonKey)
        .from(table)
        .select("id,name,body,created_at")
        .eq("page_id", pageKey)
        .order("created_at", { ascending: true })
        .limit(config.pageSize || 50)
        .then(function (result) {
          if (result.error) throw result.error;
          renderComments(section, list, result.data || []);
          status.hidden = true;
        })
        .catch(function () {
          status.classList.add("is-error");
          status.hidden = false;
          status.textContent = localeText(
            section,
            "\u7559\u8a00\u52a0\u8f7d\u5931\u8d25\uff0c\u7a0d\u540e\u5237\u65b0\u518d\u8bd5\u3002",
            "Comments failed to load. Please refresh and try again."
          );
        });
    }

    loadScript(SUPABASE_SRC, "supabase")
      .then(function () {
        return loadComments();
      })
      .catch(function () {
        mount.hidden = true;
        status.classList.add("is-error");
        status.textContent = localeText(
          section,
          "Supabase \u7559\u8a00\u811a\u672c\u52a0\u8f7d\u5931\u8d25\uff0c\u7a0d\u540e\u5237\u65b0\u518d\u8bd5\u3002",
          "The Supabase comments script failed to load. Please refresh and try again."
        );
      });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!window.supabase) return;

      var formData = new FormData(form);
      var name = String(formData.get("name") || "").trim();
      var body = String(formData.get("body") || "").trim();
      var company = String(formData.get("company") || "").trim();
      var submit = form.querySelector("button");

      if (company) {
        form.reset();
        setMessage(localeText(section, "\u5df2\u53d1\u5e03\u3002", "Posted."));
        return;
      }

      if (!name || !body) {
        setMessage(localeText(section, "\u8bf7\u586b\u5199\u6635\u79f0\u548c\u7559\u8a00\u3002", "Please add your name and comment."), true);
        return;
      }

      submit.disabled = true;
      setMessage(localeText(section, "\u53d1\u5e03\u4e2d...", "Posting..."));

      window.supabase
        .createClient(config.url, config.anonKey)
        .from(table)
        .insert({
          page_id: pageKey,
          page_url: pageUrl,
          page_title: pageTitle,
          name: name,
          body: body
        })
        .then(function (result) {
          if (result.error) throw result.error;
          form.reset();
          setMessage(localeText(section, "\u5df2\u53d1\u5e03\uff0c\u9875\u9762\u4e0b\u65b9\u5df2\u66f4\u65b0\u3002", "Posted. The list below has been updated."));
          return loadComments();
        })
        .catch(function () {
          setMessage(localeText(section, "\u53d1\u5e03\u5931\u8d25\uff0c\u7a0d\u540e\u518d\u8bd5\u3002", "Could not post. Please try again."), true);
        })
        .then(function () {
          submit.disabled = false;
        });
    });
  }

  setInitialRun50StoryTheme();

  ready(function () {
    initRun50StoryThemeToggle();
    insertRun50StoryCover();
    initRun50LanguageToggle();

    var sections = Array.prototype.slice.call(document.querySelectorAll("[data-zz-engagement]"));
    if (!sections.length) return;

    loadScript(BUSUANZI_SRC, "busuanzi").catch(function () {
      sections.forEach(function (section) {
        var count = section.querySelector("[data-zz-view-count]");
        if (count) count.textContent = "--";
      });
    });

    sections.forEach(initComments);
  });
}());
