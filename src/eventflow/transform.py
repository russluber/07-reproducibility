"""Transform cleaned event records for the DVC pipeline.

This stage adds a date column derived from the normalized timestamp while
keeping the number of rows unchanged.
"""

from pathlib import Path

import pandas as pd


CLEAN_PATH = Path("data/clean/events.csv")
TRANSFORMED_PATH = Path("data/transformed/events.csv")


def main() -> None:
    """Create data/transformed/events.csv from data/clean/events.csv."""
    df = pd.read_csv(CLEAN_PATH)

    # Extract the calendar date used by later feature engineering.
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d")

    # Preserve the normalized timestamp format from the clean stage.
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    # DVC expects this path to be produced by the transform stage.
    TRANSFORMED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(TRANSFORMED_PATH, index=False)


if __name__ == "__main__":
    main()
