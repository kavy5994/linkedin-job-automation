import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cover_letter(job_desc, resume_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a career assistant that writes concise cover letters."},
            {"role": "user", "content": f"Job Description:\n{job_desc}\n\nMy Resume:\n{resume_text}\n\nWrite a 150-word cover letter highlighting relevant skills."}
        ]
    )
    return response.choices[0].message.content