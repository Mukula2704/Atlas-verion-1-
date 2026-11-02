
let macros = { c:0, p:0, cb:0, f:0 };
let timers = { yt: { e:0, int:null }, ugc: { e:0, int:null }, app: { e:0, int:null } };

// ==========================================
// INITIALIZATION
// ==========================================

let currentCdsWeek = 1;
let currentCseWeek = 1;
function init() {
  // Header Dates
  const now = new Date();
  const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  const days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
  document.getElementById("hdrDate").textContent = `${days[now.getDay()]} ${months[now.getMonth()]} ${now.getDate()} ${now.getFullYear()}`;
  document.getElementById("dailyQuote").textContent = `"${QUOTES[Math.floor(Math.random()*QUOTES.length)]}"`;
  
  // Countdown
  now.setHours(0,0,0,0);
  const diff = Math.max(0, Math.ceil((EXAM_DATE - now)/86400000));
  const cdNum = document.getElementById("cdNum");
  if (cdNum) cdNum.textContent = diff;
  const cdsDays = document.getElementById("cdsDays");
  if (cdsDays) cdsDays.textContent = diff;

  // Build Sections
  buildBlocks();
  initProgressTab();
  renderReminders();
  updateDayProgressClock();
  buildGym();
  buildCurriculums(Math.max(1, Math.ceil((now - START_DATE)/86400000)));
  renderSavedMeals();
  
  // Initialize CDS Toggle State
  const cdsToggleState = localStorage.getItem('cc_cds_active') === 'true';
  const cdsToggle = document.getElementById('cdsToggle');
  if (cdsToggle) {
    cdsToggle.checked = cdsToggleState;
    toggleCdsView();
  }
}

function toggleCdsView() {
  const toggle = document.getElementById('cdsToggle');
  const onState = document.getElementById('cdsOnState');
  const offState = document.getElementById('cdsOffState');
  
  if (!toggle || !onState || !offState) return;
  
  if (toggle.checked) {
    onState.style.display = 'block';
    offState.style.display = 'none';
    localStorage.setItem('cc_cds_active', 'true');
  } else {
    onState.style.display = 'none';
    offState.style.display = 'block';
    localStorage.setItem('cc_cds_active', 'false');
  }
}

// ==========================================
// CORE LOGIC
// ==========================================
function switchTab(id, btn) {
  document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
  document.getElementById("tab-" + id).classList.add("active");
  btn.classList.add("active");
}

function buildBlocks() {
  document.getElementById("blocksContainer").innerHTML = SCHEDULE.map((s, i) => `
    <div class="block-card ${s.cls}" id="block-${i}" style="animation: fadeUp 0.4s ease forwards ${i*0.05}s; opacity:0; transform:translateY(15px);">
      <div class="mark-done-circle" onclick="toggleBlockDone(event, ${i})"></div>
      <div onclick="triggerOverlay('${s.cls}', '${s.title}')">
        <div class="block-icon" style="margin-bottom:10px; font-size:1.8rem;">${s.icon}</div>
        <div class="block-title" style="font-size:1.4rem;">${s.title}</div>
      </div>
    </div>
  `).join('');
}

function toggleBlockDone(e, i) {
  e.stopPropagation(); // Prevent overlay from opening
  const el = document.getElementById(`block-${i}`);
  el.classList.toggle('done');
  updateDayProgress();
}

function updateDayProgress() {
  const total = document.querySelectorAll('.block-card').length;
  if(total === 0) return;
  const done = document.querySelectorAll('.block-card.done').length;
  const pct = Math.round((done / total) * 100);
  document.getElementById('dpbPct').textContent = `${pct}%`;
  document.getElementById('dpbFill').style.width = `${pct}%`;
}

let gymHistory = JSON.parse(localStorage.getItem('cc_gym_history')) || {};

