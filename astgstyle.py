"""Shared data + plotting style for the ASTG flyby presentation figures.

All numbers are transcribed from Papers I-IV (Nesvinga, Nyambuya & Jones).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ----------------------------------------------------------------------
# Palette
# ----------------------------------------------------------------------
INK      = "#1B2430"   # near-black text
MUTED    = "#6B7A8F"   # grey
ACCENT   = "#C4562F"   # burnt orange  (ASTG / model)
ACCENT2  = "#1F6F8B"   # deep teal     (observation)
GOLD     = "#D9A441"   # highlight
GREEN    = "#3F7D57"   # success / null
PURPLE   = "#6C4F8C"   # prediction
LIGHT    = "#EDEFF2"
PAPER    = "#FFFFFF"

rcParams.update({
    "figure.facecolor":  PAPER,
    "axes.facecolor":    PAPER,
    "savefig.facecolor": PAPER,
    "font.family":       "serif",
    "font.serif":        ["DejaVu Serif"],
    "mathtext.fontset":  "dejavuserif",
    "font.size":         11,
    "axes.labelsize":    12,
    "axes.titlesize":    12.5,
    "axes.edgecolor":    INK,
    "axes.labelcolor":   INK,
    "axes.linewidth":    1.0,
    "xtick.color":       INK,
    "ytick.color":       INK,
    "xtick.labelsize":   10,
    "ytick.labelsize":   10,
    "text.color":        INK,
    "legend.frameon":    False,
    "legend.fontsize":   10,
    "lines.linewidth":   1.8,
    "grid.color":        "#D5DAE1",
    "grid.linewidth":    0.7,
})


def tidy(ax, grid=True):
    """Remove top/right spines, add a soft grid."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if grid:
        ax.grid(True, alpha=0.55, zorder=0)
        ax.set_axisbelow(True)
    return ax


# ----------------------------------------------------------------------
# Physical constants (CODATA 2022, as used in the papers)
# ----------------------------------------------------------------------
GM_E  = 3.986004418e14      # m^3 s^-2
R_E   = 6.371e6             # m
C0    = 2.99792458e8        # m s^-1
S_G   = 2 * GM_E / C0**2    # 8.870e-3 m
OMEGA_E = 7.292115e-5       # rad s^-1
KAPPA_A = 2 * OMEGA_E * R_E / C0   # 3.099e-6

LAMBDA1     = 1.951e3       # global fit, Paper II
LAMBDA1_ERR = 0.288e3

# ----------------------------------------------------------------------
# Flyby dataset  (Paper II, Tables I & II;  Paper III, Table IV)
# name, year, h_p[km], V_inf[km/s], dVp[mm/s], sigma[mm/s],
# d_in[deg], d_out[deg], r_p[Mm], V_p[km/s], eps, Dcosd, class
# ----------------------------------------------------------------------
FLYBYS = [
    dict(name="Galileo I",   short="GLL-I",  year=1990.94, hp=960,  vinf=8.949,
         dVp=+2.560, sig=0.195, din=-12.52, dout=-34.15,
         rp=7.331, Vp=13.741, eps=2.473, dcos=+0.1486, cls="anomalous"),
    dict(name="Galileo II",  short="GLL-II", year=1992.94, hp=303,  vinf=8.877,
         dVp=-2.900, sig=0.700, din=-34.26, dout=-4.87,
         rp=6.674, Vp=14.080, eps=2.319, dcos=-0.1699, cls="control"),
    dict(name="NEAR",        short="NEAR",   year=1998.06, hp=539,  vinf=6.851,
         dVp=+7.210, sig=0.006, din=-20.76, dout=-71.96,
         rp=6.910, Vp=12.740, eps=1.814, dcos=+0.6254, cls="anomalous"),
    dict(name="Cassini",     short="CAS",    year=1999.63, hp=1171, vinf=16.010,
         dVp=-1.683, sig=0.842, din=-12.92, dout=-4.99,
         rp=7.542, Vp=19.027, eps=5.850, dcos=-0.0215, cls="anomalous"),
    dict(name="Rosetta I",   short="ROS-I",  year=2005.17, hp=1955, vinf=3.863,
         dVp=+0.660, sig=0.011, din=-2.81,  dout=-34.29,
         rp=8.326, Vp=10.520, eps=1.312, dcos=+0.1726, cls="anomalous"),
    dict(name="MESSENGER",   short="MSGR",   year=2005.58, hp=2347, vinf=4.056,
         dVp=+0.0071, sig=0.004, din=+31.44, dout=-31.92,
         rp=8.719, Vp=10.387, eps=1.360, dcos=+0.0044, cls="null"),
    dict(name="Rosetta II",  short="ROS-II", year=2007.87, hp=5295, vinf=np.nan,
         dVp=0.0, sig=np.nan, din=-10.84, dout=+18.50,
         rp=np.nan, Vp=np.nan, eps=np.nan, dcos=+0.034, cls="null"),
    dict(name="Rosetta III", short="ROS-III",year=2009.87, hp=2480, vinf=np.nan,
         dVp=0.0, sig=np.nan, din=+18.36, dout=+24.35,
         rp=np.nan, Vp=np.nan, eps=np.nan, dcos=+0.038, cls="null"),
    dict(name="Juno",        short="JUNO",   year=2013.77, hp=561,  vinf=9.831,
         dVp=0.0, sig=0.200, din=+14.17, dout=+39.50,
         rp=6.932, Vp=14.548, eps=2.681, dcos=+0.1980, cls="null"),
]

