(function () {
  var BUSUANZI_SRC = "https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js";
  var VALINE_SRC = "https://unpkg.com/valine/dist/Valine.min.js";

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
      if (marker) script.dataset.zzScript = marker;
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  function localeText(section, zh, en) {
    return section.dataset.locale === "zh-CN" ? zh : en;
  }

  function getValineConfig() {
    var config = window.ZZ_ENGAGEMENT_CONFIG || {};
    return config.valine || {};
  }

  function initComments(section) {
    var mount = section.querySelector("[data-zz-valine]");
    var status = section.querySelector("[data-zz-engagement-status]");
    if (!mount || !status) return;

    var config = getValineConfig();
    if (!config.appId || !config.appKey) {
      mount.hidden = true;
      status.textContent = localeText(
        section,
        "留言区正在接入中。启用后访客不用登录，填个昵称就可以写。",
        "Comments are being connected. Once enabled, visitors can leave a name and write without logging in."
      );
      return;
    }

    status.textContent = localeText(section, "留言加载中...", "Loading comments...");
    loadScript(VALINE_SRC, "valine")
      .then(function () {
        if (!window.Valine) throw new Error("Valine did not load.");

        var valineOptions = {
          el: mount,
          appId: config.appId,
          appKey: config.appKey,
          path: section.dataset.pageKey || window.location.pathname,
          placeholder: localeText(section, "不用登录，留个名字就能聊。", "No login needed. Leave a name and say hi."),
          avatar: config.avatar || "mp",
          meta: ["nick", "mail", "link"],
          pageSize: config.pageSize || 8,
          recordIP: false,
          lang: section.dataset.locale === "zh-CN" ? "zh-CN" : "en"
        };

        if (config.serverURLs) valineOptions.serverURLs = config.serverURLs;
        new window.Valine(valineOptions);
        status.hidden = true;
        mount.hidden = false;
      })
      .catch(function () {
        mount.hidden = true;
        status.classList.add("is-error");
        status.textContent = localeText(
          section,
          "留言加载失败，稍后刷新页面再试。",
          "Comments failed to load. Please refresh and try again."
        );
      });
  }

  ready(function () {
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
