
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def ltspice_csv(filepath, sweep_var):

    df_raw = pd.read_csv(filepath, encoding="cp1252")
    steps = {}
    current_label = None
    step_rows = []

    for _, row in df_raw.iterrows():
        val = str(row[sweep_var])

        if "Step Information:" in val:
            if current_label is not None and step_rows:
                steps[current_label] = pd.DataFrame(step_rows)
                step_rows = []

            current_label = val.split(":")[1].split("(")[0].strip()

        else:
            try:
                step_rows.append({
                    sweep_var: float(row[sweep_var]),
                    "Id": abs(float(row["Id(M1)"]))
                })
            except (ValueError, TypeError):
                continue

    if current_label is not None and step_rows:
        steps[current_label] = pd.DataFrame(step_rows)

    return steps



vg_file = "Q5(IDVGU0).csv"   # ID-VG sweep at VDS = 0.4 V
vd_file = "Q5(IDVDU0).csv"   # ID-VD sweep at VGS = 1.1 V

steps_vg = ltspice_csv(vg_file, "Vg")
steps_vd = ltspice_csv(vd_file, "Vd")




# (a) Linear ID-VGS
plt.figure(figsize=(7, 5))

for k, df in steps_vg.items():
    vgs = np.linspace(0.0, 1.1, len(df))
    plt.plot(vgs, df["Id"] * 1e3, label=k, lw=2)

plt.xlabel(r"$V_{GS}$ [V]", fontsize=11)
plt.ylabel(r"$I_D$ [mA]", fontsize=11)
plt.title(
    r"$I_D - V_{GS}$ Linear Characteristic ($V_{DS} = 0.4\,$V)",
    fontsize=11
)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(frameon=True, fontsize=9)
plt.tight_layout()
plt.savefig("U0_parametric_variation_IDVG.png", dpi=300)
plt.show()


# (b) Output ID-VDS Family
plt.figure(figsize=(7, 5))

for k, df in steps_vd.items():
    vds = np.linspace(0.0, 1.1, len(df))
    plt.plot(vds, df["Id"] * 1e3, label=k, lw=2)

plt.xlabel(r"$V_{DS}$ [V]", fontsize=11)
plt.ylabel(r"$I_D$ [mA]", fontsize=11)
plt.title(
    r"$I_D - V_{DS}$ Saturation Characteristic ($V_{GS} = 1.1\,$V)",
    fontsize=11
)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(frameon=True, fontsize=9)
plt.tight_layout()
plt.savefig("U0_parametric_variation_IDVD.png", dpi=300)
plt.show()
