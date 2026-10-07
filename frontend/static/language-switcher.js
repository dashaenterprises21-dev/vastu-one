/* VASTU ONE - Language Switcher UI (Cleaned) */
(function() {
  'use strict';

  function createSwitcher(container) {
    if (!window.I18n) {
      console.warn('[LangSwitcher] I18n not loaded');
      return null;
    }

    const I18n = window.I18n;
    const root = document.createElement('div');
    root.className = 'i18n-switcher';
    root.setAttribute('role', 'region');
    root.setAttribute('aria-label', 'Language switcher');

    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'i18n-trigger';
    trigger.setAttribute('aria-haspopup', 'listbox');
    trigger.setAttribute('aria-expanded', 'false');
    trigger.innerHTML = '<span class="i18n-flag">&#127758;</span><span class="i18n-name">English</span><span class="i18n-chevron"></span>';

    const menu = document.createElement('div');
    menu.className = 'i18n-menu';
    menu.setAttribute('role', 'listbox');
    menu.innerHTML = '<div class="i18n-menu-header">Select Language</div><div class="i18n-list"></div><div class="i18n-menu-footer">Saved automatically</div>';

    const list = menu.querySelector('.i18n-list');

    root.appendChild(trigger);
    root.appendChild(menu);
    container.appendChild(root);

    let isOpen = false;

    function buildList() {
      list.innerHTML = '';
      const langs = (window.I18n && window.I18n.languages) || [];
      const current = (window.I18n && window.I18n.currentLang) || 'en';

      if (langs.length === 0) {
        list.innerHTML = '<div class="i18n-item">No languages available</div>';
        return;
      }

      langs.forEach(lang => {
        const item = document.createElement('div');
        item.className = 'i18n-item' + (lang.code === current ? ' active' : '');
        item.setAttribute('role', 'option');
        item.setAttribute('aria-selected', lang.code === current ? 'true' : 'false');
        item.setAttribute('data-lang', lang.code);
        item.innerHTML = '<span class="i18n-item-flag">' + (lang.flag || '') + '</span><span class="i18n-item-text"><span class="i18n-item-name">' + lang.name + '</span><span class="i18n-item-code">' + lang.code + '</span></span><span class="i18n-check">&#10003;</span>';
        item.addEventListener('click', async (e) => {
          e.stopPropagation();
          await changeLanguage(lang.code);
        });
        list.appendChild(item);
      });
    }

    function updateTrigger() {
      const langs = (window.I18n && window.I18n.languages) || [];
      const current = (window.I18n && window.I18n.currentLang) || 'en';
      const lang = langs.find(l => l.code === current) || { flag: '\uD83C\uDF10', name: 'English' };
      trigger.querySelector('.i18n-flag').textContent = lang.flag || '\uD83C\uDF10';
      trigger.querySelector('.i18n-name').textContent = lang.name || 'English';
    }

    async function changeLanguage(code) {
      if (code === (window.I18n && window.I18n.currentLang)) {
        close();
        return;
      }
      const ok = await window.I18n.setLanguage(code);
      if (ok) {
        updateTrigger();
        buildList();
      }
      close();
    }

    function open() {
      if (isOpen) return;
      isOpen = true;
      root.classList.add('open');
      trigger.setAttribute('aria-expanded', 'true');
      buildList();
      document.addEventListener('click', outsideClick);
      document.addEventListener('keydown', onKeyDown);
    }

    function close() {
      if (!isOpen) return;
      isOpen = false;
      root.classList.remove('open');
      trigger.setAttribute('aria-expanded', 'false');
      document.removeEventListener('click', outsideClick);
      document.removeEventListener('keydown', onKeyDown);
    }

    function toggle() { isOpen ? close() : open(); }
    function outsideClick(e) { if (!root.contains(e.target)) close(); }
    function onKeyDown(e) { if (e.key === 'Escape') close(); }

    trigger.addEventListener('click', (e) => { e.stopPropagation(); toggle(); });

    updateTrigger();
    buildList();

    if (window.I18n.onChange) {
      window.I18n.onChange(() => { updateTrigger(); buildList(); });
    }

    return { root, updateTrigger, buildList };
  }

  function autoMount() {
    document.querySelectorAll('[data-language-switcher]').forEach(el => {
      if (!el.querySelector('.i18n-switcher')) {
        createSwitcher(el);
      }
    });
  }

  window.LanguageSwitcher = {
    create: createSwitcher,
    mount: autoMount
  };

  function init() {
    if (window.I18n) {
      window.I18n.init().then(autoMount);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
