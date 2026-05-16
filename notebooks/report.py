import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import matplotlib.pyplot as plt
    import pandas as pd

    return pd, plt


@app.cell
def _(pd):
    events = pd.read_csv("data/features/events.csv")
    return (events,)


@app.cell
def _(events, plt):
    fig, ax = plt.subplots()
    ax.hist(events["duration_minutes"], bins=30, edgecolor="black")
    ax.set_title("Distribution of Event Durations")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of events")
    fig.tight_layout()
    fig
    return


if __name__ == "__main__":
    app.run()
