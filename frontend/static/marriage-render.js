/**
 * Vastu One — Marriage Analysis Renderer
 * 9 sections: yoga, spouse, married life, harmony, delay, mangal dosha, timing, matching, rules
 */

function renderMarriageAnalysis(data, targetId) {
  const t = document.getElementById(targetId);
  if (!t) return;

  const ma = (data && data.marriage_analysis) || {};
  if (Object.keys(ma).length === 0) {
    t.innerHTML = '<div style="padding:20px;color:#888;">Marriage analysis data available nahi hai.</div>';
    return;
  }

  function card(title, hindi, content, color) {
    color = color || '#D4AF37';
    return '<div style="margin-bottom:16px;padding:16px;background:rgba(255,255,255,0.02);border-left:3px solid ' + color + ';border-radius:8px;">' +
      '<div style="font-size:13px;font-weight:700;color:' + color + ';margin-bottom:10px;letter-spacing:0.5px;">' + hindi + ' <span style="color:#888;font-size:11px;font-weight:400;">' + title + '</span></div>' +
      '<div style="font-size:13px;color:#ddd;line-height:1.8;">' + content + '</div>' +
      '</div>';
  }

  function list(items) {
    if (!items || items.length === 0) return '';
    return '<ul style="padding-left:20px;margin:8px 0;">' + items.map(function(i) { return '<li style="margin-bottom:6px;color:#bbb;">' + i + '</li>'; }).join('') + '</ul>';
  }

  function kv(label, value) {
    return '<div style="display:flex;gap:12px;padding:6px 0;border-bottom:1px dashed rgba(255,255,255,0.08);">' +
      '<div style="min-width:140px;color:#888;font-size:12px;">' + label + '</div>' +
      '<div style="color:#fff;font-size:13px;flex:1;">' + value + '</div>' +
      '</div>';
  }

  let html = '';

  // 1. Marriage Yoga
  if (ma.marriage_yoga) {
    const my = ma.marriage_yoga;
    let content = '<p>' + (my.summary || '') + '</p>';
    content += kv('Strength', my.strength || '');
    content += kv('Shukra Bhava', (my.shukra_hindi || '') + ' (Bhava ' + (my.shukra_bhav || '') + ')');
    content += kv('7th Lord', my.seventh_lord || '');
    content += kv('Love/Arranged', my.love_or_arranged || '');
    content += kv('Marriage Type', my.marriage_type || '');
    html += card('Marriage Yoga', '💍 विवाह योग', content);
  }

  // 2. Spouse Analysis
  if (ma.spouse_analysis) {
    const sa = ma.spouse_analysis;
    let content = '<p>' + (sa.summary || '') + '</p>';
    content += '<div style="margin-top:12px;">';
    content += kv('7th Rashi', (sa.seventh_rashi_hindi || '') + ' (' + (sa.seventh_rashi || '') + ')');
    content += kv('Nature', sa.spouse_nature || '');
    content += kv('Profession', sa.spouse_profession || '');
    content += kv('Appearance', sa.spouse_appearance || '');
    content += kv('Direction', sa.spouse_from_direction || '');
    content += kv('Age', sa.spouse_age || '');
    if (sa.planets_in_7th && sa.planets_in_7th.length) {
      content += kv('Planets in 7th', sa.planets_in_7th.join(', '));
    }
    content += '</div>';
    html += card('Spouse Analysis', '👫 जीवनसाथी विश्लेषण', content);
  }

  // 3. Married Life
  if (ma.married_life) {
    const ml = ma.married_life;
    let content = '<p style="font-size:15px;font-weight:600;">' + (ml.summary || '') + '</p>';
    content += '<div style="margin-top:12px;">';
    content += kv('Overall', ml.overall || '');
    content += kv('Early Years', ml.early_years || '');
    content += kv('Mid Years', ml.mid_years || '');
    content += kv('Later Years', ml.later_years || '');
    content += kv('Children', ml.children_after_marriage || '');
    content += kv('Financial', ml.financial_life_after_marriage || '');
    content += '</div>';
    if (ml.challenges && ml.challenges.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#ef4444;font-size:12px;">⚠ चुनौतियां:</strong>' + list(ml.challenges) + '</div>';
    }
    if (ml.strengths && ml.strengths.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#22c55e;font-size:12px;">✓ शक्तियां:</strong>' + list(ml.strengths) + '</div>';
    }
    html += card('Married Life', '🏡 विवाहित जीवन', content);
  }

  // 4. Marital Harmony
  if (ma.marital_harmony) {
    const mh = ma.marital_harmony;
    let content = '<p>' + (mh.summary || '') + '</p>';
    if (mh.relationship_rules && mh.relationship_rules.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#D4AF37;font-size:12px;">✓ रिश्ते के नियम:</strong>' + list(mh.relationship_rules) + '</div>';
    }
    if (mh.avoid && mh.avoid.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#ef4444;font-size:12px;">✗ बचें:</strong>' + list(mh.avoid) + '</div>';
    }
    if (mh.remedies_for_harmony && mh.remedies_for_harmony.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#22c55e;font-size:12px;">🕉️ उपाय:</strong>' + list(mh.remedies_for_harmony) + '</div>';
    }
    html += card('Marital Harmony', '💞 दांपत्य सुख', content);
  }

  // 5. Delay Analysis
  if (ma.delay_analysis) {
    const da = ma.delay_analysis;
    let content = '<p>' + (da.summary || '') + '</p>';
    if (da.reasons && da.reasons.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#ef4444;font-size:12px;">विलंब के कारण:</strong>' + list(da.reasons) + '</div>';
    }
    content += kv('Duration', da.how_long || '');
    if (da.remedies && da.remedies.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#22c55e;font-size:12px;">उपाय:</strong>' + list(da.remedies) + '</div>';
    }
    html += card('Delay Analysis', '⏰ विवाह में विलंब', content);
  }

  // 6. Mangal Dosha
  if (ma.mangal_dosha) {
    const md = ma.mangal_dosha;
    let content = '<p style="font-size:15px;font-weight:600;">' + (md.summary || '') + '</p>';
    content += kv('Has Dosha', md.has_dosha ? 'हाँ' : 'नहीं');
    content += kv('Mangal Bhava', md.mangal_bhav || '');
    content += kv('Strength', md.strength || '');
    if (md.effects && md.effects.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#f97316;font-size:12px;">प्रभाव:</strong>' + list(md.effects) + '</div>';
    }
    if (md.cancellation) {
      content += '<div style="margin-top:12px;"><strong style="color:#3b82f6;font-size:12px;">Cancellation:</strong> ' + md.cancellation + '</div>';
    }
    if (md.remedies && md.remedies.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#22c55e;font-size:12px;">उपाय:</strong>' + list(md.remedies) + '</div>';
    }
    if (md.matching_rule) {
      content += '<div style="margin-top:12px;padding:10px;background:rgba(212,175,55,0.08);border-radius:6px;font-size:12px;color:#D4AF37;">💡 ' + md.matching_rule + '</div>';
    }
    html += card('Mangal Dosha', '🔴 मंगल दोष', content, md.has_dosha ? '#ef4444' : '#22c55e');
  }

  // 7. Marriage Timing
  if (ma.marriage_timing) {
    const mt = ma.marriage_timing;
    let content = '<p>' + (mt.summary || '') + '</p>';
    content += kv('Best Age', mt.best_age || '');
    content += kv('Current Planet', mt.current_planet || '');
    content += kv('Action', mt.immediate_action || '');
    if (mt.favorable_periods && mt.favorable_periods.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#22c55e;font-size:12px;">शुभ काल:</strong>';
      mt.favorable_periods.forEach(function(p) {
        content += '<div style="margin-top:8px;padding:10px;background:rgba(34,197,94,0.08);border-radius:6px;">' +
          '<div style="font-size:13px;font-weight:600;color:#22c55e;">' + p.planet + ' — ' + p.age + '</div>' +
          '<div style="font-size:11px;color:#888;margin-top:2px;">' + p.period + '</div>' +
          '<div style="font-size:12px;color:#bbb;margin-top:4px;">' + p.reason + '</div>' +
          '</div>';
      });
      content += '</div>';
    }
    html += card('Marriage Timing', '📅 विवाह का समय', content);
  }

  // 8. Matching Guidance
  if (ma.matching_guidance) {
    const mg = ma.matching_guidance;
    let content = '<p>' + (mg.summary || '') + '</p>';
    content += kv('Your 7th Rashi', (mg.your_7th_rashi_hindi || '') + ' (' + (mg.your_7th_rashi || '') + ')');
    if (mg.compatible_rashis && mg.compatible_rashis.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#22c55e;font-size:12px;">अनुकूल राशियां:</strong>';
      content += '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;">';
      mg.compatible_rashis.forEach(function(r) {
        content += '<span style="padding:4px 10px;background:rgba(34,197,94,0.15);color:#22c55e;border-radius:4px;font-size:12px;">' + r + '</span>';
      });
      content += '</div></div>';
    }
    content += kv('Nakshatras', mg.recommended_nakshatras || '');
    if (mg.avoid_if && mg.avoid_if.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#ef4444;font-size:12px;">बचें:</strong>' + list(mg.avoid_if) + '</div>';
    }
    if (mg.guna_milan_importance) {
      content += '<div style="margin-top:12px;padding:10px;background:rgba(212,175,55,0.08);border-radius:6px;font-size:12px;color:#D4AF37;">💡 ' + mg.guna_milan_importance + '</div>';
    }
    html += card('Matching Guidance', '🔮 कुंडली मिलान', content);
  }

  // 9. Practical Rules
  if (ma.practical_rules) {
    const pr = ma.practical_rules;
    let content = '<p>' + (pr.summary || '') + '</p>';
    if (pr.before_marriage && pr.before_marriage.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#D4AF37;font-size:12px;">विवाह से पहले:</strong>' + list(pr.before_marriage) + '</div>';
    }
    if (pr.after_marriage && pr.after_marriage.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#3b82f6;font-size:12px;">विवाह के बाद:</strong>' + list(pr.after_marriage) + '</div>';
    }
    if (pr.spiritual_practices && pr.spiritual_practices.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#a855f7;font-size:12px;">आध्यात्मिक अभ्यास:</strong>' + list(pr.spiritual_practices) + '</div>';
    }
    if (pr.avoid && pr.avoid.length) {
      content += '<div style="margin-top:12px;"><strong style="color:#ef4444;font-size:12px;">बचें:</strong>' + list(pr.avoid) + '</div>';
    }
    html += card('Practical Rules', '📋 व्यावहारिक नियम', content);
  }

  t.innerHTML = html;
}

window.renderMarriageAnalysis = renderMarriageAnalysis;
