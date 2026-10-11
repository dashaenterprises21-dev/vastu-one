/**
 * Vastu One — Date & Time Picker (FIXED)
 */

function closeAllPickers() {
  ['vp-date-picker', 'vp-time-picker'].forEach(function(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  });
}

// ═══ DATE PICKER ═══
function openSimpleDatePicker(input) {
  closeAllPickers();

  const rect = input.getBoundingClientRect();
  const today = new Date();
  let y, m, sel;

  if (input.value && /^\d{4}-\d{2}-\d{2}$/.test(input.value)) {
    const parts = input.value.split('-');
    y = parseInt(parts[0]);
    m = parseInt(parts[1]) - 1;
    sel = new Date(y, m, parseInt(parts[2]));
  } else {
    y = 1990;
    m = 0;
    sel = null;
  }

  const dd = document.createElement('div');
  dd.id = 'vp-date-picker';
  dd.style.cssText = 'position:fixed;z-index:999999;background:#1a1a24;border:2px solid #D4AF37;border-radius:12px;padding:16px;box-shadow:0 12px 48px rgba(0,0,0,0.8);width:340px;font-family:Inter,sans-serif;';

  // Smart position
  const pw = 340, ph = 440;
  let left = Math.max(10, Math.min(rect.left, window.innerWidth - pw - 10));
  let top = rect.bottom + 6;
  if (top + ph > window.innerHeight - 10) top = Math.max(10, rect.top - ph - 6);
  if (top < 10) top = Math.max(10, (window.innerHeight - ph) / 2);
  dd.style.left = left + 'px';
  dd.style.top = top + 'px';
  document.body.appendChild(dd);

  function render() {
    const firstDay = new Date(y, m, 1).getDay();
    const daysInMonth = new Date(y, m + 1, 0).getDate();
    const months = ["January","February","March","April","May","June","July","August","September","October","November","December"];

    let html = '';
    html += '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">';
    html += '<button type="button" data-nav="-1" style="background:#333;color:#D4AF37;border:none;width:36px;height:36px;border-radius:6px;cursor:pointer;font-size:16px;">◀</button>';
    html += '<div style="color:#D4AF37;font-weight:700;font-size:15px;">' + months[m] + ' ' + y + '</div>';
    html += '<button type="button" data-nav="1" style="background:#333;color:#D4AF37;border:none;width:36px;height:36px;border-radius:6px;cursor:pointer;font-size:16px;">▶</button>';
    html += '</div>';

    html += '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:2px;margin-bottom:6px;">';
    ["S","M","T","W","T","F","S"].forEach(function(d) {
      html += '<div style="text-align:center;font-size:11px;color:#888;padding:4px 0;">' + d + '</div>';
    });
    html += '</div>';

    html += '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:2px;">';
    for (let i = 0; i < firstDay; i++) html += '<div></div>';
    for (let d = 1; d <= daysInMonth; d++) {
      const isToday = today.getFullYear() === y && today.getMonth() === m && today.getDate() === d;
      const isSel = sel && sel.getFullYear() === y && sel.getMonth() === m && sel.getDate() === d;
      let bg = 'transparent', color = '#ddd';
      if (isSel) { bg = '#D4AF37'; color = '#000'; }
      else if (isToday) { bg = 'rgba(212,175,55,0.2)'; color = '#D4AF37'; }
      html += '<button type="button" data-day="' + d + '" style="background:' + bg + ';border:none;color:' + color + ';padding:8px 0;border-radius:6px;cursor:pointer;font-size:13px;font-weight:600;">' + d + '</button>';
    }
    html += '</div>';

    dd.innerHTML = html;

    // NAV buttons
    dd.querySelectorAll('[data-nav]').forEach(function(btn) {
      btn.onclick = function(e) {
        e.stopPropagation();
        const dir = parseInt(btn.dataset.nav);
        m += dir;
        if (m < 0) { m = 11; y--; }
        if (m > 11) { m = 0; y++; }
        render();
      };
    });

    // DAY buttons
    dd.querySelectorAll('[data-day]').forEach(function(btn) {
      btn.onclick = function(e) {
        e.stopPropagation();
        const d = parseInt(btn.dataset.day);
        const pad = function(n) { return n < 10 ? '0' + n : '' + n; };
        const newVal = y + '-' + pad(m + 1) + '-' + pad(d);
        input.value = newVal;
        console.log('✅ Date set:', newVal);
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        closeAllPickers();
      };
    });
  }

  // WHEEL — month change
  dd.addEventListener('wheel', function(e) {
    e.preventDefault();
    e.stopPropagation();
    if (e.deltaY < 0) { m--; if (m < 0) { m = 11; y--; } }
    else { m++; if (m > 11) { m = 0; y++; } }
    render();
  }, { passive: false });

  // KEYBOARD — arrow keys
  document.addEventListener('keydown', function onKey(e) {
    if (!document.getElementById('vp-date-picker')) {
      document.removeEventListener('keydown', onKey);
      return;
    }
    if (e.key === 'ArrowLeft') { m--; if (m < 0) { m = 11; y--; } render(); e.preventDefault(); }
    if (e.key === 'ArrowRight') { m++; if (m > 11) { m = 0; y++; } render(); e.preventDefault(); }
    if (e.key === 'Escape') { closeAllPickers(); document.removeEventListener('keydown', onKey); }
  });

  render();
}

