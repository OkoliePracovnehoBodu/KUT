# -*- coding: utf-8 -*-

import numpy as np

# Pomocne moduly a funkcie ku kresleniu obrazkov
import sys
sys.path.append('./figjobs/')
from figFcns_TeX import *

import os

#------------------------------------------------------------------------------


figSaveDir = './fig/'

figName = 'fj_05_' 






dataRepoDir = './dataRepo/'









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



for data_pot in datasetDict.keys(): 


    steadyStateData = np.loadtxt(
        dataRepoDir + 'ALLSCH_' + data_pot + '_steadyStateData' + '.csv', 
        delimiter=',', 
        skiprows=1,
    )


    ax0.plot(steadyStateData[:, 1], steadyStateData[:, 0],
            'o', ms=4, mfc='None', mew=0.5,    
            label=data_pot,
            )





#---------------------------------------------

XYT_labels = ['Vstup [V]', 'Výstup [V]', 'Namerané prevodové charakteristiky']

fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels)

#---------------------------------------------

plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=280)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()













