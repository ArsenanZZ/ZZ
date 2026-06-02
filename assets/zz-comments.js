(function () {
  function ready(callback) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback);
    } else {
      callback();
    }
  }

  ready(function () {
    var mount = document.querySelector("[data-zz-comments]");
    if (mount) mount.remove();
  });
}());
