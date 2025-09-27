import matplotlib.pyplot as plt
import seaborn as sns
import itertools

def plot(x, signals, labels=None, xlabel="Time", ylabel="Value", 
                    title=None, savepath=None, reference_signal=None, ax=None):
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

    # Prepare figure/axes
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4))
    else:
        fig = ax.figure

    # Style cycle for non-reference signals
    colors = ["dimgray", "gray", "lightgray"]
    linestyles = ["-", "-.", ":"]
    style_cycle = itertools.cycle([(c, ls) for c in colors for ls in linestyles])

    # Plot signals
    for i, y in enumerate(signals):
        lbl = labels[i] if labels and i < len(labels) else f"Signal {i+1}"

        if reference_signal is not None and (y is reference_signal or y is reference_signal.tolist()):
            # Reference -> fixed style
            color, ls = "black", "--"
        else:
            color, ls = next(style_cycle)

        ax.plot(x, y, label=lbl, color=color, linestyle=ls, linewidth=1.2)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, fontsize=11)
    ax.legend(frameon=False)
    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.7)
    sns.despine(ax=ax)

    plt.tight_layout()

    if save_image:  # only save if it's a standalone figure
        fig.savefig(savepath, format="pdf", bbox_inches="tight")
        print(f"✅ Figure saved to {savepath}")

    if show_image:
        plt.show()


def subplots(x, signals, labels=None, 
                     xlabels="Time", ylabels="Value", titles=None, 
                     savepath=None, reference_signal=None):
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
    fig, axes = plt.subplots(nrows=nrows, ncols=1, figsize=(7, 3*nrows), sharex=True)

    if nrows == 1:
        axes = [axes]



    for idx, (signals, ax) in enumerate(zip(signals, axes)):
        lbls = labels[idx] if labels and idx < len(labels) else None
        title = titles[idx] if titles and idx < len(titles) else None

        plot(
            x, 
            signals, 
            labels=lbls, 
            xlabel=((xlabels if xlabels is str else xlabels[0]) if idx == nrows - 1 else "") if nxlabels <= 1 else (xlabels[nxlabes-1 if idx >= nxlabels else idx]),  # only bottom gets xlabel
            ylabel=ylabels if nylabels == 1 else ylabels[nylabes-1 if idx >= nylabels else idx], 
            title=title, 
            reference_signal=reference_signal,
            ax=ax
        )

    plt.tight_layout()

    if savepath:
        fig.savefig(savepath, format="pdf", bbox_inches="tight")
        print(f"✅ Figure saved to {savepath}")

    plt.show()
