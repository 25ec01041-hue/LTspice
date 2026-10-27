
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read LTspice CSV
df = pd.read_csv(r"D:\EDA_LTSPICE\Q3.csv")

# Gate-voltage steps in the LTspice file
vgs_values = [0.3, 0.6, 0.9, 1.5]

plt.figure(figsize=(8, 6))

for i, vgs in enumerate(vgs_values):

    # Each step has 1101 data rows, preceded by a step-information row
    start = 1 + i * 1102
    end = start + 1101

    data = df.iloc[start:end].copy()

    # Convert voltage and current to numeric values
    data["Vd"] = pd.to_numeric(data["Vd"], errors="coerce")
    data["Id(M1)"] = pd.to_numeric(data["Id(M1)"], errors="coerce")
    data = data.dropna(subset=["Vd", "Id(M1)"])

    Vd = data["Vd"].to_numpy()
    Id = data["Id(M1)"].to_numpy()

    # Sort by drain voltage
    order = np.argsort(Vd)
    Vd = Vd[order]
    Id = Id[order]

    # Average duplicate VDS points to avoid zero spacing in gradient
    curve = pd.DataFrame({"Vd": Vd, "Id": Id})
    curve = curve.groupby("Vd", as_index=False).mean()

    Vd = curve["Vd"].to_numpy()
    Id = curve["Id"].to_numpy()

    # Output conductance in siemens
    gds = np.gradient(Id, Vd)

    # Output resistance in ohms
    ro = np.divide(
        1.0, gds,
        out=np.full_like(gds, np.nan),
        where=gds > 1e-15
    )

    # Plot ID-VD curve
    plt.plot(Vd, Id * 1e3, label=f"VGS = {vgs} V")


    # Calculate gds using a local linear fit in saturation
    if vgs == 1.5:
        # Select a small interval in the saturation region
        mask = (Vd >= 0.9) & (Vd <= 1.1)

        # Fit ID = gds*VDS + intercept
        gds_fit, intercept = np.polyfit(Vd[mask], Id[mask], 1)

        # Output resistance
        ro = 1 / gds_fit

        print("\nFor VGS = 1.5 V:")
        print(f"gds = {gds_fit:.6e} S")
        print(f"ro = {ro / 1000:.6f} kOhm")

        # Use your actual device width
        W_um = 1.0
        print(f"ro normalized = {ro * W_um / 1000:.6f} kOhm.um")


plt.xlabel("VDS (V)")
plt.ylabel("ID (mA)")
plt.title("MOSFET Output Characteristics")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(r"D:\EDA_LTSPICE\Q3_output.png", dpi=350)
plt.show()
