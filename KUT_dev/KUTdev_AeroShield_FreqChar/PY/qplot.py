import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import numpy as np
import pandas as pd

def set_paper_style(single_column: bool = True):
    """
    Configure Seaborn/Matplotlib for scientific paper figures.
    - single_column=True -> ~3.5 inch width
    - single_column=False -> ~7 inch width (double column)
    """
    sns.set_theme(style="whitegrid", palette="dark")  # grayscale-like palette
    
    if single_column:
        fig_width = 6.0
    else:
        fig_width = 3.0
    
    fig_height = fig_width * 0.3  # keep aspect ratio
    plt.rcParams.update({
        "figure.figsize": (fig_width, fig_height),
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.titlesize": 11,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "lines.linewidth": 0.5,
        "lines.markersize": 2.5,
        "axes.grid": True,
        "grid.linewidth": 0.25
    })

def plot(x, signals, labels=None, xlabel="Time", ylabel="Value", 
                    title=None, savepath=None, reference_signal=None, markers=None, scatter_signals=None, linewidth=1, ax=None, show_legend=True, show_plot=True):
    """
    Plot multiple signals in black & white with different line styles.
    Optionally highlight a reference signal (always black dashed).

    Parameters
    ----------
    x : array-like
        Shared x-axis values (e.g. time).
    signals : list of array-like
        Signals to plot.
    labels : list of str, optional
        Labels for each signal.
    xlabel, ylabel, title : str
        Axis labels and figure title.
    savepath : str, optional
        If provided (e.g. "figure.pdf"), saves the figure as PDF.
    reference_signal : array-like, optional
        If provided, plotted in black dashed line independent of other signals.
    ax : matplotlib.axes.Axes, optional
        Axis to plot into (for subplot use).
    """
    sns.set_theme(style="ticks", context="paper")
    
    show_image = ax is None
    save_image = savepath is not None and show_image

    isarraywithinarray = False

    if isinstance(x, list) and not isinstance(x[0], float | int):
        isarraywithinarray = True

    # Prepare figure/axes
    if ax is None:
        fig, ax = plt.subplots(dpi=300)
    else:
        fig = ax.figure

    # Style cycle for non-reference signals
    colors = ["dimgray", "red", "blue", "lightgray"]
    linestyles = ["-", "--", "-.", ":"]
    style_cycle = itertools.cycle([(c, ls) for ls in linestyles for c in colors])

    # Plot signals
    for i, y in enumerate(signals):
        lbl = labels[i] if labels and i < len(labels) else f"Signal {i+1}"

        if reference_signal is not None and (y is reference_signal or y is reference_signal.tolist()):
            # Reference -> fixed style
            color, ls = "black", "--"
        else:
            color, ls = next(style_cycle)
            marker = markers[i] if markers is not None and len(markers) > i else None
            ax.plot((x[0] if isarraywithinarray else x) if y is reference_signal else (x[i] if isarraywithinarray else x), y, label=lbl, color=color, linestyle=ls, linewidth=linewidth, marker=marker, markersize=2)

    if scatter_signals is not None:
        for i, scatters in enumerate(scatter_signals):
            nscatters = len(scatters)
            print(nscatters)
            x_scatter = scatters[0]
            y_scatter = scatters[1]
            label = scatters[2] if nscatters >= 3 else f"y{i}"
            color = scatters[3] if nscatters >= 4 else "red"
            size = scatters[4] if nscatters >= 5 else 10
            marker = scatters[5] if nscatters >= 6 else '.'
            ax.scatter(x_scatter, y_scatter, color=color, marker=marker, label=label, s=size)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, fontsize=11)
    if show_legend:
        ax.legend(frameon=False)
    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.7)
    sns.despine(ax=ax)

    plt.tight_layout()

    if save_image:  # only save if it's a standalone figure
        fig.savefig(savepath, format="pdf", bbox_inches="tight")
        print(f"✅ Figure saved to {savepath}")

    if show_image and show_plot:
        plt.show()
    else:
        plt.close(fig)


