"""
RESEARCHER MODULE
For each sub-question, searches the web via Tavily and collects
relevant snippets + source URLs.
"""
from tavily import TavilyClient


def research(questions: list[str], tavily_client: TavilyClient, max_results: int = 4) -> list[dict]:
    """
    Runs a web search for each sub-question.
    Returns a list of dicts:
    [
      {
        "question": "...",
        "sources": [
          {"title": "...", "url": "...", "content": "..."},
          ...
        ]
      },
      ...
    ]
    """
    findings = []

    for q in questions:
        print(f"[researcher] Searching: {q}")
        try:
            result = tavily_client.search(
                query=q,
                max_results=max_results,
                search_depth="advanced",
                include_answer=False,
            )
            sources = [
                {
                    "title": r.get("title", "Untitled"),
                    "url": r.get("url", ""),
                    "content": r.get("content", "")[:1500],  # cap length per source
                }
                for r in result.get("results", [])
            ]
        except Exception as e:
            print(f"[researcher] Error searching '{q}': {e}")
            sources = []

        findings.append({"question": q, "sources": sources})

    return findings
