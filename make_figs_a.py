"""Static figures, part A: dataset timeline, ASTG potential, formula behaviour."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from astgstyle import *

OUT = "figs/"

# ======================================================================
# FIG 1 -- Timeline of Earth flybys with measured anomaly
# ======================================================================
fig, ax = plt.subplots(figsize=(9.6, 3.9))
tidy(ax)

for f in FLYBYS:
    if f["cls"] == "anomalous":
        c, m, s = ACCENT, "o", 105
    elif f["cls"] == "control":
        c, m, s = MUTED, "s", 70
    else:
        c, m, s = ACCENT2, "D", 70
    ax.errorbar(f["year"], f["dVp"],
                yerr=(f["sig"] if not np.isnan(f["sig"]) else 0),
                fmt=m, ms=np.sqrt(s), color=c, mec=INK, mew=0.8,
                ecolor=c, elinewidth=1.6, capsize=3.5, zorder=5)

# Europa Clipper prediction
ax.errorbar(EUROPA["year"], EUROPA["pred"], yerr=0.35, fmt="*", ms=20,
            color=GOLD, mec=INK, mew=0.9, ecolor=GOLD, elinewidth=1.6,
            capsize=3.5, zorder=6)

ax.axhline(0, color=INK, lw=1.0, ls="--", alpha=0.6, zorder=2)

labels = {
    "Galileo I":   (0.0,  0.80, "center"),
    "Galileo II":  (0.0, -1.25, "center"),
    "NEAR":        (1.4,  0.30, "center"),
    "Cassini":     (0.4, -1.25, "center"),
    "Rosetta I":   (-1.6, 0.55, "center"),
    "MESSENGER":   (0.9, -1.05, "center"),
    "Rosetta II":  (0.1,  0.80, "center"),
    "Rosetta III": (0.4, -1.05, "center"),
    "Juno":        (0.0,  0.80, "center"),
}
for f in FLYBYS:
    dx, dy, ha = labels[f["name"]]
    ax.annotate(f["name"], (f["year"] + dx, f["dVp"] + dy),
                ha=ha, fontsize=9, color=INK)
ax.annotate("Europa Clipper\n(Dec 2026)", (EUROPA["year"] - 0.4, EUROPA["pred"] + 0.85),
            ha="center", fontsize=9, color="#8A6410", fontweight="bold")

ax.set_xlabel("Year of Earth encounter")
ax.set_ylabel(r"$\Delta V_p$  (mm s$^{-1}$)")
ax.set_xlim(1988.5, 2029.5)
ax.set_ylim(-4.6, 9.4)

from matplotlib.lines import Line2D
leg = [Line2D([], [], marker="o", ls="", color=ACCENT, mec=INK, ms=9, label="Anomalous (4)"),
       Line2D([], [], marker="D", ls="", color=ACCENT2, mec=INK, ms=8, label="Null (4)"),
       Line2D([], [], marker="s", ls="", color=MUTED, mec=INK, ms=8, label="Drag control (1)"),
       Line2D([], [], marker="*", ls="", color=GOLD, mec=INK, ms=14, label="Pre-registered")]
ax.legend(handles=leg, loc="lower right", ncol=2, handletextpad=0.3,
          columnspacing=1.2, bbox_to_anchor=(1.005, -0.03))

fig.tight_layout()
fig.savefig(OUT + "fig_timeline.pdf")
plt.close(fig)
print("fig_timeline.pdf")

# ======================================================================
# FIG 2 -- ASTG potential structure
# ======================================================================
fig = plt.figure(figsize=(9.8, 3.9))
gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 1.05, 1.0], wspace=0.34)

# --- (a) Newtonian equipotentials
axa = fig.add_subplot(gs[0])
n = 420
x = np.linspace(-3, 3, n)
z = np.linspace(-3, 3, n)
X, Z = np.meshgrid(x, z)
R = np.hypot(X, Z)
R = np.where(R < 0.62, np.nan, R)
COS = Z / R

LEV = np.linspace(-2.2, -0.34, 11)
phiN = -1.0 / R
axa.contour(X, Z, phiN, levels=LEV, colors=[MUTED], linewidths=1.2,
            linestyles="solid")
axa.add_patch(Circle((0, 0), 0.40, color=ACCENT2, zorder=5))
axa.set_title(r"(a) Newtonian:  $\Phi=-GM/r$", fontsize=11.5)

# --- (b) ASTG l=1 equipotentials (amplitude exaggerated for display)
axb = fig.add_subplot(gs[1])
A = 0.42                                   # display amplitude
phiA = -(1.0 / R) * (1 + A * COS / R)
dipole = COS / R
axb.pcolormesh(X, Z, dipole, cmap="RdBu_r", vmin=-1.6, vmax=1.6,
               shading="auto", alpha=0.42, zorder=0, rasterized=True)
axb.contour(X, Z, phiA, levels=LEV, colors=[ACCENT], linewidths=1.2,
            linestyles="solid", zorder=3)
axb.add_patch(Circle((0, 0), 0.40, color=ACCENT2, zorder=5))
axb.annotate("", xy=(0, 2.62), xytext=(0, -2.62),
             arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6), zorder=6)
axb.text(0.18, 2.28, r"$\hat{\bf S}$", fontsize=13, color=INK, zorder=6)
axb.text(-2.8, 2.45, "N", fontsize=11, color="#8C2D2D", fontweight="bold")
axb.text(-2.8, -2.75, "S", fontsize=11, color="#1F4E79", fontweight="bold")
axb.set_title(r"(b) ASTG:  $+\,(s_g/r)\lambda_1\cos\theta$", fontsize=11.5)

for a in (axa, axb):
    a.set_xlim(-3, 3); a.set_ylim(-3, 3)
    a.set_aspect("equal")
    a.set_xticks([]); a.set_yticks([])
    for sp in a.spines.values():
        sp.set_edgecolor("#C3C9D2")

# --- (c) angular factor
axc = fig.add_subplot(gs[2])
tidy(axc)
th = np.linspace(0, np.pi, 300)
axc.plot(np.degrees(th), np.cos(th), color=ACCENT, lw=2.4,
         label=r"$P_1=\cos\theta$")
axc.plot(np.degrees(th), 0.5 * (3 * np.cos(th) ** 2 - 1), color=MUTED,
         lw=1.6, ls="--", label=r"$P_2$")
axc.axhline(0, color=INK, lw=0.9, alpha=0.5)
axc.axvline(90, color=INK, lw=0.9, ls=":", alpha=0.6)
axc.text(93, -1.05, "equator", fontsize=9, color=MUTED, ha="left", va="bottom")
axc.fill_between(np.degrees(th), np.cos(th), 0,
                 where=np.cos(th) > 0, color=ACCENT, alpha=0.13)
axc.set_xlabel(r"colatitude $\theta$  (deg)")
axc.set_ylabel(r"angular factor")
axc.set_xlim(0, 180); axc.set_ylim(-1.15, 1.15)
axc.set_xticks([0, 45, 90, 135, 180])
axc.legend(loc="lower left")
axc.set_title(r"(c) spin-induced multipoles", fontsize=11.5)

fig.savefig(OUT + "fig_potential.pdf", bbox_inches="tight")
plt.close(fig)
print("fig_potential.pdf")

# ======================================================================
# FIG 3 -- Behaviour of the flyby formula
# ======================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 3.7))

# (a) eccentricity suppression of the FRACTIONAL anomaly
tidy(ax1)
e = np.linspace(1.05, 6.2, 400)
RP0 = 7.0e6
for dc, cc, lab in [(0.6, ACCENT, r"$\Delta\cos\delta=0.6$"),
                    (0.3, GOLD,   r"$0.3$"),
                    (0.15, ACCENT2, r"$0.15$")]:
    ax1.plot(e, LAMBDA1 * S_G * dc / (RP0 * (1 + e)) * 1e6,
             color=cc, lw=2.3, label=lab)
for f in ANOM:
    ax1.axvline(f["eps"], color=MUTED, lw=0.8, ls=":", alpha=0.85)
    ax1.text(f["eps"] - 0.06, 0.04, f["short"], rotation=90, fontsize=8.5,
             color=MUTED, ha="right", va="bottom")
ax1.set_xlabel(r"eccentricity  $\varepsilon$")
ax1.set_ylabel(r"$\Delta V_p/V_p$   $(\times 10^{-6})$")
ax1.set_title(r"exact $1/(1+\varepsilon)$ suppression", fontsize=11.5)
ax1.set_xlim(1, 6.2); ax1.set_ylim(0, 1.5)
ax1.legend(loc="upper right", title=r"at $r_p=7$ Mm")

# (b) predictive surface over the geometry plane
DC = np.linspace(-0.22, 0.70, 300)
EE = np.linspace(1.05, 6.10, 300)
DCg, EEg = np.meshgrid(DC, EE)
Vpg = np.sqrt((1 + EEg) * GM_E / RP0)
Zg = LAMBDA1 * S_G * DCg / (RP0 * (1 + EEg)) * Vpg * 1e3   # mm/s

lv = np.linspace(-3, 9, 25)
cf = ax2.contourf(DCg, EEg, Zg, levels=lv, cmap="RdYlBu_r", alpha=0.92,
                  extend="both")
ax2.contour(DCg, EEg, Zg, levels=[0], colors=[INK], linewidths=1.6)
cb = plt.colorbar(cf, ax=ax2, pad=0.02, ticks=[-3, 0, 3, 6, 9])
cb.set_label(r"predicted $\Delta V_p$  (mm s$^{-1}$)", fontsize=10)
cb.outline.set_edgecolor(INK)

for f in ANOM:
    ax2.plot(f["dcos"], f["eps"], "o", ms=10, color="white", mec=INK,
             mew=1.6, zorder=6)
    off = (-11, -5) if f["short"] == "NEAR" else (9, -5)
    ha = "right" if f["short"] == "NEAR" else "left"
    ax2.annotate(f["short"], (f["dcos"], f["eps"]), textcoords="offset points",
                 xytext=off, ha=ha, fontsize=9.5, color=INK,
                 fontweight="bold", zorder=7)
ax2.set_xlabel(r"$\Delta\cos\delta \equiv \cos\delta_{\rm in}-\cos\delta_{\rm out}$")
ax2.set_ylabel(r"eccentricity  $\varepsilon$")
ax2.set_title(r"predictive surface at $r_p=7$ Mm", fontsize=11.5)
ax2.set_xlim(-0.22, 0.70); ax2.set_ylim(1.05, 6.10)
for sp in ax2.spines.values():
    sp.set_edgecolor(INK)

fig.tight_layout()
fig.savefig(OUT + "fig_formula.pdf")
plt.close(fig)
print("fig_formula.pdf")
