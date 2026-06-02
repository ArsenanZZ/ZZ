(function () {
  var REPO = "ArsenanZZ/ZZ";
  var ISSUE_LABEL = "comments";

  function ready(callback) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback);
    } else {
      callback();
    }
  }

  function make(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function createUtterancesScript() {
    var script = document.createElement("script");
    script.src = "https://utteranc.es/client.js";
    script.async = true;
    script.crossOrigin = "anonymous";
    script.setAttribute("repo", REPO);
    script.setAttribute("issue-term", "pathname");
    script.setAttribute("label", ISSUE_LABEL);
    script.setAttribute("theme", "github-light");
    return script;
  }

  ready(function () {
    var mount = document.querySelector("[data-zz-comments]");
    if (!mount) return;

    mount.className = "zz-comments";
    mount.setAttribute("aria-labelledby", "zz-comments-title");
    mount.innerHTML = "";

    var shell = make("div", "zz-comments-shell");
    var intro = make("div", "zz-comments-intro");
    var eyebrow = make("div", "zz-comments-eyebrow", "GitHub Issues");
    var title = make("h2", null, "公开留言");
    var note = make(
      "p",
      "zz-comments-note",
      "留言会公开保存在这个仓库里，登录 GitHub 后即可发布。"
    );
    var status = make("p", "zz-comments-status", "正在载入留言...");
    var panel = make("div", "zz-comments-panel");

    title.id = "zz-comments-title";
    panel.setAttribute("data-zz-comments-panel", "");

    intro.appendChild(eyebrow);
    intro.appendChild(title);
    intro.appendChild(note);
    panel.appendChild(status);
    shell.appendChild(intro);
    shell.appendChild(panel);
    mount.appendChild(shell);

    var script = createUtterancesScript();
    script.addEventListener("load", function () {
      status.remove();
    });
    script.addEventListener("error", function () {
      status.textContent = "留言载入失败，请稍后刷新页面。";
      status.className = "zz-comments-status is-error";
    });

    panel.appendChild(script);
  });
}());
