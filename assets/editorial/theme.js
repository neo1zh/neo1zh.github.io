// Apply a saved preference before the first paint; system preference is the default.
try { const theme = localStorage.getItem('zihao-theme'); if (theme === 'light' || theme === 'dark') document.documentElement.dataset.theme = theme; } catch (_) {}
