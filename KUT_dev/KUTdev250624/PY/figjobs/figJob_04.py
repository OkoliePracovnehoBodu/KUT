# -*- coding: utf-8 -*-

import numpy as np

# Pomocne moduly a funkcie ku kresleniu obrazkov
import sys
sys.path.append('./figjobs/')
from figFcns_TeX import *

import os

#------------------------------------------------------------------------------


figSaveDir = './fig/'

figName = 'fj_04_' + data_pot






dataRepoDir = './dataRepo/'




steadyStateData = np.loadtxt(
    dataRepoDir + 'ALLSCH_' + data_pot + '_steadyStateData' + '.csv', 
    delimiter=',', 
    skiprows=1,
)








#------------------------------------------------------------------------------

PANELNAME = 'panel_1'

#------------------

figPlotParam = fcnDefaultFigSize(6.0, 0.17, (1-0.12), 0.12, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1,
                             # height_ratios=[40, 40, 20],
                             )

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(steadyStateData[:, 1], steadyStateData[:, 0],
         'o', ms=6, mfc='None', mew=0.8, mec='r', alpha=1.0,   
         label='namerané',
         )


ax0.plot(plot_u1, plot_y1,
         '.', ms=3, mfc='k', mew=0, mec='k',    
         label='model',
         )




#---------------------------------------------

XYT_labels = ['$u$ [V]', '$y$, $\hat y$  [V]', 'Prevodová charakteristika']

fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()












#------------------------------------------------------------------------------

PANELNAME = 'panel_2'

#------------------

figPlotParam = fcnDefaultFigSize(6.0, 0.17, (1-0.12), 0.12, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1,
                             # height_ratios=[40, 40, 20],
                             )

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(steadyStateData[:, 1], steadyStateData[:, 0],
         'o', ms=6, mfc='None', mew=0.8, mec='r', alpha=1.0,   
         label='namerané',
         )


ax0.plot(plot_u1, plot_y1,
         '.', ms=3, mfc='k', mew=0, mec='k',    
         label='model',
         )


ax0.plot(plot_u2, plot_y2,
         '.', ms=3, mfc='k', mew=0, mec='k',    
         label='',
         )


#---------------------------------------------

XYT_labels = ['$u$ [V]', '$y$, $\hat y$  [V]', 'Prevodová charakteristika']

fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()






