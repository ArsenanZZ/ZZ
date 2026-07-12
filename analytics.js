(function () {
  var firebaseConfig = {
    apiKey: "",
    authDomain: "",
    projectId: "",
    appId: ""
  };
  var tagManagerContainerId = "GTM-N8V3FBNM";

  function hasFirebaseConfig() {
    return Boolean(
      firebaseConfig.apiKey &&
      firebaseConfig.authDomain &&
      firebaseConfig.projectId &&
      firebaseConfig.appId
    );
  }

  function canUseLocalFallback() {
    return /^(localhost|127\.0\.0\.1)$/i.test(location.hostname);
  }

  function setupGoogleTagManager() {
    if (!tagManagerContainerId) return;
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      "gtm.start": new Date().getTime(),
      event: "gtm.js"
    });

    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtm.js?id=" + encodeURIComponent(tagManagerContainerId);
    document.head.appendChild(script);
  }

  function isArticlePage() {
    return Boolean(
      document.querySelector(".wechat-en-page .wechat-en-article") &&
      /\/run50\/wechat-en\/[^/]+\.html$/i.test(location.pathname)
    );
  }

  function articleId() {
    return location.pathname
      .replace(/\/index\.html$/i, "/")
      .replace(/^\/+|\/+$/g, "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "")
      .slice(0, 120);
  }

  function articleTitle() {
    return (
      document.querySelector(".wechat-en-header h1")?.textContent ||
      document.title ||
      location.pathname
    ).trim();
  }

  function formatNumber(value) {
    return new Intl.NumberFormat("en-US").format(Number(value || 0));
  }

  function formatDate(value) {
    try {
      return new Intl.DateTimeFormat("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric"
      }).format(new Date(value));
    } catch (error) {
      return "";
    }
  }

  function escapeHtml(value) {
    return String(value || "").replace(/[&<>"']/g, function (char) {
      return ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
      })[char];
    });
  }

  function injectStyles() {
    if (document.getElementById("zz-engagement-style")) return;
    var style = document.createElement("style");
    style.id = "zz-engagement-style";
    style.textContent = [
      ".zz-live-engagement{width:min(920px,100%);margin:34px auto 0;color:#dbe7f6}",
      ".zz-live-card{border:1px solid rgba(148,163,184,.25);border-radius:10px;background:#10192c;padding:20px;box-shadow:0 18px 44px rgba(0,0,0,.22)}",
      ".zz-live-head{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:16px}",
      ".zz-live-kicker{margin:0 0 5px;color:#7dd3fc;font-size:12px;font-weight:950;letter-spacing:.12em;text-transform:uppercase}",
      ".zz-live-head h2{margin:0;color:#f8fbff;font-size:24px;line-height:1.2}",
      ".zz-live-stats{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}",
      ".zz-live-stat{display:inline-flex;gap:7px;align-items:center;border:1px solid rgba(125,211,252,.24);border-radius:999px;padding:7px 11px;color:#c8d5e7;font-size:13px;font-weight:850}",
      ".zz-comment-list{display:grid;gap:10px;margin:14px 0 16px}",
      ".zz-comment{border:1px solid rgba(148,163,184,.18);border-radius:8px;background:rgba(255,255,255,.035);padding:12px 13px}",
      ".zz-comment-meta{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:5px;color:#9ee7c0;font-size:12px;font-weight:900}",
      ".zz-comment-time{color:#8fa1b8;font-weight:750}",
      ".zz-comment p{margin:0;color:#dbe7f6;line-height:1.65}",
      ".zz-comment-empty{margin:0;color:#a8b7cc;font-style:italic}",
      ".zz-comment-form{display:grid;gap:10px}",
      ".zz-comment-form input,.zz-comment-form textarea{width:100%;border:1px solid rgba(148,163,184,.24);border-radius:8px;background:#0b1020;color:#f8fbff;padding:11px 12px;font:inherit}",
      ".zz-comment-form textarea{min-height:112px;resize:vertical}",
      ".zz-comment-form button{justify-self:start;border:0;border-radius:999px;background:#9ee7c0;color:#07130d;padding:10px 16px;font-weight:950;cursor:pointer}",
      ".zz-comment-form button:disabled{opacity:.58;cursor:not-allowed}",
      ".zz-comment-status{min-height:20px;margin:0;color:#a8b7cc;font-size:13px}",
      "html[data-theme=light] .zz-live-engagement{color:#26343f}",
      "html[data-theme=light] .zz-live-card{background:#fff;border-color:#d9e2ec;box-shadow:0 18px 44px rgba(15,23,42,.08)}",
      "html[data-theme=light] .zz-live-head h2{color:#162636}",
      "html[data-theme=light] .zz-live-stat,html[data-theme=light] .zz-comment-status,html[data-theme=light] .zz-comment-empty{color:#526170}",
      "html[data-theme=light] .zz-comment{background:#f7fbff;border-color:#d9e2ec}",
      "html[data-theme=light] .zz-comment p{color:#26343f}",
      "html[data-theme=light] .zz-comment-form input,html[data-theme=light] .zz-comment-form textarea{background:#fff;color:#162636;border-color:#d0dbe8}",
      "@media(max-width:700px){.zz-live-engagement{width:100%;}.zz-live-card{border-radius:8px;padding:16px}.zz-live-head{display:block}.zz-live-stats{justify-content:flex-start;margin-top:12px}}"
    ].join("");
    document.head.appendChild(style);
  }

  function createEngagementShell() {
    var section = document.createElement("section");
    section.className = "zz-live-engagement";
    section.setAttribute("aria-label", "Reader comments and visits");
    section.innerHTML = [
      '<div class="zz-live-card">',
      '  <div class="zz-live-head">',
      '    <div><p class="zz-live-kicker">READERS</p><h2>Comments & visits</h2></div>',
      '    <div class="zz-live-stats">',
      '      <span class="zz-live-stat"><span data-zz-views>0</span> views</span>',
      '      <span class="zz-live-stat"><span data-zz-comment-count>0</span> comments</span>',
      "    </div>",
      "  </div>",
      '  <div class="zz-comment-list" data-zz-comment-list><p class="zz-comment-empty">No comments yet. Be the first to leave a note.</p></div>',
      '  <form class="zz-comment-form" data-zz-comment-form>',
      '    <input name="name" maxlength="40" autocomplete="name" placeholder="Your name" required>',
      '    <textarea name="message" maxlength="800" placeholder="Leave a comment" required></textarea>',
      '    <button type="submit">Post comment</button>',
      '    <p class="zz-comment-status" data-zz-comment-status></p>',
      "  </form>",
      "</div>"
    ].join("");
    return section;
  }

  function localStore(articleKey) {
    var statKey = "zz-local-stats:" + articleKey;
    var commentsKey = "zz-local-comments:" + articleKey;
    return {
      async incrementView() {
        var stats = JSON.parse(localStorage.getItem(statKey) || '{"views":0}');
        var viewedKey = "zz-viewed-session:" + articleKey;
        if (!sessionStorage.getItem(viewedKey)) {
          stats.views = Number(stats.views || 0) + 1;
          sessionStorage.setItem(viewedKey, "1");
          localStorage.setItem(statKey, JSON.stringify(stats));
        }
        return stats;
      },
      async getStats() {
        return JSON.parse(localStorage.getItem(statKey) || '{"views":0}');
      },
      async getComments() {
        return JSON.parse(localStorage.getItem(commentsKey) || "[]");
      },
      async addComment(comment) {
        var comments = await this.getComments();
        comments.unshift(comment);
        localStorage.setItem(commentsKey, JSON.stringify(comments.slice(0, 50)));
        return comments;
      }
    };
  }

  async function firestoreStore(articleKey) {
    var appModule = await import("https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js");
    var firestoreModule = await import("https://www.gstatic.com/firebasejs/10.12.5/firebase-firestore.js");
    var app = appModule.initializeApp(firebaseConfig);
    var db = firestoreModule.getFirestore(app);
    var statsRef = firestoreModule.doc(db, "zzArticleStats", articleKey);
    var commentsRef = firestoreModule.collection(db, "zzArticleStats", articleKey, "comments");

    return {
      async incrementView() {
        var viewedKey = "zz-viewed-session:" + articleKey;
        if (!sessionStorage.getItem(viewedKey)) {
          await firestoreModule.setDoc(statsRef, {
            title: articleTitle(),
            path: location.pathname,
            views: firestoreModule.increment(1),
            updatedAt: firestoreModule.serverTimestamp()
          }, { merge: true });
          sessionStorage.setItem(viewedKey, "1");
        }
        return this.getStats();
      },
      async getStats() {
        var snapshot = await firestoreModule.getDoc(statsRef);
        return snapshot.exists() ? snapshot.data() : { views: 0 };
      },
      async getComments() {
        var queryRef = firestoreModule.query(commentsRef, firestoreModule.orderBy("createdAt", "desc"), firestoreModule.limit(50));
        var snapshot = await firestoreModule.getDocs(queryRef);
        return snapshot.docs.map(function (doc) {
          var data = doc.data();
          return {
            name: data.name || "Guest",
            message: data.message || "",
            createdAt: data.createdAt?.toDate ? data.createdAt.toDate().toISOString() : new Date().toISOString()
          };
        });
      },
      async addComment(comment) {
        await firestoreModule.addDoc(commentsRef, {
          name: comment.name,
          message: comment.message,
          createdAt: firestoreModule.serverTimestamp(),
          pageTitle: articleTitle(),
          pagePath: location.pathname
        });
        await firestoreModule.setDoc(statsRef, {
          comments: firestoreModule.increment(1),
          updatedAt: firestoreModule.serverTimestamp()
        }, { merge: true });
        return this.getComments();
      }
    };
  }

  function renderComments(listNode, comments) {
    if (!comments.length) {
      listNode.innerHTML = '<p class="zz-comment-empty">No comments yet. Be the first to leave a note.</p>';
      return;
    }
    listNode.innerHTML = comments.map(function (comment) {
      return [
        '<article class="zz-comment">',
        '  <div class="zz-comment-meta"><span>' + escapeHtml(comment.name || "Guest") + '</span><span class="zz-comment-time">' + escapeHtml(formatDate(comment.createdAt)) + "</span></div>",
        "  <p>" + escapeHtml(comment.message) + "</p>",
        "</article>"
      ].join("");
    }).join("");
  }

  async function setupEngagement() {
    if (!isArticlePage() || document.querySelector(".zz-live-engagement")) return;
    injectStyles();

    var finishLine = document.querySelector(".wechat-finish-line");
    var page = document.querySelector(".wechat-en-page");
    if (!finishLine || !page) return;

    var shell = createEngagementShell();
    finishLine.insertAdjacentElement("afterend", shell);

    var articleKey = articleId();
    var viewsNode = shell.querySelector("[data-zz-views]");
    var commentCountNode = shell.querySelector("[data-zz-comment-count]");
    var listNode = shell.querySelector("[data-zz-comment-list]");
    var form = shell.querySelector("[data-zz-comment-form]");
    var status = shell.querySelector("[data-zz-comment-status]");
    var submit = form.querySelector("button");
    var firebaseReady = hasFirebaseConfig();
    var store = firebaseReady ? await firestoreStore(articleKey) : localStore(articleKey);

    if (!firebaseReady && !canUseLocalFallback()) {
      form.querySelectorAll("input,textarea,button").forEach(function (control) {
        control.disabled = true;
      });
      status.textContent = "Comments and visits are being connected.";
      return;
    }

    async function refresh() {
      var stats = await store.incrementView();
      var comments = await store.getComments();
      viewsNode.textContent = formatNumber(stats.views || 0);
      commentCountNode.textContent = formatNumber(stats.comments || comments.length || 0);
      renderComments(listNode, comments);
    }

    form.addEventListener("submit", async function (event) {
      event.preventDefault();
      var name = form.elements.name.value.trim();
      var message = form.elements.message.value.trim();
      if (!name || !message) return;
      submit.disabled = true;
      status.textContent = "Posting...";
      try {
        var comments = await store.addComment({
          name: name.slice(0, 40),
          message: message.slice(0, 800),
          createdAt: new Date().toISOString()
        });
        form.reset();
        renderComments(listNode, comments);
        var stats = await store.getStats();
        viewsNode.textContent = formatNumber(stats.views || 0);
        commentCountNode.textContent = formatNumber(stats.comments || comments.length || 0);
        status.textContent = "Posted. Thank you.";
      } catch (error) {
        status.textContent = "Could not post right now. Please try again later.";
      } finally {
        submit.disabled = false;
      }
    });

    try {
      await refresh();
      if (!firebaseReady) {
        status.textContent = "Local preview mode. Add Firebase config to save comments online.";
      }
    } catch (error) {
      status.textContent = "Comments are temporarily unavailable.";
    }
  }

  setupGoogleTagManager();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupEngagement);
  } else {
    setupEngagement();
  }
})();
