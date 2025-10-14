# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

# Pomocne moduly a funkcie ku kresleniu obrazkov
import sys
sys.path.append('./figjobs/')
from figFcns_TeX import *


#------------------------------------------------------------------------------

figSaveDir = './fig/'

dataRepoDir = './dataRepo/'


#------------------------------------------------------------------------------


df_main = pd.read_csv(
    datasetDict[data_item]['dataRepoPath'] + datasetDict[data_item]['dFile_TS'],
    delimiter=',',
    skiprows=1,
    header=None
)

# Convert first column from string like '1.2 sec' to float seconds
df_main[0] = df_main[0].str.replace(' sec', '').astype(float)
    

#------------------------------------------------------------------------------






#------------------------------------------------------------------------------

PANELNAME = 'panel_1'

#------------------

figPlotParam = fcnDefaultFigSize(3.0, 0.17, (1-0.17), 0.17, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1)

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(df_main.loc[:,0], df_main.loc[:,3],
         '-', lw=0.5, color='k',
         drawstyle='steps-post',
         label='',
         )

# ax0.set_ylim(0, 10)

#---------------------------------------------

XYT_labels = ['čas [s]', '[V]', 'Výstupný signál 1 (snímač teploty 1)']

fcn_setFigStyle_basicTimeSeries2(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()






#------------------------------------------------------------------------------

PANELNAME = 'panel_2'

#------------------

figPlotParam = fcnDefaultFigSize(3.0, 0.17, (1-0.17), 0.17, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1)

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(df_main.loc[:,0], df_main.loc[:,4],
         '-', lw=0.5, color='k',
         drawstyle='steps-post',
         label='',
         )

# ax0.set_ylim(0, 10)

#---------------------------------------------

XYT_labels = ['čas [s]', '[V]', 'Výstupný signál 2 (snímač teploty 2)']

fcn_setFigStyle_basicTimeSeries2(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()





#------------------------------------------------------------------------------

PANELNAME = 'panel_3'

#------------------

figPlotParam = fcnDefaultFigSize(2.5, 0.17, (1-0.21), 0.21, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1)

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(df_main.loc[:,0], df_main.loc[:,1],
         '-', lw=0.5, color='k',
         drawstyle='steps-post',
         label='',
         )

# ax0.set_ylim(0, 10)

#---------------------------------------------

XYT_labels = ['čas [s]', '[V]', 'Vstupný signál 1 (výhrevné teleso)']

fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()




#------------------------------------------------------------------------------

PANELNAME = 'panel_4'

#------------------

figPlotParam = fcnDefaultFigSize(2.5, 0.17, (1-0.21), 0.21, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1)

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(df_main.loc[:,0], df_main.loc[:,2],
         '-', lw=0.5, color='k',
         drawstyle='steps-post',
         label='',
         )

# ax0.set_ylim(0, 10)

#---------------------------------------------

XYT_labels = ['čas [s]', '[V]', 'Vstupný signál 2 (ventilátor)']

fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()