function buildGym() {
  const dayStr = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"][new Date().getDay()];
  const g = GYM_SPLIT.find(x => x.d === dayStr) || GYM_SPLIT[0];
  
  let exercisesHtml = g.ex.map((e, index) => {
    // Exclude cardio from having weight inputs
    if (e.name.toLowerCase().includes('cardio') || e.name.toLowerCase().includes('walk') || e.name.toLowerCase().includes('steps')) {
      return `
        <li class="ex-item" style="flex-direction:column; align-items:flex-start; margin-bottom:12px; border-bottom: 1px solid rgba(255,180,200,0.05); padding-bottom:10px;">
          <div style="display:flex; justify-content:space-between; width:100%;">
            <span style="font-weight:600; font-size:1.1rem; color:var(--green);">${e.name}</span>
            <span class="ex-sets">${e.sets}</span>
          </div>
          <div style="font-size:12px; color:var(--muted2); margin-top:4px;"><i>↳ ${e.note}</i></div>
        </li>
      `;
    }

    let hist = gymHistory[e.name] || [];
    let targetWeight = "";
    let isScaleUp = false;
    
    // Extract default target from the note if history is empty
    let match = e.note.match(/(\d+(?:\.\d+)?)kg/);
    if (match) targetWeight = match[1];

    let historyHtml = '<div style="font-size:11px; color:var(--muted); margin-bottom:8px;">No past logs.</div>';
    
    if (hist.length > 0) {
      targetWeight = hist[hist.length - 1].weight;
      
      // Auto scale logic
      if (hist.length >= 2) {
        let last1 = hist[hist.length - 1].weight;
        let last2 = hist[hist.length - 2].weight;
        if (last1 === last2 && last1 > 0) {
          isScaleUp = true;
          let inc = (g.c === 'gcard-legs') ? 5 : 2.5;
          targetWeight = Number(last1) + inc;
        }
      }
      
      // Show up to past 3 logs
      let pastLogs = hist.slice(-3).reverse();
      historyHtml = `<div style="font-size:11px; color:var(--muted); margin-bottom:8px;">
        <strong>Past Logs:</strong><br>
        ${pastLogs.map(h => `• ${h.weight}kg x ${h.reps} reps (${h.sets} sets)`).join('<br>')}
      </div>`;
    }

    return `
      <li class="ex-item" style="flex-direction:column; align-items:flex-start; margin-bottom:15px; border-bottom: 1px solid rgba(255,180,200,0.05); padding-bottom:15px;">
        <div style="display:flex; justify-content:space-between; width:100%; margin-bottom:4px;">
          <span style="font-weight:600; font-size:1.1rem;">${e.name}</span>
          <span class="ex-sets" style="background:rgba(255,255,255,0.1); padding:2px 8px; border-radius:4px;">${e.sets}</span>
        </div>
        ${e.note ? `<div style="font-size:12px; color:var(--muted2); line-height:1.4; margin-bottom:8px;"><i>↳ ${e.note}</i></div>` : ''}
        
        <div style="width:100%; background:var(--surface2); padding:10px; border-radius:8px;">
          ${historyHtml}
          <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
            ${isScaleUp ? `<span style="font-size:11px; background:var(--rose); color:#000; padding:4px 6px; border-radius:4px; font-weight:bold;">🔥 Scale Up</span>` : ''}
            <input type="number" step="0.5" id="gWt_${index}" data-name="${e.name}" value="${targetWeight}" class="log-input" style="width:65px; text-align:center; padding:6px;" placeholder="kg">
            <input type="number" id="gRp_${index}" class="log-input" style="width:65px; text-align:center; padding:6px;" placeholder="Reps">
            <input type="number" id="gSt_${index}" class="log-input" style="width:65px; text-align:center; padding:6px;" placeholder="Sets">
          </div>
        </div>
      </li>
    `;
  }).join('');

  const todayHtml = `
    <div class="gym-card ${g.c}">
      <div class="gym-day">${g.d}</div>
      <div class="gym-type">${g.t}</div>
      <div class="gym-warmup"><strong>Warmup:</strong> ${g.w}</div>
      <ul class="ex-list" style="margin-top:15px;">
        ${exercisesHtml}
      </ul>
    </div>`;
    
  const grid = document.getElementById("gymGrid");
  if(grid) grid.innerHTML = todayHtml;

  const fullHtml = GYM_SPLIT.map(split => `
    <div class="gym-card ${split.c} ${split.d === dayStr ? 'active' : ''}">
      <div class="gym-day">${split.d}</div>
      <div class="gym-type" style="font-size:14px;">${split.t}</div>
      <div class="gym-warmup" style="font-size:11px; margin-bottom:10px;">${split.w}</div>
      <ul class="ex-list">
        ${split.ex.map(e => `
          <li class="ex-item" style="padding:6px 0; border-bottom: 1px solid rgba(255,180,200,0.05); justify-content:space-between;">
            <span style="font-size:12px;">${e.name}</span>
            <span style="font-size:11px; color:var(--muted2);">${e.sets}</span>
          </li>
        `).join('')}
      </ul>
    </div>`).join('');
  const fullGrid = document.getElementById("gymFullGrid");
  if(fullGrid) fullGrid.innerHTML = fullHtml;
}

function switchGymView(view, btn) {
  document.getElementById('btnGymToday').classList.remove('active');
  document.getElementById('btnGymWeek').classList.remove('active');
  btn.classList.add('active');
  
  if(view === 'today') {
    document.getElementById('gymTodayView').style.display = 'block';
    document.getElementById('gymFullWeekView').style.display = 'none';
  } else {
    document.getElementById('gymTodayView').style.display = 'none';
    document.getElementById('gymFullWeekView').style.display = 'block';
  }
}

