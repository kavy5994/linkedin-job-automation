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

# Example
print(generate_cover_letter(
    job_title="Data Scientist",
    company="Google",
    skills=["Python", "Machine Learning", "SQL"]
))