// ═══ TIME PICKER ═══
function openSimpleTimePicker(input) {
  closeAllPickers();

  const rect = input.getBoundingClientRect();
  let h = 12, min = 0, isPM = false;

  if (input.value && /^\d{1,2}:\d{2}/.test(input.value)) {
    const parts = input.value.split(':');
    h = parseInt(parts[0]);
    min = parseInt(parts[1]);
    isPM = h >= 12;
    h = h % 12 || 12;
  }

  const dd = document.createElement('div');
  dd.id = 'vp-time-picker';
  dd.style.cssText = 'position:fixed;z-index:999999;background:#1a1a24;border:2px solid #D4AF37;border-radius:12px;padding:16px;box-shadow:0 12px 48px rgba(0,0,0,0.8);width:340px;font-family:Inter,sans-serif;';

  const pw = 340, ph = 480;
  let left = Math.max(10, Math.min(rect.left, window.innerWidth - pw - 10));
  let top = rect.bottom + 6;
  if (top + ph > window.innerHeight - 10) top = Math.max(10, rect.top - ph - 6);
  if (top < 10) top = Math.max(10, (window.innerHeight - ph) / 2);
  dd.style.left = left + 'px';
  dd.style.top = top + 'px';
  document.body.appendChild(dd);

  function render() {
    let html = '<div style="text-align:center;color:#D4AF37;font-weight:700;margin-bottom:12px;font-size:14px;">Select Time</div>';

    html += '<div style="font-size:10px;color:#888;letter-spacing:1.5px;margin-bottom:6px;">HOUR</div>';
    html += '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin-bottom:12px;">';
    for (let i = 1; i <= 12; i++) {
      const bg = i === h ? '#D4AF37' : '#333';
      const color = i === h ? '#000' : '#ddd';
      html += '<button type="button" data-hour="' + i + '" style="background:' + bg + ';border:none;color:' + color + ';padding:8px 0;border-radius:6px;cursor:pointer;font-size:12px;font-weight:600;">' + i + '</button>';
    }
    html += '</div>';

    html += '<div style="font-size:10px;color:#888;letter-spacing:1.5px;margin-bottom:6px;">MINUTE</div>';
    html += '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin-bottom:12px;">';
    for (let i = 0; i < 60; i += 5) {
      const bg = i === min ? '#D4AF37' : '#333';
      const color = i === min ? '#000' : '#ddd';
      const pad = i < 10 ? '0' + i : '' + i;
      html += '<button type="button" data-min="' + i + '" style="background:' + bg + ';border:none;color:' + color + ';padding:6px 0;border-radius:6px;cursor:pointer;font-size:11px;font-weight:600;">' + pad + '</button>';
    }
    html += '</div>';

    html += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:12px;">';
    html += '<button type="button" data-am="1" style="background:' + (!isPM ? '#D4AF37' : '#333') + ';border:none;color:' + (!isPM ? '#000' : '#ddd') + ';padding:10px;border-radius:6px;cursor:pointer;font-weight:700;">AM</button>';
    html += '<button type="button" data-pm="1" style="background:' + (isPM ? '#D4AF37' : '#333') + ';border:none;color:' + (isPM ? '#000' : '#ddd') + ';padding:10px;border-radius:6px;cursor:pointer;font-weight:700;">PM</button>';
    html += '</div>';

    const pad = function(n) { return n < 10 ? '0' + n : '' + n; };
    html += '<div style="text-align:center;padding:10px;background:rgba(212,175,55,0.1);border-radius:6px;margin-bottom:10px;color:#D4AF37;font-size:18px;font-weight:700;">' + pad(h) + ':' + pad(min) + ' ' + (isPM ? 'PM' : 'AM') + '</div>';

    html += '<button type="button" id="vp-apply" style="width:100%;background:#D4AF37;color:#000;border:none;padding:12px;border-radius:6px;cursor:pointer;font-weight:700;font-size:13px;">Apply Time</button>';

    dd.innerHTML = html;

    dd.querySelectorAll('[data-hour]').forEach(function(b) {
      b.onclick = function(e) { e.stopPropagation(); h = parseInt(b.dataset.hour); render(); };
    });
    dd.querySelectorAll('[data-min]').forEach(function(b) {
      b.onclick = function(e) { e.stopPropagation(); min = parseInt(b.dataset.min); render(); };
    });
    dd.querySelector('[data-am]').onclick = function(e) { e.stopPropagation(); isPM = false; render(); };
    dd.querySelector('[data-pm]').onclick = function(e) { e.stopPropagation(); isPM = true; render(); };
    dd.querySelector('#vp-apply').onclick = function(e) {
      e.stopPropagation();
      let hh = h % 12;
      if (isPM) hh += 12;
      const pad = function(n) { return n < 10 ? '0' + n : '' + n; };
      const newVal = pad(hh) + ':' + pad(min);
      input.value = newVal;
      console.log('✅ Time set:', newVal);
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
      closeAllPickers();
    };
  }

  // WHEEL
  dd.addEventListener('wheel', function(e) {
    e.preventDefault();
    if (e.deltaY < 0) { min = (min - 5 + 60) % 60; }
    else { min = (min + 5) % 60; }
    render();
  }, { passive: false });

  render();
}

