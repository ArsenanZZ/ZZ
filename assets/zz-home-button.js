(function () {
  if (document.querySelector("[data-zz-home-button]")) return;

  function ready(callback) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback);
    } else {
      callback();
    }
  }

  function injectStyle() {
    if (document.querySelector("[data-zz-home-button-style]")) return;
    var style = document.createElement("style");
    style.dataset.zzHomeButtonStyle = "true";
    style.textContent = [
      ".zz-home-button{position:fixed;z-index:9998;left:16px;bottom:16px;display:inline-flex;align-items:center;gap:8px;min-height:38px;padding:0 13px;border:1px solid rgba(17,24,39,.16);border-radius:999px;background:rgba(255,255,255,.88);color:#111827!important;text-decoration:none!important;font:800 13px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;letter-spacing:0;box-shadow:0 12px 34px rgba(15,23,42,.16);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);}",
      ".zz-home-button::before{content:'';width:9px;height:9px;border-radius:50%;background:currentColor;box-shadow:0 0 0 4px rgba(17,24,39,.08);}",
      ".zz-home-button:hover{transform:translateY(-1px);box-shadow:0 16px 38px rgba(15,23,42,.20);}",
      "html[data-run50-theme='dark'] .zz-home-button,html[data-run50-map-theme='dark'] .zz-home-button{border-color:rgba(255,255,255,.18);background:rgba(14,21,30,.82);color:#f5f7fb!important;box-shadow:0 14px 34px rgba(0,0,0,.34);}",
      "@media (prefers-color-scheme:dark){html:not([data-run50-theme='light']):not([data-run50-map-theme='light']) .zz-home-button{border-color:rgba(255,255,255,.18);background:rgba(14,21,30,.82);color:#f5f7fb!important;box-shadow:0 14px 34px rgba(0,0,0,.34);}}",
      "@media (max-width:640px){.zz-home-button{left:10px;bottom:10px;min-height:34px;padding:0 11px;font-size:12px;}}"
    ].join("\n");
    document.head.appendChild(style);
  }

  ready(function () {
    injectStyle();
    var link = document.createElement("a");
    link.href = "https://zhennanzhang.com/";
    link.className = "zz-home-button";
    link.dataset.zzHomeButton = "true";
    link.setAttribute("aria-label", "Back to zhennanzhang.com homepage");
    link.textContent = "Home";
    document.body.appendChild(link);
  });
}());
