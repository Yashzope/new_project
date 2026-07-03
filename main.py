"""
DEEPDIVE AGENT - Main entry point
"""
import os
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

import planner
import researcher
import synthesizer
import formatter


def main():
    load_dotenv()

    groq_key = os.getenv("GROQ_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")

    if not groq_key or not tavily_key:
        print("ERROR: Missing API keys. Check your .env file.")
        return

    model = Groq(api_key=groq_key)
    tavily_client = TavilyClient(api_key=tavily_key)

    topic = input("Enter a research topic: ").strip()
    if not topic:
        print("No topic entered. Exiting.")
        return

    print("\n[1/4] Planning sub-questions...")
    questions = planner.plan(topic, model)
    print(f"  Generated {len(questions)} sub-questions:")
    for q in questions:
        print(f"   - {q}")

    print("\n[2/4] Researching each sub-question...")
    findings = researcher.research(questions, tavily_client)

    print("\n[3/4] Synthesizing report...")
    report = synthesizer.synthesize(topic, findings, model)

    print("\n[4/4] Saving report...")
    filepath = formatter.save(report, topic)

    print(f"\n✅ Done! Report saved to: {filepath}")


if __name__ == "__main__":
    main()