# -*- coding: utf-8 -*-

import numpy as np

# Pomocne moduly a funkcie ku kresleniu obrazkov
import sys
sys.path.append('./figjobs/')
from figFcns_TeX import *

import os

#------------------------------------------------------------------------------


figSaveDir = './fig/'

figName = 'fj_03_' + data_pot






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
         'o', ms=6, mfc='None', mew=0.8, mec='r', alpha=0.05,   
         label='',
         )





#---------------------------------------------

XYT_labels = ['Vstup [V]', 'Výstup [V]', 'Nameraná prevodová charakteristika']

fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()












#------------------------------------------------------------------------------

PANELNAME = 'panel_2'

#------------------

figPlotParam = fcnDefaultFigSize(3.5, 0.17, (1-0.16), 0.16, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1,
                             # height_ratios=[40, 40, 20],
                             )

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


tmpInValue = 4

tmpMask = (steadyStateData[:, 1] >= tmpInValue-0.1) & (steadyStateData[:, 1] <= tmpInValue+0.1)


ax0.plot(steadyStateData[tmpMask, 1], steadyStateData[tmpMask, 0],
         'o', ms=6, mfc='None', mew=0.8, mec='r', alpha=0.05,
         label='',
         )





#---------------------------------------------

XYT_labels = ['Vstup [V]', 'Výstup [V]', f'Nameraná prevodová charakteristika - detail pre vstupnú hodnotu {tmpInValue:.1f} V'.replace('.', ',')]

fcn_setFigStyle_for_figJob_03_panel_2(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()






