from pathlib import Path

import pandas as pd


TRANSFORMED_PATH = Path("data/transformed/events.csv")
FEATURES_PATH = Path("data/features/events.csv")


def main() -> None:
    df = pd.read_csv(TRANSFORMED_PATH)

    df["duration_minutes"] = df["duration_seconds"] / 60
    df["weekday"] = pd.to_datetime(df["date"]).dt.day_name()

    FEATURES_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(FEATURES_PATH, index=False)


if __name__ == "__main__":
    main()
