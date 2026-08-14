"""Animation frame sequences for \\animategraphics.

Produces  anim/flyby-NN.png, anim/potential-NN.png, anim/europa-NN.png
Each sequence loops seamlessly and its frame 0 stands alone as a static figure.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from astgstyle import *

OUT = "anim/"
os.makedirs(OUT, exist_ok=True)
NF = 32                      # frames per sequence
DPI = 96

DIVN = plt.get_cmap("RdBu_r")
NORM = Normalize(-75, 75)


def decl_color(d):
    return DIVN(NORM(d))


# ======================================================================
# A -- flyby traversal: orbital plane + declination track  (NEAR)
# ======================================================================
F = [f for f in FLYBYS if f["name"] == "NEAR"][0]
eps, rp = F["eps"], F["rp"]
eta = eta_of(eps)
numax = 0.80 * eta
nu_full = np.linspace(-numax, numax, 600)
r_full = hyperbola(nu_full, rp, eps)
x_full = r_full * np.cos(nu_full)
y_full = r_full * np.sin(nu_full)
d_full = declination_track(nu_full, F["din"], F["dout"], eps)

nu_dec = np.linspace(-eta * 0.999, eta * 0.999, 600)
d_dec = declination_track(nu_dec, F["din"], F["dout"], eps)

LIMA = 30.0

for k in range(NF):
    t = k / NF
    nu_now = -numax + 2 * numax * t
    r_now = hyperbola(nu_now, rp, eps)
    xn, yn = r_now * np.cos(nu_now), r_now * np.sin(nu_now)
    dn = declination_track(np.array([nu_now]), F["din"], F["dout"], eps)[0]

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.2, 3.9),
                                 gridspec_kw=dict(width_ratios=[1.0, 1.12],
                                                  wspace=0.30))
    # --- orbital plane
    ax.plot(x_full, y_full, color=MUTED, lw=1.3, zorder=3)
    trail = nu_full <= nu_now
    ax.plot(x_full[trail], y_full[trail], color=ACCENT, lw=2.6, zorder=4)
    ax.add_patch(Circle((0, 0), 6.371, fc=ACCENT2, ec=INK, lw=1.2, zorder=5))
    ax.plot(rp, 0, "x", ms=9, color=INK, mew=2.0, zorder=6)
    ax.text(rp + 2.0, 1.6, "perigee", fontsize=9, color=INK)
    ax.plot(xn, yn, "o", ms=13, color=decl_color(dn), mec=INK, mew=1.3,
            zorder=8)
    ax.set_xlim(-LIMA, LIMA); ax.set_ylim(-LIMA, LIMA)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor("#C3C9D2")
    ax.set_title("NEAR, 1998 -- orbital plane", fontsize=11)
    ax.text(-LIMA + 2, LIMA - 3.5, r"$\varepsilon=1.81$", fontsize=10,
            color=INK, va="top")

    # --- declination track
    tidy(bx)
    bx.plot(np.degrees(nu_dec), d_dec, color=MUTED, lw=1.5, zorder=3)
    tr2 = nu_dec <= nu_now
    bx.plot(np.degrees(nu_dec[tr2]), d_dec[tr2], color=ACCENT, lw=2.6, zorder=4)
    bx.axhline(0, color=INK, lw=1.0, alpha=0.6, zorder=2)
    bx.axhline(F["din"], color=ACCENT2, lw=1.0, ls=":", zorder=2)
    bx.axhline(F["dout"], color=ACCENT2, lw=1.0, ls=":", zorder=2)
    bx.text(-126, F["din"] + 3.0, r"$\delta_{\rm in}=-20.8^\circ$",
            fontsize=9.5, color=ACCENT2)
    bx.text(126, F["dout"] - 9.0, r"$\delta_{\rm out}=-72.0^\circ$",
            fontsize=9.5, color=ACCENT2, ha="right")
    bx.plot(np.degrees(nu_now), dn, "o", ms=12, color=decl_color(dn),
            mec=INK, mew=1.3, zorder=8)
    bx.set_xlabel(r"true anomaly $\nu$  (deg)")
    bx.set_ylabel(r"declination $\delta$  (deg)")
    bx.set_xlim(-132, 132); bx.set_ylim(-84, 8)
    bx.set_title(r"$\delta$ sampled asymmetrically about perigee", fontsize=11)
    bx.text(0.975, 0.06, rf"$\delta = {dn:+.1f}^\circ$",
            transform=bx.transAxes, ha="right", fontsize=12,
            fontweight="bold", color=INK,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=MUTED))

    fig.savefig(f"{OUT}flyby-{k}.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
print(f"flyby-0..{NF-1}.png")

# ======================================================================
# B -- growth of the l=1 deformation
# ======================================================================
n = 340
xg = np.linspace(-3, 3, n)
zg = np.linspace(-3, 3, n)
Xg, Zg = np.meshgrid(xg, zg)
Rg = np.hypot(Xg, Zg)
Rg = np.where(Rg < 0.62, np.nan, Rg)
COSg = Zg / Rg
LEV = np.linspace(-2.2, -0.34, 11)
AMAX = 0.42

for k in range(NF):
    t = k / NF
    A = AMAX * 0.5 * (1 - np.cos(2 * np.pi * t))
    phi = -(1.0 / Rg) * (1 + A * COSg / Rg)

    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    ax.pcolormesh(Xg, Zg, (A / AMAX) * COSg / Rg, cmap="RdBu_r",
                  vmin=-1.6, vmax=1.6, shading="auto", alpha=0.42,
                  zorder=0, rasterized=True)
    ax.contour(Xg, Zg, phi, levels=LEV, colors=[ACCENT], linewidths=1.3,
               linestyles="solid", zorder=3)
    ax.add_patch(Circle((0, 0), 0.40, color=ACCENT2, zorder=5))
    ax.annotate("", xy=(0, 2.62), xytext=(0, -2.62),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6), zorder=6)
    ax.text(0.18, 2.28, r"$\hat{\bf S}$", fontsize=14, color=INK, zorder=6)
    ax.text(-2.85, 2.45, "N", fontsize=12, color="#8C2D2D", fontweight="bold")
    ax.text(-2.85, -2.80, "S", fontsize=12, color="#1F4E79", fontweight="bold")
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor("#C3C9D2")
    ax.set_title(r"$\Phi=-\frac{GM}{r}\left[1+\frac{s_g}{r}\lambda_1\cos\theta\right]$",
                 fontsize=12, pad=10)
    fig.savefig(f"{OUT}potential-{k}.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
print(f"potential-0..{NF-1}.png")

# ======================================================================
# C -- NEAR (southern, asymmetric) vs Europa Clipper (northern, symmetric)
# ======================================================================
CASES = [
    dict(lab="NEAR  (1998)", eps=F["eps"], rp=F["rp"], din=F["din"],
         dout=F["dout"], dcos=F["dcos"], note=r"$\Delta V_p=+7.2$ mm s$^{-1}$"),
    dict(lab="Europa Clipper  (Dec 2026)", eps=EUROPA["eps"], rp=EUROPA["rp"],
         din=EUROPA["din"], dout=EUROPA["dout"], dcos=EUROPA["dcos"],
         note=r"predicted $+0.05$ mm s$^{-1}$"),
]
for c in CASES:
    c["eta"] = eta_of(c["eps"])
    c["numax"] = 0.80 * c["eta"]
    nu = np.linspace(-c["numax"], c["numax"], 600)
    c["nu"] = nu
    r = hyperbola(nu, c["rp"], c["eps"])
    c["x"], c["y"] = r * np.cos(nu), r * np.sin(nu)
    nud = np.linspace(-c["eta"] * 0.999, c["eta"] * 0.999, 600)
    c["nud"] = nud
    c["d"] = declination_track(nud, c["din"], c["dout"], c["eps"])

for k in range(NF):
    t = k / NF
    fig, axs = plt.subplots(1, 2, figsize=(9.4, 4.0), sharey=True,
                            gridspec_kw=dict(wspace=0.14))
    for ax, c in zip(axs, CASES):
        tidy(ax)
        nu_now = -c["eta"] * 0.999 + 2 * c["eta"] * 0.999 * t
        dn = declination_track(np.array([nu_now]), c["din"], c["dout"],
                               c["eps"])[0]
        ax.axhspan(0, 90, color=ACCENT2, alpha=0.09, zorder=0)
        ax.axhspan(-90, 0, color=ACCENT, alpha=0.09, zorder=0)
        ax.plot(np.degrees(c["nud"]), c["d"], color=MUTED, lw=1.5, zorder=3)
        tr = c["nud"] <= nu_now
        ax.plot(np.degrees(c["nud"][tr]), c["d"][tr], color=INK, lw=2.6,
                zorder=4)
        ax.axhline(0, color=INK, lw=1.1, zorder=2)
        ax.plot(np.degrees(nu_now), dn, "o", ms=13, color=decl_color(dn),
                mec=INK, mew=1.3, zorder=8)
        ax.set_xlabel(r"true anomaly $\nu$  (deg)")
        ax.set_xlim(-150, 150); ax.set_ylim(-84, 56)
        ax.set_title(c["lab"], fontsize=11.5)
        ax.text(0.03, 0.05,
                rf"$\Delta\cos\delta = {c['dcos']:+.4f}$" + "\n" + c["note"],
                transform=ax.transAxes, fontsize=10.5, va="bottom",
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=MUTED,
                          lw=0.8))
    axs[0].set_ylabel(r"declination $\delta$  (deg)")
    axs[0].text(144, 46, "north", fontsize=9.5, color=ACCENT2, ha="right")
    axs[0].text(144, -80, "south", fontsize=9.5, color=ACCENT, ha="right")
    fig.savefig(f"{OUT}europa-{k}.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
print(f"europa-0..{NF-1}.png")
