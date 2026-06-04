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
