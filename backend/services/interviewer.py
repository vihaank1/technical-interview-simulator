from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def clean_json(raw_text):

    cleaned = re.sub(
        r"```json|```",
        "",
        raw_text
    ).strip()

    return json.loads(cleaned)


def generate_question(role, difficulty):

    prompt = f"""
    Generate ONE {difficulty} technical interview question
    for a {role} role.

    Keep it concise.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert interviewer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def evaluate_answer(question, answer):

    prompt = f"""
    Evaluate this interview answer.

    Question:
    {question}

    Candidate Answer:
    {answer}

    Return ONLY valid JSON.

    {{
        "score": 8,
        "strengths": [
            "...",
            "..."
        ],
        "weaknesses": [
            "...",
            "..."
        ],
        "feedback": [
            "...",
            "..."
        ]
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional technical interviewer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    raw = response.choices[0].message.content

    try:
        return clean_json(raw)

    except Exception as e:

        return {
            "score": 5,
            "strengths": [
                "Answer received"
            ],
            "weaknesses": [
                "Evaluation parsing failed"
            ],
            "feedback": [
                str(e),
                raw
            ]
        }