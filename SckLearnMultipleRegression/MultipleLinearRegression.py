import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
import os

sns.set()

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# CSV is in the SAME folder as the script
DATA_FILE = "1.02.Multiple Linear Regression.csv"


# -------------------------------------------------------------------------
# Compute Adjusted R²
# -------------------------------------------------------------------------
def compute_adjusted_r2(X, y, model):
    r2 = model.score(X, y)
    N = X.shape[0]
    P = X.shape[1]
    adj_r2 = 1 - (1 - r2) * (N - 1) / (N - P - 1)
    return r2, adj_r2


# -------------------------------------------------------------------------
# SIMPLE LINEAR REGRESSION
# -------------------------------------------------------------------------
def run_simple_regression(save=False):
    data = pd.read_csv(DATA_FILE)
    X = data['SAT'].values.reshape(-1, 1)
    y = data['GPA']

    reg = LinearRegression()
    reg.fit(X, y)
    y_pred = reg.predict(X)

    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue')
    plt.plot(X, y_pred, color='red')
    plt.title("Simple Regression")
    plt.xlabel("SAT")
    plt.ylabel("GPA")

    if save:
        plt.savefig(f"{OUTPUT_DIR}/simple_regression.png")

    plt.show()


# -------------------------------------------------------------------------
# MULTIPLE LINEAR REGRESSION (2D)
# -------------------------------------------------------------------------
def run_multiple_regression_2D(save=False):
    data = pd.read_csv(DATA_FILE)
    X = data[['SAT', 'Rand 1,2,3']]
    y = data['GPA']

    reg = LinearRegression()
    reg.fit(X, y)
    y_pred = reg.predict(X)

    plt.figure(figsize=(10, 6))
    plt.scatter(X['SAT'], y, color='blue')
    plt.scatter(X['SAT'], y_pred, color='red')
    plt.title("Multiple Regression (2D)")
    plt.xlabel("SAT")
    plt.ylabel("GPA")

    if save:
        plt.savefig(f"{OUTPUT_DIR}/multiple_regression_2D.png")

    plt.show()


# -------------------------------------------------------------------------
# MULTIPLE LINEAR REGRESSION (3D)
# -------------------------------------------------------------------------
def run_multiple_regression_3D(save=False):
    data = pd.read_csv(DATA_FILE)
    X = data[['SAT', 'Rand 1,2,3']]
    y = data['GPA']

    reg = LinearRegression()
    reg.fit(X, y)

    sat_range = np.linspace(X['SAT'].min(), X['SAT'].max(), 10)
    rand_range = np.linspace(X['Rand 1,2,3'].min(), X['Rand 1,2,3'].max(), 10)
    SAT_grid, RAND_grid = np.meshgrid(sat_range, rand_range)

    Z = (
        reg.intercept_
        + reg.coef_[0] * SAT_grid
        + reg.coef_[1] * RAND_grid
    )

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(X['SAT'], X['Rand 1,2,3'], y)
    ax.plot_surface(SAT_grid, RAND_grid, Z, alpha=0.4)
    ax.set_title("3D Regression Plane")
    ax.set_xlabel("SAT")
    ax.set_ylabel("Rand")
    ax.set_zlabel("GPA")

    if save:
        plt.savefig(f"{OUTPUT_DIR}/multiple_regression_3D.png")

    plt.show()


# -------------------------------------------------------------------------
# MAIN EXECUTION BLOCK
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n=== Regression Suite Started ===\n")

    print("Running Simple Regression...")
    run_simple_regression(save=True)

    print("Running Multiple Regression 2D...")
    run_multiple_regression_2D(save=True)

    print("Running Multiple Regression 3D...")
    run_multiple_regression_3D(save=True)

    print("\n=== All analyses complete. PNGs saved in outputs/ ===\n")
