"""Build final event features for the DVC pipeline.

This stage adds the assignment's required derived columns to the transformed
event table and writes the final dataset used by the report notebook.
"""

from pathlib import Path

import pandas as pd


TRANSFORMED_PATH = Path("data/transformed/events.csv")
FEATURES_PATH = Path("data/features/events.csv")


def main() -> None:
    """Create data/features/events.csv from data/transformed/events.csv."""
    df = pd.read_csv(TRANSFORMED_PATH)

    # Convert event durations from seconds to minutes.
    df["duration_minutes"] = df["duration_seconds"] / 60

    # Add the full weekday name for each event date.
    df["weekday"] = pd.to_datetime(df["date"]).dt.day_name()

    # DVC expects this path to be produced by the features stage.
    FEATURES_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(FEATURES_PATH, index=False)


if __name__ == "__main__":
    main()
