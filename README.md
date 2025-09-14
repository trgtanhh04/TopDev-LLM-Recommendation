# Project Report: LLM-powered Job Recommendation and CV–JD Matching

## 1. Introduction

### 1.1 Objectives
- Apply and understand Large Language Models (LLMs) via training and deployment.
- Practice finetuning/transfer learning for domain-specific data.
- Build NLP skills and deliver a practical application.
- Evaluate and analyze model performance.

### 1.2 Motivation
Online job search is noisy; candidates (especially fresh graduates) struggle to assess fit, while companies need better reach. We build a smart website that:
- Crawls TopDev jobs.
- Lets users upload CVs, then uses LLMs to analyze and match with JDs.
- Improves job search UX; extensible to auto-recommendations, labor market analytics, and employer–candidate matching.

---

## 2. Data Collection

### 2.1 Source
- TopDev.vn crawler.
- 984 job postings, 16 fields.

### 2.2 Schema
| # | Attribute            | Type     | Description |
|---|----------------------|----------|-------------|
| 0 | job_title            | object   | Job title (e.g., IT Helpdesk, Data Engineer) |
| 1 | company_name         | object   | Company name (e.g., Vingroup, MoMo) |
| 2 | salary               | float64  | Numeric or [min, max] range |
| 3 | address              | object   | Location/district |
| 4 | posted_date          | datetime | Posting date (e.g., 2025-06-21) |
| 5 | industry             | object   | Industry (e.g., Education, Software) |
| 6 | company_size         | float64  | Size (number or [min, max]) |
| 7 | company_nationality  | object   | Country (e.g., China, India, UK, Vietnam) |
| 8 | years_experience     | float64  | Years or [min, max] |
| 9 | position_level       | object   | Level (Intern, Middle, Senior, …) |
|10 | employment_type      | object   | In-office, Remote, … |
|11 | contract_type        | object   | Fulltime, Freelance, … |
|12 | technologies_used    | object   | Tech stack (e.g., .NET, Java) |
|13 | job_description      | object   | JD text |
|14 | company_url          | object   | Company URL |
|15 | url                  | object   | Job URL |

Note: Column names may be standardized later (e.g., posted_date → date_posted, years_experience → experience_years, url → job_url). Keep consistent across the pipeline.

---

## 3. Data Preprocessing

- Read raw_data.csv (984 × 16).
- Drop unused field: date_posted/posted_date.
- Nulls: only 1 null at salary → drop the row (negligible).
- Salary:
  - “Negotiable” → NaN.
  - Parse numbers; ranges → [min, max].
  - USD → VND at 1 USD = 25,000 VND.
- experience_years: extract number/range; no number → 0.
- company_size: extract number/range; no number → NaN.
- Save as preprocessed_data.csv.

---

## 4. System Workflow

1) Job data:
   - Crawl TopDev → preprocess → CSV.
2) LLM integration:
   - Upload CV (PDF) → extract structured info via Mistral → build CV embedding.
   - Build job embeddings from title + skills/tech + description.
   - Store vectors + metadata (job_id, company, location, salary, job_url) in MongoDB; optional Vector DB (FAISS/Pinecone) for fast similarity search.
3) Retrieval:
   - Cosine/ANN similarity to get top-k (k=10) nearest jobs to the CV.
4) Results:
   - Return top 10 jobs to UI; enable “Compare with CV” for score, missing skills, and learning path.

Tip: Add an architecture/sequence diagram in docs/images/ and embed it here.

---

## 5. LLM Integration

### 5.1 Model
- Platform: MistralAI API
- Model: mistral-medium
- Endpoint: https://api.mistral.ai/v1/chat/completions
- API key via environment variable (e.g., .env)

### 5.2 Procedure

Step 1 — Job embeddings:
- Concatenate relevant fields (job_title, technologies_used, job_description).
- Call API to get embeddings.
- Store vectors + metadata in MongoDB; optionally sync to Vector DB.

Step 2 — CV upload & extraction:
- User uploads CV (PDF).
- Use Mistral to extract candidate info to strict JSON; then build CV embedding.

CV extraction prompt (recommended, strict JSON):
```
You are an information extraction engine. Extract structured data from the CV content below and output a single valid JSON object matching exactly this schema (no extra text):

{
  "full_name": string|null,
  "email": string|null,
  "phone": string|null,
  "job_title": string|null,
  "education": [
    { "degree": string|null, "university": string|null, "start_year": number|null, "end_year": number|null }
  ],
  "experience": [
    { "job_title": string|null, "company": string|null, "start_date": string|null, "end_date": string|null, "description": string|null }
  ],
  "skills": [string],
  "certifications": [
    { "certificate_name": string|null, "organization": string|null }
  ],
  "languages": [string]
}

Rules:
- Missing scalars → null; missing lists → [].
- Email lowercase; phone in E.164 if possible; dates as "YYYY-MM" or "YYYY" and "Present" for ongoing roles.
- Skills: deduplicate; short phrases only.
- Languages: names only (omit proficiency).
CV:
{cv_text}
```

