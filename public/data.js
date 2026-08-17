// ==========================================
// COMMAND CENTER - DATA ARCHITECTURE
// ==========================================
const EXAM_DATE = new Date("2026-09-13");
const START_DATE = new Date("2026-07-10");

const QUOTES = [
  "No one who works hard regrets it. Everyone who quits does.",
  "The stars on your shoulders aren't given; they are earned in the dark.",
  "September 13th doesn't care if your legs were shot from the 60km ride. Show up anyway.",
  "The Officers Training Academy is waiting for the man you are building right now. Do not keep them waiting.",
  "Sweat saves blood. The highway traffic today makes the drill square easier tomorrow.",
  "You are training to lead soldiers. Do not negotiate with your own weakness.",
  "A future officer doesn't complain about a 100g protein limit; he executes the mission with the rations he has.",
  "The uniform won't fit a man who quits when he's tired.",
  "Every CDS previous year’s question you solve is one step closer to the merit list.",
  "They are looking for elite mental grit. Your 45-day survival plan is exactly that.",
  "You want the Special Forces? Then start treating this commute like your selection course.",
  "The work you do in the shadows on the highway will show in the light on the parade ground.",
  "The potholes and the traffic are just resistance training for your mind. Keep pedaling.",
  "Your legs are burning on the pedals because the fat is leaving. Don't stop.",
  "No Greek God illusions. Just a rugged, tactical athlete being forged day by day.",
  "The barbell doesn't care about your commute. Move the weight.",
  "You don't need motivation when you have a 45-day deadline. Execute the split.",
  "Vehicle days are your shield. Cycle days are your sword. Use them tactically.",
  "Sleep is a weapon. 8 hours is a tactical requirement, not a luxury.",
  "The fatigue you feel at kilometer 45 is where the average man breaks. You are not average.",
  "The dark circles will fade when you lock in the sleep. The muscle you build will stay forever.",
  "A 72-hour fast proved your mind controls your body. Don't forget you have that power.",
  "Embrace the suck. The heavier the squats feel on Saturday night, the closer you are to the breakthrough.",
  "Clearing backlogs and writing code—it’s all part of the same mental endurance test.",
  "A flawless CI/CD pipeline requires the exact same precision as your workout split.",
  "2027 is the target. Every study session, every cleared subject, secures the perimeter.",
  "Building a Hyperledger voting system takes architecture. So does building a tactical body.",
  "You control the infrastructure of your life, just like Terraform. Code it right.",
  "Don't let the capstone project slip. Officers execute on all fronts simultaneously.",
  "Debug your mindset the same way you debug a smart contract. Find the error, patch it, and run it again.",
  "Indu is watching you become the man you promised her you'd be. Don't stop.",
  "Build the physique, earn the commission, and give Indu the life she deserves.",
  "Mom needs a role model for her channel. Show her what relentless consistency looks like.",
  "Be the rock Mom can lean on. Your strength elevates your whole family.",
  "Engraved rings and surprises are beautiful, but your uncompromising discipline is the greatest gift you can offer Indu.",
  "When the ride gets too heavy, remember whose name is on the line. Do it for Indu.",
  "Financial freedom for Mom starts with the investments and the discipline you build today.",
  "The silver pendant is just a symbol; the real gift to Indu is the uncompromising, elite man you are becoming.",
  "When the commute feels too long, think about the exact future you and Indu are building together. That is the real destination.",
  "Mom is watching your daily grind. Show her that the same dedication it takes to build a secure portfolio is what it takes to build an unbreakable body.",
  "Every time you push past the pain barrier on those pedals, you are forging a stronger protector for Indu.",
  "Those anniversaries you plan for Indu deserve a man who is disciplined enough to lead. Be that man.",
  "You are managing Mom's financial future while building your own physical resilience. Carry the weight for your family, and keep carrying it.",
  "Indu deserves the absolute best, most hardened version of you. Do not let a little highway fatigue stand in the way of giving her that.",
  "Mom's success as a creator and your success on the military parade ground are fueled by the exact same fire. Lead the charge for both of you.",
  "When you feel like skipping the heavy leg session, remember that Indu's belief in you is non-negotiable. Match her belief with your actions.",
  "Your family's legacy shifts with you. The sweat you pour onto the asphalt today buys the freedom and security they will rely on tomorrow.",
  "There is no biological difference between you and the men who succeed, only a difference in grit.",
  "Motivation fades when the alarm goes off. Discipline puts your feet on the floor.",
  "The pain of discipline weighs ounces. The pain of regret weighs tons.",
  "No one is coming to ride the 30km for you. Own it.",
  "Stop negotiating with the voice in your head that wants comfort. It is your enemy.",
  "45 days. No cheating. No excuses. Just ruthless execution.",
  "You are Mukul A. Act like it.",
  "If it were easy, everyone would have the commission and the athletic core.",
  "You can either have excuses or results. You can never have both.",
  "Do not lower your goals to meet your budget. Raise your discipline to meet your goals.",
  "You survived today. Now eat your rice, sleep your 8 hours, and prepare to go to war again tomorrow.",
  "Nobody cares how tired you are. Let your results do the talking.",
  "Let them sleep. Let them walk. You have a cycle to catch and a future to claim.",
  "Your body is listening to everything your mind says. Tell it to push harder.",
  "The body achieves what the mind believes. Keep going.",
  "Discipline is choosing between what you want now and what you want most.",
  "Every rep, every kilometre, every page — it compounds. Trust the process.",
  "You're not tired, you're just uncomfortable. Push through.",
  "September 13th is coming whether you're ready or not. Be ready.",
  "The physique, the commission, the channel — all of it is built in the boring moments.",
  "One day you'll look back and thank yourself for not quitting today.",
  "Indu believes in you. Don't let yourself down.",
  "Hard days build the foundation. Easy days are for people with average goals.",
  "Stay locked in. Distractions are expensive.",
  "Your future self is watching you right now. Make him proud."
];