function saveTodayWorkout() {
  const inputsWeight = document.querySelectorAll('input[id^="gWt_"]');
  let hasData = false;
  
  inputsWeight.forEach(wtInput => {
    let index = wtInput.id.split('_')[1];
    let rpInput = document.getElementById(`gRp_${index}`);
    let stInput = document.getElementById(`gSt_${index}`);
    
    let wt = parseFloat(wtInput.value);
    let rp = parseInt(rpInput.value) || 0;
    let st = parseInt(stInput.value) || 0;
    let name = wtInput.getAttribute('data-name');
    
    if (!isNaN(wt) && wt > 0 && rp > 0 && st > 0) {
      hasData = true;
      if (!gymHistory[name]) gymHistory[name] = [];
      
      // Store weight, reps, sets, and date
      gymHistory[name].push({ 
        date: new Date().toISOString(), 
        weight: wt,
        reps: rp,
        sets: st
      });
    }
  });

  if (hasData) {
    localStorage.setItem('cc_gym_history', JSON.stringify(gymHistory));
    const msg = document.getElementById('gymSaveMsg');
    if (msg) {
      msg.style.display = 'block';
      setTimeout(() => msg.style.display = 'none', 3000);
    }
    buildGym(); // Refresh to show new logs
  } else {
    alert("Please fill out Weight, Reps, and Sets for at least one exercise to save.");
  }
}

let cc_cds_done = JSON.parse(localStorage.getItem('cc_cds_done')) || [];
let cc_cse_done = JSON.parse(localStorage.getItem('cc_cse_done')) || [];

function markCdsDone(day) {
  if (!cc_cds_done.includes(day)) {
    cc_cds_done.push(day);
    localStorage.setItem('cc_cds_done', JSON.stringify(cc_cds_done));
    buildCurriculums(window.lastCalculatedDay || 1);
  }
}

function markCseDone(day) {
  if (!cc_cse_done.includes(day)) {
    cc_cse_done.push(day);
    localStorage.setItem('cc_cse_done', JSON.stringify(cc_cse_done));
    buildCurriculums(window.lastCalculatedDay || 1);
  }
}

function calculateStreak(arr) {
  if(arr.length === 0) return 0;
  let sorted = [...arr].sort((a,b)=>b-a);
  let streak = 1;
  for(let i=0; i<sorted.length-1; i++) {
    if(sorted[i] - sorted[i+1] === 1) streak++;
    else break;
  }
  return streak;
}

function buildCurriculums(currentDay) {
  window.lastCalculatedDay = currentDay;
  // Update Header Stats for CDS
  const cdsDay = Math.min(CDS.length, Math.max(1, currentDay));
  const cdsDoneCount = cc_cds_done.length;
  if(document.getElementById("cdsStudyDay")) document.getElementById("cdsStudyDay").textContent = cdsDay;
  if(document.getElementById("cdsDaysLeft")) document.getElementById("cdsDaysLeft").textContent = 78 - cdsDoneCount;
  if(document.getElementById("cdsDaysDone")) document.getElementById("cdsDaysDone").textContent = cdsDoneCount;
  if(document.getElementById("cdsStreak")) document.getElementById("cdsStreak").textContent = calculateStreak(cc_cds_done) + " 🔥";

  // Update Header Stats for CSE
  const cseDay = Math.min(CSE.length, Math.max(1, currentDay));
  const cseDoneCount = cc_cse_done.length;
  const currCsePhase = CSE.find(x => x.d === cseDay)?.ph.replace('PHASE ','').split('-')[0].trim() || '1';
  if(document.getElementById("cseCurrentDay")) document.getElementById("cseCurrentDay").textContent = cseDay;
  if(document.getElementById("csePhase")) document.getElementById("csePhase").textContent = currCsePhase;
  if(document.getElementById("cseDaysDone")) document.getElementById("cseDaysDone").textContent = cseDoneCount;
  if(document.getElementById("cseStreak")) document.getElementById("cseStreak").textContent = calculateStreak(cc_cse_done) + " 🔥";

  // Render initial weeks based on current day
  const cdsWkObj = CDS.find(x => x.d === cdsDay) || CDS[0];
  const cseWkObj = CSE.find(x => x.d === cseDay) || CSE[0];
  
  if(!window.currentCdsWeek) currentCdsWeek = cdsWkObj.wk;
  if(!window.currentCseWeek) currentCseWeek = cseWkObj.wk;

  renderCDS();
  renderCSE();
}



function initProgressTab() {
  const today = new Date();
  const tStart = new Date("2026-07-01");
  const diffTime = today - tStart;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  if(diffDays <= 0) {
    document.getElementById("progHeroText").textContent = "Starts July 1, 2026";
  } else if (diffDays <= 60) {
    document.getElementById("progHeroText").textContent = "DAY " + diffDays;
    document.getElementById("progHeroText").style.fontSize = "2.5rem";
  } else {
    document.getElementById("progHeroText").textContent = "TRANSFORMATION COMPLETE";
  }
}

let remindersData = JSON.parse(localStorage.getItem('cc_reminders')) || [
  {time: "06:00", text: "Wake up — 10 vocab words before anything else"},
  {time: "10:05", text: "CDS block starts NOW"},
  {time: "21:00", text: "Wind down — CDS review"}
];

