# -*- coding: utf-8 -*-

import numpy as np

# Pomocne moduly a funkcie ku kresleniu obrazkov
import sys
sys.path.append('./figjobs/')
from figFcns_TeX import *

import os

#------------------------------------------------------------------------------


figSaveDir = './fig/'

figName = 'fj_02_' + selectedFile











#------------------------------------------------------------------------------

PANELNAME = 'panel_1'

#------------------

figPlotParam = fcnDefaultFigSize(5.5, 0.17, (1-0.14), 0.14, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1,
                             # height_ratios=[40, 40, 20],
                             )

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(workdata_t, workdata_y,
         '-', lw=0.8, color='k',
        #  ms=2, mfc='none', mec='k', mew=0.3,
         drawstyle='steps-post',
         label='meranie',
         )

ax0.plot(simdata_t + files_dict[selectedFile]['releasetime'], simdata_y,
         '-', lw=0.4, color='r',
        #  ms=2, mfc='none', mec='k', mew=0.3,
        #  drawstyle='steps-post',
         label='simulácia',
         )

#---------------------------------------------
# determine y lim for LinearLocator
tmpMax = np.ceil(np.max(np.abs(  workdata_y  )))
ax0.set_ylim([-tmpMax, tmpMax])

#---------------------------------------------

XYT_labels = ['čas [s]', '[°]', 'Výstupný signál (poloha, uhol ramena kyvadla)']

fcn_setFigStyle_basicTimeSeries_var2(fig, figPlotParam, XYT_labels)

#---------------------------------------------

plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()


# save plotted data for panel_1 as CSV (include sim data columns; pad shorter series with blanks '')
sim_t_shift = simdata_t + files_dict[selectedFile]['releasetime']

n_w = len(workdata_t)
n_s = len(sim_t_shift)
n = max(n_w, n_s)

fmt_num = lambda x: '%.6e' % x

rows = []
for i in range(n):
    wt = fmt_num(workdata_t[i]) if i < n_w else ''
    wy = fmt_num(workdata_y[i]) if i < n_w else ''
    st = fmt_num(sim_t_shift[i]) if i < n_s else ''
    sy = fmt_num(simdata_y[i]) if i < n_s else ''
    rows.append([wt, wy, st, sy])

np.savetxt(figSaveDir + figName + '_' + PANELNAME +'.csv',
           rows,
           delimiter=',',
           header='work_t,work_y,sim_t,sim_y',
           fmt='%s')







#------------------------------------------------------------------------------

PANELNAME = 'panel_2'

#------------------

figPlotParam = fcnDefaultFigSize(4.25, 0.17, (1-0.15), 0.15, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])


subPlots = gridspec.GridSpec(1, 1,
                             # height_ratios=[40, 40, 20],
                             )

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(workdata_t, np.deg2rad(workdata_dy),
         '-', lw=0.7, color='k',
        #  ms=2, mfc='none', mec='k', mew=0.3,
         drawstyle='steps-post',
        #  label='meranie',
         )

ax0.plot(simdata_t + files_dict[selectedFile]['releasetime'], simdata_dy,
         '-', lw=0.4, color='r',
        #  ms=2, mfc='none', mec='k', mew=0.3,
        #  drawstyle='steps-post',
        #  label='simulácia',
         )


#---------------------------------------------
# determine y lim for LinearLocator
tmpMax = np.ceil(np.max(np.abs(np.deg2rad(workdata_dy))))
ax0.set_ylim([-tmpMax, tmpMax])

#---------------------------------------------

XYT_labels = ['čas [s]', '[rad/s]', 'Uhlová rýchlosť ']

fcn_setFigStyle_basicTimeSeries_var2(fig, figPlotParam, XYT_labels)

#---------------------------------------------

plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()


# save plotted data for panel_2 as CSV (include sim data columns; pad shorter series with blanks '')
sim_t_shift = simdata_t + files_dict[selectedFile]['releasetime']

n_w = len(workdata_t)
n_s = len(sim_t_shift)
n = max(n_w, n_s)

fmt_num = lambda x: '%.6e' % x

rows = []
for i in range(n):
    wt = fmt_num(workdata_t[i]) if i < n_w else ''
    # save workdata_dy in radians to match plotted values
    wy = fmt_num(np.deg2rad(workdata_dy[i])) if i < n_w else ''
    st = fmt_num(sim_t_shift[i]) if i < n_s else ''
    sy = fmt_num(simdata_dy[i]) if i < n_s else ''
    rows.append([wt, wy, st, sy])

np.savetxt(figSaveDir + figName + '_' + PANELNAME +'.csv',
           rows,
           delimiter=',',
           header='work_t,work_dy_rad,sim_t,sim_dy',
           fmt='%s')








