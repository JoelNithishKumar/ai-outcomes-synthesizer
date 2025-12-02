from typing import Dict, Any, Tuple

import pandas as pd
import statsmodels.formula.api as smf


def run_eda(df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
    """Simple descriptive statistics and missingness."""
    outcome = config["outcome_cols"][0]
    group_col = config.get("group_col")

    desc = df[outcome].describe().to_dict()
    missing = df.isna().sum().to_dict()

    group_stats = None
    if group_col and group_col in df.columns:
        group_stats = df.groupby(group_col)[outcome].describe().to_dict()

    return {
        "overall_desc": desc,
        "missing_counts": missing,
        "group_stats": group_stats,
    }


def run_mixed_model(df: pd.DataFrame, config: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Simple linear mixed model:
      outcome ~ time * group + covariates, random intercept for participant.
    """
    id_col = config["id_col"]
    time_col = config["time_col"]
    outcome = config["outcome_cols"][0]
    group_col = config.get("group_col")
    covariates = config.get("covariates", [])

    formula_parts = [time_col]
    if group_col:
        formula_parts.append(group_col)
        formula_parts.append(f"{time_col}:{group_col}")
    formula_parts += covariates

    rhs_terms = []
    for x in formula_parts:
        if x not in df.columns:
            continue
        if df[x].dtype == "object":
            rhs_terms.append(f"C({x})")
        else:
            rhs_terms.append(x)

    rhs = " + ".join(rhs_terms)
    formula = f"{outcome} ~ {rhs}"

    model = smf.mixedlm(formula, df, groups=df[id_col])
    result = model.fit(reml=False)

    summary_text = result.summary().as_text()
    params = result.params.to_dict()
    pvalues = result.pvalues.to_dict()

    summary_dict = {
        "formula": formula,
        "params": params,
        "pvalues": pvalues,
        
    }

    return summary_text, summary_dict
