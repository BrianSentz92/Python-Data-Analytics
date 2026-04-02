"""
PRACTICAL LINEAR REGRESSION — DATA CLEANING + VISUALS (SHOW + SAVE PNGs)

Expected files in the SAME folder as this script:
- 1.04 Real-life+example.csv
- PracticalLinearRegression.py

Outputs:
- cars_cleaned.csv
- figures/*.png

================================================================================
WHY WE INCLUDE VISUALIZATIONS (AS PNGs + ON-SCREEN)
================================================================================
These plots are *evidence* that cleaning was necessary and effective.

We choose two plot types because they answer two different regression risk questions:

1) HISTOGRAMS (one variable)
   Question: "Is this variable distorted by outliers or heavy skew?"
   Why it matters: outliers can dominate linear regression coefficients and lead
   to unstable predictions for normal cases.

2) SCATTER PLOTS (two variables)
   Question: "Does this feature have a plausible relationship with price?"
   Why it matters: scatter plots reveal leverage points (extreme values that pull
   the regression line) and show whether relationships make sense.

We do BEFORE vs AFTER plots to:
- establish a baseline (raw data problems)
- prove that cleaning improved model readiness

We SAVE plots as PNGs so GitHub shows the evidence without rerunning code.
We SHOW plots during runtime so you get immediate visual feedback while developing.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Helpers
# -----------------------------
def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to avoid mismatch bugs."""
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def plot_hist(series: pd.Series, title: str, xlabel: str, filename: str,
              figures_dir: Path, show: bool = True) -> None:
    """
    WHY THIS PLOT:
    Histograms expose skew and outliers that can distort regression coefficients.
    Saving as PNG makes cleaning decisions defensible in a portfolio repo.
    """
    plt.figure()
    series.dropna().hist(bins=40)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    plt.tight_layout()

    # Save first (artifact)
    plt.savefig(figures_dir / filename)

    # Show second (human feedback)
    if show:
        plt.show(block=False)

    # Close to prevent memory buildup and duplicate plots
    plt.close()


def plot_scatter(x: pd.Series, y: pd.Series, title: str, xlabel: str, ylabel: str,
                 filename: str, figures_dir: Path, show: bool = True) -> None:
    """
    WHY THIS PLOT:
    Scatter plots validate expected feature→price relationships and expose leverage points.
    Saving as PNG provides “before vs after” evidence for cleaning.
    """
    plt.figure()
    plt.scatter(x, y, alpha=0.5)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()

    plt.savefig(figures_dir / filename)

    if show:
        plt.show(block=False)

    plt.close()


