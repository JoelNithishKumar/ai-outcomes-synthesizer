from typing import Dict, Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_trajectories(df: pd.DataFrame, config: Dict[str, Any]):
    """Plot outcome over time, optionally by group."""
    outcome = config["outcome_cols"][0]
    time_col = config["time_col"]
    group_col = config.get("group_col")

    fig, ax = plt.subplots(figsize=(6, 4))

    if group_col and group_col in df.columns:
        sns.lineplot(
            data=df,
            x=time_col,
            y=outcome,
            hue=group_col,
            estimator="mean",
            errorbar="ci",
            ax=ax,
        )
    else:
        sns.lineplot(
            data=df,
            x=time_col,
            y=outcome,
            estimator="mean",
            errorbar="ci",
            ax=ax,
        )

    ax.set_title(f"{outcome} over {time_col}")
    return fig


def plot_sensor_feature(df: pd.DataFrame, feature: str, config: Dict[str, Any]):
    """Plot a sensor feature over time."""
    time_col = config["time_col"]
    group_col = config.get("group_col")

    fig, ax = plt.subplots(figsize=(6, 4))

    if feature not in df.columns:
        ax.text(0.5, 0.5, f"{feature} not found", ha="center", va="center")
        return fig

    if group_col and group_col in df.columns:
        sns.lineplot(
            data=df,
            x=time_col,
            y=feature,
            hue=group_col,
            estimator="mean",
            errorbar="ci",
            ax=ax,
        )
    else:
        sns.lineplot(
            data=df,
            x=time_col,
            y=feature,
            estimator="mean",
            errorbar="ci",
            ax=ax,
        )

    ax.set_title(f"{feature} over {time_col}")
    return fig
