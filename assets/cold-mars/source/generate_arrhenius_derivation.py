"""Render the Arrhenius diffusion explainer used by the Mars essay."""

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
BLUE = "#4f93bc"
PALE_BLUE = "#e5f0f4"
ORANGE = "#df7650"
PALE_ORANGE = "#f5e8e0"
PURPLE = "#765a7d"
PALE_PURPLE = "#eee7f0"
PAPER = "#f7f5ef"


def rounded_panel(axis: mpl.axes.Axes, y: float, height: float) -> None:
    axis.add_patch(
        FancyBboxPatch(
            (0.025, y),
            0.95,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.024",
            transform=axis.transAxes,
            facecolor="white",
            edgecolor=LINE,
            linewidth=1.5,
        )
    )


def flow_arrow(
    axis: mpl.axes.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str = "#6a706c",
) -> None:
    axis.add_patch(
        FancyArrowPatch(
            start,
            end,
            transform=axis.transAxes,
            arrowstyle="-|>",
            mutation_scale=16,
            linewidth=1.8,
            color=color,
        )
    )


def equation_box(
    axis: mpl.axes.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    equation: str,
    caption: str,
    face: str,
    edge: str,
) -> None:
    x, y = xy
    axis.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.01,rounding_size=0.015",
            transform=axis.transAxes,
            facecolor=face,
            edgecolor=edge,
            linewidth=1.4,
        )
    )
    axis.text(
        x + width / 2,
        y + height * 0.61,
        equation,
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=14,
        color=INK,
    )
    axis.text(
        x + width / 2,
        y + height * 0.20,
        caption,
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=9.2,
        color=MUTED,
    )


