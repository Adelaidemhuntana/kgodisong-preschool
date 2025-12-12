import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise Exception("API_KEY missing")

client = Groq(
    api_key=GROQ_API_KEY,
)


def call_llama(messages, model="llama-3.1-8b-instant", **kwargs):
    """
    Handles raw chat completion calls to the Llama API.
    messages = [
        {"role": "system", "content": "..."},
        {"role": "system", "content": "..."}
    ]
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.6,
            **kwargs
        )
        return response.choices[0].message.content

    except Exception as e:
        print("API Error:", e)
        return "Sorry, the AI service is temporarily unavailable."


def ask_health_assistant(question: str, age: str):
    """
    Safe child-health assistant wrapper.
    Applies safety rules, disclaimers, and structured prompts.
    """

    SAFE_SYSTEM_PROMPT = """
    You are a child-health guidance assistant.
    You cater for the South African region.
    You MUST NOT diagnose diseases.
    If prompt not a symptom for an age specified child, channel the user.
    Give short, simple, high-level steps parents can do at home.
    Always include red-flag warnings.
    ALWAYS end with: "If symptoms worsen or life is at risk, seek urgent medical care.
    """

    user_prompt = f"""
    Question: {question}
    Age range: {age}
    
    Provide:
    1. Immediate safe steps parents can do at home.
    2. Red flags to watch for.
    3. When to call clinic or emergency services.
    """

    messages = [
        {"role": "system", "content": SAFE_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    return call_llama(messages)


def ask_emergency(question: str):
    """
    Returns structured JSON using function-calling pattern
    """

    messages = [
        {
            "role": "system",
            "content": """
            You assist with medical emergencies using JSON output.
            DO NOT give diagnoses.
            return JSON ONLY in this structure:
            
            {
                "action": "call_ambulance" | "perform_first_aid" | "monitor",
                "steps": ["step 1", "step 2"],
                 "red_flags": ["flag_1", "flag_2"],
                 "advice": "Short sentence only
            }""",
        },
        {
            "role": "user", "content": f"Emergency for a {age}-year-old: {question}",
        }
    ]
    return call_llama(messages)