// ═══ ATTACH ═══
function attachCustomPickers() {
  document.querySelectorAll('input[type="date"]').forEach(function(inp) {
    if (inp.dataset.pickerAttached) return;
    inp.dataset.pickerAttached = 'true';
    inp.readOnly = true;
    inp.style.cursor = 'pointer';
    inp.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      openSimpleDatePicker(inp);
    });
  });
  document.querySelectorAll('input[type="time"]').forEach(function(inp) {
    if (inp.dataset.pickerAttached) return;
    inp.dataset.pickerAttached = 'true';
    inp.readOnly = true;
    inp.style.cursor = 'pointer';
    inp.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      openSimpleTimePicker(inp);
    });
  });
  console.log('✅ Custom pickers attached');
}

// Close on outside click
document.addEventListener('click', function(e) {
  const d1 = document.getElementById('vp-date-picker');
  const d2 = document.getElementById('vp-time-picker');
  if (d1 && !d1.contains(e.target) && e.target.type !== 'date') closeAllPickers();
  if (d2 && !d2.contains(e.target) && e.target.type !== 'time') closeAllPickers();
});

// Auto-attach
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', attachCustomPickers);
} else {
  attachCustomPickers();
}

window.openSimpleDatePicker = openSimpleDatePicker;
window.openSimpleTimePicker = openSimpleTimePicker;
window.attachCustomPickers = attachCustomPickers;
window.openDatePicker = openSimpleDatePicker;
window.openTimePicker = openSimpleTimePicker;
