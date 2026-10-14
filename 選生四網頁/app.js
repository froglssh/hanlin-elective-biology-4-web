(function () {
  // reveal on scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('in');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }

  // lightbox for textbook figures
  var lb = document.getElementById('lightbox');
  if (!lb) return;
  var img = lb.querySelector('img'), cap = lb.querySelector('figcaption'), lastFocus = null;
  function open(src, text) {
    lastFocus = document.activeElement;
    img.src = src;
    img.alt = text || '放大圖解';
    cap.textContent = text || '';
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
    var closeBtn = lb.querySelector('.lb-close');
    if (closeBtn) closeBtn.focus();
  }
  function close() {
    lb.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  document.querySelectorAll('.fig-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      open(b.dataset.full, b.dataset.cap);
    });
  });
  lb.addEventListener('click', function (e) {
    if (e.target !== img) close();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !lb.hidden) close();
  });
})();
