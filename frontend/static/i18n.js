/* VASTU ONE - i18n Core Engine */
(function() {
  'use strict';

  const STORAGE_KEY = 'vastu_lang';
  const DEFAULT_LANG = 'en';
  const SUPPORTED = ['en', 'hi', 'hinglish'];

  const I18n = {
    currentLang: null,
    translations: {},
    languages: [],
    listeners: [],

    async init() {
      // 1. Load saved language
      const saved = localStorage.getItem(STORAGE_KEY);
      this.currentLang = (saved && SUPPORTED.includes(saved)) ? saved : DEFAULT_LANG;

      // 2. Fetch languages list
      try {
        const res = await fetch('/api/i18n/languages');
        const data = await res.json();
        this.languages = data.languages || [];
      } catch (e) {
        console.warn('[i18n] Could not fetch languages:', e);
        this.languages = [];
      }

      // 3. Load current translations
      await this.load(this.currentLang);

      // 4. Apply to DOM
      this.applyToDOM();

      return this;
    },

    async load(lang) {
      if (!SUPPORTED.includes(lang)) lang = DEFAULT_LANG;
      try {
        const res = await fetch('/api/i18n/translations/' + lang);
        if (!res.ok) throw new Error('HTTP ' + res.status);
        this.translations = await res.json();
        this.currentLang = lang;
        localStorage.setItem(STORAGE_KEY, lang);
        document.documentElement.lang = lang;
        return true;
      } catch (e) {
        console.error('[i18n] Load failed:', e);
        return false;
      }
    },

    t(key, fallback) {
      if (!key) return fallback || '';
      const parts = key.split('.');
      let val = this.translations;
      for (const p of parts) {
        if (val && typeof val === 'object' && p in val) {
          val = val[p];
        } else {
          return fallback !== undefined ? fallback : key;
        }
      }
      return typeof val === 'string' ? val : (fallback !== undefined ? fallback : key);
    },

    applyToDOM(root) {
      root = root || document;
      const nodes = root.querySelectorAll('[data-i18n]');
      nodes.forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translated = this.t(key);
        if (translated && translated !== key) {
          if (el.hasAttribute('data-i18n-attr')) {
            const attr = el.getAttribute('data-i18n-attr');
            el.setAttribute(attr, translated);
          } else {
            el.textContent = translated;
          }
        }
      });

      // Placeholders
      root.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        const translated = this.t(key);
        if (translated && translated !== key) {
          el.setAttribute('placeholder', translated);
        }
      });
    },

    async setLanguage(lang) {
      const ok = await this.load(lang);
      if (ok) {
        this.applyToDOM();
        this.listeners.forEach(fn => {
          try { fn(lang); } catch (e) { console.error(e); }
        });
      }
      return ok;
    },

    onChange(fn) {
      if (typeof fn === 'function') this.listeners.push(fn);
    }
  };

  window.I18n = I18n;
})();
