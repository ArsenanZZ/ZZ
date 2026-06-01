(function () {
  function ready(callback) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback);
    } else {
      callback();
    }
  }

  function normalizePath() {
    var path = window.location.pathname.replace(/\/+/g, "/");
    if (path.endsWith("/")) path += "index.html";
    return path;
  }

  function getInitials(name) {
    var trimmed = name.trim();
    if (!trimmed) return "ZZ";
    return trimmed.slice(0, 2).toUpperCase();
  }

  function formatTime(value) {
    try {
      return new Intl.DateTimeFormat("zh-CN", {
        dateStyle: "medium",
        timeStyle: "short"
      }).format(new Date(value));
    } catch (error) {
      return value;
    }
  }

  function loadComments(key) {
    try {
      var parsed = JSON.parse(localStorage.getItem(key) || "[]");
      return Array.isArray(parsed) ? parsed : [];
    } catch (error) {
      return [];
    }
  }

  function saveComments(key, comments) {
    localStorage.setItem(key, JSON.stringify(comments));
  }

  function text(tag, className, value) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    node.textContent = value;
    return node;
  }

  ready(function () {
    var mount = document.querySelector("[data-zz-comments]");
    if (!mount) return;

    var key = "zz-comments:v1:" + normalizePath();
    var comments = loadComments(key);

    mount.className = "zz-comments";
    mount.innerHTML = [
      '<div class="zz-comments-head">',
      "  <div>",
      "    <h2>留言</h2>",
      '    <div class="zz-comments-note">保存在当前浏览器</div>',
      "  </div>",
      '  <div class="zz-comments-count" data-zz-count></div>',
      "</div>",
      '<form class="zz-comments-form" data-zz-form>',
      '  <div class="zz-comments-row">',
      '    <input name="name" type="text" maxlength="28" placeholder="名字" autocomplete="name">',
      '    <textarea name="message" maxlength="1200" placeholder="写下你的想法" required></textarea>',
      "    <button type=\"submit\">发布</button>",
      "  </div>",
      "</form>",
      '<div class="zz-comments-list" data-zz-list></div>'
    ].join("");

    var countNode = mount.querySelector("[data-zz-count]");
    var form = mount.querySelector("[data-zz-form]");
    var list = mount.querySelector("[data-zz-list]");

    function render() {
      list.textContent = "";
      countNode.textContent = comments.length + " 条留言";

      if (!comments.length) {
        list.appendChild(text("p", "zz-comments-empty", "还没有留言。"));
        return;
      }

      comments.slice().reverse().forEach(function (comment) {
        var item = document.createElement("article");
        item.className = "zz-comment";

        var avatar = text("div", "zz-comment-avatar", getInitials(comment.name));
        var body = document.createElement("div");
        var name = text("p", "zz-comment-name", comment.name || "ZZ Visitor");
        var time = text("div", "zz-comment-time", formatTime(comment.createdAt));
        var message = text("p", "zz-comment-text", comment.message);

        body.appendChild(name);
        body.appendChild(time);
        body.appendChild(message);
        item.appendChild(avatar);
        item.appendChild(body);
        list.appendChild(item);
      });
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = new FormData(form);
      var message = String(data.get("message") || "").trim();
      if (!message) return;

      comments.push({
        id: String(Date.now()),
        name: String(data.get("name") || "").trim() || "ZZ Visitor",
        message: message,
        createdAt: new Date().toISOString()
      });

      saveComments(key, comments);
      form.reset();
      render();
    });

    render();
  });
}());