function renderReminders() {
  const container = document.getElementById("remindersContainer");
  if(!container) return;
  
  // Sort by time
  remindersData.sort((a,b) => a.time.localeCompare(b.time));
  
  container.innerHTML = remindersData.map((r, i) => `
    <div class="reminder-card">
      <div class="reminder-time">${r.time}</div>
      <div class="reminder-text">${r.text}</div>
      <button class="reminder-del" onclick="deleteReminder(${i})">×</button>
    </div>
  `).join('');
}

function addReminder() {
  const time = document.getElementById("newRemTime").value;
  const text = document.getElementById("newRemText").value;
  if(!time || !text) return;
  remindersData.push({time, text});
  localStorage.setItem('cc_reminders', JSON.stringify(remindersData));
  document.getElementById("newRemTime").value = "";
  document.getElementById("newRemText").value = "";
  renderReminders();
}

function deleteReminder(i) {
  remindersData.splice(i, 1);
  localStorage.setItem('cc_reminders', JSON.stringify(remindersData));
  renderReminders();
}

function updateDayProgressClock() {
  const now = new Date();
  const hrs = now.getHours();
  const mins = now.getMinutes();
  const totalMins = hrs * 60 + mins;
  const pct = Math.min(100, Math.round((totalMins / 1440) * 100));
  
  const pctEl = document.getElementById("remDayPct");
  const fillEl = document.getElementById("remDayFill");
  if(pctEl) pctEl.textContent = pct + "%";
  if(fillEl) fillEl.style.width = pct + "%";
  
  let currentActivity = "Sleep";
  if(hrs >= 6 && hrs < 7) currentActivity = "Gym Session";
  else if(hrs >= 7 && hrs < 8) currentActivity = "Morning Routine";
  else if(hrs >= 8 && hrs < 17) currentActivity = "Deep Work / Career";
  else if(hrs >= 17 && hrs < 21) currentActivity = "App Dev / Skill Building";
  else if(hrs >= 21 && hrs < 22) currentActivity = "Wind down & Journal";
  
  const nowEl = document.getElementById("remDayNow");
  if(nowEl) nowEl.textContent = currentActivity;
  
  setTimeout(updateDayProgressClock, 60000); // update every minute
}

function renderCDS() {
  // Build Nav
  const totalWeeks = 12;
  let navHtml = '';
  for(let i=1; i<=totalWeeks; i++) {
    navHtml += `<button class="week-pill ${i === currentCdsWeek ? 'active' : ''}" onclick="currentCdsWeek=${i}; renderCDS()">Week ${i}</button>`;
  }
  const cdsNav = document.getElementById("cdsWeekNav");
  if(cdsNav) cdsNav.innerHTML = navHtml;

  // Build Container
  const days = CDS.filter(x => x.wk === currentCdsWeek);
  let html = days.map(d => {
    const isDone = cc_cds_done.includes(d.d);
    return `
    <div class="curr-card ${isDone ? 'done' : ''}" style="align-items:flex-start; flex-direction:column; padding: 1.5rem; gap:10px; ${isDone ? 'opacity:0.6; border-color:var(--accent-code);' : ''}">
      <div style="display:flex; justify-content:space-between; width:100%;">
        <div class="curr-meta">Day ${d.d} · Phase ${d.ph} · ${d.sub}</div>
        <div class="curr-badge">${d.type}</div>
      </div>
      <div class="curr-title" style="font-size:1.1rem; color:var(--cream);">${d.topic}</div>
      <div class="curr-sub" style="font-size:13px;">${d.detail}</div>
      <div style="font-size:11px; color:var(--muted); font-style:italic; margin-top:5px;">"${QUOTES[Math.floor(Math.random()*QUOTES.length)]}"</div>
      ${isDone ? 
        `<button class="btn-done" style="margin-top:10px; align-self:flex-end; background:var(--accent-code); color:var(--bg); border:none;" disabled>COMPLETED</button>` : 
        `<button class="btn-done" style="margin-top:10px; align-self:flex-end;" onclick="markCdsDone(${d.d})">Mark Done</button>`}
    </div>
  `}).join('');
  const cdsCont = document.getElementById("cdsContainer");
  if(cdsCont) cdsCont.innerHTML = html;
}

