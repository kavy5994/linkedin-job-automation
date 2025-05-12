# File: ai_generator.py
from openai import OpenAI
import json

def generate_cover_letter(job_title, company, skills):
    client = OpenAI(api_key="your_openai_key")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional career coach"},
            {"role": "user", "content": f"""
                Write a 250-word cover letter for {job_title} at {company}.
                Highlight these skills: {', '.join(skills)}.
                Use professional tone.
            """}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content
# Add to ai_generator.py
import os

def save_cover_letter(content, job_title, company):
    os.makedirs("cover_letters", exist_ok=True)
    filename = f"cover_letters/{company}_{job_title[:20]}.txt".replace("/", "_")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

# Usage:
cover_text = generate_cover_letter(...)
save_cover_letter(cover_text, "Data Scientist", "Google")


# Example
cover_text = generate_cover_letter(
    job_title="Data Scientist",
    company="Google",
    skills=["Python", "Machine Learning", "SQL"]
)

save_cover_letter(cover_text, "Data Scientist", "Google")