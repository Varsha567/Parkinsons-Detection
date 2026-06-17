# Parkinson's Disease Dataset: Exploratory Data Analysis (EDA) Observations

This document summarizes the insights and observations obtained during the Exploratory Data Analysis (EDA) of the Parkinson's Disease vocal dataset (`parkinsons.data`).

---

## 1. Dataset Shape & Dimensionality

- **Shape**: `(195, 24)`
- **Observations**:
  - The dataset consists of **195 rows** and **24 columns**.
  - Each row corresponds to a single voice recording sample from a subject.
  - The columns consist of `name` (an identifier string), `status` (the binary target), and **22 numerical voice feature measurements**.

---

## 2. Column Information & Data Types

- **Features by Type**:
  - **Categorical / Identifier**: `name` (type `object`/`string`)
  - **Target Variable**: `status` (type `int64` - binary classification where `1` = Parkinson's Disease, `0` = Healthy Control)
  - **Biomedical Voice Features**: 22 continuous variables (type `float64`)
- **Memory Footprint**: Extremely lightweight (around 36.7 KB).

---

## 3. Missing Value Analysis

- **Null Counts**: `0` across all columns.
- **Observation**:
  - The dataset has **complete data** with zero missing values, so no imputation, interpolation, or drop strategies are needed.

---

## 4. Descriptive Statistics & Scaling Requirements

> [!WARNING]
> **Scale Disparity Detected:** There is a significant difference in range between different voice features.
> - Vocal fundamental frequencies (`MDVP:Fo(Hz)`, `MDVP:Fhi(Hz)`, `MDVP:Flo(Hz)`) have a large range (from **65.48 Hz** up to **592.03 Hz**).
> - Jitter and shimmer variance features are measured as tiny decimal ratios (e.g., `MDVP:Jitter(Abs)` has a mean of **0.000044**).
> - **Recommendation**: If using distance-based algorithms (like KNN, SVM) or gradient-based models (like Logistic Regression), **feature scaling (Standardization / Min-Max Scaling) is mandatory**. Tree-based classifiers like XGBoost are scale-invariant but scaling remains best practice.

---

## 5. Class Distribution & Imbalance

- **Target Counts (`status`)**:
  - `1` (Parkinson's Disease): **147 cases** (~75.4%)
  - `0` (Healthy Controls): **48 cases** (~24.6%)
- **Observations**:
  - The dataset is **moderately imbalanced** (3:1 ratio of Parkinson's cases to healthy cases).
  - **Impact on Modeling**: Standard metrics like accuracy can be misleading. We should evaluate performance using **F1-score**, **Precision**, and **Recall** (Sensitivity and Specificity). Stratified splitting (e.g., `stratify=y`) must be used to preserve target proportions.

---

## 6. Feature Correlation

> [!NOTE]
> **High Multi-collinearity:**
> - Several frequency variation features (jitter measures: `MDVP:Jitter(%)`, `MDVP:Jitter(Abs)`, `MDVP:RAP`, `MDVP:PPQ`, `Jitter:DDP`) and amplitude variation features (shimmer measures: `MDVP:Shimmer`, `MDVP:Shimmer(dB)`, `Shimmer:APQ3`, `Shimmer:APQ5`, `MDVP:APQ`, `Shimmer:DDA`) show **strong positive correlations (r > 0.90)**.
> - This forms highly distinct red clusters in the correlation heatmap.
> - Tree-based models like XGBoost handle multicollinearity natively, but linear models will struggle with unstable coefficients unless regularized (e.g., Ridge/Lasso).

---

## 7. Baseline XGBoost Model Performance

A baseline XGBoost classifier was trained with a **Stratified 80/20 train/test split**:

- **Overall Accuracy**: **92.31%** (36 out of 39 test cases correctly classified)
- **Detailed Classification Report**:

| Class | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **0 (Healthy)** | 0.89 | 0.80 | 0.84 | 10 |
| **1 (Parkinson's)** | 0.93 | 0.97 | 0.95 | 29 |
| **Accuracy** | | | **0.92** | 39 |

- **Observations**:
  - The model has excellent sensitivity (Recall = **97%** for class 1), meaning it successfully detects almost all Parkinson's cases in the test set.
  - Recall for healthy cases is **80%** (2 out of 10 controls were misclassified as Parkinson's), which is likely a side-effect of the moderate class imbalance and small test sample size.

---

## 8. Feature Importance (XGBoost)

Here are the top 10 most influential features according to XGBoost split importances:

| Rank | Feature | Importance Score | Feature Description |
| :---: | :--- | :---: | :--- |
| 1 | **PPE** | 0.2167 | Pitch Period Entropy (measure of fundamental frequency variation) |
| 2 | **spread1** | 0.1964 | Nonlinear measure of fundamental frequency variation |
| 3 | **NHR** | 0.0965 | Noise-to-Harmonics Ratio (measure of noise in the voice) |
| 4 | **MDVP:Jitter(%)** | 0.0567 | Frequency jitter percentage |
| 5 | **MDVP:Flo(Hz)** | 0.0553 | Minimum vocal fundamental frequency |
| 6 | **MDVP:Shimmer(dB)** | 0.0535 | Shimmer in decibels (amplitude variation) |
| 7 | **MDVP:Shimmer** | 0.0421 | Shimmer percentage (amplitude variation) |
| 8 | **MDVP:Fo(Hz)** | 0.0405 | Average vocal fundamental frequency |
| 9 | **MDVP:APQ** | 0.0372 | 11-point amplitude perturbation quotient |
| 10 | **Shimmer:APQ5** | 0.0325 | 5-point amplitude perturbation quotient |

> [!IMPORTANT]
> **Clinical Alignment:**
> - `PPE` (21.67%) and `spread1` (19.64%) dominate feature importance, accounting for over **41%** of the model's predictive power.
> - Both features capture the dysfunction of the vocal cords in maintaining stable pitches and frequencies, which is a known physiological symptom of Parkinson's Disease (dysphonia).
