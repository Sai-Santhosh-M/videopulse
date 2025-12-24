const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');
require("dotenv").config();

const app = express();
const PORT = 3000;

// --------------------
// View engine setup
// --------------------
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// --------------------
// Middleware
// --------------------
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({ extended: true }));

// --------------------
// GET /  → READY STATE
// --------------------
app.get('/', (req, res) => {
  res.render('index', {
    uiState: 'ready',
    sentimentData: null,
    comments: [],
    transcript: null
  });
});

// --------------------
// POST / → RUN ANALYSIS
// --------------------
app.post('/', (req, res) => {
  const videoUrl = req.body.videoUrl;
  console.log("🎥 Video URL received:", videoUrl);

  // ⛔ DO NOT render loading here
  // Loading is handled on frontend via JS

  // STEP 1: Fetch comments
  exec(`python youtube.py "${videoUrl}"`, (err1) => {
    if (err1) return renderError(res);

    // STEP 2: Sentiment analysis
    exec(`python analysis.py`, (err2) => {
      if (err2) return renderError(res);

      // STEP 3: Download audio
      exec(`python get_audio.py "${videoUrl}"`, (err3) => {
        if (err3) return renderError(res);

        // STEP 4: Transcribe
        exec(`python whisper_transcribe.py`, (err4) => {
          if (err4) return renderError(res);

          // STEP 5: Summarize
          exec(`python summarize.py`, (err5) => {
            if (err5) return renderError(res);

            // --------------------
            // Load sentiment results
            // --------------------
            let parsed;
            try {
              parsed = JSON.parse(
                fs.readFileSync(
                  path.join(__dirname, 'results.json'),
                  'utf-8'
                )
              );
            } catch (err) {
              console.error("❌ Failed to read results.json");
              return renderError(res);
            }

            // --------------------
            // Load summary
            // --------------------
            let summaryText = '';
            try {
              summaryText = fs.readFileSync(
                path.join(__dirname, 'summary.txt'),
                'utf-8'
              );
            } catch {
              summaryText = "Summary not available.";
            }

            // --------------------
            // FINAL: RENDER RESULT
            // --------------------
            res.render('index', {
              uiState: 'result',
              sentimentData: parsed,
              comments: parsed.details,
              transcript: summaryText
            });
          });
        });
      });
    });
  });
});

// --------------------
// Error fallback
// --------------------
function renderError(res) {
  res.render('index', {
    uiState: 'ready',
    sentimentData: null,
    comments: [],
    transcript: null
  });
}

// --------------------
// Start server
// --------------------
app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});