CV–JD matching prompt:
```
You are a professional career advisor. Based on the candidate’s CV and the job description, analyze and return structured feedback as valid JSON only:

CV:
{cv_json}
Job Description:
{job_json}

Return:
{
  "match_score": 0-100,
  "missing_skills": ["...", "..."],
  "recommendations": [
    { "skill": "skill name", "course": "course name", "link": "course url" }
  ],
  "summary": "Short advice summary (3-4 lines)"
}
```

Step 3 — Search:
- Use CV embedding to query nearest JD embeddings (cosine/ANN).

Step 4 — Output:
- Return top 10 matches with score, gaps, and learning recommendations.

---

## 6. Website Design and Implementation

### 6.1 System Overview
- Upload/manage CV (stored in browser for privacy).
- Browse jobs/companies and view JD details.
- Compare CV vs JD to get score, gaps, and AI advice.
- Support filtering, search, pagination, favorites.

### 6.2 Backend
- Python; Flask (current) / FastAPI (scalable option).
- Responsibilities:
  - Store/query job and company data (TopDev).
  - Ingest and parse CV PDFs.
  - Integrate Mistral for scoring, missing skills, and learning paths.
  - Provide RESTful endpoints.
- Example endpoint: POST /give_advice (input: CV + JD; output: score, feedback, missing_skills, recommendations).

### 6.3 Frontend
- Vue 3 (Composition API) + Vite, SFC.
- Features:
  - Upload/enter CV (JSON), persist in localStorage.
  - Send CV + JD to backend for analysis.
  - Display match score, missing skills, and recommendations next to JD.

### 6.4 Deployment
- Backend: https://topdev-llm-recommendation-backend.onrender.com
- Frontend: https://topdev-llm-recommendation-frontend.onrender.com

---

## 7. LLM Evaluation

### 7.1 Human Evaluation
- 23 CV × 10 jobs = 230 pairs (random).
- 4 annotators; 0–100 scale:
  - 0–10: Not suitable
  - 11–30: Far from requirements
  - 31–60: Basic fit
  - 61–80: Fair fit
  - 81–100: Strong fit
- Mean of 4 ratings → Human Score.

### 7.2 LLM Scoring
- mistral-medium produces match_score via the matching prompt (Section 5.2).
- Call this the LLM Score.

### 7.3 Metrics (to fill after runs)
- MAE(Human, LLM): …
- RMSE(Human, LLM): …
- Pearson/Spearman: …
- Error distribution (histogram): …
- Bland–Altman (optional): …

### 7.4 Error Analysis
- Typical gaps:
  - Deep domain skills not explicit (e.g., specific cloud provider).
  - Unstructured/ambiguous JD.
  - Long/noisy CV (OCR artifacts).
- Mitigations:
  - JD normalization (template + rule-based).
  - Stricter prompts; temperature=0.
  - Domain ontology and re-ranking rules.

---

## 8. Limitations & Future Work
- Limitations: CV/JD quality, domain shift, API cost/latency.
- Future:
  - Dedicated Vector DB (FAISS/Pinecone) at scale.
  - Better extraction (NER/RE: spaCy/transformers).
  - VI-specific tuning; hybrid retrieval (BM25+dense).
  - Explainability (JD/CV highlights), RBAC/multi-tenant, analytics.

---

## 9. Resources & Deployment
- Demo (Frontend): https://topdev-llm-recommendation-frontend.onrender.com
- Backend: https://topdev-llm-recommendation-backend.onrender.com
- Mistral API: mistral-medium, chat completions endpoint.
- Environment: MISTRAL_API_KEY in backend .env

---

## Appendix

### A. Original CV extraction prompt (compact)
```
Extract the following candidate information fields from the CV content (as plain text) below in the exact JSON format:
{
"full_name": "...",
"email": "...",
"phone": "...",
"job_title": "...",
"education": [
  { "degree": "...", "university": "...", "start_year": ..., "end_year": ... }
],
"experience": [
  { "job_title": "...", "company": "...", "start_date": "...", "end_date": "...", "description": "..." }
],
"skills": ["...", "..."],
"certifications": [
  { "certificate_name": "...", "organization": "..." }
],
"languages": ["...", "..."]
}
```

### B. Recommended LLM settings
- temperature = 0, top_p = 1 (deterministic JSON).
- Strip code fences if present before parsing.
- Validate against JSON Schema; on error, re-prompt with a short validation message.
