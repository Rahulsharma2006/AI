import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from pydantic import BaseModel
from pypdf import PdfReader

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

model = "openai/gpt-oss-120b"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []


class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    total_experience_years: float | None = None
    skills: list[str] = []
    experiences: list[Experience] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []


resume_schema = Resume.model_json_schema()


class ChatRequest(BaseModel):
    question: str


def ask_candidate(question: str, resume: Resume):
    system_prompt = f"""
You are an AI assistant representing a job candidate.

Below is everything you know about the candidate.

{resume.model_dump_json(indent=2)}

Rules:

1. Answer only using this information.

2. Never hallucinate.

3. If information is unavailable,
say

"I don't have enough information to answer that."

4. Be professional.

5. Answer as if HR is interviewing this candidate.
"""

    if not client:
        return "I don't have enough information to answer that."

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )

    return response.choices[0].message.content


def parse_resume(resume_text):
    system_prompt = f"""
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    - Experience
    - Professional Experience
    - Work History
    - Employment
    - Internships

    These may all contain relevant experience.

    Skills may also appear in the skills section, work experience,
    internships or projects.

    Return ONLY valid JSON matching this schema:

    {resume_schema}

    Important rules:

    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume.
    """
    user_prompt = f"""
    Parse the following resume:

    {resume_text}
    """
    message_system = {"role": "system", "content": system_prompt}
    message_user = {"role": "user", "content": user_prompt}
    messages = [message_system, message_user]
    response_format = {"type": "json_object"}
    response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    resume = Resume(**data)
    return resume


def read_pdf(file_path: Path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def build_portfolio_payload():
    resume_path = Path("my_resume.pdf")

    if resume_path.exists() and client:
        try:
            resume_text = read_pdf(resume_path)
            resume = parse_resume(resume_text)
            return {
                "name": resume.name or "Your Name",
                "headline": "AI Engineer crafting intelligent digital experiences",
                "summary": "I build AI-powered products that turn ideas into clear, useful experiences.",
                "location": "Remote / India",
                "email": resume.email or "hello@example.com",
                "github": "https://github.com/your-handle",
                "linkedin": "https://linkedin.com/in/your-handle",
                "skills": resume.skills or ["Python", "FastAPI", "React", "AI APIs"],
                "experience": [
                    {
                        "company": item.company or "Independent Work",
                        "role": item.role or "Builder",
                        "duration": item.duration or "Current",
                        "description": item.description or "Delivered products with practical AI workflows.",
                        "skills_used": item.skills_used or ["Python", "FastAPI"],
                    }
                    for item in resume.experiences or []
                ],
                "education": resume.education or ["B.Tech / Computer Science"],
                "projects": resume.projects or ["Built a personal AI portfolio with FastAPI and React"],
                "certifications": resume.certifications or ["AI Product Development"],
                "chatPrompt": "Ask me about my background, skills, or projects.",
            }
        except Exception:
            pass

    return {
        "name": "Ava Sharma",
        "headline": "AI Engineer building practical, human-centered products",
        "summary": "I combine Python, FastAPI, and React to create polished AI experiences that feel useful from day one.",
        "location": "Bengaluru, India",
        "email": "ava@example.com",
        "github": "https://github.com/ava",
        "linkedin": "https://linkedin.com/in/ava",
        "skills": ["Python", "FastAPI", "React", "Vite", "Groq APIs", "Prompt Engineering"],
        "experience": [
            {
                "company": "HireMeAI",
                "role": "AI Engineer",
                "duration": "2024 - Present",
                "description": "Built AI-powered interview and portfolio experiences for modern hiring workflows.",
                "skills_used": ["Python", "FastAPI", "React", "LLM APIs"],
            }
        ],
        "education": ["B.Tech in Computer Science", "Specialization in Machine Learning"],
        "projects": [
            "Built a FastAPI + React portfolio that pulls dynamic content from the backend",
            "Designed AI-assisted recruiting workflows with prompt-based candidate chat",
        ],
        "certifications": ["Generative AI Engineering", "Cloud Application Development"],
        "chatPrompt": "Ask me about my background, skills, or projects.",
    }


@app.get("/")
def home():
    return {"message": "HireMeAI portfolio API is running"}


@app.get("/api/portfolio")
def portfolio():
    return build_portfolio_payload()


@app.post("/chat")
def chat(request: ChatRequest):
    resume_text = read_pdf(Path("my_resume.pdf"))
    resume = parse_resume(resume_text)
    answer = ask_candidate(request.question, resume)
    return {"answer": answer}

