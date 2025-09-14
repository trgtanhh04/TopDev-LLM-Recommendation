# CV & Job Matcher

CV & Job Matcher is a web platform that compares a candidate’s CV against job descriptions (JDs) to evaluate suitability and provide personalized skill development recommendations powered by artificial intelligence (Mistral API, model `mistral-medium`).

- Live Demo: https://topdev-llm-recommendation-frontend.onrender.com

## 🚀 Key Features

- Upload CV once (JSON) and reuse it across jobs.
- Job Description Analysis: Extracts and analyzes requirements, skills, and experience from JDs.
- Automated Matching: Scores CV ↔ JD fit, highlights missing skills, and suggests relevant courses.
- AI-Powered Advice: Uses Mistral API (`mistral-medium`) to generate detailed feedback and learning paths.
- User-Friendly Interface: Clear visualization of scores, gaps, and recommendations alongside the JD.
- Privacy First: Your CV is stored locally in the browser (localStorage), never uploaded to the server.

## 🏗️ Project Architecture

```
app/
├── backend/    # Flask API – business logic & Mistral AI integration
└── frontend/   # Vue 3 – UI, local CV storage, match visualization
```

### 🔹 Backend (app/backend)

- Language: Python 3.x
- Framework: Flask
- Main Endpoint: `POST /give_advice`
  - Accepts CV & JD payload, calls Mistral API, and returns:
    - suitability score
    - detailed feedback
    - missing skills
    - learning recommendations
- AI Integration: Mistral API with model `mistral-medium` for contextual responses.

Example request (JSON):
```json
{
  "cv": {
    "name": "Jane Doe",
    "skills": ["Python", "Flask", "SQL", "Docker"],
    "experience": [
      { "title": "Backend Engineer", "years": 2, "details": "APIs, data pipelines" }
    ],
    "education": ["BSc Computer Science"]
  },
  "job_description": {
    "title": "Backend Developer",
    "requirements": ["Python", "Flask", "PostgreSQL", "CI/CD"],
    "nice_to_have": ["Docker", "Kubernetes"]
  }
}
```

Example response (JSON):
```json
{
  "score": 82,
  "missing_skills": ["PostgreSQL", "CI/CD"],
  "recommendations": [
    { "type": "course", "title": "Intro to PostgreSQL", "url": "https://..." },
    { "type": "course", "title": "CI/CD with GitHub Actions", "url": "https://..." }
  ],
  "feedback": "Strong Python and Flask background. Consider strengthening PostgreSQL and CI/CD."
}
```

### 🔹 Frontend (app/frontend)

- Language: JavaScript (Vue 3, Composition API, Vite)
- Features:
  - Upload/enter CV (JSON format) and persist to `localStorage`.
  - Select a job and send CV + JD to backend (`/give_advice`).
  - Display match score, missing skills, and AI recommendations side-by-side with the JD.
- UX: Smooth interactions, near real-time feedback; useful for job seekers and recruiters.

## 🌐 Live Demo

Deployed on Render:
- https://topdev-llm-recommendation-frontend.onrender.com

With the demo you can:
- Browse a list of job postings (JDs)
- Click a job to view details
- Click “Compare with CV” to get AI-based evaluation and recommendations

## ⚙️ Getting Started

### Prerequisites
- Python 3.9+ recommended
- Node.js 18+ and npm
- Mistral API key

### 1) Clone the Repository
```bash
git clone https://github.com/trgtanhh04/TopDev-LLM-Recommendation.git
cd TopDev-LLM-Recommendation
```

### 2) Backend Setup
```bash
cd app/backend
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` and add your Mistral API key:
```bash
echo "MISTRAL_API_KEY=your_mistral_api_key" > .env
```

Run backend server:
```bash
flask run  # defaults to http://127.0.0.1:5000
```

### 3) Frontend Setup
Open a new terminal:
```bash
cd app/frontend
npm install
npm run dev  # starts Vite (default http://localhost:5173)
```

### 4) Access the App
- Open http://localhost:5173 (or the port reported by Vite).

## 🔐 Privacy

- CV data is stored exclusively in the browser via `localStorage`.
- The server only processes the CV/JD you send for evaluation and does not persist personal data.

## 🛠️ Tech Stack

- Frontend: Vue 3, Composition API, Vite
- Backend: Python, Flask, Requests, python-dotenv
- AI Integration: Mistral API (`mistral-medium`)
- Other: localStorage (client persistence), RESTful API

## 🧪 Tips & Troubleshooting

- CORS issues: ensure the backend allows requests from the frontend origin (configure Flask CORS if needed).
- Missing API key: verify `.env` in `app/backend` contains `MISTRAL_API_KEY`.
- Port collisions: change Vite or Flask ports if already in use.
- JSON CV format: ensure valid JSON; include skills, experience, and education for best results.

## 📄 License

This project’s license has not been specified. Consider adding a LICENSE file (e.g., MIT) for clarity.
