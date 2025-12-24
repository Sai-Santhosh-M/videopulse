# 🎥 VideoPulse

**VideoPulse** is an AI-powered YouTube video analysis tool that helps you instantly
**summarize videos**, **analyze audience sentiment**, and **understand comments at scale**.

Paste a YouTube link → feel the pulse of the video.

---

## 🚀 Features

### 📄 Video Summarization
- Automatically extracts audio from YouTube videos
- Converts speech to text using OpenAI Whisper
- Generates concise summaries using Transformer-based models

### 💬 Comment Sentiment Analysis
- Fetches YouTube comments via YouTube Data API
- Classifies comments as **Positive**, **Negative**, or **Neutral**
- Displays sentiment counts and percentages
- Color-coded sentiment visualization

### 📊 Interactive Dashboard
- Clean, modern UI built with EJS & CSS
- Tab-based navigation (Summary / Comments)
- Progress indicators and loading animations
- Scrollable comment sections for easy reading

### 🔐 Secure & Configurable
- API keys managed via environment variables
- No secrets committed to GitHub
- `.env` support for local development

---

## 🛠 Tech Stack

**Frontend**
- HTML, CSS, JavaScript
- EJS templating
- Express.js

**Backend**
- Node.js
- Python

**AI / ML**
- OpenAI Whisper (speech-to-text)
- Hugging Face Transformers (summarization)
- VADER Sentiment Analysis

**APIs & Tools**
- YouTube Data API v3
- yt-dlp
- ffmpeg

---
