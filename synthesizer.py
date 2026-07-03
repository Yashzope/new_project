"""
SYNTHESIZER MODULE
Takes all research findings and asks the LLM to write a structured,
cited report.
"""
from groq import Groq

MODEL_NAME = "llama-3.3-70b-versatile"


def synthesize(topic: str, findings: list[dict], client: Groq) -> str:
    """
    Builds a big context blob of all findings, then asks the LLM to
    write a structured Markdown report with inline numbered citations
    and a source list at the end.
    """
    source_list = []
    context_blocks = []
    citation_counter = 1
    url_to_number = {}

    for f in findings:
        block_lines = [f"### Sub-question: {f['question']}"]
        for src in f["sources"]:
            url = src["url"]
            if url not in url_to_number:
                url_to_number[url] = citation_counter
                source_list.append(f"[{citation_counter}] {src['title']} - {url}")
                citation_counter += 1
            num = url_to_number[url]
            block_lines.append(f"(Source [{num}]) {src['content']}")
        context_blocks.append("\n".join(block_lines))

    context_text = "\n\n".join(context_blocks)
    sources_text = "\n".join(source_list)

    prompt = f"""You are a research analyst writing a structured report.

TOPIC: "{topic}"

Below is raw research material gathered from the web, organized by
sub-question. Each snippet is tagged with a citation number in brackets,
e.g. [3].

RESEARCH MATERIAL:
{context_text}

INSTRUCTIONS:
- Write a well-structured Markdown report on the topic.
- Include: a short Executive Summary, then organized sections with headers
  covering the key themes (group related material logically).
- Every factual claim must include an inline citation like [1], [2] matching
  the citation numbers provided above. Use the SAME numbers as given.
- Do not invent facts or sources. Only use what's in the research material.
- Do NOT write a Sources section yourself — I will append it separately.
- Keep the tone objective and analytical.

Write the report body now (everything except the Sources section):
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=4000,
    )
    report_body = response.choices[0].message.content.strip()

    full_report = f"# Research Report: {topic}\n\n{report_body}\n\n## Sources\n\n{sources_text}\n"
    return full_report