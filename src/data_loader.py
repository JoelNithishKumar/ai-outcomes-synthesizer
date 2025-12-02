import json
from typing import Tuple, Dict, Any

import pandas as pd


def load_config(config_file) -> Dict[str, Any]:
    """Load JSON config from a file-like object or a file path."""
    if hasattr(config_file, "read"):
        config = json.load(config_file)
    else:
        with open(config_file, "r") as f:
            config = json.load(f)
    return config


def load_data(csv_file) -> pd.DataFrame:
    """Load clinical CSV data from a file-like object or a file path."""
    if hasattr(csv_file, "read"):
        df = pd.read_csv(csv_file)
    else:
        df = pd.read_csv(csv_file)
    return df


def load_multimodal(config: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """
    Load additional modality tables from config.
    Returns a dict like {"sensor": df_sensor, "text": df_text}.
    """
    modalities_cfg = config.get("modalities", {})
    modalities = {}

    for name, mcfg in modalities_cfg.items():
        file_path = mcfg.get("file")
        if not file_path:
            continue
        mdf = pd.read_csv(file_path)
        modalities[name] = mdf

    return modalities


def merge_sensor_into_main(
    df: pd.DataFrame,
    config: Dict[str, Any],
    modalities: Dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Merge sensor features into the main DataFrame based on merge_on keys.
    """
    sensor_cfg = config.get("modalities", {}).get("sensor")
    if sensor_cfg and "sensor" in modalities:
        merge_on = sensor_cfg.get("merge_on", [])
        sensor_df = modalities["sensor"]
        df = df.merge(sensor_df, on=merge_on, how="left")
    return df


def validate_data(df: pd.DataFrame, config: Dict[str, Any]) -> Tuple[bool, str]:
    """Basic validation: check required columns exist."""
    required_cols = [config["id_col"], config["time_col"]] + config["outcome_cols"]
    if config.get("group_col"):
        required_cols.append(config["group_col"])
    if config.get("covariates"):
        required_cols.extend(config["covariates"])

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        return False, f"Missing columns in data: {missing}"

    return True, "OK"
