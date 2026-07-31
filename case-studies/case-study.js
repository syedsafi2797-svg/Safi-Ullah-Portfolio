/* Anti-theft protection: block right-click save, drag, and keyboard save on media */
(function () {
  function isMedia(t) {
    return t && (t.tagName === 'IMG' || t.tagName === 'VIDEO');
  }

  // Right-click -> no context menu on images/videos
  document.addEventListener('contextmenu', function (e) {
    if (isMedia(e.target)) e.preventDefault();
  });

  // Drag -> blocked
  document.addEventListener('dragstart', function (e) {
    if (isMedia(e.target)) e.preventDefault();
  });

  // Keyboard shortcuts that save media (Ctrl+S / Cmd+S, Ctrl+P / Cmd+P)
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'p' || e.key === 'u')) {
      e.preventDefault();
      return false;
    }
  });

  // Force draggable=false on all media (defense in depth)
  document.querySelectorAll('img, video').forEach(function (el) {
    el.setAttribute('draggable', 'false');
  });
})();
