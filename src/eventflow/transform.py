from pathlib import Path

import pandas as pd


CLEAN_PATH = Path("data/clean/events.csv")
TRANSFORMED_PATH = Path("data/transformed/events.csv")


def main() -> None:
    df = pd.read_csv(CLEAN_PATH)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d")
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    TRANSFORMED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(TRANSFORMED_PATH, index=False)


if __name__ == "__main__":
    main()