function renderCSE() {
  // Build Nav
  const totalWeeks = 10;
  let navHtml = '';
  for(let i=1; i<=totalWeeks; i++) {
    navHtml += `<button class="week-pill ${i === currentCseWeek ? 'active' : ''}" onclick="currentCseWeek=${i}; renderCSE()">Week ${i}</button>`;
  }
  const cseNav = document.getElementById("cseWeekNav");
  if(cseNav) cseNav.innerHTML = navHtml;

  // Build Container
  const days = CSE.filter(x => x.wk === currentCseWeek);
  let html = days.map(d => {
    const isDone = cc_cse_done.includes(d.d);
    return `
    <div class="curr-card ${isDone ? 'done' : ''}" style="align-items:flex-start; flex-direction:column; padding: 1.5rem; gap:10px; ${isDone ? 'opacity:0.6; border-color:var(--accent-code);' : ''}">
      <div style="display:flex; justify-content:space-between; width:100%;">
        <div class="curr-meta">Day ${d.d} · Week ${d.wk} · ${d.ph}</div>
        <div class="curr-badge" style="background:transparent; border-color:var(--border3); color:var(--text); border-radius:6px; padding:3px 10px;">${d.type}</div>
      </div>
      <div class="curr-title" style="font-size:1.1rem; color:var(--cream);">${d.topic}</div>
      <div class="curr-sub" style="font-size:13px;">${d.detail}</div>
      <div style="font-size:11px; color:var(--muted); font-style:italic; margin-top:5px;">"${QUOTES[Math.floor(Math.random()*QUOTES.length)]}"</div>
      ${isDone ? 
        `<button class="btn-done" style="margin-top:10px; align-self:flex-end; background:var(--accent-code); color:var(--bg); border:none;" disabled>COMPLETED</button>` : 
        `<button class="btn-done" style="margin-top:10px; align-self:flex-end;" onclick="markCseDone(${d.d})">Mark Done</button>`}
    </div>
  `}).join('');
  const cseCont = document.getElementById("cseContainer");
  if(cseCont) cseCont.innerHTML = html;
}

// ==========================================
// NUTRITION & MACROS
// ==========================================
let customMeals = JSON.parse(localStorage.getItem('cc_custom_meals')) || [];

function addMacros(c, p, cb, f) {
  macros.c += c; macros.p += p; macros.cb += cb; macros.f += f;
  renderMacros();
  spawnRipple(window.innerWidth/2, window.innerHeight/2);
}

function renderMacros() {
  document.getElementById("nCal").textContent = macros.c;
  document.getElementById("nProt").textContent = macros.p + "g";
  document.getElementById("nCarb").textContent = macros.cb + "g";
  document.getElementById("nFat").textContent = macros.f + "g";
}

function renderSavedMeals() {
  const grid = document.getElementById("savedMealsGrid");
  if(customMeals.length === 0) {
    grid.innerHTML = '<div style="font-size:12px; color:var(--muted); text-align:center;">No meals saved yet. Build one below!</div>';
    return;
  }
  grid.innerHTML = customMeals.map(m => `
    <button class="quick-add-btn" style="text-align:left;" onclick="addMacros(${m.c}, ${m.p}, ${m.cb}, ${m.f})">
      <div style="font-weight:bold;">${m.n}</div>
      <div style="font-size:11px; color:var(--muted); margin-top:4px;">${m.c} kcal | ${m.p}P ${m.cb}C ${m.f}F</div>
    </button>
  `).join('');
}

function saveCustomMeal() {
  const n = document.getElementById("mName").value || 'Custom Meal';
  const c = parseInt(document.getElementById("mCal").value) || 0;
  const p = parseInt(document.getElementById("mProt").value) || 0;
  const cb = parseInt(document.getElementById("mCarb").value) || 0;
  const f = parseInt(document.getElementById("mFat").value) || 0;
  if(c === 0) return;

  customMeals.push({n, c, p, cb, f});
  localStorage.setItem('cc_custom_meals', JSON.stringify(customMeals));
  renderSavedMeals();

  document.getElementById("mName").value = '';
  document.getElementById("mCal").value = '';
  document.getElementById("mProt").value = '';
  document.getElementById("mCarb").value = '';
  document.getElementById("mFat").value = '';
}

function addCustomFood() {
  const c = parseInt(document.getElementById("mCal").value) || 0;
  const p = parseInt(document.getElementById("mProt").value) || 0;
  const cb = parseInt(document.getElementById("mCarb").value) || 0;
  const f = parseInt(document.getElementById("mFat").value) || 0;
  if(c === 0) return;
  addMacros(c, p, cb, f);
  
  document.getElementById("mCal").value = '';
  document.getElementById("mProt").value = '';
  document.getElementById("mCarb").value = '';
  document.getElementById("mFat").value = '';
}

// ==========================================
// BARCODE SCANNER
// ==========================================
let html5QrcodeScanner = null;

function toggleScanner() {
  const reader = document.getElementById("reader");
  const btn = document.getElementById("scanBtn");
  
  if (reader.style.display === "block") {
    if(html5QrcodeScanner) html5QrcodeScanner.clear();
    reader.style.display = "none";
    btn.textContent = "Scan Barcode";
  } else {
    reader.style.display = "block";
    btn.textContent = "Close Scanner";
    
    html5QrcodeScanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 }, false);
    html5QrcodeScanner.render(onScanSuccess, onScanFailure);
  }
}

