// back-button.js — Floating Back Button for all pages
(function() {
  const path = window.location.pathname.replace(/\/$/, '');
  const isHome = path === '' || path === '/index.html' || path === '/';
  if (isHome) return;

  const btn = document.createElement('button');
  btn.id = 'globalBackBtn';
  btn.innerHTML = '←';
  btn.title = 'Back';
  btn.style.cssText = `
    position: fixed;
    top: 80px;
    left: 16px;
    z-index: 99999;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    border: none;
    font-size: 22px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
  `;

  btn.onmouseenter = () => {
    btn.style.transform = 'scale(1.1)';
    btn.style.boxShadow = '0 6px 16px rgba(16, 185, 129, 0.55)';
  };
  btn.onmouseleave = () => {
    btn.style.transform = 'scale(1)';
    btn.style.boxShadow = '0 4px 12px rgba(16, 185, 129, 0.35)';
  };

  btn.onclick = function() {
    if (window.history.length > 1) {
      window.history.back();
    } else {
      window.location.href = '/index.html';
    }
  };

  function insert() {
    if (!document.getElementById('globalBackBtn')) {
      document.body.appendChild(btn);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', insert);
  } else {
    insert();
  }
})();
