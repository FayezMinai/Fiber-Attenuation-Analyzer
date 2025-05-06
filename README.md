# Fiber Attenuation Analyzer

A Python-based graphical tool for modeling and visualizing optical fiber attenuation using experimental measurements.

## 📌 Description

This tool imports a CSV file containing measured optical power versus fiber length, fits an exponential attenuation model:

\[
P(L) = P_0 \, e^{-\alpha L}
\]

and generates plots in both linear (mW) and logarithmic (dB) domains, with shaded 95% confidence intervals.

---

## ✨ Features

- **Graphical User Interface (GUI):** Prompts user to select a CSV file and shows the required format
- **Data Fitting:** Uses `scipy.optimize.curve_fit` to estimate the initial power \( P_0 \) and attenuation coefficient \( \alpha \)
- **Confidence Bands:** Shades 95% confidence intervals around fitted models
- **Dual-Domain Visualization:** Plots in both linear (mW) and logarithmic (dB) scales for analysis

---

## 🔧 Prerequisites

- **Python 3.6+**

### Required Libraries:
- `numpy`
- `pandas`
- `matplotlib`
- `scipy`
- `tkinter` (usually bundled with Python)

Install all dependencies using:

```bash
pip install -r requirements.txt
