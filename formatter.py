"""
FORMATTER MODULE
Saves the final report to a Markdown file in outputs/.
"""
import os
import re
from datetime import datetime


def save(report: str, topic: str, output_dir: str = "outputs") -> str:
    """
    Saves the report as a timestamped Markdown file.
    Returns the file path.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Make a safe filename from the topic
    safe_topic = re.sub(r"[^a-zA-Z0-9]+", "_", topic.strip().lower())[:50]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_topic}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    return filepath
