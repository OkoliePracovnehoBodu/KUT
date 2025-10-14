# -*- coding: utf-8 -*-

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

###############################################################################

mpl.rcParams['figure.dpi'] = 120
mpl.rcParams['savefig.facecolor'] = 'w'

mpl.rcParams['font.size'] = 10

mpl.rcParams['font.family'] = 'serif'

###############################################################################

#######################################
mpl.rcParams['text.usetex'] = True

# mpl.rcParams['text.latex.unicode'] = True
mpl.rcParams['text.latex.preamble'] = r'\usepackage[T1]{fontenc} \usepackage{lmodern}'
# mpl.rcParams['text.latex.preamble'] = r'\usepackage[T1]{fontenc} \usepackage{txfonts}'

#######################################
# mpl.rcParams['text.usetex'] = False

# mpl.rcParams['font.family'] = 'lmsans10-regular'
# mpl.rcParams['mathtext.fontset'] = 'cm'


###############################################################################

mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['xtick.labelsize'] = mpl.rcParams['font.size']

mpl.rcParams['ytick.direction'] = 'out'
mpl.rcParams['ytick.labelsize'] = mpl.rcParams['font.size']

mpl.rcParams['axes.xmargin'] = 0.01
mpl.rcParams['axes.ymargin'] = 0.03

mpl.rcParams['axes.titlesize'] = mpl.rcParams['font.size']
mpl.rcParams['axes.labelsize'] = mpl.rcParams['font.size']
mpl.rcParams['legend.fontsize'] = mpl.rcParams['font.size']#'small'#
mpl.rcParams['legend.frameon'] = False
mpl.rcParams['legend.borderpad'] = 0.1
mpl.rcParams['legend.borderaxespad'] = 0.0
mpl.rcParams['legend.labelspacing'] = 0.2
mpl.rcParams['legend.numpoints'] = 1

###############################################################################

def fcnDefaultFigSize(figSizeTotalHeight,
                      fig_lrPadding,
                      fig_top,
                      fig_bottom,
                      fig_hspace,
                      figSizePlotWidth
                      ):

    figSizeLeftAdj = fig_lrPadding
    figSizeRightAdj = 1.0 - fig_lrPadding

    figSizeTotalWidth = figSizePlotWidth / (figSizeRightAdj - figSizeLeftAdj)


    return [figSizeTotalWidth/2.54,
            figSizeTotalHeight/2.54,
            fig_lrPadding,
            fig_hspace,
            fig_top,
            fig_bottom,
            ]

###############################################################################

def fcnDefaultLayoutAdj(fig, fig_lrPadding, fig_hspace, fig_top, fig_bottom):
    fig.tight_layout()

    fig.subplots_adjust(left=fig_lrPadding)
    fig.subplots_adjust(right=1-fig_lrPadding)

    fig.subplots_adjust(hspace=fig_hspace)
    fig.subplots_adjust(top=fig_top)
    fig.subplots_adjust(bottom=fig_bottom)

###############################################################################

def fcnDefaultAxisStyle(ax):
    ax.grid(which='major', color='#cccccc', alpha=1.0, linewidth=0.33, linestyle='-', dashes=[7,0])
    ax.grid(which='minor', color='#dddddd', alpha=1.0, linewidth=0.33, linestyle=':', dashes=[4,3])
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

###############################################################################

def fcnDefaultTwinAxisStyle(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)

###############################################################################














from matplotlib.ticker import (AutoMinorLocator,
                               MultipleLocator,
                               FormatStrFormatter,
                               LinearLocator,
                               )

import matplotlib.dates as mdates




###############################################################################



# -----------------------------------------------------------------------------
def fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels):

    fcnDefaultLayoutAdj(fig, figPlotParam[2], figPlotParam[3], figPlotParam[4], figPlotParam[5])

    for ax in fig.get_axes():

        fcnDefaultAxisStyle(ax)

        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.xaxis.set_minor_locator(AutoMinorLocator())

        ax.ticklabel_format(axis='y', useOffset=False)

        ax.set_xlabel(
            XYT_labels[0], 
            ha='left', 
            va='top',
            )

        ax.xaxis.set_label_coords(1.068, -0.068, transform=ax.transAxes)  

        ax.set_ylabel(
            XYT_labels[1], 
            ha='right', 
            va='bottom', 
            rotation=0,  
            )

        ax.yaxis.set_label_coords(-0.068, 1.068, transform=ax.transAxes)

        ax.set_title(
            XYT_labels[2], 
            ha='left', 
            va='bottom',
            x=0.0,
            y=1.068,
            transform=ax.transAxes
            )

        
        handles_ax, labels_ax = ax.get_legend_handles_labels()

        ax.legend(
            handles_ax, labels_ax, 
            ncol=1, 
            handlelength=0.8, 
            markerfirst=True, 
            loc=2, bbox_to_anchor=(1.01, 1.00)
        )









# -----------------------------------------------------------------------------
def fcn_setFigStyle_basicTimeSeries2(fig, figPlotParam, XYT_labels):

    fcnDefaultLayoutAdj(fig, figPlotParam[2], figPlotParam[3], figPlotParam[4], figPlotParam[5])

    for ax in fig.get_axes():

        fcnDefaultAxisStyle(ax)

        ax.yaxis.set_major_locator(MultipleLocator(1))

        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.xaxis.set_minor_locator(AutoMinorLocator())

        ax.ticklabel_format(axis='y', useOffset=False)

        ax.set_xlabel(
            XYT_labels[0], 
            ha='left', 
            va='top',
            )

        ax.xaxis.set_label_coords(1.068, -0.068, transform=ax.transAxes)  

        ax.set_ylabel(
            XYT_labels[1], 
            ha='right', 
            va='bottom', 
            rotation=0,  
            )

        ax.yaxis.set_label_coords(-0.068, 1.068, transform=ax.transAxes)

        ax.set_title(
            XYT_labels[2], 
            ha='left', 
            va='bottom',
            x=0.0,
            y=1.068,
            transform=ax.transAxes
            )

        
        handles_ax, labels_ax = ax.get_legend_handles_labels()

        ax.legend(
            handles_ax, labels_ax, 
            ncol=1, 
            handlelength=0.8, 
            markerfirst=True, 
            loc=2, bbox_to_anchor=(1.01, 1.00)
        )