def render(output: Path) -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "mathtext.fontset": "dejavuserif",
            "svg.fonttype": "none",
            "svg.hashsalt": "cold-mars-arrhenius-explainer-v2",
            "text.color": INK,
        }
    )
    # The figure is displayed in a narrow article column. A compact physical
    # canvas makes labels larger relative to the SVG viewBox without changing
    # the panel geometry or the asset's near-square aspect ratio.
    figure, axis = plt.subplots(figsize=(8.0, 7.833), facecolor=PAPER)
    figure.subplots_adjust(0, 0, 1, 1)
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.axis("off")

    rounded_panel(axis, 0.69, 0.275)
    rounded_panel(axis, 0.375, 0.275)
    rounded_panel(axis, 0.045, 0.285)

    # ------------------------------------------------------------------
    # 1. A repeatable hop through a solid framework.
    # ------------------------------------------------------------------
    axis.text(
        0.055,
        0.93,
        "1 · argon must squeeze through a bottleneck between cavities",
        transform=axis.transAxes,
        fontsize=13,
        color=MUTED,
        va="center",
    )
    cage_centers = [(0.13, 0.81), (0.265, 0.81), (0.40, 0.81)]
    for center in cage_centers:
        axis.add_patch(
            RegularPolygon(
                center,
                numVertices=6,
                radius=0.076,
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
            0.023,
            transform=axis.transAxes,
            facecolor=ORANGE,
            edgecolor="#b85e3d",
            linewidth=1.6,
        )
    )
    axis.text(
        cage_centers[0][0],
        cage_centers[0][1],
        "Ar",
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=9.2,
        color="white",
    )
    axis.add_patch(
        Circle(
            cage_centers[1],
            0.023,
            transform=axis.transAxes,
            facecolor="white",
            edgecolor=PURPLE,
            linewidth=1.7,
            linestyle=(0, (3, 2)),
        )
    )
    flow_arrow(axis, (0.16, 0.81), (0.234, 0.81))
    axis.plot(
        [0.198, 0.198],
        [0.77, 0.85],
        transform=axis.transAxes,
        color=PURPLE,
        linewidth=3,
        solid_capstyle="round",
    )
    axis.text(
        0.13,
        0.708,
        "stable cavity",
        transform=axis.transAxes,
        ha="center",
        fontsize=9.5,
        color=MUTED,
    )
    axis.text(
        0.265,
        0.708,
        "neighboring cavity",
        transform=axis.transAxes,
        ha="center",
        fontsize=9.5,
        color=MUTED,
    )
    axis.text(
        0.198,
        0.866,
        "narrow passage",
        transform=axis.transAxes,
        ha="center",
        fontsize=9.5,
        color=PURPLE,
    )

    # Potential energy along the same hop.
    x0, x1 = 0.51, 0.93
    y0, y1 = 0.72, 0.88
    axis.plot([x0, x1], [y0, y0], transform=axis.transAxes, color="#777c78", lw=1.3)
    axis.plot([x0, x0], [y0, y1], transform=axis.transAxes, color="#777c78", lw=1.3)
    u = np.linspace(0, 1, 260)
    energy = 0.13 + 0.68 * np.exp(-((u - 0.5) / 0.17) ** 2)
    energy -= 0.09 * np.exp(-((u - 0.06) / 0.14) ** 2)
    energy -= 0.09 * np.exp(-((u - 0.94) / 0.14) ** 2)
    xp = x0 + u * (x1 - x0)
    yp = y0 + energy * (y1 - y0)
    axis.plot(xp, yp, transform=axis.transAxes, color=PURPLE, lw=3)
    peak = int(np.argmax(energy))
    well = 14
    axis.plot(
        [xp[peak], xp[peak]],
        [yp[well], yp[peak]],
        transform=axis.transAxes,
        color=ORANGE,
        lw=2,
        linestyle=(0, (4, 3)),
    )
    axis.text(
        xp[peak] + 0.024,
        (yp[well] + yp[peak]) / 2,
        r"activation energy  $E_a$",
        transform=axis.transAxes,
        fontsize=11,
        color="#b85e3d",
        va="center",
    )
    axis.text(
        0.72,
        0.696,
        "position along the hop",
        transform=axis.transAxes,
        ha="center",
        fontsize=9.5,
        color=MUTED,
    )
    axis.text(
        0.486,
        0.805,
        "energy",
        transform=axis.transAxes,
        ha="center",
        va="center",
        rotation=90,
        fontsize=9.5,
        color=MUTED,
    )

    # ------------------------------------------------------------------
    # 2. Boltzmann weight of the activated configuration.
    # ------------------------------------------------------------------
    axis.text(
        0.055,
        0.615,
        "2 · warmer atoms clear the same barrier more often",
        transform=axis.transAxes,
        fontsize=13,
        color=MUTED,
        va="center",
    )
    plot_left, plot_right = 0.075, 0.535
    plot_bottom, plot_top = 0.405, 0.575
    axis.plot(
        [plot_left, plot_right],
        [plot_bottom, plot_bottom],
        transform=axis.transAxes,
        color="#777c78",
        lw=1.3,
    )
    axis.plot(
        [plot_left, plot_left],
        [plot_bottom, plot_top],
        transform=axis.transAxes,
        color="#777c78",
        lw=1.3,
    )
    e = np.linspace(0, 5.5, 320)
    theta_cold, theta_warm = 0.82, 1.52
    cold = np.exp(-e / theta_cold)
    warm = np.exp(-e / theta_warm)
    max_density = 1.0
    x = plot_left + e / e.max() * (plot_right - plot_left)
    y_cold = plot_bottom + cold / max_density * (plot_top - plot_bottom)
    y_warm = plot_bottom + warm / max_density * (plot_top - plot_bottom)
    axis.plot(x, y_cold, transform=axis.transAxes, color=BLUE, lw=2.8)
    axis.plot(x, y_warm, transform=axis.transAxes, color=ORANGE, lw=2.8)
    barrier_energy = 2.5
    barrier_x = plot_left + barrier_energy / e.max() * (plot_right - plot_left)
    axis.plot(
        [barrier_x, barrier_x],
        [plot_bottom, plot_top],
        transform=axis.transAxes,
        color=PURPLE,
        lw=2,
        linestyle=(0, (4, 3)),
    )
    barrier_index = int(np.argmin(np.abs(e - barrier_energy)))
    for value, color in (
        (y_cold[barrier_index], BLUE),
        (y_warm[barrier_index], ORANGE),
    ):
        axis.plot(
            [plot_left, barrier_x],
            [value, value],
            transform=axis.transAxes,
            color=color,
            lw=1.1,
            alpha=0.65,
            linestyle=(0, (3, 3)),
        )
        axis.scatter(
            [barrier_x],
            [value],
            transform=axis.transAxes,
            s=28,
            facecolor=color,
            edgecolor="white",
            linewidth=0.8,
            zorder=5,
        )
    axis.text(
        plot_left + 0.06,
        plot_top - 0.025,
        "cold",
        transform=axis.transAxes,
        color=BLUE,
        fontsize=10.5,
    )
    axis.text(
        plot_left + 0.16,
        plot_top - 0.055,
        "warm",
        transform=axis.transAxes,
        color="#bd5e39",
        fontsize=10.5,
    )
    axis.text(
        barrier_x + 0.008,
        plot_top - 0.005,
        r"$E_a$",
        transform=axis.transAxes,
        color=PURPLE,
        fontsize=11,
    )
    axis.text(
        0.305,
        0.388,
        "energy of a lattice configuration",
        transform=axis.transAxes,
        ha="center",
        fontsize=9.2,
        color=MUTED,
    )
    axis.text(
        0.055,
        0.49,
        "relative\nBoltzmann weight",
        transform=axis.transAxes,
        ha="center",
        va="center",
        rotation=90,
        fontsize=9.2,
        color=MUTED,
    )

    equation_box(
        axis,
        (0.60, 0.424),
        0.33,
        0.108,
        r"$\dfrac{w_T(E_a)}{w_T(0)}=\exp\!\left[-E_a/(R_gT)\right]$",
        "relative population at the bottleneck",
        PALE_ORANGE,
        "#d8a78e",
    )
    axis.text(
        0.765,
        0.575,
        r"$\dfrac{w_T(E)}{w_T(0)}=\exp\!\left[-E/(R_gT)\right]$",
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=11.3,
        color=INK,
    )

    # ------------------------------------------------------------------
    # 3. Successful hops become a diffusion coefficient.
    # ------------------------------------------------------------------
    axis.text(
        0.055,
        0.295,
        "3 · many unbiased hops become diffusion",
        transform=axis.transAxes,
        fontsize=13,
        color=MUTED,
        va="center",
    )
    equation_box(
        axis,
        (0.06, 0.19),
        0.16,
        0.075,
        r"$\nu_0$",
        "attempts / second",
        PALE_BLUE,
        "#9bbdcd",
    )
    axis.text(
        0.245,
        0.228,
        "×",
        transform=axis.transAxes,
        fontsize=18,
        color=MUTED,
        ha="center",
        va="center",
    )
    equation_box(
        axis,
        (0.27, 0.19),
        0.22,
        0.075,
        r"$e^{-E_a/(R_gT)}$",
        "successful fraction",
        PALE_ORANGE,
        "#d8a78e",
    )
    axis.text(
        0.515,
        0.228,
        "=",
        transform=axis.transAxes,
        fontsize=17,
        color=MUTED,
        ha="center",
        va="center",
    )
    equation_box(
        axis,
        (0.54, 0.19),
        0.16,
        0.075,
        r"$\Gamma(T)$",
        "hops / second",
        PALE_PURPLE,
        "#bea7c5",
    )
    flow_arrow(axis, (0.71, 0.228), (0.76, 0.228))

    # Small random walk.
    grid_x = np.linspace(0.77, 0.94, 5)
    grid_y = np.linspace(0.185, 0.265, 4)
    for gx in grid_x:
        axis.plot(
            [gx, gx],
            [grid_y[0], grid_y[-1]],
            transform=axis.transAxes,
            color="#d6dad7",
            lw=0.9,
        )
    for gy in grid_y:
        axis.plot(
            [grid_x[0], grid_x[-1]],
            [gy, gy],
            transform=axis.transAxes,
            color="#d6dad7",
            lw=0.9,
        )
    path = np.array(
        [
            [grid_x[0], grid_y[1]],
            [grid_x[1], grid_y[1]],
            [grid_x[1], grid_y[2]],
            [grid_x[2], grid_y[2]],
            [grid_x[2], grid_y[3]],
            [grid_x[3], grid_y[3]],
            [grid_x[3], grid_y[2]],
            [grid_x[4], grid_y[2]],
        ]
    )
    axis.plot(path[:, 0], path[:, 1], transform=axis.transAxes, color="#2e79a8", lw=2.6)
    axis.scatter(
        [path[0, 0], path[-1, 0]],
        [path[0, 1], path[-1, 1]],
        transform=axis.transAxes,
        s=38,
        c=[ORANGE, PURPLE],
        zorder=4,
    )

    axis.text(
        0.055,
        0.118,
        r"$\left\langle|\Delta\mathbf{x}|^2\right\rangle"
        r"=\Gamma(T)t\ell^2=6D(T)t$",
        transform=axis.transAxes,
        fontsize=13.3,
        color=INK,
        va="center",
    )
    axis.add_patch(
        FancyBboxPatch(
            (0.47, 0.075),
            0.465,
            0.072,
            boxstyle="round,pad=0.012,rounding_size=0.014",
            transform=axis.transAxes,
            facecolor=PALE_PURPLE,
            edgecolor="#bea7c5",
            linewidth=1.5,
        )
    )
    axis.text(
        0.702,
        0.120,
        r"$D(T)=D_0\exp\!\left[-E_a/(R_gT)\right]$",
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=14.5,
        color=PURPLE,
    )
    axis.text(
        0.702,
        0.091,
        r"$D_0=\ell^2\nu_0/6$",
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=10.8,
        color=MUTED,
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
