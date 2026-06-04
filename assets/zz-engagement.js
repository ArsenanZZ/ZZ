(function () {
  var BUSUANZI_SRC = "https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js";
  var CUSDIS_SRC = "https://cusdis.com/js/cusdis.es.js";

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

  function localeText(section, zh, en) {
    return section.dataset.locale === "zh-CN" ? zh : en;
  }

  function getCusdisConfig() {
    var config = window.ZZ_ENGAGEMENT_CONFIG || {};
    return config.cusdis || {};
  }

  function initComments(section) {
    var mount = section.querySelector("[data-zz-cusdis]");
    var status = section.querySelector("[data-zz-engagement-status]");
    if (!mount || !status) return;

    var config = getCusdisConfig();
    if (!config.appId) {
      mount.hidden = true;
      status.textContent = localeText(
        section,
        "\u7559\u8a00\u5c06\u6539\u7528 Cusdis\u3002\u586b\u5165 Cusdis App ID \u540e\uff0c\u8bfb\u8005\u4e0d\u7528\u767b\u5f55\u5c31\u53ef\u4ee5\u63d0\u4ea4\u7559\u8a00\uff0c\u5ba1\u6838\u540e\u663e\u793a\u3002",
        "Comments will use Cusdis. Add a Cusdis App ID and readers can submit without logging in; comments appear after approval."
      );
      return;
    }

    var pageKey = section.dataset.pageKey || window.location.pathname;
    mount.hidden = false;
    mount.id = "cusdis_thread";
    mount.dataset.host = config.host || "https://cusdis.com";
    mount.dataset.appId = config.appId;
    mount.dataset.pageId = pageKey;
    mount.dataset.pageUrl = section.dataset.pageUrl || window.location.href;
    mount.dataset.pageTitle = section.dataset.pageTitle || document.title;
    mount.dataset.theme = config.theme || "light";

    status.textContent = localeText(section, "\u7559\u8a00\u52a0\u8f7d\u4e2d...", "Loading comments...");
    loadScript(CUSDIS_SRC, "cusdis")
      .then(function () {
        status.hidden = true;
      })
      .catch(function () {
        mount.hidden = true;
        status.classList.add("is-error");
        status.textContent = localeText(
          section,
          "\u7559\u8a00\u52a0\u8f7d\u5931\u8d25\uff0c\u7a0d\u540e\u5237\u65b0\u9875\u9762\u518d\u8bd5\u3002",
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
