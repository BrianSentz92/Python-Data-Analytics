"""
UNDERFITTING vs OVERFITTING (ELI5 + PM-friendly)

WHY THIS SCRIPT EXISTS:
Data science interviewers LOVE asking: "What is overfitting and how do we deal with it?"
This script shows it visually, because overfitting can look “amazing” until you test on new data.

WHAT YOU WILL SEE:
- A set of dots (our data points)
- Two model lines:
  1) UNDERFITTING model (too simple): a straight line
  2) OVERFITTING model (too complex): a very wiggly curve

WHY THE VISUALIZATION MATTERS (MAIN POINT):
- Training data = what the model learned from
- Test data = “surprise quiz” data it NEVER saw before

A model can “look great” on training data and still fail in real life.
The plot makes that risk obvious.
"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error


def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """ELI5: Mean Squared Error = average of (prediction error)^2. Lower is better."""
    return mean_squared_error(y_true, y_pred)


def main():
    # ============================================================
    # 1) MAKE TOY DATA (FAKE REALITY)
    # ============================================================
    # ELI5:
    # We create a relationship that is CURVED (not a straight line),
    # then add noise (messiness) like real-world data.
    rng = np.random.default_rng(42)

    X = np.linspace(-3, 3, 80).reshape(-1, 1)          # "input"
    y = (X.flatten() ** 2) + rng.normal(0, 1.0, 80)    # "output" with noise

    # ============================================================
    # 2) SPLIT INTO TRAIN vs TEST
    # ============================================================
    # ELI5:
    # TRAIN = data the model is allowed to learn from
    # TEST  = data the model has never seen (like production)
    #
    # WHY THIS IS IMPORTANT:
    # Overfitting is when the model "memorizes" training data.
    # The test set is the simplest reality-check to detect that.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    # ============================================================
    # 3) UNDERFITTING MODEL (TOO SIMPLE)
    # ============================================================
    # ELI5:
    # A straight line is too simple for a curved pattern.
    # So it will be wrong on BOTH train and test (generally).
    underfit = LinearRegression()
    underfit.fit(X_train, y_train)

    y_train_pred_under = underfit.predict(X_train)
    y_test_pred_under = underfit.predict(X_test)

    # ============================================================
    # 4) OVERFITTING MODEL (TOO COMPLEX)
    # ============================================================
    # ELI5:
    # A high-degree polynomial can bend and wiggle a LOT.
    # It can “hug” the training data and look amazing,
    # but it often captures noise instead of true signal.
    #
    # Translation:
    # - Training error becomes very low
    # - Test error gets worse (model doesn’t generalize)
    overfit = Pipeline(steps=[
        ("poly", PolynomialFeatures(degree=10, include_bias=False)),
        ("model", LinearRegression())
    ])
    overfit.fit(X_train, y_train)

    y_train_pred_over = overfit.predict(X_train)
    y_test_pred_over = overfit.predict(X_test)

    # ============================================================
    # 5) PRINT METRICS (THE "SCOREBOARD")
    # ============================================================
    # ELI5:
    # - If TRAIN error is low but TEST error is high => overfitting
    # - If both TRAIN and TEST errors are high => underfitting
    print("\n================ RESULTS ================")
    print("UNDERFITTING (Linear Regression)")
    print(f"Train MSE: {mse(y_train, y_train_pred_under):.3f}")
    print(f"Test  MSE: {mse(y_test, y_test_pred_under):.3f}")

    print("\nOVERFITTING (Polynomial degree=10)")
    print(f"Train MSE: {mse(y_train, y_train_pred_over):.3f}")
    print(f"Test  MSE: {mse(y_test, y_test_pred_over):.3f}")
    print("========================================\n")

    # ============================================================
    # 6) VISUALIZATION (THIS IS THE WHOLE POINT)
    # ============================================================
    # WHAT THE PLOT IS SUPPOSED TO SHOW:
    #
    # 1) Training points vs Test points:
    #    - Training = history the model can "cheat" on
    #    - Test = new data / real world
    #
    # 2) Underfit line:
    #    - Too simple, misses the curved pattern
    #
    # 3) Overfit curve:
    #    - Too wiggly, hugs training points
    #    - Often behaves strangely between points
    #
    # WHY THIS MATTERS FOR A PM:
    # - Overfitting looks good in a demo.
    # - Test performance is what predicts production performance.
    x_plot = np.linspace(-3, 3, 300).reshape(-1, 1)

    plt.figure()
    plt.scatter(X_train, y_train, alpha=0.7, label="TRAIN data (seen by model)")
    plt.scatter(X_test, y_test, alpha=0.7, label="TEST data (unseen 'surprise quiz')")

    plt.plot(x_plot, underfit.predict(x_plot), linewidth=2, label="UNDERFIT model (too simple)")
    plt.plot(x_plot, overfit.predict(x_plot), linewidth=2, label="OVERFIT model (too complex)")

    plt.title("Underfitting vs Overfitting (Why Train/Test Split Matters)")
    plt.xlabel("X (input)")
    plt.ylabel("y (output)")
    plt.legend()
    plt.tight_layout()

    # PyCharm needs this to open the plot window
    plt.show()


if __name__ == "__main__":
    main()
