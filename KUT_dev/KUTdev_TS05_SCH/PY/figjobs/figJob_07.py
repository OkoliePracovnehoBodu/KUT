# -*- coding: utf-8 -*-

import numpy as np

# Pomocne moduly a funkcie ku kresleniu obrazkov
import sys
sys.path.append('./figjobs/')
from figFcns_TeX import *

import os

#------------------------------------------------------------------------------


figSaveDir = './fig/'

figName = 'fj_07_' 






dataRepoDir = './dataRepo/'









#------------------------------------------------------------------------------

PANELNAME = 'panel_1'

#------------------

figPlotParam = fcnDefaultFigSize(9.0, 0.17, (1-0.0), 0.0, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1,
                             # height_ratios=[40, 40, 20],
                             )

#---------------------------------------------
ax0 = plt.subplot(subPlots[0], projection='3d')




tmp_mask = allDteadyStateData[:, 0] < 0.1

ax0.plot3D(
    allDteadyStateData[tmp_mask, 2], 
    allDteadyStateData[tmp_mask, 1],
    allDteadyStateData[tmp_mask, 0],
    '.', ms=5, mfc='b', mew=0,
    label='saturovaná oblasť',
)


tmp_mask = allDteadyStateData[:, 0] > 9.9

ax0.plot3D(
    allDteadyStateData[tmp_mask, 2], 
    allDteadyStateData[tmp_mask, 1],
    allDteadyStateData[tmp_mask, 0],
    '.', ms=5, mfc='r', mew=0,
    label='saturovaná oblasť',
)



tmp_mask = np.logical_and(
    allDteadyStateData[:, 0] >= 0.1, 
    allDteadyStateData[:, 0] <= 9.9
)

ax0.plot3D(
    allDteadyStateData[tmp_mask, 2], 
    allDteadyStateData[tmp_mask, 1],
    allDteadyStateData[tmp_mask, 0],
    '.', ms=5, mfc='g', mew=0,
    label='nesaturovaná oblasť',
)




tmp_mask = np.logical_and(
    plot_y1 >= 0.1, 
    plot_y1 <= 9.9
)

tmp_mask = np.logical_not(tmp_mask)

plot_y1[tmp_mask] = np.nan

ax0.plot3D(
    plot_mesh[1],
    plot_mesh[0],
    plot_y1,
    '.', ms=2, mfc='m', mew=0, alpha=0.5,
    label='model',
)




ax0.set_xlabel('Signál o polohe potenciometra [V]')
ax0.set_ylabel('Vstupný signál [V]')
ax0.set_zlabel('Výstupný signál [V]')
# ax0.set_title('Všetky namerané ustálené stavy systému')

handles_ax, labels_ax = ax0.get_legend_handles_labels()

ax0.legend(
    handles_ax, labels_ax, 
    ncol=1, 
    handlelength=0.8, 
    markerfirst=True, 
    loc=3, bbox_to_anchor=(1.2, 0.00)
)





ax0.view_init(elev=10, azim=(-45-10), roll=0)


plt.tight_layout()


#---------------------------------------------

# XYT_labels = ['Vstup [V]', 'Výstup [V]', 'Namerané prevodové charakteristiky']

# fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels)

#---------------------------------------------

plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=280)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()













