# Chapter 1: Global State, Navigation, and DOM Manipulation

This chapter breaks down the exact variables and functions that control how the application behaves, remembers state, and switches between views without reloading the page.

## 1. Global State Variables (Lines 760 - 775)
In `index.html`, right after initializing Firebase, we declare our "Global State". These variables exist in the browser's RAM as long as the tab is open.

```javascript
let macros = { c:0, p:0, cb:0, f:0 };
let timers = { yt: { e:0, int:null }, ugc: { e:0, int:null }, app: { e:0, int:null } };
let uploadedScreenshots = [];
let cc_cds_done = [];
let cc_cse_done = [];
let customMeals = [];
let remindersData = [ ... ];
let hydrationGlasses = 0;
let completedBlocks = [];
let gymToday = [];
const todayStr = new Date().toISOString().split('T')[0];
```

### Why we did this:
Instead of querying the HTML DOM every time we want to know how many calories you've eaten (e.g., `document.getElementById('nCal').innerText`), we store the "source of truth" in these Javascript variables. 
* `timers`: This object tracks three different timers (Job Hunt, Freelance, App Dev). `e` stands for elapsed seconds, and `int` holds the `setInterval` ID so we can pause it later.
* `todayStr`: We use `new Date().toISOString().split('T')[0]` to get a string like `"2026-08-28"`. This is crucial for checking if a new day has started so we can reset your calories.

---

## 2. The Single Page Application Navigation (Lines 1100 - 1115)

Traditional websites have multiple HTML files (`about.html`, `contact.html`). When you click a link, the browser flashes white and loads the new file. We built a **Single Page Application (SPA)**, meaning everything is in `index.html`, and we use Javascript to hide/show sections.

### The `switchTab()` Function
```javascript
function switchTab(tabId, btnElem) {
  // 1. Hide all panels
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  
  // 2. Remove 'active' styling from all buttons
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  
  // 3. Show the requested panel
  document.getElementById('tab-' + tabId).classList.add('active');
  
  // 4. Highlight the clicked button
  btnElem.classList.add('active');
}
```

### How it works line-by-line:
1. `document.querySelectorAll('.panel')` grabs every single `<div>` that has the class `panel`. It returns a NodeList (like an array).
2. `.forEach(p => p.classList.remove('active'))` loops through all of them and removes the `.active` CSS class. In our CSS, `.panel` has `display: none`, but `.panel.active` has `display: block`. By removing the class, we hide everything on the screen instantly.
3. We do the exact same thing to the navigation buttons to remove the gold/red highlight.
4. `document.getElementById('tab-' + tabId).classList.add('active');` takes the string you passed in (e.g., `"cse"`), concatenates it to `"tab-cse"`, finds that specific `<div>`, and makes it visible.

### What else can be done here?
Currently, if you refresh the page, it always defaults to the Dashboard tab. We could use the **Browser History API** (`window.history.pushState()`) to append `?tab=cse` to the URL. This way, if you refresh the page, Javascript can read the URL and automatically open the tab you were looking at.

---

## 3. The Central Initialization (Line 1886)

At the very bottom of the file, we call `init()`. 
```javascript
function init() {
  setInterval(updateClocks, 1000);
  buildCurriculums(1);
  checkAndResetDaily();
  initCloudSync();
  renderSavedMeals();
  renderReminders();
}
```
### Why we did this:
When the HTML finishes loading, we need to "kickstart" the Javascript engine. 
* `setInterval(updateClocks, 1000)` tells the browser to run the `updateClocks()` function every 1000 milliseconds (1 second). This is what makes your dashboard clock tick in real-time.
* `initCloudSync()` opens the WebSocket connection to Firebase.

If we didn't have an `init()` function and just ran these commands globally, they might try to execute *before* the HTML elements exist on the screen, causing a `null` error. By placing `init()` at the very bottom of the file, we guarantee the DOM is fully loaded before we start attaching data to it.
