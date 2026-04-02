Practical Linear Regression: Real-World Data Cleaning (Used Cars)

This project demonstrates a realistic data cleaning workflow for a used-car pricing problem prior to building a linear regression model.

The focus is intentionally **not** on model accuracy yet.  
Instead, the goal is to make the dataset **safe, defensible, and interpretable** for modeling.

This mirrors how real data science work happens in production.

---

## Project Objective

Predict the price of a used car based on its specifications, including:

- brand
- body type
- mileage
- engine volume
- year of production

Before any modeling can occur, the raw dataset must be cleaned to address:

- missing values  
- extreme outliers  
- invalid domain values  
- high-cardinality categorical variables  

---

Why Visualizations Are Included

The visualizations in this project are not exploratory fluff.  
They are evidence that cleaning decisions were necessary and effective.

Each visualization answers a specific modeling risk question.

1. Histograms (Univariate)
Question: 
Is this variable heavily skewed or dominated by extreme outliers?

Why it matters:
Linear regression is sensitive to extreme values.  
A small number of unusually large observations can dominate coefficients and lead to unstable predictions.

---

2. Scatter Plots (Bivariate)
Question:  
Does this feature have a plausible relationship with price?

Why it matters: 
Linear regression assumes stable, mostly monotonic relationships.  
Scatter plots expose leverage points and reveal whether the data behaves logically.

---
3. Before vs After Comparisons
Cleaning decisions must be defensible.

By saving before-and-after plots, we:
- prove the data had real problems
- show that cleaning improved distributions
- document decisions for reviewers and stakeholders

---

Visual Evidence

All plots are saved automatically to the 'figures` folder.

Price Distribution
Before Price Distribution(figures/before_price_distribution.png)
After Price Distribution(figures/after_price_distribution.png)

Mileage vs Price
Before Mileage vs Price(figures/before_mileage_vs_price.png)
After Mileage vs Price(figures/after_mileage_vs_price.png)

Year vs Price
Before Year vs Price(figures/before_year_vs_price.png)
After Year vs Price(figures/after_year_vs_price.png)

---

Cleaning Steps

1. Normalize column names
2. Rename enginev → `engine_volume`
3. Drop `model` column
4. Remove missing values
5. Remove price outliers (top 1%)
6. Remove mileage outliers (top 1%)
7. Apply engine volume domain rules
8. Remove extreme vintage vehicles
9. Reset index and save cleaned data

Output: `cars_cleaned.csv`

---

How to Run

bash
pip install pandas matplotlib


Run `PracticalLinearRegression.py` in PyCharm.

---

PM Perspective

Most ML risk exists before modeling.

This project focuses on:
- explainability
- defensible assumptions
- data quality risk reduction
- stakeholder-readable artifacts

---

Next Steps

- Log-transform price
- Encode categorical variables
- Train and evaluate a regression model
