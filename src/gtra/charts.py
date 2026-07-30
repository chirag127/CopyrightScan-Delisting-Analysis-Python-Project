"""Reusable chart helpers."""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.use("Agg")

PALETTE = sns.color_palette(
    [
        "#1d4e89",
        "#2e86ab",
        "#a23b72",
        "#f18f01",
        "#c73e1d",
        "#3b1f2b",
        "#44bba4",
        "#e94f37",
    ]
)
THEME = {"style": "whitegrid", "palette": PALETTE}

FIG_W = 10
FIG_H_BAR = 6
FIG_H_LINE = 5


def apply_theme() -> None:
    sns.set_theme(**THEME)
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlesize": 13,
            "axes.titleweight": "semibold",
            "figure.facecolor": "white",
        }
    )


def save(fig: plt.Figure, name: str, out: Path) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    path = out / name
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.close(fig)
    print(f"  saved: {path}")
    return path


def barh(series, title: str, xlabel: str, color_idx: int = 0) -> plt.Figure:
    apply_theme()
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H_BAR))
    series.sort_values().plot.barh(ax=ax, color=PALETTE[color_idx % len(PALETTE)])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.yaxis.label.set_visible(False)
    fig.tight_layout()
    return fig


def line(series, title: str, ylabel: str, color_idx: int = 1) -> plt.Figure:
    apply_theme()
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H_LINE))
    series.plot(ax=ax, marker="o", color=PALETTE[color_idx % len(PALETTE)], linewidth=2)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    return fig


def scatter(
    x, y, title: str, xlabel: str, ylabel: str, color_idx: int = 3
) -> plt.Figure:
    apply_theme()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y, alpha=0.3, s=10, color=PALETTE[color_idx % len(PALETTE)])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    return fig
