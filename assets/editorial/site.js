'use strict';
const themeButton = document.querySelector('.theme-toggle');
const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
function darkMode() { return document.documentElement.dataset.theme ? document.documentElement.dataset.theme === 'dark' : systemTheme.matches; }
function updateThemeButton() { themeButton.setAttribute('aria-label', `Switch to ${darkMode() ? 'light' : 'dark'} theme`); }
themeButton.hidden = false;
updateThemeButton();
systemTheme.addEventListener('change', updateThemeButton);
themeButton.addEventListener('click', () => {
  const theme = darkMode() ? 'light' : 'dark';
  document.documentElement.dataset.theme = theme;
  try { localStorage.setItem('zihao-theme', theme); } catch (_) {}
  updateThemeButton();
});
