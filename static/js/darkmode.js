// static/js/darkmode.js
document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('darkModeToggle');
  if (!toggleBtn) return;

  toggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');

    // Toggle icon between sun/moon
    const icon = toggleBtn.querySelector('i');
    if (document.body.classList.contains('dark-mode')) {
      icon.classList.replace('bi-moon-fill', 'bi-sun-fill');
      localStorage.setItem('theme', 'dark');
    } else {
      icon.classList.replace('bi-sun-fill', 'bi-moon-fill');
      localStorage.setItem('theme', 'light');
    }
  });

  // Persist theme on reload
  if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-mode');
    const icon = toggleBtn.querySelector('i');
    if (icon) icon.classList.replace('bi-moon-fill', 'bi-sun-fill');
  }
});
