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
