import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Load CSV data
df_11mv = pd.read_csv(r"Q2(1.1v).csv")
df_uaub = pd.read_csv(r"Q4(uaub).csv")
df_vsat = pd.read_csv(r"Q4(vsat).csv")

# Ensure smooth Vgs vector (accounting for export formatting)
vgs = np.linspace(0.0, 1.1, len(df_uaub))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Linear scale overlay
ax1.plot(vgs, df_11mv["Id(M1)"] * 1e3, "b-", label="Linear baseline (Vds = 1.1 V)")
ax1.plot(
    vgs,
    df_uaub["Id(M1)"] * 1e3,
    "orange",
    label="UA=UB=0 (Enormal OFF, Vds=1.1V)",
)
ax1.plot(
    vgs,
    df_vsat["Id(M1)"] * 1e3,
    "g-",
    label="VSAT x 100 (HighFieldSat OFF, Vds=1.1V)",
)
ax1.set_xlabel(r"$V_{GS}$ (V)")
ax1.set_ylabel(r"$I_D$ (mA)")
ax1.set_title(r"Transfer Characteristics ($I_D - V_{GS}$)")
ax1.grid(True)
ax1.legend()

# Semi-logarithmic scale overlay
ax2.semilogy(
    vgs,
    np.abs(df_11mv["Id(M1)"]),
    "b-",
    label="Linear baseline (Vds = 1.1 V)",
)
ax2.semilogy(
    vgs,
    np.abs(df_uaub["Id(M1)"]),
    "orange",
    label="UA=UB=0 (Enormal OFF, Vds=1.1V)",
)
ax2.semilogy(
    vgs,
    np.abs(df_vsat["Id(M1)"]),
    "g-",
    label="VSAT x 100 (HighFieldSat OFF, Vds=1.1V)",
)
ax2.set_xlabel(r"$V_{GS}$ (V)")
ax2.set_ylabel(r"$I_D$ (A) [Log Scale]")
ax2.set_title(r"Subthreshold & Overdrive Characteristics")
ax2.grid(True, which="both", ls=":")
ax2.legend()

plt.tight_layout()
plt.show()