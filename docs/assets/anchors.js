/* 页内锚点：滚动定位，但不新增历史记录
   否则每点一个 #hash 都会压一条记录，浏览器「后退」要按很多次才回到上一页。 */
(function () {
  function closestAnchor(node) {
    while (node && node.nodeType === 1) {
      if (node.tagName === 'A' && node.getAttribute('href')) return node;
      node = node.parentNode;
    }
    return null;
  }

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = closestAnchor(e.target);
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) !== '#' || href.length < 2) return;
    var el = document.querySelector(href);
    if (!el) return;

    e.preventDefault();
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    try {
      history.replaceState(null, '', href);
    } catch (err) {
      /* file:// 某些浏览器限制 replaceState，退回锚点跳转但不平滑 */
      location.hash = href;
    }
    el.classList.remove('flash');
    void el.offsetWidth;
    el.classList.add('flash');
    setTimeout(function () { el.classList.remove('flash'); }, 1100);
  }, false);
})();
