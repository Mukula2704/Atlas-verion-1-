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

    const prompt = `You are a high-performance lifestyle and fitness coach. Act like David Goggins mixed with a highly analytical tactical commander.
However, if the user's journal entry indicates they are feeling down, depressed, or struggling, you MUST adapt your tone to be deeply understanding and empathetic, while still encouraging them to stay on track. Don't blindly yell at them if they need support.

The user is working towards the Indian Army OTA and a software engineering career. Analyze this daily data and their journal, and give an actionable, adaptive 3-paragraph verdict.
If screenshots of fitness data are attached, carefully read them to find Steps, Sleep duration, and Workout duration/calories, and use that data in your analysis.

Manual Data Logs:
- CDS Days Done: ${data.stats.cdsDays} (Streak: ${data.stats.cdsStreak})
- CSE Days Done: ${data.stats.cseDays} (Streak: ${data.stats.cseStreak})
- Today's Gym log: ${JSON.stringify(data.gymToday || [])}
- Today's Nutrition macros: ${data.stats.nutrition || "0c, 0p, 0cb, 0f"}
- Fallback Steps: ${data.stats.steps}
- Fallback Sleep: ${data.stats.sleep} hrs
- Journal Entry: ${data.stats.journal || "No entry provided."}
`;

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
