# Phishing URL Analyzer

> **Real-time, AI-powered phishing detection for the modern web.**

![Status](https://img.shields.io/badge/Status-Operational-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-orange)

## Overview

**Phishing URL Analyzer** is a sophisticated cybersecurity tool designed to detect and analyze potentially malicious URLs in real-time. By combining traditional heuristic analysis with advanced AI models (Groq/Llama 3), it provides a multi-layered verdict on website safety.

The application features a **Cyberpunk/Sci-Fi themed UI** that offers deep insights into risk factors, technical signals, and an explainable AI verdict, making it suitable for both security researchers and general users.

## Features

- **Real-time URL Scanning**: Instant analysis of URLs for known phishing patterns and malicious indicators.
- **AI-Powered Analysis**: Utilizes **Groq & Llama 3** to provide a contextual explanation of *why* a site is safe or malicious.
- **Comprehensive Risk Scoring**: 
  - **Verdict**: SAFE, SUSPICIOUS, or MALICIOUS.
  - **Safety Score**: 0-100 numerical rating.
  - **Risk Breakdown**: Specific flags (e.g., "Suspicious TLD", "IP Address Host").
- **Technical Signal Extraction**: Detects HTTPS usage, URL length anomalies, and suspicious domain structures.
- **Immersive UI**: A responsive, high-performance interface built with React & Vite, featuring a "glitch" aesthetic and dark mode.

## Tech Stack

### Frontend
- **Framework**: [React 19](https://react.dev/)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **Styling**: Vanilla CSS (Cyberpunk Theme)
- **Deployment**: Vercel

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Language**: Python 3.8+
- **AI Inference**: [Groq SDK](https://groq.com/)
- **Validation**: Pydantic

## Getting Started

Follow these instructions to set up the project locally for development and testing.

### Prerequisites
- **Node.js** (v18+)
- **Python** (v3.8+)
- **Groq API Key** (Get one at [console.groq.com](https://console.groq.com/))

### Installation

For detailed deployment instructions, see [deployment_guide.md](deployment_guide.md).

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/phishing-analyser.git
cd phishing-analyser
```

#### 2. Backend Setup
Navigate to the backend directory and install dependencies:
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory:
```env
GROQ_API_KEY=your_groq_api_key_here
FRONTEND_URL=http://localhost:5173
```

#### 3. Frontend Setup
Navigate to the frontend directory and install dependencies:
```bash
cd ../frontend
npm install
```

Create a `.env` file in the `frontend` directory (optional for local dev):
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### Running the Application

#### Start the Backend
```bash
# In the backend directory
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

#### Start the Frontend
```bash
# In the frontend directory
npm run dev
```
The UI will be available at `http://localhost:5173`.

## API Reference

### Analyze URL
**POST** `/api/analyze`

Analyzes a given URL and returns a detailed safety report.

**Request Body:**
```json
{
  "url": "http://suspicious-site.com/login"
}
```

**Response:**
```json
{
  "url": "http://suspicious-site.com/login",
  "verdict": "MALICIOUS",
  "safety_score": 15,
  "risk_breakdown": ["Suspicious TLD", "Keyword Match"],
  "ai_analysis": {
    "score": 10,
    "explanation": "The URL mimics a login page but uses a known malicious TLD..."
  },
  "signals": {
    "has_https": false,
    "url_length": 32
  }
}
```

## Roadmap & Remaining Tasks

- [ ] **Visual Analytics**: Implement charts for threat distribution and scan history.
- [ ] **User History**: Local storage or database integration to save user scan history.
- [ ] **Browser Extension**: Build a Chrome/Edge extension for on-the-fly protection.
- [ ] **Rate Limiting**: Add API rate limiting to prevent abuse.
- [ ] **Improved Heuristics**: Add more sophisticated regex patterns and reputation lookups.

## Contributing
Contributions are welcome! Please fork the repository and submit a Pull Request.

## License
This project is licensed under the MIT License.
