import os
from typing import Dict, Any, Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_methods_results_text(
    config: Dict[str, Any],
    model_summary: Dict[str, Any],
    text_examples: Optional[str] = None,
) -> Dict[str, str]:
    """
    Use an LLM to generate draft Methods, Results, and an Executive Summary.
    Optionally integrates anonymized text-note excerpts for multimodal interpretation.
    """
    prompt = f"""
You are helping write a scientific manuscript for a longitudinal mental-health / behavioral study.

STUDY DESIGN:
- ID column: {config["id_col"]}
- Time variable: {config["time_col"]}
- Outcome(s): {config["outcome_cols"]}
- Grouping variable: {config.get("group_col")}
- Covariates: {config.get("covariates")}

MODEL SUMMARY:
- Formula: {model_summary.get("formula")}
- Parameters: {model_summary.get("params")}
- P-values: {model_summary.get("pvalues")}
"""

    if text_examples:
        prompt += f"""
The study also collected qualitative text notes over time. Here are some anonymized excerpts:

{text_examples}

Please integrate any consistent qualitative themes (e.g., mood, engagement, functioning) into the interpretation where appropriate.
"""

    prompt += """
TASK:
1) Write a concise Methods paragraph describing the statistical analysis.
2) Write a concise Results paragraph describing the main effects and interactions, using neutral academic tone.
3) Write a 3–4 sentence Executive Summary suitable for an internal report to non-technical stakeholders.

Return each section clearly labeled: METHODS:, RESULTS:, EXECUTIVE SUMMARY:
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert biostatistician and scientific writer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content

    sections = {"methods": "", "results": "", "executive_summary": ""}

    current = None
    for line in content.splitlines():
        l = line.strip()
        if l.upper().startswith("METHODS"):
            current = "methods"
            continue
        elif l.upper().startswith("RESULTS"):
            current = "results"
            continue
        elif l.upper().startswith("EXECUTIVE SUMMARY"):
            current = "executive_summary"
            continue

        if current:
            sections[current] += line + "\n"

    return sections