function onScanSuccess(decodedText, decodedResult) {
  toggleScanner();
  const url = `https://world.openfoodfacts.org/api/v0/product/${decodedText}.json`;
  
  fetch(url)
    .then(res => res.json())
    .then(data => {
      if(data.status === 1) {
        const p = data.product;
        const name = p.product_name || "Unknown Product";
        const nut = p.nutriments || {};
        
        const kcal = nut['energy-kcal_100g'] || 0;
        const prot = nut.proteins_100g || 0;
        const carb = nut.carbohydrates_100g || 0;
        const fat = nut.fat_100g || 0;
        
        if (confirm(`Log 100g of ${name}?\n${kcal} kcal | ${prot}g Prot | ${carb}g Carb | ${fat}g Fat`)) {
          addMacros(Math.round(kcal), Math.round(prot), Math.round(carb), Math.round(fat));
        }
      } else {
        if(confirm("Product not found. Would you like to log macros manually?")) {
          switchTab('nutrition', document.querySelector('.nav-btn[onclick="switchTab(\\\'nutrition\\\',this)"]'));
          document.getElementById('mName').focus();
        }
      }
    })
    .catch(err => {
      console.error(err);
      if(confirm("Error fetching product data. Would you like to log macros manually?")) {
        switchTab('nutrition', document.querySelector('.nav-btn[onclick="switchTab(\\\'nutrition\\\',this)"]'));
        document.getElementById('mName').focus();
      }
    });
}

function onScanFailure(error) {
  // Quiet failure for frame scanning
}

// ==========================================
// GEMINI AI OVERSEER
// ==========================================
function saveGeminiKey() {
  const key = document.getElementById("geminiKey").value;
  if(key) {
    localStorage.setItem('cc_gemini_key', key);
    alert("Gemini API Key Saved to Local Storage!");
    document.getElementById("geminiKey").value = '';
  }
}

function generateAIAnalysis() {
  const key = localStorage.getItem('cc_gemini_key');
  if(!key) {
    alert("Please paste and save your Gemini API key first.");
    return;
  }
  
  const box = document.getElementById("aiReportBox");
  box.innerHTML = "<em>Analyzing all metrics and your journal... Please wait...</em>";
  
  let recentJournals = JSON.parse(localStorage.getItem('cc_journals') || '[]');
  let journalContext = recentJournals.length > 0 ? "My recent journal entry: " + recentJournals[0].text : "No recent journal entries.";

  const prompt = `Act as a high-performance fitness and productivity coach for me (Mukul). I am aiming for a Greek God physique and building my career.
  Read my daily data and my personal journal entry. If my journal shows I am struggling or feeling down, adapt your tone to be understanding and empathetic, while still holding me accountable to my goals. Do not just blindly act like David Goggins if I need support, but don't let me make excuses either.
  
  Data for today: 
  Steps: ${document.getElementById("mSteps") ? document.getElementById("mSteps").textContent : "0"}, Sleep: ${document.getElementById("mSleep") ? document.getElementById("mSleep").textContent : "0"}h, 
  Nutrition: ${macros.c}kcal, ${macros.p}g Protein. 
  
  ${journalContext}

  Give me a 3-paragraph, actionable analysis on my progress and mindset.`;

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${key}`;
  
  fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
  })
  .then(res => res.json())
  .then(data => {
    if(data.error) {
      box.innerHTML = `<span style="color:var(--accent-warn)">API Error: ${data.error.message}</span>`;
    } else {
      const text = data.candidates[0].content.parts[0].text;
      box.innerHTML = `<strong>Coach's Verdict:</strong><br><br>${text}`;
    }
  })
  .catch(err => {
    box.innerHTML = `<span style="color:var(--accent-warn)">Network Error fetching AI analysis. Check your key.</span>`;
  });
}

// ==========================================
// JOURNAL SYSTEM
// ==========================================
function saveJournal() {
  const input = document.getElementById("journalInput");
  const isBackdate = document.getElementById("journalBackdate") && document.getElementById("journalBackdate").checked;
  const text = input.value.trim();
  if(!text) {
    alert("Please write something before saving.");
    return;
  }
  
  let entryDate = new Date();
  if (isBackdate) {
    entryDate.setDate(entryDate.getDate() - 1);
    // Set time to around 10:00 PM for consistency with "last night"
    entryDate.setHours(22, 0, 0, 0);
  }
  
  let journals = JSON.parse(localStorage.getItem('cc_journals') || '[]');
  journals.unshift({
    date: entryDate.toLocaleString(),
    text: text
  });
  
  // Sort journals by date descending just in case backdating mixed up the order
  journals.sort((a, b) => new Date(b.date) - new Date(a.date));
  
  localStorage.setItem('cc_journals', JSON.stringify(journals));
  input.value = "";
  if (document.getElementById("journalBackdate")) {
    document.getElementById("journalBackdate").checked = false;
  }
  renderJournals();
  alert(isBackdate ? "Journal saved for yesterday night." : "Journal saved.");
}

function renderJournals() {
  const container = document.getElementById("journalEntriesContainer");
  if(!container) return;
  
  let journals = JSON.parse(localStorage.getItem('cc_journals') || '[]');
  container.innerHTML = "";
  
  journals.forEach(j => {
    let div = document.createElement('div');
    div.className = "log-form-box";
    div.style.padding = "1rem";
    div.innerHTML = `
      <div style="font-size:10px; color:var(--muted); margin-bottom:8px;">${j.date}</div>
      <div style="font-size:13px; color:var(--text); line-height:1.5;">${j.text.replace(/\\n/g, '<br>')}</div>
    `;
    container.appendChild(div);
  });
}