EUROPA = dict(name="Europa Clipper", short="EC", year=2026.92, hp=3234.6,
              vinf=11.558, din=+29.38, dout=+30.60,
              rp=9.606, Vp=14.717, eps=4.219, dcos=+0.0107,
              pred=+0.05, pi=(-4.00, +4.11), anderson=+0.30)

# Predictions vs observation (Paper II, Table III)
PREDICTIONS = [
    ("Galileo I",  +2.560, 0.195, +1.388, (-2.46,  5.23)),
    ("NEAR",       +7.210, 0.006, +7.092, ( 2.25, 11.93)),
    ("Cassini",    -1.683, 0.842, -0.137, (-5.38,  5.11)),
    ("Rosetta I",  +0.660, 0.011, +1.633, (-1.37,  4.63)),
    ("MESSENGER",  +0.0071,0.004, +0.038, (-2.83,  2.90)),
]

# Leave-one-out diagnostics (Paper II, Table IV)
LOO = [
    ("Galileo I", 0.030,  +1.00, 0.03, 1901),
    ("NEAR",      0.900,  +0.34, 1.03, 1659),
    ("Cassini",   0.0002, -0.94, 0.005, 1948),
    ("Rosetta I", 0.070,  -1.11, 0.09, 2039),
]

ANOM = [f for f in FLYBYS if f["cls"] == "anomalous"]


# ----------------------------------------------------------------------
# Orbit helpers
# ----------------------------------------------------------------------
def eta_of(eps):
    """Half-angle between the asymptotes (true anomaly at r -> infinity)."""
    return np.arccos(-1.0 / eps)


def orbit_elements(din_deg, dout_deg, eps):
    """Recover (inclination, argument of perigee) from the two asymptotic
    declinations, using velocity-direction declinations: the inbound velocity
    is antiparallel to the inbound position asymptote.

    sin(d_in)  = -sin(i) sin(w - eta)
    sin(d_out) =  sin(i) sin(w + eta)
    """
    eta = eta_of(eps)
    A = -np.sin(np.radians(din_deg))
    B = np.sin(np.radians(dout_deg))
    P = (A + B) / (2 * np.cos(eta))     # sin(i) sin(w)
    Q = (B - A) / (2 * np.sin(eta))     # sin(i) cos(w)
    sini = np.hypot(P, Q)
    w = np.arctan2(P, Q)
    sini = min(sini, 1.0)
    return sini, w, eta


def flight_path_angle(nu, eps):
    """Flight-path angle gamma, measured from the local horizontal."""
    return np.arctan2(eps * np.sin(nu), 1.0 + eps * np.cos(nu))


def declination_track(nu, din_deg, dout_deg, eps):
    """Declination of the VELOCITY direction along the trajectory.

    The velocity direction lies at (90 deg - gamma) from the radius vector in
    the direction of motion, so its argument of latitude is
        u_v = omega + nu + pi/2 - gamma(nu).
    At nu = +eta this reduces to omega + eta, and at nu = -eta to
    omega - eta + pi, reproducing the two asymptotic declinations exactly.
    """
    sini, w, _ = orbit_elements(din_deg, dout_deg, eps)
    gam = flight_path_angle(nu, eps)
    uv = w + nu + 0.5 * np.pi - gam
    return np.degrees(np.arcsin(np.clip(sini * np.sin(uv), -1, 1)))


def hyperbola(nu, rp_Mm, eps):
    """Polar radius (Mm) of the hyperbolic orbit at true anomaly nu."""
    return rp_Mm * (1 + eps) / (1 + eps * np.cos(nu))


def astg_dVp(dcos, rp_Mm, eps, Vp_kms, lam=LAMBDA1):
    """ASTG perigee anomaly in mm/s."""
    rp = rp_Mm * 1e6
    return lam * S_G / (rp * (1 + eps)) * dcos * Vp_kms * 1e6
