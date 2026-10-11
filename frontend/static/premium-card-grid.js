/**
 * Vastu One — Premium Card Grid Renderer
 * Category-wise 46 cards with collapsible groups
 */

var CARD_CATEGORIES = [
  {
    id: 'life',
    icon: '🌟',
    title: 'Life Analysis',
    cards: [
      { icon: '📚', title: 'Education', desc: 'Field · Higher studies · Obstacles', panel: 'education' },
      { icon: '💼', title: 'Career Analysis', desc: 'Field · Job vs Business · Timing', panel: 'career' },
      { icon: '📈', title: 'Business Guidance', desc: 'Type · Partner · Alone vs Together', panel: 'business' },
      { icon: '👤', title: 'Personal Life', desc: 'Personality · Strengths · Weaknesses', panel: 'personal' },
      { icon: '💑', title: 'Marriage', desc: 'Timing · Partner · Happiness', panel: 'marriage-life' },
      { icon: '👶', title: 'Children', desc: 'Count · Timing · Nature', panel: 'children' },
      { icon: '🌍', title: 'Location', desc: 'City · Country · Direction', panel: 'location' },
      { icon: '��', title: 'Wealth Analysis', desc: 'Level · Source · Timing', panel: 'wealth' },
      { icon: '🏥', title: 'Health', desc: 'Weak organs · Prevention', panel: 'health' },
      { icon: '🕉️', title: 'Spiritual Path', desc: 'Bhakti · Gyan · Dhyan', panel: 'spiritual' },
      { icon: '🌟', title: 'Dreams Fulfillment', desc: 'Timing · Best period', panel: 'dreams' },
      { icon: '📕', title: 'Lal Kitab Analysis', desc: 'Unique Totke · Low-Cost Remedies', panel: 'lalkitab' },
    ]
  },
  {
    id: 'charts',
    icon: '📊',
    title: 'Charts & Deep Analysis',
    cards: [
      { icon: '📊', title: 'Detailed Life Analysis', desc: 'Deep Elaboration · Case Study', panel: 'life-elaborated' },
      { icon: '📊', title: 'North Indian Chart', desc: 'Lagna + 9 Planets + 12 Bhavas', panel: 'north-chart' },
      { icon: '📊', title: 'South Indian Chart', desc: 'Rashi-based traditional layout', panel: 'south-chart' },
      { icon: '⏳', title: 'Vimshottari Dasha', desc: '120 Years — Past · Present · Future', panel: 'dasha-timeline' },
      { icon: '🌳', title: 'Nested Periods', desc: 'Maha → Antar → Pratyantar', panel: 'vimshottari-tree' },
      { icon: '📊', title: 'Ashtakavarga Grid', desc: 'Planet-wise + Total strength', panel: 'ashtakavarga' },
      { icon: '⏰', title: 'Time-Based Prediction', desc: 'Past · Present · Future · Karma', panel: 'time-prediction' },
      { icon: '��', title: 'Marriage Analysis', desc: 'Vivah Yog · Spouse · Married Life', panel: 'marriage-analysis' },
    ]
  },
  {
    id: 'phase1',
    icon: '⭐',
    title: 'Foundation (Phase 1)',
    cards: [
      { icon: '📅', title: 'Panchang', desc: 'Tithi · Nakshatra · Rahu Kaal', panel: 'panchang' },
      { icon: '🔗', title: 'Graha Maitri', desc: 'Planetary friendships', panel: 'graha-maitri' },
      { icon: '👁️', title: 'Planetary Aspects', desc: 'Full Vedic Drishti', panel: 'aspects' },
      { icon: '💎', title: 'Gemstone Report', desc: 'Ratna with weight · metal · day', panel: 'gemstone' },
      { icon: '⭐', title: 'Nakshatra Report', desc: '27 Nakshatras · devta · gana', panel: 'nakshatra' },
    ]
  },
  {
    id: 'phase2',
    icon: '🪐',
    title: 'Predictions (Phase 2)',
    cards: [
      { icon: '🪐', title: 'Sade Sati', desc: 'Shani transit · 3 phases', panel: 'sade-sati' },
      { icon: '🐍', title: 'Kaal Sarp Dosha', desc: 'Check · type · remedies', panel: 'kaal-sarp' },
      { icon: '🌍', title: 'Transit (Gochar)', desc: '12-month forecast', panel: 'transit' },
      { icon: '🎭', title: 'Yogini Dasha', desc: '8 Yogini periods', panel: 'yogini-dasha' },
      { icon: '👴', title: 'Pitru Dosha', desc: 'Ancestral karma', panel: 'pitru-dosha' },
    ]
  },
  {
    id: 'phase3',
    icon: '🌟',
    title: 'Precision (Phase 3)',
    cards: [
      { icon: '🌟', title: 'Extended Yogas', desc: 'Raja · Dhana · Mahapurusha', panel: 'yogas-extended' },
      { icon: '⚠️', title: 'Extended Doshas', desc: 'Grahan · Guru Chandal', panel: 'doshas-extended' },
      { icon: '🌀', title: 'Sudarshan Chakra', desc: 'Lagna + Chandra + Surya', panel: 'sudarshan' },
    ]
  },
  {
    id: 'phase4',
    icon: '🔮',
    title: 'Unique (Phase 4)',
    cards: [
      { icon: '🔮', title: 'KP System', desc: 'Sub-lord · Ruling Planets', panel: 'kp-system' },
      { icon: '🎂', title: 'Varshphal', desc: 'Annual chart · Muntha', panel: 'varshphal' },
      { icon: '🏥', title: 'Medical Astrology', desc: 'Weak organs · longevity', panel: 'medical' },
    ]
  },
  {
    id: 'phase5',
    icon: '📐',
    title: 'Advanced (Phase 5)',
    cards: [
      { icon: '📐', title: 'Shadvarga Charts', desc: 'D-1 · D-2 · D-3 · D-4 · D-7 · D-9 · D-10', panel: 'shadvarga' },
      { icon: '💑', title: 'Guna Milan', desc: 'Ashtakoota · 36-point matching', panel: 'guna-milan' },
      { icon: '🔢', title: 'Numerology', desc: 'Mulank · Bhagyank · Chaldean', panel: 'numerology' },
      { icon: '📜', title: 'Classical References', desc: 'BPHS shloka numbers', panel: 'classical-refs' },
    ]
  },
  {
    id: 'phase6',
    icon: '🔱',
    title: 'Final (Phase 6)',
    cards: [
      { icon: '🔱', title: 'Nakshatra Nadi', desc: 'Nadi · Devta · Gana', panel: 'nakshatra-nadi' },
      { icon: '🎯', title: 'Jaimini System', desc: 'Char Dasha · Karakamsha', panel: 'jaimini' },
      { icon: '🔮', title: 'KP Enhanced', desc: 'Sub-Sub Lord · Ruling Planets', panel: 'kp-enhanced' },
      { icon: '📅', title: 'Varshphal 5-Year', desc: '5 saal forecast', panel: 'varshphal-enhanced' },
      { icon: '🌐', title: 'Transit Enhanced', desc: '12-month detailed', panel: 'transit-enhanced' },
      { icon: '📕', title: 'Lal Kitab Enhanced', desc: '3 Teva · House-wise remedies', panel: 'lalkitab-enhanced' },
    ]
  }
];

