document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('menu-toggle');
  const overlay = document.getElementById('overlay');

  if (btn) {
    btn.addEventListener('click', () => {
      document.body.classList.toggle('sidebar-open');
    });
  }

  if (overlay) {
    overlay.addEventListener('click', () => {
      document.body.classList.remove('sidebar-open');
    });
  }

  // закрываем по Esc
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') document.body.classList.remove('sidebar-open');
  });
});