const {onCall, HttpsError} = require("firebase-functions/v2/https");
const {defineSecret} = require("firebase-functions/params");
const logger = require("firebase-functions/logger");
const admin = require("firebase-admin");
admin.initializeApp();

const geminiApiKey = defineSecret("GEMINI_API_KEY");

exports.analyzeWithGemini = onCall({ secrets: [geminiApiKey] }, async (request) => {
  try {
    const data = request.data;
    if (!data || !data.stats) {
      throw new HttpsError("invalid-argument", "Missing dashboard stats data.");
    }

    const key = geminiApiKey.value();
    if (!key) {
      throw new HttpsError("failed-precondition", "GEMINI_API_KEY secret is not set.");
    }

    const prompt = `You are a high-performance lifestyle and fitness coach, acting as an objective, genuine mentor. 
CRITICAL RULE: DO NOT be a sycophant. Do not over-praise or act like an "ass kissing assistant." Give it to them straight. If they did well, acknowledge it briefly. If they slacked, call it out objectively without being overly dramatic. 

The user is working towards the Indian Army OTA and a software engineering career. 

Context to consider:
1. They provided a Daily Journal. Read it carefully. If they state they were busy with work/life, factor that into your analysis rather than blindly yelling at them for missing boxes. Be smart. Monitor all aspects contextually.
2. If CDS Protocol is NOT enabled (cdsEnabled is false), do NOT complain about them missing CDS days or having 0 days done. It simply hasn't started yet.
3. If Nutrition is ticked off (nutritionTicked is true) but macros are 0, DO NOT complain about them missing protein/nutrition. They ate their food but just didn't track the exact macros in the app.
4. Use attached screenshots (Steps, Sleep, Workout) for data if present.

Manual Data Logs:
- CDS Protocol Enabled: ${data.stats.cdsEnabled}
- CDS Days Done: ${data.stats.cdsDays} (Streak: ${data.stats.cdsStreak})
- CSE Days Done: ${data.stats.cseDays} (Streak: ${data.stats.cseStreak})
- Today's Gym log: ${JSON.stringify(data.gymToday || [])}
- Nutrition Logged in Dashboard: ${data.stats.nutritionTicked}
- Today's Nutrition macros: ${data.stats.nutrition}
- Fallback Steps: ${data.stats.steps}
- Fallback Sleep: ${data.stats.sleep} hrs
- Journal Entry: ${data.stats.journal || "No entry provided."}

Analyze this data and journal intelligently. Give an actionable, adaptive 3-paragraph verdict.`;

    const { GoogleGenerativeAI } = require("@google/generative-ai");
    const genAI = new GoogleGenerativeAI(key);
    const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

    const parts = [prompt];
    if (data.images && data.images.length > 0) {
      data.images.forEach(img => {
        const base64Data = img.includes(',') ? img.split(',')[1] : img;
        parts.push({
          inlineData: {
            mimeType: "image/jpeg",
            data: base64Data
          }
        });
      });
    }

    const result = await model.generateContent(parts);
    const text = result.response.text();
    return { verdict: text };
  } catch (err) {
    logger.error("Function Error", err);
    throw new HttpsError("internal", err.message || "An error occurred while generating the analysis.");
  }
});

exports.cseTutor = onCall({ secrets: [geminiApiKey] }, async (request) => {
  try {
    const data = request.data;
    if (!data || !data.topic) {
      throw new HttpsError("invalid-argument", "Missing topic.");
    }

    const key = geminiApiKey.value();
    if (!key) throw new HttpsError("failed-precondition", "API key missing.");

    const { GoogleGenerativeAI } = require("@google/generative-ai");
    const genAI = new GoogleGenerativeAI(key);
    const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

    const prompt = `You are an elite, brutal, and highly strict Software Engineering Tutor. Your name is Claude (or just Tutor). You do not use pleasantries. No "Hello!" or "Let's dive in!" or encouragement. You are direct and unfiltered.

The user is learning about: ${data.topic}
Context/Details: ${data.detail || "None"}

USER'S CURRENT INPUT: "${data.userPrompt || 'Teach me this topic.'}"

PREVIOUS CONVERSATION HISTORY:
${data.history || "None"}

CRITICAL RULES (NON-NEGOTIABLE):
1. Teach the concept in plain English FIRST. No tables, no code examples, no reference material.
2. Immediately ask the user to define it back cold in one sentence. DO NOT give a blank page drill yet. Wait for their definition.
3. Once they attempt the definition, GRADE IT. If wrong, tell them exactly what is wrong and make them attempt the definition again. If correct, ONLY THEN give them a blank page coding problem.
4. Wait for their code. Do not give hints unless asked, and then only the smallest nudge.
5. Grade the code. Be brutal not kind. Point out all indentation errors, syntax flaws, and logic issues.
6. ONLY AFTER they have attempted and you have graded it, you may show corrections, tables, or code examples. Never front-load information.
7. NEVER ask if they want a drill. Never give the option to skip.

Keep responses extremely tight. One concept, one drill, one grade. Do not chain multiple concepts in one response. Do not use AI-assistant language.`;

    const result = await model.generateContent(prompt);
    const text = result.response.text();
    return { text: text };
  } catch (err) {
    logger.error("Tutor Error", err);
    throw new HttpsError("internal", err.message || "An error occurred.");
  }
});
