# -*- coding: utf-8 -*-

import numpy as np

# Pomocne moduly a funkcie ku kresleniu obrazkov
import sys
sys.path.append('./figjobs/')
from figFcns_TeX import *


#------------------------------------------------------------------------------


figSaveDir = './fig/'









data_main = np.loadtxt(
    datasetDict[data_pot]['dataRepoPath'] + datasetDict[data_pot]['dataFile_main'], 
    delimiter=',', 
)




#------------------------------------------------------------------------------

PANELNAME = 'panel_1'

#------------------

# figPlotParam = fcnDefaultFigSize(3.5, 0.17, 0.83, 0.17, 0.5, 13)
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

# ax0.set_ylim(0, 10)

#---------------------------------------------

XYT_labels = ['čas [s]', '[V]', 'Výstupný signál (napätie tachodynama)']

fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()

save_arr = np.column_stack((data_main[:, 0], data_main[:, 1]))
save_path = figSaveDir + figName + '_' + PANELNAME + '.csv'
np.savetxt(save_path, save_arr, delimiter=',', header='time,signal', comments='')








#------------------------------------------------------------------------------

PANELNAME = 'panel_2'

#------------------

# figPlotParam = fcnDefaultFigSize(3.5, 0.17, 0.83, 0.17, 0.5, 13)
figPlotParam = fcnDefaultFigSize(2.8, 0.17, (1-0.19), 0.19, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1,
                             # height_ratios=[40, 40, 20],
                             )

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(data_main[:, 0], data_main[:, 2],
         '-', lw=0.5, color='k',
         drawstyle='steps-post',
         label='',
         )

ax0.set_ylim(0, 10)

#---------------------------------------------

XYT_labels = ['čas [s]', '[V]', 'Signál polohy potenciometra (stanovuje prevádzkovú podmienku systému)']

fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()

save_arr = np.column_stack((data_main[:, 0], data_main[:, 2]))
save_path = figSaveDir + figName + '_' + PANELNAME + '.csv'
np.savetxt(save_path, save_arr, delimiter=',', header='time,signal', comments='')





#------------------------------------------------------------------------------

PANELNAME = 'panel_3'

#------------------

# figPlotParam = fcnDefaultFigSize(3.5, 0.17, 0.83, 0.17, 0.5, 13)
figPlotParam = fcnDefaultFigSize(2.8, 0.17, (1-0.19), 0.19, 0.5, 13)
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

# ax0.set_ylim(0, 10)

#---------------------------------------------

XYT_labels = ['čas [s]', '[V]', 'Vstupný signál (signál ovládajúci napájacie napätie motora)']

fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, XYT_labels)

#---------------------------------------------

# plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()


save_arr = np.column_stack((data_main[:, 0], data_main[:, 3]))
save_path = figSaveDir + figName + '_' + PANELNAME + '.csv'
np.savetxt(save_path, save_arr, delimiter=',', header='time,signal', comments='')