const SCHEDULE = [
  {
    "icon": "🏋️",
    "title": "Gym",
    "cls": "blk-gym"
  },
  {
    "icon": "💼",
    "title": "Job Hunt",
    "cls": "blk-career"
  },
  {
    "icon": "💻",
    "title": "App Dev",
    "cls": "blk-cse"
  },
  {
    "icon": "🚀",
    "title": "Freelance",
    "cls": "blk-freelance"
  },
  {
    "icon": "🥗",
    "title": "Nutrition",
    "cls": "blk-nutrition"
  },
  {
    "icon": "📖",
    "title": "CDS Prep",
    "cls": "blk-cds"
  },
  {
    "icon": "📝",
    "title": "Journal",
    "cls": "blk-journal"
  },
  {
    "icon": "💗",
    "title": "Indu",
    "cls": "blk-gf"
  }
];

const GYM_SPLIT = [
  {
    d: "Mon", t: "Heavy Push (Chest, Shoulders, Triceps)", c: "gcard-push", 
    w: "Dynamic chest stretches, Light band presses", 
    ex: [
      { name: "Machine Chest Press", sets: "3x6-8", note: "Heavy load, 55-60kg." },
      { name: "Incline DB Press", sets: "3x8-10", note: "25kg+ per hand." },
      { name: "DB Lateral Raises", sets: "3x12", note: "10-12.5kg per hand." },
      { name: "Tricep Cable Pushdowns", sets: "3x12", note: "60kg, squeeze at the bottom." },
      { name: "Incline Walk (Cardio)", sets: "15 Min", note: "130 bpm heart rate." }
    ]
  },
  {
    d: "Tue", t: "Heavy Pull (Back, Biceps, Wrists)", c: "gcard-pull", 
    w: "Dead hangs (2x30s), Light lat pulldowns", 
    ex: [
      { name: "Lat Pulldown", sets: "3x8-10", note: "Heavy, 60-65kg." },
      { name: "Seated Cable Row", sets: "3x10", note: "60kg, pull to belly button." },
      { name: "Hammer Curls", sets: "3x10", note: "Wrist safe! 12.5-15kg per hand." },
      { name: "Dead Hangs", sets: "3xMax Time", note: "Tendon strength and grip." },
      { name: "Incline Walk (Cardio)", sets: "15 Min", note: "Keep moving to burn fat." }
    ]
  },
  {
    d: "Wed", t: "Heavy Legs & Core", c: "gcard-legs", 
    w: "Bodyweight squats, hip openers", 
    ex: [
      { name: "45-Degree Hack Squat", sets: "3x6-8", note: "70-80kg, deep stretch." },
      { name: "Barbell Hip Thrusts", sets: "3x10", note: "50-60kg." },
      { name: "Lying Leg Curls", sets: "3x10", note: "20kg, squeeze hamstrings." },
      { name: "Weighted Cable Crunches", sets: "3x15", note: "Heavy weight for core blocks." },
      { name: "Incline Walk (Cardio)", sets: "15 Min", note: "Flush the legs." }
    ]
  },
  {
    d: "Thu", t: "Upper Body (Metabolic Supersets)", c: "gcard-push", 
    w: "Rotator cuff work, band dislocations", 
    ex: [
      { name: "Superset: Flat DB Press & Lat Pulldown", sets: "3x10", note: "25kg DBs / 55kg Pulldown. No rest between." },
      { name: "Superset: Lateral Raises & EZ-Bar Curls", sets: "3x12", note: "10kg DBs / 20kg EZ-Bar." },
      { name: "Tricep Overhead Cable Extensions", sets: "3x12", note: "Burnout the triceps." },
      { name: "Incline Walk (Cardio)", sets: "15 Min", note: "Sweat it out." }
    ]
  },
  {
    d: "Fri", t: "Lower Body (Metabolic) & Tendons", c: "gcard-legs", 
    w: "Dynamic leg swings, empty hack squat", 
    ex: [
      { name: "Hack Squat", sets: "3x10-12", note: "60kg, higher reps for metabolic burn." },
      { name: "Leg Extensions", sets: "3x15", note: "25-30kg, constant tension." },
      { name: "Farmer's Walks", sets: "3x60 sec", note: "Grab heavy DBs, walk. Builds grip & core." },
      { name: "EZ-Bar Reverse Curls", sets: "3x15", note: "Palms down. Protects the wrist joint." },
      { name: "Incline Walk (Cardio)", sets: "15 Min", note: "Final cardio of the week." }
    ]
  },
  {
    d: "Sat", t: "Active Fat Burn", c: "gcard-pull", 
    w: "Stretching and mobility", 
    ex: [
      { name: "Steady State Cardio", sets: "30-45 Min", note: "Cycle or Treadmill. Zone 2." },
      { name: "Core Work (Optional)", sets: "3xFail", note: "Planks or leg raises." }
    ]
  },
  {
    d: "Sun", t: "Full Rest", c: "gcard-legs", 
    w: "Relax and recover", 
    ex: [
      { name: "10,000 Steps", sets: "Daily Goal", note: "Keep non-exercise activity high." }
    ]
  }
];

