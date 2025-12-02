import numpy as np
import pandas as pd
from pathlib import Path


def generate_longitudinal_multimodal(
    n_participants: int = 120,
    n_timepoints: int = 6,
    seed: int = 42,
    outdir: str = "data",
):
    """
    Synthetic longitudinal multimodal psychiatry-style dataset.

    Outputs three CSVs:
      - clinical_longitudinal_data.csv
      - sensor_longitudinal_data.csv
      - text_notes_longitudinal_data.csv
    """
    rng = np.random.default_rng(seed)
    out_path = Path(outdir)
    out_path.mkdir(parents=True, exist_ok=True)

    rows_clinical = []
    rows_sensor = []
    rows_text = []

    participant_ids = np.arange(1, n_participants + 1)

    for pid in participant_ids:
        age = rng.normal(35, 10)
        gender = rng.choice(["Male", "Female", "Other"], p=[0.45, 0.45, 0.10])
        treatment_group = rng.integers(0, 2)

        # baseline severity (higher = worse)
        baseline = rng.normal(22, 6)

        for t in range(1, n_timepoints + 1):
            # Symptom improvement per timepoint (treatment improves faster)
            if treatment_group == 1:
                time_effect = -1.6 * t
            else:
                time_effect = -0.6 * t

            noise = rng.normal(0, 3)
            symptom_score = baseline + time_effect + noise

            # Sensor features: worse symptoms -> fewer steps, worse sleep, more phone use
            avg_steps = max(500, 12000 - symptom_score * 200 + rng.normal(0, 800))
            sleep_hours = np.clip(
                8 - (symptom_score - 15) * 0.1 + rng.normal(0, 0.6),
                3.5,
                10,
            )
            phone_usage = np.clip(
                120 + symptom_score * 8 + rng.normal(0, 40),
                30,
                600,
            )

            if symptom_score > 22:
                mood_phrase = "feeling very overwhelmed and anxious"
            elif symptom_score > 18:
                mood_phrase = "struggling with mood but noticing some better days"
            elif symptom_score > 14:
                mood_phrase = "feeling somewhat better and more hopeful"
            else:
                mood_phrase = "feeling much more stable and engaged in daily activities"

            if treatment_group == 1:
                treatment_phrase = "engaging regularly with therapy and treatment exercises"
            else:
                treatment_phrase = "attending check-ins but not in the intensive treatment group"

            note_text = (
                f"At visit {t}, the participant reports {mood_phrase}, "
                f"while {treatment_phrase}. Sleep and energy fluctuate."
            )

            rows_clinical.append(
                {
                    "participant_id": pid,
                    "timepoint": t,
                    "treatment_group": treatment_group,
                    "symptom_score": symptom_score,
                    "age": age,
                    "gender": gender,
                }
            )

            rows_sensor.append(
                {
                    "participant_id": pid,
                    "timepoint": t,
                    "avg_steps": avg_steps,
                    "sleep_hours": sleep_hours,
                    "phone_usage_minutes": phone_usage,
                }
            )

            rows_text.append(
                {
                    "participant_id": pid,
                    "timepoint": t,
                    "note_text": note_text,
                }
            )

    clinical_df = pd.DataFrame(rows_clinical)
    sensor_df = pd.DataFrame(rows_sensor)
    text_df = pd.DataFrame(rows_text)

    clinical_df.to_csv(out_path / "clinical_longitudinal_data.csv", index=False)
    sensor_df.to_csv(out_path / "sensor_longitudinal_data.csv", index=False)
    text_df.to_csv(out_path / "text_notes_longitudinal_data.csv", index=False)

    print(f"Saved clinical, sensor, and text data to {out_path.resolve()}")


if __name__ == "__main__":
    generate_longitudinal_multimodal()