def main():
    # Toggle for development vs automation/CI runs
    SHOW_PLOTS = True  # set False if you only want PNGs

    # -----------------------------
    # 1) Paths (script + CSV live together)
    # -----------------------------
    project_dir = Path(__file__).resolve().parent
    raw_csv_path = project_dir / "1.04 Real-life+example.csv"
    cleaned_csv_path = project_dir / "cars_cleaned.csv"

    figures_dir = project_dir / "figures"
    figures_dir.mkdir(exist_ok=True)

    if not raw_csv_path.exists():
        raise FileNotFoundError(
            f"CSV not found at: {raw_csv_path}\n"
            f"Fix: put '1.04 Real-life+example.csv' in the same folder as this script."
        )

    # -----------------------------
    # 2) Load + normalize columns
    # -----------------------------
    raw_data = pd.read_csv(raw_csv_path)
    data = standardize_column_names(raw_data)

    # Your dataset uses enginev; lecture concept calls this engine_volume
    data = data.rename(columns={"enginev": "engine_volume"})

    required_cols = ["price", "brand", "body", "mileage", "engine_volume", "year"]
    missing = [c for c in required_cols if c not in data.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"Available columns: {list(data.columns)}"
        )

    print("\n=== RAW DATA LOADED ===")
    print("Rows:", len(data), "Cols:", len(data.columns))
    print("Columns:", list(data.columns))

    # -----------------------------
    # 3) BEFORE CLEANING PLOTS (baseline evidence)
    # -----------------------------
    plot_hist(data["price"], "BEFORE: Price distribution (raw)", "Price",
              "before_price_distribution.png", figures_dir, show=SHOW_PLOTS)
    plot_hist(data["mileage"], "BEFORE: Mileage distribution (raw)", "Mileage",
              "before_mileage_distribution.png", figures_dir, show=SHOW_PLOTS)
    plot_hist(data["engine_volume"], "BEFORE: Engine volume distribution (raw)", "Engine Volume (L)",
              "before_engine_volume_distribution.png", figures_dir, show=SHOW_PLOTS)
    plot_hist(data["year"], "BEFORE: Year distribution (raw)", "Year",
              "before_year_distribution.png", figures_dir, show=SHOW_PLOTS)

    plot_scatter(data["mileage"], data["price"], "BEFORE: Mileage vs Price (raw)", "Mileage", "Price",
                 "before_mileage_vs_price.png", figures_dir, show=SHOW_PLOTS)
    plot_scatter(data["year"], data["price"], "BEFORE: Year vs Price (raw)", "Year", "Price",
                 "before_year_vs_price.png", figures_dir, show=SHOW_PLOTS)

    # -----------------------------
    # 4) Drop 'model' column (too many unique values)
    # -----------------------------
    if "model" in data.columns:
        unique_models = data["model"].nunique(dropna=True)
        print(f"\nDropping 'model' (unique values: {unique_models})")
        data = data.drop(columns=["model"])

    # -----------------------------
    # 5) Missing values: drop rows with ANY missing values
    # -----------------------------
    rows_before = len(data)
    data_no_mv = data.dropna(axis=0).copy()
    dropped_mv = rows_before - len(data_no_mv)
    print(f"\nDropped rows with missing values: {dropped_mv} ({dropped_mv / rows_before:.2%})")

    # -----------------------------
    # 6) Remove PRICE outliers (top 1%)
    # -----------------------------
    price_99 = data_no_mv["price"].quantile(0.99)
    rows_before = len(data_no_mv)
    data_no_mv = data_no_mv[data_no_mv["price"] <= price_99].copy()
    print(f"\nPrice 99th percentile cutoff: {price_99:.2f}")
    print(f"Removed price outliers: {rows_before - len(data_no_mv)}")

    # -----------------------------
    # 7) Remove MILEAGE outliers (top 1%)
    # -----------------------------
    mileage_99 = data_no_mv["mileage"].quantile(0.99)
    rows_before = len(data_no_mv)
    data_no_mv = data_no_mv[data_no_mv["mileage"] <= mileage_99].copy()
    print(f"\nMileage 99th percentile cutoff: {mileage_99:.2f}")
    print(f"Removed mileage outliers: {rows_before - len(data_no_mv)}")

    # -----------------------------
    # 8) Engine volume cleanup (domain knowledge)
    # -----------------------------
    rows_before = len(data_no_mv)
    data_no_mv = data_no_mv[
        (data_no_mv["engine_volume"] >= 0.6) &
        (data_no_mv["engine_volume"] <= 6.5)
    ].copy()
    print(f"\nRemoved unrealistic engine_volume values: {rows_before - len(data_no_mv)}")

    # -----------------------------
    # 9) Year cleanup (remove vintage cars, bottom 1%)
    # -----------------------------
    year_01 = data_no_mv["year"].quantile(0.01)
    rows_before = len(data_no_mv)
    data_no_mv = data_no_mv[data_no_mv["year"] >= year_01].copy()
    print(f"\nYear 1st percentile cutoff: {year_01:.0f}")
    print(f"Removed vintage-year outliers: {rows_before - len(data_no_mv)}")

    # -----------------------------
    # 10) Save cleaned dataset
    # -----------------------------
    data_cleaned = data_no_mv.reset_index(drop=True)
    data_cleaned.to_csv(cleaned_csv_path, index=False)
    print(f"\n✅ Saved cleaned dataset to: {cleaned_csv_path}")

    # -----------------------------
    # 11) AFTER CLEANING PLOTS (proof of improvement)
    # -----------------------------
    plot_hist(data_cleaned["price"], "AFTER: Price distribution (cleaned)", "Price",
              "after_price_distribution.png", figures_dir, show=SHOW_PLOTS)
    plot_hist(data_cleaned["mileage"], "AFTER: Mileage distribution (cleaned)", "Mileage",
              "after_mileage_distribution.png", figures_dir, show=SHOW_PLOTS)
    plot_hist(data_cleaned["engine_volume"], "AFTER: Engine volume distribution (cleaned)", "Engine Volume (L)",
              "after_engine_volume_distribution.png", figures_dir, show=SHOW_PLOTS)
    plot_hist(data_cleaned["year"], "AFTER: Year distribution (cleaned)", "Year",
              "after_year_distribution.png", figures_dir, show=SHOW_PLOTS)

    plot_scatter(data_cleaned["mileage"], data_cleaned["price"],
                 "AFTER: Mileage vs Price (cleaned)", "Mileage", "Price",
                 "after_mileage_vs_price.png", figures_dir, show=SHOW_PLOTS)
    plot_scatter(data_cleaned["year"], data_cleaned["price"],
                 "AFTER: Year vs Price (cleaned)", "Year", "Price",
                 "after_year_vs_price.png", figures_dir, show=SHOW_PLOTS)

    print(f"\n✅ Saved figures to: {figures_dir}")
    print("✅ Tip: If too many windows open, set SHOW_PLOTS = False to only save PNGs.")


if __name__ == "__main__":
    main()
