from typing import Dict, Any


def build_markdown_report(
    config: Dict[str, Any],
    eda_summary: Dict[str, Any],
    model_text: str,
    llm_sections: Dict[str, str],
) -> str:
    """Combine everything into a Markdown report string."""
    md = []
    md.append("# Longitudinal Outcomes Report\n")

    md.append("## Study Configuration\n")
    md.append(f"- ID column: `{config['id_col']}`\n")
    md.append(f"- Time column: `{config['time_col']}`\n")
    md.append(f"- Outcome(s): `{config['outcome_cols']}`\n")
    md.append(f"- Group: `{config.get('group_col')}`\n")
    md.append(f"- Covariates: `{config.get('covariates')}`\n")

    md.append("\n## Descriptive Statistics\n")
    md.append("**Overall:**\n")
    md.append(f"{eda_summary['overall_desc']}\n\n")

    if eda_summary.get("group_stats"):
        md.append("**By Group:**\n")
        md.append(f"{eda_summary['group_stats']}\n\n")

    md.append("## Mixed-Effects Model Summary\n")
    md.append("```text\n")
    md.append(model_text)
    md.append("\n```\n")

    md.append("## Methods (AI-Generated Draft)\n")
    md.append(llm_sections.get("methods", "") + "\n")

    md.append("## Results (AI-Generated Draft)\n")
    md.append(llm_sections.get("results", "") + "\n")

    md.append("## Executive Summary (AI-Generated Draft)\n")
    md.append(llm_sections.get("executive_summary", "") + "\n")

    return "\n".join(md)
