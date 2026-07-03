"""
PLANNER MODULE
Takes a topic and breaks it into structured sub-questions
that will guide the research phase.
"""
import json
from groq import Groq

MODEL_NAME = "llama-3.3-70b-versatile"


def plan(topic: str, client: Groq, num_questions: int = 6) -> list[str]:
    """
    Ask the LLM to break the topic into sub-questions.
    Returns a list of question strings.
    """
    prompt = f"""You are a research planner. Given a topic, break it down into
{num_questions} distinct, non-overlapping sub-questions that together would
produce a comprehensive research report on the topic.

Topic: "{topic}"

Respond ONLY with a valid JSON array of strings, nothing else. No markdown
fences, no preamble. Example format:
["question 1", "question 2", "question 3"]
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    text = response.choices[0].message.content.strip()

    # Clean up in case the model adds markdown fences anyway
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        questions = json.loads(text)
        if isinstance(questions, list) and all(isinstance(q, str) for q in questions):
            return questions
    except json.JSONDecodeError:
        pass

    print("[planner] Warning: could not parse questions, using fallback.")
    return [topic]