// ═══════════════════════════════════════════
// CDS 78-DAY CURRICULUM
// ═══════════════════════════════════════════
const CDS = [
  {d:1,ph:1,wk:1,sub:"GK",topic:"Modern History",detail:"1857 Revolt — causes, events, aftermath. Flash table: Ancient/Medieval key facts. Science: Newton's Laws basics.",type:"Teach + Drill"},
  {d:2,ph:1,wk:1,sub:"English",topic:"Spotting Errors",detail:"Subject-Verb Agreement — Each, Every, Neither, Either rules. 20 PYQs drill.",type:"Drill"},
  {d:3,ph:1,wk:1,sub:"GK",topic:"Modern History",detail:"INC formation, Moderate vs Extremist phase. Science: Motion & Force.",type:"Teach + Drill"},
  {d:4,ph:1,wk:1,sub:"English",topic:"Spotting Errors",detail:"Collective nouns, Pronoun-antecedent agreement. 20 PYQs.",type:"Drill"},
  {d:5,ph:1,wk:1,sub:"GK",topic:"Modern History",detail:"Partition of Bengal, Swadeshi Movement, Morley-Minto Reforms. Science: Work, Energy, Power.",type:"Teach + Drill"},
  {d:6,ph:1,wk:1,sub:"Mixed",topic:"Week 1 Review",detail:"10-min Ancient/Medieval flash table + Spotting errors practice set.",type:"Review + PYQ"},
  {d:7,ph:1,wk:1,sub:"GK",topic:"Modern History",detail:"Non-Cooperation 1920, Chauri Chaura, Civil Disobedience. Science: Electricity basics.",type:"Teach + Drill"},
  {d:8,ph:1,wk:2,sub:"English",topic:"Spotting Errors",detail:"Tense errors, Prepositions intro. 20 PYQs.",type:"Drill"},
  {d:9,ph:1,wk:2,sub:"GK",topic:"Geography",detail:"Physical features of India — mountains, plateaus, plains, rivers. Science: Chemistry elements.",type:"Teach + Drill"},
  {d:10,ph:1,wk:2,sub:"English",topic:"Sentence Improvement",detail:"Core sentence improvement patterns. 20 PYQs.",type:"Drill"},
  {d:11,ph:1,wk:2,sub:"GK",topic:"Geography",detail:"Indian rivers — origin, tributaries, significance. Science: Acids, Bases, Salts.",type:"Teach + Drill"},
  {d:12,ph:1,wk:2,sub:"Mixed",topic:"Review",detail:"Geography map quiz + error spotting mixed set.",type:"Review + PYQ"},
  {d:13,ph:1,wk:2,sub:"GK",topic:"Modern History",detail:"Quit India 1942, INA, Subhas Chandra Bose. Science: Biology — cells and tissues.",type:"Teach + Drill"},
  {d:14,ph:1,wk:2,sub:"English",topic:"Spotting Errors",detail:"Prepositions deep drill — at/in/on/by/with/for. 25 PYQs.",type:"Drill"},
  {d:15,ph:1,wk:3,sub:"GK",topic:"Geography",detail:"World geography — continents, oceans, passes, straits. Science: Human digestive system.",type:"Teach + Drill"},
  {d:16,ph:1,wk:3,sub:"English",topic:"Ordering of Sentences",detail:"S1-S6 structure strategy. 20 PYQs.",type:"Teach + Drill"},
  {d:17,ph:1,wk:3,sub:"GK",topic:"Polity",detail:"Constitution — Preamble, Fundamental Rights (Art 12-35). Science: Circulatory system.",type:"Teach + Drill"},
  {d:18,ph:1,wk:3,sub:"English",topic:"Fill in the Blanks",detail:"Prepositions + determiners in context. 25 PYQs.",type:"Drill"},
  {d:19,ph:1,wk:3,sub:"GK",topic:"Polity",detail:"DPSP (Art 36-51), Fundamental Duties, Amendment procedure. Science: Respiratory system.",type:"Teach + Drill"},
  {d:20,ph:1,wk:3,sub:"English",topic:"Mixed Drill",detail:"Spotting errors + ordering + fill blanks. 30 PYQs timed 30 min.",type:"Timed Drill"},
  {d:21,ph:1,wk:3,sub:"GK",topic:"Science Consolidation",detail:"Physics: Motion, Force, Work, Electricity — all blocks revision + drill.",type:"Revision"},
  {d:22,ph:1,wk:4,sub:"GK",topic:"Science Consolidation",detail:"Chemistry: Elements, reactions, acids/bases. Biology: Cell systems.",type:"Revision"},
  {d:23,ph:1,wk:4,sub:"GK",topic:"Polity",detail:"Parliament, President, Governor — powers and differences. Judicial Review.",type:"Teach + Drill"},
  {d:24,ph:1,wk:4,sub:"English",topic:"Vocabulary",detail:"50-word synonym/antonym intensive. One-word substitution patterns.",type:"Vocab Drill"},
  {d:25,ph:1,wk:4,sub:"Mixed",topic:"Phase 1 Review",detail:"Full mixed PYQ set — 40 questions timed 40 min. Score and identify gaps.",type:"Phase Test"},
  {d:26,ph:2,wk:4,sub:"English",topic:"Grammar Intensive",detail:"All spotting error rules consolidated. Parts of speech identification.",type:"Drill"},
  {d:27,ph:2,wk:4,sub:"GK",topic:"Science",detail:"Physics — Optics, Sound, Magnetism. PYQ drill 20 questions.",type:"Teach + Drill"},
  {d:28,ph:2,wk:4,sub:"English",topic:"Ordering of Sentences",detail:"Advanced S1-S6 patterns. 25 PYQs timed.",type:"Timed Drill"},
  {d:29,ph:2,wk:5,sub:"GK",topic:"Science",detail:"Chemistry — periodic table basics, chemical reactions, everyday chemistry.",type:"Teach + Drill"},
  {d:30,ph:2,wk:5,sub:"English",topic:"Comprehension",detail:"2 passages + questions. Skim strategy, elimination technique.",type:"Teach + Drill"},
  {d:31,ph:2,wk:5,sub:"GK",topic:"Science",detail:"Biology — reproduction, genetics basics, diseases and immunity.",type:"Teach + Drill"},
  {d:32,ph:2,wk:5,sub:"Mixed",topic:"Science Review",detail:"Science PYQ set — 30 questions timed. Score and drill misses.",type:"PYQ Test"},
  {d:33,ph:2,wk:5,sub:"GK",topic:"Current Affairs",detail:"Last 6 months — Defence news, India operations, military exercises.",type:"Teach + Drill"},
  {d:34,ph:2,wk:5,sub:"English",topic:"Comprehension",detail:"Speed reading — 2 passages in 20 min. Accuracy check.",type:"Timed Drill"},
  {d:35,ph:2,wk:5,sub:"GK",topic:"Current Affairs",detail:"Government schemes, awards, summits, international relations.",type:"Teach + Drill"},
  {d:36,ph:2,wk:6,sub:"English",topic:"Idioms & Phrasal Verbs",detail:"High-frequency CDS idioms. 20 PYQs.",type:"Vocab Drill"},
  {d:37,ph:2,wk:6,sub:"GK",topic:"Current Affairs",detail:"Sports, science & tech developments, important appointments.",type:"Teach + Drill"},
  {d:38,ph:2,wk:6,sub:"English",topic:"Mini Mock",detail:"Full English mini-mock — 40 questions, 40 minutes. Score and analyse.",type:"Mini Mock"},
  {d:39,ph:2,wk:6,sub:"Mixed",topic:"Review",detail:"Current affairs rapid drill + English gap fill.",type:"Review"},
  {d:40,ph:2,wk:6,sub:"GK",topic:"History Revision",detail:"Modern History rapid fire — all acts, sessions, movements. 30 PYQs.",type:"Revision + PYQ"},
  {d:41,ph:2,wk:6,sub:"English",topic:"Spotting Errors",detail:"Full error spotting set — 30 questions timed 25 min.",type:"Timed Drill"},
  {d:42,ph:2,wk:6,sub:"GK",topic:"Geography Revision",detail:"Rapid fire — rivers, ranges, passes, world geography. 25 PYQs.",type:"Revision + PYQ"},
  {d:43,ph:2,wk:7,sub:"English",topic:"Vocabulary",detail:"Synonym/antonym intensive — 60 words. One-word substitution 20 PYQs.",type:"Vocab Drill"},
  {d:44,ph:2,wk:7,sub:"GK",topic:"Polity Revision",detail:"All articles rapid recall — President, Parliament, Courts. 25 PYQs.",type:"Revision + PYQ"},
  {d:45,ph:2,wk:7,sub:"Mixed",topic:"Phase 2 Test",detail:"60-question mixed GK + English. Timed 60 min. Full scoring and error log.",type:"Phase Test"},
  {d:46,ph:2,wk:7,sub:"GK",topic:"Science Revision",detail:"All science blocks rapid drill. 30 PYQs timed.",type:"Revision + PYQ"},
  {d:47,ph:2,wk:7,sub:"English",topic:"Ordering of Sentences",detail:"30 PYQs timed — this must be a scoring zone by now.",type:"Timed Drill"},
  {d:48,ph:2,wk:7,sub:"GK",topic:"Defence & Military GK",detail:"Army structure, ranks, exercises, operations, weapons systems.",type:"Teach + Drill"},
  {d:49,ph:2,wk:7,sub:"English",topic:"Full Mixed",detail:"All English types — 50 questions timed 50 min.",type:"Timed Drill"},
  {d:50,ph:2,wk:8,sub:"Mixed",topic:"Pre-Mock Assessment",detail:"80 questions — 40 English + 40 GK. Full 80-min paper. Target: 55+.",type:"Full Assessment"},
  {d:51,ph:3,wk:8,sub:"Mock",topic:"English Full Paper",detail:"120 questions — 2 hours. No breaks. Score and analyse every wrong answer.",type:"Full Mock"},
  {d:52,ph:3,wk:8,sub:"Mock",topic:"GK Full Paper",detail:"120 questions — 2 hours. Score and categorise misses by topic.",type:"Full Mock"},
  {d:53,ph:3,wk:8,sub:"Mock",topic:"English Full Paper",detail:"Second English full paper. Target: +10 marks vs Day 51.",type:"Full Mock"},
  {d:54,ph:3,wk:8,sub:"Mixed",topic:"Stamina Mock",detail:"English 2hrs + GK 2hrs back to back. Full stamina test. 4.5hr session.",type:"Stamina Mock"},
  {d:55,ph:3,wk:8,sub:"Mock",topic:"GK Full Paper",detail:"Third GK full paper. Target: 70+ marks.",type:"Full Mock"},
  {d:56,ph:3,wk:8,sub:"Mock",topic:"English Full Paper",detail:"Third English paper. Target: 80+ marks.",type:"Full Mock"},
  {d:57,ph:3,wk:9,sub:"Mixed",topic:"Stamina Mock",detail:"Full 4-hour dual paper stamina test. Score both papers.",type:"Stamina Mock"},
  {d:58,ph:3,wk:9,sub:"Mock",topic:"English Full Paper",detail:"Paper 4. Track improvement curve across all four.",type:"Full Mock"},
  {d:59,ph:3,wk:9,sub:"Mock",topic:"GK Full Paper",detail:"Paper 4. Score target: 75+.",type:"Full Mock"},
  {d:60,ph:3,wk:9,sub:"Mixed",topic:"Stamina Mock",detail:"Final full stamina test — 4 hrs. Benchmark before Phase 4.",type:"Stamina Mock"},
  {d:61,ph:3,wk:9,sub:"Mixed",topic:"Current Affairs Final",detail:"Latest news refresh — defence, appointments, events.",type:"Current Affairs"},
  {d:62,ph:3,wk:9,sub:"Mixed",topic:"Full Revision",detail:"Flash cards — all articles, history dates, geography facts, science formulae.",type:"Revision"},
  {d:63,ph:3,wk:9,sub:"Mixed",topic:"Phase 3 Final Assessment",detail:"Full dual paper — English + GK. Target: 85+ combined.",type:"Full Assessment"},
  {d:64,ph:4,wk:10,sub:"Mixed",topic:"Final Scan",detail:"30-minute scan only — Constitution articles, important acts, science formulae. Done by noon.",type:"Light Revision"},
  {d:65,ph:4,wk:10,sub:"EXAM",topic:"CDS 2 2026 — EXAM DAY",detail:"OTA. English + GK. You have put in the work. Trust the preparation.",type:"EXAM DAY"}
];

