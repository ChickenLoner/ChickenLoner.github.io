// themes/soc-theme.js
// Synchronous — load WITHOUT defer. Applies data-theme to <html> before
// any render to prevent flash of wrong theme.
// Exports window.SocTheme = { toggle, get, set }.
(function () {
  var KEY = 'soc-theme';
  var DEFAULT = 'dark';

  function apply(theme) {
    document.documentElement.setAttribute('data-theme', theme);
  }

  function get() {
    try { return localStorage.getItem(KEY) || DEFAULT; }
    catch (_) { return DEFAULT; }
  }

  function set(theme) {
    try { localStorage.setItem(KEY, theme); } catch (_) {}
    apply(theme);
    document.dispatchEvent(new CustomEvent('soc-theme-change', { detail: theme }));
  }

  function toggle() {
    set(get() === 'dark' ? 'light' : 'dark');
  }

  apply(get());

  window.SocTheme = { toggle: toggle, get: get, set: set };
})();
