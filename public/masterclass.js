const AI_MASTERCLASS = [
  {
    day: 1,
    title: "The Supervisor-Critic Swarm Architecture",
    topic: "Multi-Agent Systems",
    detail: "Instead of relying on a single LLM (which hallucinates), we built a 'Swarm'. We use Gemini as the strict 'Supervisor' who reviews the work of the 'Workers' (GPT-4o, Claude, and Gemini). The Supervisor forces them to debate until they reach mathematical consensus, entirely preventing hallucination. This is achieved via asynchronous API calls, bringing latency down to 10-15 seconds.",
    codeSnippet: "async function swarmDebate(problem) {\n  const v1 = await Promise.all([callGPT(problem), callClaude(problem)]);\n  const critique = await callSupervisor(v1);\n  return await callRefinement(critique);\n}"
  },
  {
    day: 2,
    title: "The Sherlock Module (Hyper-Context)",
    topic: "Data Engineering & Vector Databases",
    detail: "To make the AI hyper-observant, we feed it massive context. We scrape Huawei Health (biometrics) and GPS. When you ask a question, the AI doesn't just read your prompt; it pulls your sleep data and location from yesterday via a local Vector Database (ChromaDB) to deduce *why* you are asking the question. E.g., deducing a sore throat from an ice-cream shop visit and low HRV.",
    codeSnippet: "def get_context():\n  sleep_data = scrape_huawei()\n  location = get_gps()\n  return chroma_db.query([sleep_data, location])"
  },
  {
    day: 3,
    title: "Headless Action Node (The Hands)",
    topic: "Android UIAutomator & Appium",
    detail: "APIs for Swiggy or Amazon are locked. To bypass this, we use the Vivo Android phone as a headless server without a SIM. The AI writes Appium scripts to literally open the apps, click the coordinates on the screen, and add items to your cart, bridging the digital AI brain into the physical world.",
    codeSnippet: "driver.find_element(By.XPATH, '//android.widget.TextView[@text=\"Add to Cart\"]').click()"
  },
  {
    day: 4,
    title: "The Distraction Shield & AI Voicemail",
    topic: "Telecom Interception & Webhooks",
    detail: "Since the Vivo has no SIM, we installed Tasker on the primary phone. When a bank SMS or call comes in, Tasker sends a Webhook to Firebase. If a call is ignored, the Vivo phone acts as an answering machine using Text-to-Speech, transcribes the caller's message using Whisper, and pushes it to this Dashboard.",
    codeSnippet: "app.post('/webhook/sms', (req, res) => {\n  const text = req.body.message;\n  firebase.collection('sms_stream').add({ text });\n});"
  },
  {
    day: 5,
    title: "Firebase Realtime Nervous System",
    topic: "WebSockets & NoSQL",
    detail: "The Dashboard UI (Frontend) and the Python Brain (Backend) communicate entirely through Firebase Firestore using `onSnapshot` listeners. Instead of the UI polling the server, Firebase holds an open WebSocket connection, instantly pushing thoughts, logs, and actions to your screen in real-time.",
    codeSnippet: "db.collection('ai_stream').onSnapshot(snapshot => {\n  snapshot.docChanges().forEach(change => {\n    if (change.type === 'added') appendToTerminal(change.doc.data());\n  });\n});"
  }
];
