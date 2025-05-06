#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def exponential_model(L, P0, alpha):
    """Exponential attenuation: P(L) = P0 * exp(-alpha * L)."""
    return P0 * np.exp(-alpha * L)

def main():
    # --- 1. Set up GUI and inform user of CSV format ---
    root = tk.Tk()
    root.withdraw()  # hide main window

    messagebox.showinfo(
        "CSV Format Info",
        "Please select a CSV file with exactly two columns:\n"
        " • Column 1: Fiber length [meters]\n"
        " • Column 2: Measured power [mW]\n\n"
        "Ensure your CSV uses meters and mW as units."
    )

    file_path = filedialog.askopenfilename(
        title="Select Fiber Attenuation CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    root.destroy()

    if not file_path:
        print("No file selected—exiting.")
        return

    # --- 2. Load data (ignore any headers; use first two columns) ---
    df = pd.read_csv(file_path, header=None)
    L = df.iloc[:, 0].values  # lengths in meters
    P = df.iloc[:, 1].values  # powers in mW

    # --- 3. Fit exponential model P(L) = P0 * exp(-alpha L) ---
    # Initial guess: P0 = max(P), alpha = 0.1
    popt, pcov = curve_fit(exponential_model, L, P, p0=(P.max(), 0.1))
    P0, alpha = popt
    perr = np.sqrt(np.diag(pcov))  # standard errors

    # 95% CI for parameters
    ci95 = 1.96 * perr
    P0_lo, P0_hi = P0 - ci95[0], P0 + ci95[0]
    alpha_lo, alpha_hi = alpha - ci95[1], alpha + ci95[1]

    # --- 4. Prepare fit curves + CI bands ---
    L_fit = np.linspace(L.min(), L.max(), 500)
    P_fit = exponential_model(L_fit, P0, alpha)
    P_lo  = exponential_model(L_fit, P0_lo, alpha_lo)
    P_hi  = exponential_model(L_fit, P0_hi, alpha_hi)

    # --- 5. Plot: Linear domain ---
    plt.figure()
    plt.scatter(L, P, label="Measured data")
    plt.plot(L_fit, P_fit, label="Best-fit",   linewidth=2)
    plt.fill_between(L_fit, P_lo, P_hi, alpha=0.3, label="95% CI")
    plt.xlabel("Fiber length (m)")
    plt.ylabel("Power (mW)")
    plt.title("Exponential Attenuation Fit (Linear Domain)")
    plt.legend()
    plt.grid(True)

    # --- 6. Plot: dB domain (10·log₁₀ of everything) ---
    P_db     = 10 * np.log10(P)
    P_fit_db = 10 * np.log10(P_fit)
    P_lo_db  = 10 * np.log10(P_lo)
    P_hi_db  = 10 * np.log10(P_hi)

    plt.figure()
    plt.scatter(L, P_db,     label="Data (dB)")
    plt.plot(L_fit, P_fit_db, label="Fit (dB)", linewidth=2)
    plt.fill_between(L_fit, P_lo_db, P_hi_db, alpha=0.3, label="95% CI")
    plt.xlabel("Fiber length (m)")
    plt.ylabel("Power (dB·mW)")
    plt.title("Exponential Attenuation Fit (dB Domain)")
    plt.legend()
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()