var cardCounter = 0;

function renderPremiumCardGrid() {
  var target = document.getElementById('premium-card-grid');
  if (!target) {
    // Create container
    var container = document.createElement('div');
    container.id = 'premium-card-grid';
    container.style.cssText = 'margin: 40px 0;';
    
    // Insert after result sections or at specific place
    var anchor = document.getElementById('sec-basic');
    if (anchor) {
      anchor.parentNode.insertBefore(container, anchor);
    } else {
      var result = document.getElementById('result');
      if (result) result.appendChild(container);
    }
    target = container;
  }

  var html = '';
  CARD_CATEGORIES.forEach(function(cat, catIdx) {
    html += '<div class="card-category" data-cat="' + cat.id + '">';
    html += '<div class="card-category-header" onclick="toggleCategory(\'' + cat.id + '\')">';
    html += '<div class="card-category-left">';
    html += '<span class="card-category-icon">' + cat.icon + '</span>';
    html += '<span class="card-category-title">' + cat.title + '</span>';
    html += '<span class="card-category-count">' + cat.cards.length + ' Cards</span>';
    html += '</div>';
    html += '<span class="card-category-toggle">▼</span>';
    html += '</div>';
    html += '<div class="card-category-body">';

    cat.cards.forEach(function(card, idx) {
      cardCounter++;
      html += '<div class="premium-card" onclick="scrollToPanel(\'' + card.panel + '\')">';
      html += '<span class="premium-card-num">' + String(cardCounter).padStart(2, '0') + '</span>';
      html += '<div class="premium-card-header">';
      html += '<span class="premium-card-icon">' + card.icon + '</span>';
      html += '<span class="premium-card-title">' + card.title + '</span>';
      html += '</div>';
      html += '<div class="premium-card-desc">' + card.desc + '</div>';
      html += '<span class="premium-card-arrow">→</span>';
      html += '</div>';
    });

    html += '</div></div>';
  });

  target.innerHTML = html;
  console.log('✅ Premium card grid rendered — ' + cardCounter + ' cards');
}

function toggleCategory(catId) {
  var cat = document.querySelector('.card-category[data-cat="' + catId + '"]');
  if (cat) cat.classList.toggle('collapsed');
}

// Auto-render when result shown
var origRender6 = window.renderExtendedSections;
window.renderExtendedSections = function(data) {
  if (origRender6) origRender6(data);
  setTimeout(renderPremiumCardGrid, 1200);
};

window.renderPremiumCardGrid = renderPremiumCardGrid;
window.toggleCategory = toggleCategory;
console.log('✅ Premium card grid loaded');