// Call renderJournals on load
window.addEventListener('DOMContentLoaded', () => {
  if(document.getElementById('journalEntriesContainer')) {
    renderJournals();
  }
});

// ==========================================
// TIMERS & HUAWEI PARSER
// ==========================================
function toggleTimer(id) {
  let t = timers[id];
  if(t.int) { clearInterval(t.int); t.int = null; } 
  else {
    t.int = setInterval(() => {
      t.e++;
      const h = Math.floor(t.e / 3600);
      const m = Math.floor((t.e % 3600) / 60);
      const s = t.e % 60;
      document.getElementById(id === 'yt' ? 'displayYT' : 'displayApp').textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
    }, 1000);
  }
}

function parseDataFile(e) {
  const f = e.target.files[0];
  if(!f) return;
  // Simulating the parser reading Huawei CSV formats
  setTimeout(() => {
    document.getElementById("mSteps").textContent = "12,450";
    document.getElementById("mSleep").textContent = "6.8";
    document.getElementById("mHrv").textContent = "58";
    document.getElementById("mCycle").textContent = "18.2";
  }, 500);
}

// ==========================================
// OVERLAY SYSTEM & RIPPLES
// ==========================================
function triggerOverlay(cls, title) {
  const ov = document.getElementById("focusOverlay");
  ['focus-default','focus-gf','focus-cds','focus-cse','focus-cycle','focus-gym'].forEach(id => {
    let el = document.getElementById(id);
    if(el) el.style.display = 'none';
  });
  
  const currentDay = Math.max(1, Math.ceil((new Date() - START_DATE)/86400000));
  
  if (cls === 'blk-gf') {
    document.getElementById("focus-gf").style.display = 'block';
    const timeElem = document.getElementById("fgfTime");
    if(timeElem) timeElem.style.display = 'none';
  } else if (cls === 'blk-cds') {
    document.getElementById("focus-cds").style.display = 'block';
    document.getElementById("fcdsTitle").textContent = "Today's CDS";
    const timeElem = document.getElementById("fcdsTime");
    if(timeElem) timeElem.style.display = 'none';
    
    // Inject day's data
    const cdsDayObj = CDS.find(x => x.d === Math.min(CDS.length, currentDay)) || CDS[0];
    const quote = QUOTES[Math.floor(Math.random()*QUOTES.length)];
    const subElem = document.querySelector("#focus-cds .focus-sub");
    if(subElem) subElem.innerHTML = `<div style="text-align:left; background:rgba(0,0,0,0.3); padding:1rem; border-radius:10px; border:1px solid var(--border);">
      <div style="font-size:12px; color:var(--muted); margin-bottom:5px;">PHASE ${cdsDayObj.ph} | WEEK ${cdsDayObj.wk} | DAY ${cdsDayObj.d}</div>
      <div style="font-size:18px; color:var(--cream); font-weight:600; margin-bottom:8px;">${cdsDayObj.topic}</div>
      <div style="font-size:14px; color:var(--text); line-height:1.4; margin-bottom:15px;">${cdsDayObj.detail}</div>
      <div style="font-size:12px; color:var(--rose); font-style:italic;">"${quote}"</div>
    </div>`;
  } else if (cls === 'blk-cse') { // CSE
    const fcse = document.getElementById("focus-cse");
    if(fcse) fcse.style.display = 'block';
    const titleEl = document.getElementById("fcseTitle");
    if(titleEl) titleEl.textContent = "Today's CSE";
    
    const cseDayObj = CSE.find(x => x.d === Math.min(CSE.length, currentDay)) || CSE[0];
    const quote = QUOTES[Math.floor(Math.random()*QUOTES.length)];
    const subElem = document.getElementById("fcseSub");
    if(subElem) subElem.innerHTML = `<div style="text-align:left; background:rgba(0,0,0,0.3); padding:1rem; border-radius:10px; border:1px solid var(--border);">
      <div style="font-size:12px; color:var(--muted); margin-bottom:5px;">PHASE ${cseDayObj.ph} | WEEK ${cseDayObj.wk} | DAY ${cseDayObj.d}</div>
      <div style="font-size:18px; color:var(--cream); font-weight:600; margin-bottom:8px;">${cseDayObj.topic}</div>
      <div style="font-size:14px; color:var(--text); line-height:1.4; margin-bottom:15px;">${cseDayObj.detail}</div>
      <div style="font-size:12px; color:var(--accent-code); font-style:italic;">"${quote}"</div>
    </div>`;
  } else if (cls === 'blk-travel') {
    document.getElementById("focus-cycle").style.display = 'block';
    const timeElem = document.getElementById("fcycTime");
    if(timeElem) timeElem.style.display = 'none';
  } else if (cls === 'blk-gym') {
    document.getElementById("focus-gym").style.display = 'block';
    document.getElementById("fgymTitle").textContent = "Today's Split";
    const timeElem = document.getElementById("fgymTime");
    if(timeElem) timeElem.style.display = 'none';
    
    const dayStr = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"][new Date().getDay()];
    const g = GYM_SPLIT.find(x => x.d === dayStr) || GYM_SPLIT[0];
    const quote = QUOTES[Math.floor(Math.random()*QUOTES.length)];
    
    const subElem = document.getElementById("fgymWarmup");
    if(subElem) subElem.innerHTML = `<div style="text-align:left; background:rgba(0,0,0,0.3); padding:1rem; border-radius:10px; border:1px solid var(--border);">
      <div style="font-size:18px; color:var(--cream); font-weight:600; margin-bottom:8px;">${g.t}</div>
      <div style="font-size:12px; color:var(--muted); margin-bottom:12px;"><strong>Warmup:</strong> ${g.w}</div>
      <ul style="list-style:none; padding:0; margin:0 0 15px 0;">
        ${g.ex.map(e => `<li style="padding:6px 0; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; font-size:14px;"><span>${e.name}</span><span style="color:var(--muted2);">${e.sets}</span></li>`).join('')}
      </ul>
      <div style="font-size:12px; color:var(--rose); font-style:italic; text-align:center;">"${quote}"</div>
    </div>`;
  } else {
    document.getElementById("focus-default").style.display = 'block';
    document.getElementById("fdTitle").textContent = title;
    const timeElem = document.getElementById("fdTime");
    if(timeElem) timeElem.style.display = 'none';
  }
  
  ov.classList.add("active");
}

