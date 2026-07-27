"""Render the single-domain step-heating figure used by the Mars essay.

The laboratory schedule follows the temperature sequence in the local Nakhla
dataset and assumes a representative five-minute hold at every step. The
single spherical domain uses the high-retentivity parameters reported by
Shuster & Weiss (2005):

    Ea = 117 kJ/mol
    ln(D0 / r^2) = 5.7, with D0 / r^2 in s^-1

For a sphere with an initially uniform argon concentration,

    F(Theta) = 1 - 6/pi^2 sum_n exp(-n^2 pi^2 Theta) / n^2

where Theta is the cumulative integral of D(t)/r^2 over time.
"""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/cold-mars-matplotlib")

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


R_GAS = 8.314462618
EA_J_PER_MOL = 117_000.0
LOG_D0_OVER_R2 = 5.7
STEP_SECONDS = 300.0
ROCK_AGE_MY = 1300.0
K40_HALF_LIFE_MY = 1248.0
SECONDS_PER_MY = 1e6 * 365.25 * 24 * 3600

TEMPERATURES_C = np.array(
    [
        250,
        275,
        300,
        325,
        350,
        375,
        400,
        425,
        450,
        475,
        500,
        525,
        550,
        562,
        575,
        587,
        600,
        612,
        625,
        650,
        675,
        700,
        750,
        800,
        850,
        900,
        1000,
        1100,
        1250,
    ],
    dtype=float,
)


def fractional_release(progress: np.ndarray, modes: int = 800) -> np.ndarray:
    """Exact spherical release, with its convergent short-time expansion."""
    progress = np.asarray(progress, dtype=float)
    safe = np.maximum(progress, 1e-300)
    short = 6.0 * np.sqrt(safe / np.pi) - 3.0 * progress
    flat = safe.reshape(-1)
    n = np.arange(1, modes + 1, dtype=float)
    long = 1.0 - np.sum(
        (6.0 / (np.pi**2 * n**2))[None, :]
        * np.exp(-flat[:, None] * np.pi**2 * n[None, :] ** 2),
        axis=1,
    )
    result = np.where(flat < 0.05, short.reshape(-1), long)
    return np.clip(result, 0.0, 1.0).reshape(progress.shape)


def laboratory_release() -> tuple[np.ndarray, np.ndarray]:
    rates = np.exp(
        LOG_D0_OVER_R2
        - EA_J_PER_MOL / (R_GAS * (TEMPERATURES_C + 273.15))
    )
    cumulative = fractional_release(np.cumsum(rates * STEP_SECONDS))
    incremental = np.diff(cumulative, prepend=0.0)
    return incremental, cumulative


def retained_radiogenic_argon(temperatures_c: np.ndarray) -> np.ndarray:
    """Fraction of continuously produced 40Ar retained after ROCK_AGE_MY."""
    temperatures_c = np.asarray(temperatures_c, dtype=float)
    production_times_my = np.linspace(0.0, ROCK_AGE_MY, 1601)
    decay_rate_per_my = np.log(2.0) / K40_HALF_LIFE_MY
    production_rate = decay_rate_per_my * np.exp(
        -decay_rate_per_my * production_times_my
    )
    total_produced = 1.0 - np.exp(-decay_rate_per_my * ROCK_AGE_MY)

    rates = np.exp(
        LOG_D0_OVER_R2
        - EA_J_PER_MOL
        / (R_GAS * (temperatures_c[:, None] + 273.15))
    )
    diffusion_time_s = (
        ROCK_AGE_MY - production_times_my[None, :]
    ) * SECONDS_PER_MY
    survival = 1.0 - fractional_release(rates * diffusion_time_s)
    retained = np.trapezoid(
        production_rate[None, :] * survival,
        production_times_my,
        axis=1,
    )
    return retained / total_produced


def style_axis(axis: mpl.axes.Axes) -> None:
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color("#777b77")
    axis.spines["bottom"].set_color("#777b77")
    axis.tick_params(colors="#555a56", labelsize=8, length=3)
    axis.grid(axis="y", color="#dedbd2", linewidth=0.8, alpha=0.8)
    axis.set_axisbelow(True)


