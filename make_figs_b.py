"""Static figures, part B: the global fit, predictions, diagnostics,
hemispheric structure, and the Europa Clipper pre-registered test."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.lines import Line2D
from astgstyle import *

OUT = "figs/"

# ======================================================================
# FIG 4 -- the global single-parameter fit
# ======================================================================
fig, ax = plt.subplots(figsize=(8.2, 4.6))
tidy(ax)

X, Y, YE, NM = [], [], [], []
for f in ANOM:
    rp = f["rp"] * 1e6
    X.append(S_G * f["dcos"] / (rp * (1 + f["eps"])))
    Y.append(f["dVp"] * 1e-3 / (f["Vp"] * 1e3))
    YE.append(f["sig"] * 1e-3 / (f["Vp"] * 1e3))
    NM.append(f["short"])
X, Y, YE = np.array(X), np.array(Y), np.array(YE)

SX, SY = 1e10, 1e7                       # display scalings
xs = np.linspace(-0.25e-10, 3.15e-10, 100)
lo = (LAMBDA1 - LAMBDA1_ERR) * xs
hi = (LAMBDA1 + LAMBDA1_ERR) * xs
ax.fill_between(xs * SX, lo * SY, hi * SY, color=ACCENT, alpha=0.18,
                zorder=2, label=r"$\pm1\sigma$ on $\hat\lambda_1$")
ax.plot(xs * SX, LAMBDA1 * xs * SY, color=ACCENT, lw=2.5, zorder=3,
        label=r"$\hat\lambda_1=1951$, no intercept")

ax.errorbar(X * SX, Y * SY, yerr=YE * SY, fmt="o", ms=10, color=ACCENT2,
            mec=INK, mew=1.0, ecolor=INK, elinewidth=1.4, capsize=4,
            zorder=6, label="Anomalous flybys")
for xi, yi, nm in zip(X, Y, NM):
    dx, dy = (-13, 7) if nm == "NEAR" else (13, -4)
    ha = "right" if nm == "NEAR" else "left"
    ax.annotate(nm, (xi * SX, yi * SY), textcoords="offset points",
                xytext=(dx, dy), ha=ha, fontsize=10.5, fontweight="bold",
                color=INK, zorder=7)

ax.axhline(0, color=INK, lw=0.9, alpha=0.55)
ax.axvline(0, color=INK, lw=0.9, alpha=0.55)
ax.set_xlabel(r"$X \equiv s_g\,\Delta\cos\delta\,/\,[\,r_p(1+\varepsilon)\,]$"
              r"   $(\times10^{-10})$")
ax.set_ylabel(r"$Y \equiv \Delta V_p/V_p$   $(\times10^{-7})$")

ax.text(0.035, 0.955,
        "\n".join([r"$\hat\lambda_1 = (1.951\pm0.288)\times10^{3}$",
                   r"$R^2 = 0.904$",
                   r"$t = 6.77$,   $p = 0.0066$",
                   r"$n=4$,  one free parameter"]),
        transform=ax.transAxes, va="top", ha="left", fontsize=11.5,
        bbox=dict(boxstyle="round,pad=0.55", fc=LIGHT, ec=MUTED, lw=0.9))
ax.legend(loc="lower right", fontsize=10)
ax.set_xlim(-0.25, 3.15)
ax.set_ylim(-1.5, 6.6)

fig.tight_layout()
fig.savefig(OUT + "fig_fit.pdf")
plt.close(fig)
print("fig_fit.pdf")

# ======================================================================
# FIG 5 -- predictions vs observations
# ======================================================================
fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.0, 4.2),
                               gridspec_kw=dict(width_ratios=[1.35, 1.0],
                                                wspace=0.30))
tidy(axL)
names = [p[0] for p in PREDICTIONS]
obs = np.array([p[1] for p in PREDICTIONS])
sig = np.array([p[2] for p in PREDICTIONS])
pred = np.array([p[3] for p in PREDICTIONS])
yy = np.arange(len(names))[::-1]

w = 0.34
for i, y in enumerate(yy):
    axL.barh(y + w / 2, obs[i], height=w, color=ACCENT2, ec=INK, lw=0.8,
             zorder=4)
    axL.barh(y - w / 2, pred[i], height=w, color=ACCENT, ec=INK, lw=0.8,
             zorder=4)
    axL.errorbar(obs[i], y + w / 2, xerr=max(sig[i], 0.02), fmt="none",
                 ecolor=INK, elinewidth=1.2, capsize=3, zorder=6)

axL.axvline(0, color=INK, lw=1.0, alpha=0.7, zorder=5)
axL.set_yticks(yy)
axL.set_yticklabels(names, fontsize=11)
axL.set_xlabel(r"$\Delta V_p$  (mm s$^{-1}$)")
axL.set_title("Single global $\\lambda_1$, all geometry-driven", fontsize=11.5)
axL.legend(handles=[Line2D([], [], color=ACCENT2, lw=8, label="Observed"),
                    Line2D([], [], color=ACCENT, lw=8, label="ASTG predicted")],
           loc="lower right", fontsize=10)
axL.set_xlim(-3.0, 8.4)

# right: 1:1 agreement
tidy(axR)
lim = [-3.2, 8.4]
axR.plot(lim, lim, color=MUTED, lw=1.4, ls="--", zorder=2, label="1:1")
axR.plot(pred, obs, "o", ms=11, color=ACCENT, mec=INK, mew=1.1, zorder=6)
for nm, p_, o_ in zip(names, pred, obs):
    dx, dy = (10, -12) if nm == "NEAR" else (10, 6)
    axR.annotate(nm, (p_, o_), textcoords="offset points", xytext=(dx, dy),
                 fontsize=9.5, color=INK)
axR.set_xlim(lim); axR.set_ylim(lim)
axR.set_aspect("equal")
axR.set_xlabel(r"predicted $\Delta V_p$  (mm s$^{-1}$)")
axR.set_ylabel(r"observed $\Delta V_p$  (mm s$^{-1}$)")
axR.set_title("NEAR: 1.8\\% error", fontsize=11.5)
axR.axhline(0, color=INK, lw=0.8, alpha=0.45)
axR.axvline(0, color=INK, lw=0.8, alpha=0.45)
axR.legend(loc="upper left", fontsize=10)

fig.savefig(OUT + "fig_predictions.pdf", bbox_inches="tight")
plt.close(fig)
print("fig_predictions.pdf")

# ======================================================================
# FIG 6 -- robustness diagnostics panel
# ======================================================================
fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.6))
nm3 = [l[0] for l in LOO]
h3 = np.array([l[1] for l in LOO])
sr3 = np.array([l[2] for l in LOO])
lam3 = np.array([l[4] for l in LOO])
xpos = np.arange(4)

a = axes[0]; tidy(a)
a.bar(xpos, h3, color=ACCENT2, ec=INK, lw=0.8, width=0.6, zorder=4)
a.set_xticks(xpos); a.set_xticklabels(nm3, rotation=32, ha="right", fontsize=9)
a.set_ylabel(r"leverage $h_i$")
a.set_title("(a) leverage", fontsize=11)
a.set_ylim(0, 1.02)

a = axes[1]; tidy(a)
a.axhspan(-2, 2, color=GREEN, alpha=0.12, zorder=1)
a.bar(xpos, sr3, color=ACCENT, ec=INK, lw=0.8, width=0.6, zorder=4)
a.axhline(0, color=INK, lw=1.0, zorder=5)
a.set_xticks(xpos); a.set_xticklabels(nm3, rotation=32, ha="right", fontsize=9)
a.set_ylabel("standardized residual")
a.set_title(r"(b) all residuals $<2\sigma$", fontsize=11)
a.set_ylim(-2.2, 2.2)

a = axes[2]; tidy(a)
a.axhspan(LAMBDA1 - LAMBDA1_ERR, LAMBDA1 + LAMBDA1_ERR, color=ACCENT,
          alpha=0.16, zorder=1, label=r"$\pm1\sigma$")
a.axhline(LAMBDA1, color=ACCENT, lw=2.0, zorder=3, label="full sample")
a.plot(xpos, lam3, "o", ms=10, color=GOLD, mec=INK, mew=1.0, zorder=6,
       label="leave-one-out")
a.set_xticks(xpos); a.set_xticklabels(nm3, rotation=32, ha="right", fontsize=9)
a.set_ylabel(r"$\hat\lambda_1$")
a.set_title("(c) stable to within 1.2$\\times$", fontsize=11)
a.set_ylim(1450, 2350)
a.legend(fontsize=8.5, loc="lower left")

fig.tight_layout()
fig.savefig(OUT + "fig_diagnostics.pdf")
plt.close(fig)
print("fig_diagnostics.pdf")

# ======================================================================
# FIG 7 -- hemispheric structure
# ======================================================================
fig, (axA, axB) = plt.subplots(1, 2, figsize=(10.2, 4.5),
                               gridspec_kw=dict(width_ratios=[1.15, 1.0],
                                                wspace=0.28))
tidy(axA)
axA.axhspan(-90, 0, xmin=0, xmax=0.5, color=ACCENT, alpha=0.10, zorder=0)
axA.axhspan(0, 90, xmin=0.5, xmax=1, color=ACCENT2, alpha=0.10, zorder=0)
axA.axhline(0, color=INK, lw=1.1, zorder=3)
axA.axvline(0, color=INK, lw=1.1, zorder=3)

OFFS = {"Galileo I": (10, 4), "Galileo II": (-10, 5), "NEAR": (10, 4),
        "Cassini": (10, 4), "Rosetta I": (10, -13), "MESSENGER": (10, 4),
        "Rosetta II": (-11, 4), "Rosetta III": (11, -12), "Juno": (-11, 6)}
for f in FLYBYS:
    if f["cls"] == "anomalous":
        c, m, s = ACCENT, "o", 11
    elif f["cls"] == "control":
        c, m, s = MUTED, "s", 9
    else:
        c, m, s = ACCENT2, "D", 9
    axA.plot(f["din"], f["dout"], m, ms=s, color=c, mec=INK, mew=1.0, zorder=6)
    dx, dy = OFFS[f["name"]]
    axA.annotate(f["short"], (f["din"], f["dout"]), textcoords="offset points",
                 xytext=(dx, dy), ha="right" if dx < 0 else "left",
                 fontsize=9, color=INK, zorder=7)

axA.plot(EUROPA["din"], EUROPA["dout"], "*", ms=22, color=GOLD, mec=INK,
         mew=1.1, zorder=8)
axA.annotate("Europa Clipper", (EUROPA["din"], EUROPA["dout"]),
             textcoords="offset points", xytext=(13, 9), ha="left",
             fontsize=9.5, color="#8A6410", fontweight="bold", zorder=8)

axA.text(-88, -86, "all-southern", fontsize=10.5, color=ACCENT,
         fontweight="bold")
axA.text(74, 80, "all-northern", fontsize=10.5, color=ACCENT2,
         fontweight="bold", ha="right")
axA.set_xlabel(r"$\delta_{\rm in}$  (deg)")
axA.set_ylabel(r"$\delta_{\rm out}$  (deg)")
axA.set_xlim(-92, 78); axA.set_ylim(-95, 92)
axA.set_title("Every anomalous encounter is all-southern", fontsize=11.5)

# --- right: declination span of each encounter
tidy(axB, grid=False)
axB.axvspan(0, 90, color=ACCENT2, alpha=0.09, zorder=0)
axB.axvspan(-90, 0, color=ACCENT, alpha=0.09, zorder=0)
axB.axvline(0, color=INK, lw=1.2, zorder=3)

order = ["Galileo I", "NEAR", "Cassini", "Rosetta I",
         "MESSENGER", "Rosetta II", "Rosetta III", "Juno"]
byname = {f["name"]: f for f in FLYBYS}
ypos = np.arange(len(order))[::-1]
for y, nm in zip(ypos, order):
    f = byname[nm]
    c = ACCENT if f["cls"] == "anomalous" else ACCENT2
    axB.plot([f["din"], f["dout"]], [y, y], color=c, lw=2.6, alpha=0.85,
             zorder=4, solid_capstyle="round")
    axB.plot(f["din"], y, "o", ms=7, color="white", mec=c, mew=1.8, zorder=6)
    axB.plot(f["dout"], y, "o", ms=8, color=c, mec=INK, mew=0.9, zorder=6)

yE = -1
axB.plot([EUROPA["din"], EUROPA["dout"]], [yE, yE], color=GOLD, lw=3.0,
         zorder=4, solid_capstyle="round")
axB.plot(EUROPA["din"], yE, "o", ms=7, color="white", mec=GOLD, mew=1.8,
         zorder=6)
axB.plot(EUROPA["dout"], yE, "*", ms=16, color=GOLD, mec=INK, mew=0.9,
         zorder=6)

axB.set_yticks(list(ypos) + [yE])
axB.set_yticklabels([byname[n]["short"] for n in order] + ["EUROPA CLIPPER"],
                    fontsize=9)
for lab, nm in zip(axB.get_yticklabels(), order + ["EC"]):
    if nm in byname and byname[nm]["cls"] == "anomalous":
        lab.set_color(ACCENT); lab.set_fontweight("bold")
axB.get_yticklabels()[-1].set_color("#8A6410")
axB.get_yticklabels()[-1].set_fontweight("bold")

axB.set_xlabel(r"declination $\delta$  (deg)")
axB.set_xlim(-90, 60); axB.set_ylim(-1.9, 8.0)
axB.text(-86, 7.6, "south", fontsize=9.5, color=ACCENT)
axB.text(56, 7.6, "north", fontsize=9.5, color=ACCENT2, ha="right")
axB.set_title(r"span from $\delta_{\rm in}$ (open) to $\delta_{\rm out}$ (filled)",
              fontsize=11.5)
axB.spines["left"].set_visible(False)
axB.tick_params(axis="y", length=0)

fig.savefig(OUT + "fig_hemisphere.pdf", bbox_inches="tight")
plt.close(fig)
print("fig_hemisphere.pdf")

# ======================================================================
# FIG 8 -- Europa Clipper pre-registered prediction
# ======================================================================
fig, (axP, axQ) = plt.subplots(1, 2, figsize=(10.2, 4.2),
                               gridspec_kw=dict(width_ratios=[1.0, 1.15],
                                                wspace=0.30))
tidy(axP)
mods = ["ASTG\n(this work)", "Anderson\n(1998 empirical)"]
vals = [EUROPA["pred"], EUROPA["anderson"]]
cols = [ACCENT, MUTED]
axP.bar(mods, vals, color=cols, ec=INK, lw=1.0, width=0.5, zorder=4)
axP.errorbar(0, EUROPA["pred"],
             yerr=[[EUROPA["pred"] - EUROPA["pi"][0]],
                   [EUROPA["pi"][1] - EUROPA["pred"]]],
             fmt="none", ecolor=INK, elinewidth=1.6, capsize=6, zorder=6)
axP.axhline(0, color=INK, lw=1.0)
axP.set_ylabel(r"predicted $\Delta V_p$  (mm s$^{-1}$)")
axP.set_ylim(-4.8, 4.9)
axP.set_title("Pre-registered, parameter-free", fontsize=11.5)
axP.annotate(r"$+0.05$", (0, EUROPA["pred"]), textcoords="offset points",
             xytext=(0, 12), ha="center", fontsize=11, fontweight="bold",
             color=ACCENT)
axP.annotate(r"$+0.30$", (1, EUROPA["anderson"]), textcoords="offset points",
             xytext=(0, 12), ha="center", fontsize=11, color=INK)
axP.text(0.02, 0.03, "95\\% prediction interval shown",
         transform=axP.transAxes, fontsize=9, color=MUTED)

# geometry comparison
tidy(axQ)
comp = [("NEAR", 0.6254, ACCENT), ("Galileo I", 0.1486, ACCENT),
        ("Rosetta I", 0.1726, ACCENT), ("Juno", 0.1980, ACCENT2),
        ("MESSENGER", 0.0044, ACCENT2), ("Europa Clipper", 0.0107, GOLD)]
nmc = [c[0] for c in comp]
vc = [c[1] for c in comp]
cc = [c[2] for c in comp]
yy = np.arange(len(nmc))[::-1]
axQ.barh(yy, vc, color=cc, ec=INK, lw=0.9, height=0.58, zorder=4)
axQ.set_yticks(yy); axQ.set_yticklabels(nmc, fontsize=10.5)
axQ.set_xlabel(r"$|\Delta\cos\delta|$")
axQ.set_title("Near-equatorial symmetry, like MESSENGER", fontsize=11.5)
for y, v in zip(yy, vc):
    axQ.text(v + 0.012, y, f"{v:.4f}", va="center", fontsize=9.5, color=INK)
axQ.set_xlim(0, 0.76)

fig.savefig(OUT + "fig_europa.pdf", bbox_inches="tight")
plt.close(fig)
print("fig_europa.pdf")
