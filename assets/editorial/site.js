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
const tools = document.querySelector('.publication-tools');
const entries = [...document.querySelectorAll('.publication-entry')];
const filters = [...document.querySelectorAll('[data-filter]')];
function filterPublications(value) {
  let visible = 0;
  entries.forEach(entry => { entry.hidden = value !== 'all' && entry.dataset.category !== value; if (!entry.hidden) visible++; });
  document.querySelectorAll('.publication-group').forEach(group => { group.hidden = ![...group.querySelectorAll('.publication-entry')].some(entry => !entry.hidden); });
  filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === value)));
  document.querySelector('.result-count').textContent = `${visible} ${visible === 1 ? 'paper' : 'papers'}`;
}
tools.hidden = false;
filters.forEach(button => button.addEventListener('click', () => filterPublications(button.dataset.filter)));
filterPublications('all');