def subplots(x, signals, labels=None, 
                     xlabels="Time", ylabels="Value", titles=None, 
                     savepath=None, reference_signal=None, show_plot=True, show_legend=True):
    """
    Plot multiple vertically aligned subplots in B&W.
    Each subplot can contain one or more signals.

    Parameters
    ----------
    x : array-like
        Shared x-axis values.
    signals : list of list of signals
        Outer list = each subplot, inner list = signals in that subplot.
    labels : list of list of str, optional
        Labels for each subplot's signals.
    xlabel, ylabel : str
        Axis labels.
    titles : list of str, optional
        Titles for each subplot.
    savepath : str, optional
        Save figure as PDF if provided.
    reference_signal : array-like, optional
        Signal to highlight in all subplots (black dashed).
    """
    sns.set_theme(style="ticks", context="paper")

    nrows = len(signals)
    nylabels = 1 if ylabels is str else len(ylabels)
    nxlabels = 1 if xlabels is str else len(xlabels)
    fig, axes = plt.subplots(nrows=nrows, ncols=1, figsize=(3.5, 2 * nrows), sharex=True, dpi=300)

    if nrows == 1:
        axes = [axes]

    for idx, (signals, ax) in enumerate(zip(signals, axes)):
        lbls = labels[idx] if labels and idx < len(labels) else None
        title = titles[idx] if titles and idx < len(titles) else None

        plot(
            x, 
            signals, 
            labels=lbls, 
            xlabel=((xlabels if xlabels is str else xlabels[0]) if idx == nrows - 1 else "") if nxlabels <= 1 else (xlabels[nxlabels-1 if idx >= nxlabels else idx]),  # only bottom gets xlabel
            ylabel=ylabels if nylabels == 1 else ylabels[nylabels-1 if idx >= nylabels else idx], 
            title=title, 
            reference_signal=reference_signal,
            ax=ax,
            show_legend=show_legend,
            show_plot=show_plot
        )

    plt.tight_layout()

    if savepath:
        fig.savefig(savepath, format="pdf", bbox_inches="tight")
        print(f"✅ Figure saved to {savepath}")
    
    if show_plot:        
        plt.show()
    else:
        plt.close(fig)

def scatter(x, signals, labels=None, reference=None,
                    xlabel="Time", ylabel="Value", size=10, title=None, savepath=None):
    """
    Plot multiple signals as scatter (points only, no connecting lines),
    black & white with different markers.
    
    Parameters
    ----------
    x : array-like
        Shared x-axis values.
    signals : list of array-like
        Signals to scatter plot.
    labels : list of str, optional
        Labels for each signal.
    reference : array-like, optional
        A special reference signal (always plotted as black 'x').
    xlabel, ylabel, title : str
        Axis labels and figure title.
    savepath : str, optional
        If given, saves the figure as PDF.
    """
    sns.set_theme(style="ticks", context="paper")

    isarraywithinarray = False

    if isinstance(x, list) and not isinstance(x[0], float | int):
        isarraywithinarray = True

    # Define grayscale markers
    colors = ["black", "dimgray", "gray", "lightgray"]
    markers = [".", "o", "s", "D", "^", "v", "P", "x", "X"]
    style_cycle = itertools.cycle([(c, m) for m in markers for c in colors])

    fig, ax = plt.subplots(dpi=300)

    # Plot reference if provided
    if reference is not None:
        ax.scatter(x[0] if isarraywithinarray else x, reference, color="red", marker="x", label="Reference", s=np.ceil(size*0.5))

    for i, y in enumerate(signals):
        if y is reference:
            continue  # already plotted as reference
        color, marker = next(style_cycle)
        lbl = labels[i] if labels and i < len(labels) else f"Signal {i+1}"
        ax.scatter(x[i] if isarraywithinarray else x, y, color=color, marker=marker, label=lbl, s=size)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, fontsize=11)
    ax.legend(frameon=False)
    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.7)
    sns.despine(ax=ax)
    plt.tight_layout()

    if savepath:
        fig.savefig(savepath, format="pdf", bbox_inches="tight")
        print(f"✅ Saved scatter plot to {savepath}")

    plt.show()
