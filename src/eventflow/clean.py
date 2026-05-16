"""Clean raw event records for the DVC pipeline.

This stage reads the raw event log, removes rows that do not meet the
assignment's validity rules, and writes a normalized CSV for downstream
pipeline stages.
"""

from pathlib import Path

import pandas as pd


RAW_PATH = Path("data/raw/events.csv")
CLEAN_PATH = Path("data/clean/events.csv")

VALID_EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}


def main() -> None:
    """Create data/clean/events.csv from data/raw/events.csv."""
    df = pd.read_csv(RAW_PATH)

    # Drop rows with missing required fields.
    df = df.dropna(subset=["user_id", "timestamp", "event_type", "duration_seconds"])

    # Make duration numeric, then drop invalid or non-positive durations.
    df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")
    df = df.dropna(subset=["duration_seconds"])
    df = df[df["duration_seconds"] > 0]

    # Keep only valid event types.
    df = df[df["event_type"].isin(VALID_EVENT_TYPES)]

    # Parse mixed timestamp formats, then drop timestamps that cannot be parsed.
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", format="mixed")
    df = df.dropna(subset=["timestamp"])

    # Normalize timestamp to ISO 8601 without fractional seconds.
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    # Keep columns in the original order.
    df = df[["user_id", "timestamp", "event_type", "duration_seconds"]]

    # DVC expects this path to be produced by the clean stage.
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)


if __name__ == "__main__":
    main()