function closeFocus() {
  document.getElementById("focusOverlay").classList.remove("active");
  spawnRipple(window.innerWidth/2, window.innerHeight/2);
}

function spawnRipple(x, y) {
  const r = document.createElement("div"); r.className = "tap-ripple";
  const size = Math.min(window.innerWidth, window.innerHeight) * 1.5;
  r.style.cssText = `width:${size}px; height:${size}px; left:${x-size/2}px; top:${y-size/2}px;`;
  document.body.appendChild(r);
  setTimeout(() => r.remove(), 700);
}

init();

// ==========================================
// AI NEURAL LINK SYSTEM
// ==========================================

const aiTerminal = document.getElementById("aiTerminalStream");
const visionFeed = document.getElementById("aiVisionFeed");
const aiNodes = {
  server: document.getElementById("node-server"),
  vision: document.getElementById("node-vision")
};

function addAILog(source, message) {
  if (!aiTerminal) return;
  const now = new Date();
  const timeStr = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
  
  const entry = document.createElement("div");
  entry.className = "ai-log-entry";
  entry.innerHTML = `
    <span class="ai-log-time">[${timeStr}]</span>
    <span class="ai-log-source ${source.toUpperCase()}">${source.toUpperCase()}:</span>
    ${message}
  `;
  
  aiTerminal.appendChild(entry);
  aiTerminal.scrollTop = aiTerminal.scrollHeight;
}

// Temporary Simulation of AI Node Activity (until Firebase is connected)
setTimeout(() => {
  addAILog("SYSTEM", "Handshake complete. Neural Link established.");
  if (aiNodes.server) aiNodes.server.classList.add("online");
}, 1500);

setTimeout(() => {
  addAILog("VISION", "OpenCV module initialized. Requesting spatial geometry...");
  if (aiNodes.vision) aiNodes.vision.classList.add("online");
}, 3000);

setTimeout(() => {
  addAILog("SWARM", "Retrieving historical context vectors. Awaiting tasks.");
}, 4500);

// ==========================================
// AI PROJECT MASTERCLASS
// ==========================================
function openMasterclass() {
  const modal = document.getElementById('masterclassModal');
  const container = document.getElementById('masterclassContent');
  if (!modal || !container) return;
  
  if (typeof AI_MASTERCLASS === 'undefined') {
    container.innerHTML = '<div style="color:var(--rose);">Error: masterclass.js not loaded. Refresh the page.</div>';
    modal.style.display = 'flex';
    return;
  }

  let html = `<div style="color:var(--muted); font-size:12px; margin-bottom:10px;">Study this curriculum to understand the AI backend architecture.</div>`;
  
  AI_MASTERCLASS.forEach(lesson => {
    html += `
      <div style="background:rgba(0,0,0,0.5); padding:1rem; border-radius:10px; border:1px solid var(--border);">
        <div style="font-size:12px; color:var(--rose); margin-bottom:5px;">LESSON ${lesson.day} | ${lesson.topic}</div>
        <div style="font-size:18px; color:var(--cream); font-weight:600; margin-bottom:8px;">${lesson.title}</div>
        <div style="font-size:14px; color:var(--text); line-height:1.5; margin-bottom:15px;">${lesson.detail}</div>
        <div style="background:#0a0808; padding:10px; border-radius:6px; border:1px solid var(--border2); font-family:var(--mono); font-size:12px; color:#a9dc76; overflow-x:auto; white-space:pre-wrap;">${lesson.codeSnippet}</div>
      </div>
    `;
  });

  container.innerHTML = html;
  modal.style.display = 'flex';
}