def render(output: Path) -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.labelcolor": "#444946",
            "text.color": "#252927",
            "svg.fonttype": "none",
            "svg.hashsalt": "cold-mars-single-domain-step-heating",
        }
    )
    incremental, cumulative = laboratory_release()

    # The essay displays this figure in a narrow media column, so the four
    # stages run vertically. Each plot can then use the full column width.
    figure = plt.figure(figsize=(8.0, 11.0), facecolor="#f7f5ef")
    grid = figure.add_gridspec(
        4,
        1,
        height_ratios=(0.78, 1.0, 1.0, 1.0),
        left=0.12,
        right=0.965,
        bottom=0.075,
        top=0.88,
        hspace=0.65,
    )
    schedule_axis = figure.add_subplot(grid[0, 0])
    release_axis = figure.add_subplot(grid[1, 0])
    cumulative_axis = figure.add_subplot(grid[2, 0])
    inversion_axis = figure.add_subplot(grid[3, 0])

    figure.suptitle(
        "a simulated single-domain step-heating experiment",
        x=0.51,
        y=0.973,
        fontsize=19,
        fontfamily="DejaVu Serif",
        fontweight="normal",
    )
    figure.text(
        0.51,
        0.935,
        "5 min per step · spherical grains · "
        r"$E_a=117$ kJ mol$^{-1}$ · "
        r"$\ln[(D_0/r^2)/(1\ \mathrm{s}^{-1})]=5.7$",
        ha="center",
        color="#666b67",
        fontsize=9.5,
    )

    steps = np.arange(1, len(TEMPERATURES_C) + 1)
    schedule_axis.step(
        steps,
        TEMPERATURES_C,
        where="post",
        color="#df7650",
        linewidth=2.6,
    )
    schedule_axis.set_xlim(1, len(steps))
    schedule_axis.set_ylim(200, 1300)
    schedule_axis.set_ylabel("oven temperature (°C)")
    schedule_axis.set_xlabel("five-minute extraction step")
    schedule_axis.set_yticks([250, 500, 750, 1000, 1250])
    schedule_axis.set_title(
        "1 · hold the rock at successively hotter temperatures",
        loc="left",
        fontsize=10.5,
        pad=8,
    )
    style_axis(schedule_axis)

    bar_widths = np.diff(
        np.r_[
            TEMPERATURES_C[0] - 12.5,
            0.5 * (TEMPERATURES_C[:-1] + TEMPERATURES_C[1:]),
            TEMPERATURES_C[-1] + 75,
        ]
    )
    release_axis.bar(
        TEMPERATURES_C,
        incremental,
        width=bar_widths * 0.78,
        color="#6fa7c1",
        edgecolor="#4e8ba8",
        linewidth=0.6,
        align="center",
    )
    release_axis.set_xlim(225, 925)
    release_axis.set_ylim(0, max(incremental) * 1.25)
    release_axis.set_ylabel("fraction released\nin this step")
    release_axis.set_xlabel("oven temperature (°C)")
    release_axis.set_title(
        "2 · collect the argon released during each hold",
        loc="left",
        fontsize=10.5,
        pad=8,
    )
    style_axis(release_axis)

    visible = TEMPERATURES_C <= 900
    cumulative_axis.step(
        TEMPERATURES_C[visible],
        cumulative[visible],
        where="post",
        color="#2879a6",
        linewidth=2.8,
    )
    cumulative_axis.scatter(
        TEMPERATURES_C[visible],
        cumulative[visible],
        color="#2879a6",
        s=11,
        zorder=3,
    )
    cumulative_axis.set_xlim(225, 925)
    cumulative_axis.set_ylim(0, 1.03)
    cumulative_axis.set_ylabel("cumulative fraction released")
    cumulative_axis.set_xlabel("oven temperature (°C)")
    cumulative_axis.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    cumulative_axis.set_title(
        "3 · the measured cumulative curve is a staircase",
        loc="left",
        fontsize=10.5,
        pad=8,
    )
    style_axis(cumulative_axis)

    q_temperatures: dict[float, float] = {}
    for quantile in (0.1, 0.5, 0.9):
        index = int(np.flatnonzero(cumulative >= quantile)[0])
        q_temperatures[quantile] = TEMPERATURES_C[index]
        cumulative_axis.axhline(
            quantile,
            xmax=(TEMPERATURES_C[index] - 225) / 700,
            color="#aaa79f",
            linewidth=0.7,
            linestyle=(0, (3, 3)),
        )
    cumulative_axis.annotate(
        "one domain still empties over many steps:\n"
        f"10–90% release spans "
        f"{q_temperatures[0.1]:.0f}–{q_temperatures[0.9]:.0f}°C",
        xy=(q_temperatures[0.5], 0.5),
        xytext=(330, 0.78),
        arrowprops={"arrowstyle": "->", "color": "#747873", "lw": 1},
        fontsize=8.5,
        color="#555a56",
        ha="left",
        va="center",
    )

    candidate_temperatures = np.linspace(-80.0, 70.0, 240)
    retained = retained_radiogenic_argon(candidate_temperatures)
    target_temperature = 0.0
    measured_retention = float(
        retained_radiogenic_argon(np.array([target_temperature]))[0]
    )
    inversion_axis.plot(
        candidate_temperatures,
        retained,
        color="#765a7d",
        linewidth=3.0,
    )
    inversion_axis.axhline(
        measured_retention,
        color="#df7650",
        linewidth=2.0,
        linestyle=(0, (4, 3)),
    )
    inversion_axis.axvline(
        target_temperature,
        ymax=measured_retention,
        color="#df7650",
        linewidth=2.0,
        linestyle=(0, (4, 3)),
    )
    inversion_axis.scatter(
        [target_temperature],
        [measured_retention],
        s=58,
        color="#df7650",
        edgecolor="white",
        linewidth=1.2,
        zorder=5,
    )
    inversion_axis.set_xlim(-80, 70)
    inversion_axis.set_ylim(0, 1.03)
    inversion_axis.set_xlabel("candidate refrigerator temperature (°C)")
    inversion_axis.set_ylabel("fraction of radiogenic ⁴⁰Ar retained")
    inversion_axis.set_title(
        "4 · invert the natural argon",
        loc="left",
        fontsize=10.5,
        pad=8,
    )
    style_axis(inversion_axis)
    inversion_axis.text(
        -75,
        0.18,
        "known age\n"
        r"+ fitted $E_a,\ D_0/r^2$"
        "\n+ measured natural ⁴⁰Ar",
        fontsize=9,
        linespacing=1.5,
        bbox={
            "boxstyle": "round,pad=0.55",
            "facecolor": "#eee7f0",
            "edgecolor": "#bca9c2",
        },
    )
    inversion_axis.annotate(
        r"$T_\mathrm{fridge}$",
        xy=(target_temperature, measured_retention),
        xytext=(12, 0.78),
        arrowprops={"arrowstyle": "->", "color": "#b85e3d", "lw": 1.2},
        color="#b85e3d",
        fontsize=10,
    )

    figure.text(
        0.12,
        0.021,
        "Exact spherical diffusion solution. The staircase connects discrete measurements;\n"
        "diffusion within each five-minute hold is continuous.",
        color="#70746f",
        fontsize=7.8,
        linespacing=1.35,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        output,
        format="svg",
        facecolor=figure.get_facecolor(),
        metadata={"Date": None, "Creator": "simulate_single_domain_step_heating.py"},
    )
    plt.close(figure)
    output.write_text(
        "\n".join(line.rstrip() for line in output.read_text().splitlines()) + "\n"
    )


if __name__ == "__main__":
    render(
        Path(__file__).resolve().parents[1]
        / "step-heating-inversion.svg"
    )
