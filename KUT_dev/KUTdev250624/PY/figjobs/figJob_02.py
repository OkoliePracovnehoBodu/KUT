# -*- coding: utf-8 -*-

import numpy as np

# Pomocne moduly a funkcie ku kresleniu obrazkov
import sys
sys.path.append('./figjobs/')
from figFcns_TeX import *

import os

#------------------------------------------------------------------------------


figSaveDir = './fig/'

figName = 'fj_02_' + data_pot






dataRepoDir = './dataRepo/'




data_main = np.loadtxt(
    datasetDict[data_pot]['dataRepoPath'] + datasetDict[data_pot]['dataFile_main'], 
    delimiter=',', 
)





sch_files = [
    f for f in os.listdir(dataRepoDir)
    if f.startswith('SCH') and data_pot in f
]




#------------------------------------------------------------------------------

PANELNAME = 'panel_1'

#------------------

figPlotParam = fcnDefaultFigSize(4.5, 0.17, (1-0.15), 0.15, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1,
                             # height_ratios=[40, 40, 20],
                             )

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(data_main[:, 0], data_main[:, 1],
         '-', lw=0.5, color='k',
         drawstyle='steps-post',
         label='',
         )

for sch_file in sch_files:

    sch_data = np.loadtxt(
        dataRepoDir + sch_file,
        delimiter=',',
        skiprows=1,  
    )

    ax0.plot(sch_data[:, 0], sch_data[:, 1],
             '-', lw=1.9, color='r',
             drawstyle='steps-post',
             solid_capstyle='butt',
             label='',
             )

ax0.set_ylim(0, 10)

#---------------------------------------------

XYT_labels = ['čas [s]', '[V]', 'Výstupný signál (napätie tachodynama)']

fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()












#------------------------------------------------------------------------------

PANELNAME = 'panel_3'

#------------------


figPlotParam = fcnDefaultFigSize(4.5, 0.17, (1-0.15), 0.15, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1,
                             # height_ratios=[40, 40, 20],
                             )

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(data_main[:, 0], data_main[:, 3],
         '-', lw=0.5, color='k',
         drawstyle='steps-post',
         label='',
         )

for sch_file in sch_files:

    sch_data = np.loadtxt(
        dataRepoDir + sch_file,
        delimiter=',',
        skiprows=1,  
    )

    ax0.plot(sch_data[:, 0], sch_data[:, 2],
             '-', lw=1.9, color='r',
             drawstyle='steps-post',
             solid_capstyle='butt',
             label='',
             )

ax0.set_ylim(0, 10)

#---------------------------------------------

XYT_labels = ['čas [s]', '[V]', 'Vstupný signál (signál ovládajúci napájacie napätie motora)']

fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()











