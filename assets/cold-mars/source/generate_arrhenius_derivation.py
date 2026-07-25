"""Render the compact Arrhenius diffusion derivation used by the Mars essay."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/cold-mars-matplotlib")

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, RegularPolygon


INK = "#252927"
MUTED = "#59605c"
LINE = "#d4d0c6"
BLUE = "#4f8ba7"
PALE_BLUE = "#dcecf0"
ORANGE = "#df7650"
PURPLE = "#765a7d"
PAPER = "#f7f5ef"


def panel(axis: mpl.axes.Axes, y: float, height: float) -> None:
    axis.add_patch(
        FancyBboxPatch(
            (0.035, y),
            0.93,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.025",
            transform=axis.transAxes,
            facecolor="white",
            edgecolor=LINE,
            linewidth=1.5,
        )
    )


def arrow(axis: mpl.axes.Axes, start: tuple[float, float], end: tuple[float, float]) -> None:
    axis.add_patch(
        FancyArrowPatch(
            start,
            end,
            transform=axis.transAxes,
            arrowstyle="-|>",
            mutation_scale=16,
            linewidth=1.8,
            color="#6a706c",
        )
    )


def text_box(
    axis: mpl.axes.Axes,
    center: tuple[float, float],
    width: float,
    height: float,
    equation: str,
    caption: str,
    facecolor: str,
    edgecolor: str,
) -> None:
    x, y = center
    axis.add_patch(
        FancyBboxPatch(
            (x - width / 2, y - height / 2),
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            transform=axis.transAxes,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=1.4,
        )
    )
    axis.text(
        x,
        y + 0.018,
        equation,
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=15,
        color=INK,
    )
    axis.text(
        x,
        y - 0.043,
        caption,
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=9.5,
        color=MUTED,
    )


def render(output: Path) -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "mathtext.fontset": "dejavuserif",
            "svg.fonttype": "none",
            "svg.hashsalt": "cold-mars-arrhenius-derivation",
            "text.color": INK,
        }
    )
    figure, axis = plt.subplots(figsize=(9.6, 7.6), facecolor=PAPER)
    figure.subplots_adjust(0, 0, 1, 1)
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.axis("off")

    panel(axis, 0.665, 0.285)
    panel(axis, 0.385, 0.225)
    panel(axis, 0.055, 0.275)

    # 1. A metastable cage and the activation barrier.
    axis.text(
        0.065,
        0.918,
        "1 · one activated hop",
        transform=axis.transAxes,
        fontsize=13,
        color=MUTED,
        va="center",
    )
    cage_centers = [(0.135, 0.785), (0.265, 0.785), (0.395, 0.785)]
    for center in cage_centers:
        axis.add_patch(
            RegularPolygon(
                center,
                numVertices=6,
                radius=0.074,
                orientation=np.pi / 6,
                transform=axis.transAxes,
                facecolor="#eff5f6",
                edgecolor="#7ca6b6",
                linewidth=2,
            )
        )
    axis.add_patch(
        Circle(
            cage_centers[0],
            0.022,
            transform=axis.transAxes,
            facecolor=ORANGE,
            edgecolor="#b85e3d",
            linewidth=1.7,
        )
    )
    axis.text(
        cage_centers[0][0],
        cage_centers[0][1],
        "Ar",
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=9.5,
        color="white",
    )
    axis.add_patch(
        Circle(
            cage_centers[1],
            0.022,
            transform=axis.transAxes,
            facecolor="white",
            edgecolor=PURPLE,
            linewidth=1.7,
            linestyle=(0, (3, 2)),
        )
    )
    arrow(axis, (0.165, 0.785), (0.234, 0.785))
    axis.plot(
        [0.199, 0.199],
        [0.747, 0.823],
        transform=axis.transAxes,
        color=PURPLE,
        linewidth=3,
        solid_capstyle="round",
    )
    axis.text(
        0.135,
        0.688,
        "stable cage",
        transform=axis.transAxes,
        ha="center",
        fontsize=9.5,
        color=MUTED,
    )
    axis.text(
        0.265,
        0.688,
        "neighboring cage",
        transform=axis.transAxes,
        ha="center",
        fontsize=9.5,
        color=MUTED,
    )
    axis.text(
        0.199,
        0.842,
        "bottleneck",
        transform=axis.transAxes,
        ha="center",
        fontsize=9.5,
        color=PURPLE,
    )

    # Energy along the same hop.
    x0, x1 = 0.51, 0.91
    y0, y1 = 0.705, 0.875
    axis.plot([x0, x1], [y0, y0], transform=axis.transAxes, color="#777c78", lw=1.4)
    axis.plot([x0, x0], [y0, y1], transform=axis.transAxes, color="#777c78", lw=1.4)
    u = np.linspace(0, 1, 240)
    energy = 0.12 + 0.62 * np.exp(-((u - 0.5) / 0.17) ** 2)
    energy -= 0.08 * np.exp(-((u - 0.08) / 0.13) ** 2)
    energy -= 0.08 * np.exp(-((u - 0.92) / 0.13) ** 2)
    xp = x0 + u * (x1 - x0)
    yp = y0 + energy * (y1 - y0)
    axis.plot(xp, yp, transform=axis.transAxes, color=PURPLE, lw=3)
    peak_index = int(np.argmax(energy))
    peak_x, peak_y = xp[peak_index], yp[peak_index]
    well_y = y0 + float(energy[12]) * (y1 - y0)
    axis.plot(
        [peak_x, peak_x],
        [well_y, peak_y],
        transform=axis.transAxes,
        color=ORANGE,
        lw=1.8,
        linestyle=(0, (4, 3)),
    )
    axis.text(
        peak_x + 0.025,
        (well_y + peak_y) / 2,
        r"activation energy  $E_a$",
        transform=axis.transAxes,
        fontsize=11,
        color="#b85e3d",
        va="center",
    )
    axis.text(
        0.71,
        0.678,
        "position along the hop",
        transform=axis.transAxes,
        ha="center",
        fontsize=9.5,
        color=MUTED,
    )
    axis.text(
        0.485,
        0.79,
        "energy",
        transform=axis.transAxes,
        ha="center",
        va="center",
        rotation=90,
        fontsize=9.5,
        color=MUTED,
    )

    # 2. Attempt frequency × Boltzmann fraction = successful hop rate.
    axis.text(
        0.065,
        0.574,
        "2 · thermal attempts",
        transform=axis.transAxes,
        fontsize=13,
        color=MUTED,
        va="center",
    )
    text_box(
        axis,
        (0.17, 0.475),
        0.20,
        0.105,
        r"$\nu_0$",
        "attempts per second",
        PALE_BLUE,
        "#9bbdcd",
    )
    text_box(
        axis,
        (0.50, 0.475),
        0.25,
        0.105,
        r"$\exp\!\left[-E_a/(R_gT)\right]$",
        "fraction reaching the bottleneck",
        "#f4e8e0",
        "#d8a78e",
    )
    text_box(
        axis,
        (0.83, 0.475),
        0.23,
        0.105,
        r"$\Gamma(T)$",
        "successful hops per second",
        "#eee7f0",
        "#bea7c5",
    )
    arrow(axis, (0.275, 0.475), (0.355, 0.475))
    axis.text(
        0.315,
        0.475,
        "×",
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=18,
        color=MUTED,
        bbox={"facecolor": PAPER, "edgecolor": "none", "pad": 1},
    )
    arrow(axis, (0.63, 0.475), (0.705, 0.475))
    axis.text(
        0.667,
        0.475,
        "=",
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=17,
        color=MUTED,
        bbox={"facecolor": PAPER, "edgecolor": "none", "pad": 1},
    )

    # 3. The hopping random walk defines diffusivity.
    axis.text(
        0.065,
        0.292,
        "3 · many unbiased hops",
        transform=axis.transAxes,
        fontsize=13,
        color=MUTED,
        va="center",
    )
    grid_x = np.linspace(0.085, 0.385, 7)
    grid_y = np.linspace(0.095, 0.235, 5)
    for x in grid_x:
        axis.plot([x, x], [grid_y[0], grid_y[-1]], transform=axis.transAxes, color="#d6dad7", lw=1)
    for y in grid_y:
        axis.plot([grid_x[0], grid_x[-1]], [y, y], transform=axis.transAxes, color="#d6dad7", lw=1)
    path = np.array(
        [
            [grid_x[0], grid_y[1]],
            [grid_x[1], grid_y[1]],
            [grid_x[1], grid_y[2]],
            [grid_x[2], grid_y[2]],
            [grid_x[3], grid_y[2]],
            [grid_x[3], grid_y[3]],
            [grid_x[4], grid_y[3]],
            [grid_x[4], grid_y[2]],
            [grid_x[5], grid_y[2]],
            [grid_x[5], grid_y[1]],
            [grid_x[6], grid_y[1]],
        ]
    )
    axis.plot(path[:, 0], path[:, 1], transform=axis.transAxes, color="#2e79a8", lw=3)
    axis.scatter(
        [path[0, 0], path[-1, 0]],
        [path[0, 1], path[-1, 1]],
        transform=axis.transAxes,
        s=55,
        c=[ORANGE, PURPLE],
        zorder=4,
    )
    axis.text(
        0.235,
        0.075,
        r"jump length $\ell$",
        transform=axis.transAxes,
        ha="center",
        fontsize=9.5,
        color=MUTED,
    )

    axis.text(
        0.48,
        0.225,
        r"$\left\langle |\Delta\mathbf{x}|^2 \right\rangle"
        r"=\Gamma(T)t\ell^2=6D(T)t$",
        transform=axis.transAxes,
        fontsize=14,
        color=INK,
        va="center",
    )
    axis.text(
        0.48,
        0.165,
        r"$D_0\equiv \ell^2\nu_0/6$",
        transform=axis.transAxes,
        fontsize=14,
        color=INK,
        va="center",
    )
    axis.add_patch(
        FancyBboxPatch(
            (0.465, 0.082),
            0.445,
            0.055,
            boxstyle="round,pad=0.012,rounding_size=0.014",
            transform=axis.transAxes,
            facecolor="#eee7f0",
            edgecolor="#bea7c5",
            linewidth=1.5,
        )
    )
    axis.text(
        0.687,
        0.109,
        r"$D(T)=D_0\exp\!\left[-E_a/(R_gT)\right]$",
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=15.5,
        color=PURPLE,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        output,
        format="svg",
        facecolor=figure.get_facecolor(),
        metadata={"Date": None, "Creator": "generate_arrhenius_derivation.py"},
    )
    plt.close(figure)
    output.write_text(
        "\n".join(line.rstrip() for line in output.read_text().splitlines()) + "\n"
    )


if __name__ == "__main__":
    render(Path(__file__).resolve().parents[1] / "arrhenius-diffusion.svg")