// ═══════════════════════════════════════════
// CSE 10-WEEK CURRICULUM
// ═══════════════════════════════════════════
const CSE = [
  {
    "wk": 1,
    "d": 1,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Teach + Define",
    "topic": "What is an Algorithm?",
    "detail": "A step-by-step instruction set to solve a problem — like a recipe your computer follows"
  },
  {
    "wk": 1,
    "d": 1,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Teach + Define",
    "topic": "What is a Program vs Script vs Function",
    "detail": "Program = full app. Script = single task file. Function = reusable block inside code"
  },
  {
    "wk": 1,
    "d": 2,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Write from scratch",
    "topic": "Variables and Data Types",
    "detail": "Named boxes that store values — int float str bool list dict"
  },
  {
    "wk": 1,
    "d": 3,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Write from scratch",
    "topic": "Operators and Expressions",
    "detail": "Symbols that do math or compare values — + - * / == != > <"
  },
  {
    "wk": 1,
    "d": 4,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Teach + Define",
    "topic": "What is a Compiler vs Interpreter",
    "detail": "Compiler converts whole code at once. Interpreter runs line by line — Python is interpreted"
  },
  {
    "wk": 1,
    "d": 5,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Write from scratch",
    "topic": "Conditionals — if elif else",
    "detail": "Decision making in code — if this is true do this otherwise do that"
  },
  {
    "wk": 1,
    "d": 6,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Teach + Define",
    "topic": "What is Memory — RAM vs Storage",
    "detail": "RAM = temporary fast memory your program runs in. Storage = permanent. Variables live in RAM"
  },
  {
    "wk": 1,
    "d": 7,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Blank page test",
    "topic": "Week 1 Assessment",
    "detail": "All vocab terms + write two functions from blank page"
  },
  {
    "wk": 2,
    "d": 8,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Write from scratch",
    "topic": "Loops — for and while",
    "detail": "Repeat a block of code until a condition is met"
  },
  {
    "wk": 2,
    "d": 9,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Teach + Define",
    "topic": "What is Time Complexity — Big O basics",
    "detail": "How fast does your code run as input grows — O(n) O(n²) O(1)"
  },
  {
    "wk": 2,
    "d": 10,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Write from scratch",
    "topic": "Functions — define call return",
    "detail": "Reusable named blocks of code that take input and give output"
  },
  {
    "wk": 2,
    "d": 11,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Teach + Define",
    "topic": "What is an API",
    "detail": "A contract between two programs to talk to each other — like a waiter between kitchen and customer"
  },
  {
    "wk": 2,
    "d": 12,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Write from scratch",
    "topic": "Lists and List Operations",
    "detail": "Ordered collection of items — append remove index slice sort"
  },
  {
    "wk": 2,
    "d": 13,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Write from scratch",
    "topic": "Dictionaries and Key-Value Logic",
    "detail": "Store data as pairs — name maps to value like a real dictionary"
  },
  {
    "wk": 2,
    "d": 14,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Blank page test",
    "topic": "Week 2 Assessment",
    "detail": "5 questions: 2 vocab define 2 blank page code 1 debug a broken snippet"
  },
  {
    "wk": 3,
    "d": 15,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Teach + Define",
    "topic": "What is OOPs — the concept",
    "detail": "Programming style where you model real things as objects with properties and behaviours"
  },
  {
    "wk": 3,
    "d": 16,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Write from scratch",
    "topic": "Classes and Objects",
    "detail": "Blueprint vs actual thing — Class is blueprint Object is the real instance"
  },
  {
    "wk": 3,
    "d": 17,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Teach + Define",
    "topic": "4 Pillars of OOPs — vocab only",
    "detail": "Encapsulation Inheritance Polymorphism Abstraction — what each means in plain English"
  },
  {
    "wk": 3,
    "d": 18,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Write from scratch",
    "topic": "Inheritance in code",
    "detail": "Child class gets properties of parent class — like a son inheriting traits"
  },
  {
    "wk": 3,
    "d": 19,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Teach + Define",
    "topic": "What is a Database — SQL vs NoSQL",
    "detail": "SQL = structured tables with relations. NoSQL = flexible documents like JSON"
  },
  {
    "wk": 3,
    "d": 20,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Write from scratch",
    "topic": "File Handling — read write append",
    "detail": "Open a file write data to it read it back close it"
  },
  {
    "wk": 3,
    "d": 21,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Blank page test",
    "topic": "Week 3 Assessment — OOPs focus",
    "detail": "Write a full class from scratch + define all 4 OOPs pillars + debug one broken class"
  },
  {
    "wk": 4,
    "d": 22,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Teach + Define",
    "topic": "What is a Data Structure",
    "detail": "A way of organising data so it can be used efficiently — Array Stack Queue Tree Graph"
  },
  {
    "wk": 4,
    "d": 23,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Write from scratch",
    "topic": "Arrays and Strings — manipulation",
    "detail": "Indexed collections and text — the most common interview data types"
  },
  {
    "wk": 4,
    "d": 24,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Teach + Define + Code",
    "topic": "What is a Stack and Queue — with code",
    "detail": "Stack = last in first out like a pile of plates. Queue = first in first out like a line"
  },
  {
    "wk": 4,
    "d": 25,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Write from scratch",
    "topic": "Error Handling — try except finally",
    "detail": "What to do when code breaks at runtime — catch the error handle it gracefully"
  },
  {
    "wk": 4,
    "d": 26,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Teach + Define",
    "topic": "What is Git — terms and workflow",
    "detail": "Version control — track changes collaborate revert — commit push pull branch merge"
  },
  {
    "wk": 4,
    "d": 27,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Build session",
    "topic": "Putting it all together — mini project",
    "detail": "Build a CLI contact book — add search delete contacts — stored in a file"
  },
  {
    "wk": 4,
    "d": 28,
    "ph": "PHASE 1 - VOCABULARY & PYTHON FOUNDATION",
    "type": "Full mock test",
    "topic": "4-Week Comprehensive Assessment",
    "detail": "10 questions — vocab define debug blank page build a function explain Big O of your code"
  },
  {
    "wk": 5,
    "d": 29,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Define",
    "topic": "What is a Sorting Algorithm",
    "detail": "A method to arrange data in order — Bubble Selection Merge Quick Sort"
  },
  {
    "wk": 5,
    "d": 30,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Write from scratch",
    "topic": "Bubble Sort from scratch",
    "detail": "Compare adjacent elements swap if out of order repeat until sorted"
  },
  {
    "wk": 5,
    "d": 31,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Pattern",
    "topic": "Two Pointer Pattern",
    "detail": "Use two variables pointing to different positions to avoid nested loops — reduces O(n²) to O(n)"
  },
  {
    "wk": 5,
    "d": 32,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Write from scratch",
    "topic": "Frequency Map Pattern",
    "detail": "Count occurrences using a dictionary — find duplicates find most common find missing"
  },
  {
    "wk": 5,
    "d": 33,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Define",
    "topic": "What is Machine Learning — real definition",
    "detail": "Teaching a machine to find patterns in data without explicit rules"
  },
  {
    "wk": 5,
    "d": 34,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Build session",
    "topic": "Python with sklearn — first model",
    "detail": "Load iris dataset train a classifier predict on new data evaluate accuracy"
  },
  {
    "wk": 5,
    "d": 35,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Blank page test",
    "topic": "Week 5 Assessment",
    "detail": "Sort a list from scratch + solve one two-pointer problem + define ML types"
  },
  {
    "wk": 6,
    "d": 36,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Define",
    "topic": "Supervised vs Unsupervised vs Reinforcement Learning",
    "detail": "Supervised = labelled data. Unsupervised = find hidden patterns. Reinforcement = learn by reward"
  },
  {
    "wk": 6,
    "d": 37,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Build + Explain",
    "topic": "Linear Regression from scratch concept",
    "detail": "Find best line through data points to predict continuous values"
  },
  {
    "wk": 6,
    "d": 38,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Define",
    "topic": "What is Overfitting and Underfitting",
    "detail": "Overfit = memorised training data fails on new data. Underfit = too simple to learn anything"
  },
  {
    "wk": 6,
    "d": 39,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Write from scratch",
    "topic": "Sliding Window Pattern",
    "detail": "Use a window that slides across data — find max sum subarray longest substring"
  },
  {
    "wk": 6,
    "d": 40,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Define",
    "topic": "What is a Neural Network — plain English",
    "detail": "Layers of connected nodes that transform input to output — inspired by the brain loosely"
  },
  {
    "wk": 6,
    "d": 41,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Build session",
    "topic": "Blockchain project — add one feature",
    "detail": "Add a simple REST API endpoint to your existing project using Flask"
  },
  {
    "wk": 6,
    "d": 42,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Mock interview format",
    "topic": "Week 6 Assessment",
    "detail": "Define 5 ML terms cold + solve one sliding window problem + explain your blockchain feature"
  },
  {
    "wk": 7,
    "d": 43,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Define",
    "topic": "What is an OS — CPU Scheduling Algorithms",
    "detail": "OS manages hardware resources. CPU scheduling = who gets the CPU next — FCFS RR SJF"
  },
  {
    "wk": 7,
    "d": 44,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Define",
    "topic": "What is a Process vs Thread",
    "detail": "Process = independent running program. Thread = lightweight unit inside a process"
  },
  {
    "wk": 7,
    "d": 45,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Write from scratch",
    "topic": "Recursion — concept and code",
    "detail": "A function that calls itself with a smaller version of the problem"
  },
  {
    "wk": 7,
    "d": 46,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Define",
    "topic": "What is a REST API — full breakdown",
    "detail": "Representational State Transfer — stateless client server communication over HTTP using GET POST PUT DELETE"
  },
  {
    "wk": 7,
    "d": 47,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Build session",
    "topic": "Build a REST API with Flask",
    "detail": "Create endpoints for a simple task manager — add get delete tasks"
  },
  {
    "wk": 7,
    "d": 48,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Define + Defend",
    "topic": "What is Blockchain — explain YOUR project",
    "detail": "Distributed ledger — immutable chained blocks — consensus mechanisms"
  },
  {
    "wk": 7,
    "d": 49,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Mock interview",
    "topic": "Week 7 Assessment",
    "detail": "OS vocab + recursion blank page + explain REST API design + defend blockchain project"
  },
  {
    "wk": 8,
    "d": 50,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Write",
    "topic": "Linked List — concept and code",
    "detail": "Chain of nodes where each node points to the next — no index access"
  },
  {
    "wk": 8,
    "d": 51,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Define",
    "topic": "What is Cloud Computing — AWS GCP Azure basics",
    "detail": "Renting compute storage and services over internet instead of owning hardware"
  },
  {
    "wk": 8,
    "d": 52,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Build session",
    "topic": "Second ML project — NLP Sentiment Classifier",
    "detail": "Train a model to classify text as positive or negative using sklearn"
  },
  {
    "wk": 8,
    "d": 53,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Teach + Define",
    "topic": "What is Docker — plain English",
    "detail": "Package your app and all its dependencies into a container that runs anywhere"
  },
  {
    "wk": 8,
    "d": 54,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Timed drill",
    "topic": "LeetCode Easy — 5 problems timed",
    "detail": "Array and string problems — Two Sum, Reverse String, Valid Palindrome, Contains Duplicate, FizzBuzz"
  },
  {
    "wk": 8,
    "d": 55,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Build session",
    "topic": "LinkedIn profile build session",
    "detail": "Headline summary experience projects skills — optimised for AI-ML fresher roles"
  },
  {
    "wk": 8,
    "d": 56,
    "ph": "PHASE 2 - DSA PATTERNS + ML FOUNDATIONS",
    "type": "Full mock",
    "topic": "8-Week Comprehensive Assessment",
    "detail": "Full mock technical interview — 45 minutes — vocab DSA ML project defence coding"
  },
  {
    "wk": 9,
    "d": 57,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Script + Rehearse",
    "topic": "Behavioural questions — your real answers",
    "detail": "Tell me about yourself. Your biggest weakness. A project you are proud of."
  },
  {
    "wk": 9,
    "d": 58,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Teach + Design",
    "topic": "System Design basics — fresher level",
    "detail": "How would you design a URL shortener. How would you design a chat app."
  },
  {
    "wk": 9,
    "d": 59,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Timed drill",
    "topic": "LeetCode Medium — attempt 3 problems",
    "detail": "Sliding window + two pointer + hash map medium problems"
  },
  {
    "wk": 9,
    "d": 60,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Research + Apply",
    "topic": "20 companies list + application strategy",
    "detail": "Bengaluru startups and remote AI-ML roles — specific companies and JD targeting"
  },
  {
    "wk": 9,
    "d": 61,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Full mock",
    "topic": "Mock technical interview — full simulation",
    "detail": "45-minute session with me acting as interviewer — no breaks no hints"
  },
  {
    "wk": 9,
    "d": 62,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Teach + Define",
    "topic": "What is System Design — key terms",
    "detail": "Scalability Load Balancing Caching CDN Database Sharding Microservices"
  },
  {
    "wk": 9,
    "d": 63,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Full mock + review",
    "topic": "Week 9 Assessment + Job Hunt Review",
    "detail": "Mock interview + check how many applications sent + review any responses received"
  },
  {
    "wk": 10,
    "d": 64,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Rehearse + Time",
    "topic": "Explain your projects under 3 minutes each",
    "detail": "Blockchain voting system and NLP classifier — tight clear compelling explanation"
  },
  {
    "wk": 10,
    "d": 65,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Teach + Define",
    "topic": "Advanced OOPs — design patterns basics",
    "detail": "Singleton Factory Observer — what they are and when to use them"
  },
  {
    "wk": 10,
    "d": 66,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Action session",
    "topic": "Follow up and track applications",
    "detail": "Email follow-ups LinkedIn outreach to hiring managers — active not passive hunt"
  },
  {
    "wk": 10,
    "d": 67,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Teach + Roleplay",
    "topic": "Negotiate your offer — what to say",
    "detail": "How to respond to an offer. When to push back. What numbers are realistic."
  },
  {
    "wk": 10,
    "d": 68,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Full mock",
    "topic": "CDS mock paper — timed",
    "detail": "Full English + GK paper under exam conditions"
  },
  {
    "wk": 10,
    "d": 69,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Timed drill",
    "topic": "LeetCode Medium — 5 problems timed",
    "detail": "Mixed patterns — hash map tree basics recursion string manipulation"
  },
  {
    "wk": 10,
    "d": 70,
    "ph": "PHASE 3 - INTERVIEW MODE + JOB HUNT",
    "type": "Full mock interview",
    "topic": "10-Week Graduation Assessment",
    "detail": "Full technical interview simulation — 60 minutes — every domain covered"
  }
];
