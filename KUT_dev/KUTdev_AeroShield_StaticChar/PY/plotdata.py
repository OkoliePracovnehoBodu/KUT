import qplot as qplt
import pandas as pd
import numpy as np
import seaborn as sns

FILE_PATH = './DATA/ss_char.csv'

sns.set_theme(style="ticks", palette="gray", context="paper")  # clean look
sns.set_context("paper", font_scale=1.2)


df = pd.read_csv(FILE_PATH)
df.columns = df.columns.str.strip()


du = df.u.diff()/df.dt
duind = du > 0
mask = duind.to_numpy().astype(bool)
dtind = df.t[mask]
dtind_diff = dtind.diff()
dtind_max = np.where(mask)[0]-1
dtind_min = np.floor(dtind_max[:-1] - np.diff(dtind_max)*0.5).astype(np.int32)

print("Columns: ", df.columns, ' | count: ', df.t.count())

print(dtind_diff.agg(['std', 'mean', 'max', 'min']))

iseries = pd.DataFrame({"v": range(df.t.count())})
imask = pd.Series(False, iseries.index)

means = []
ts = []
us = []
tind_filt = []

for i, (rmin, rmax) in enumerate(zip(dtind_min, dtind_max)):
	tind = dtind_max[i - 1] + 1 if i > 0 else 0
	# print('i:', i, '. lower:', dtind_max[i-1] if i > 0 else 0, ' | upper:', rmax)
	imask |= iseries['v'].between(rmin, rmax)
	mean_val = df.loc[rmin:rmax, "y"].mean()
	means.append(mean_val)
	means.append(mean_val)
	tind_filt += [tind, rmax]

ts = df.t[tind_filt]
us = df.u[tind_filt]
y_filt = df.y[imask]
t_filt = df.t[imask]


# exit(0)
# print(df.u[tind_filt])

qplt.plot([df.t, t_filt, ts, ts], signals=[df.y, y_filt, means, us], reference_signal=df.y, xlabel='t [s]', ylabel='du', title='Static Characteristic', labels=['y', 'y_filt', 'y_mean', 'u_mean'], savepath='ss_char.pdf')


# qplt.plot(df.t, signals=[df.y], xlabel='t [s]', ylabel='angle [deg]', title='System Response', labels=['y'], savepath='measurement.pdf')
# qplt.plot(df.u, signals=[df.y], xlabel='u [%PWM]', ylabel='angle [deg]', title='Gain response', savepath='gain_response.pdf')
# qplt.subplots(df.t, signals=[[df.y], [df.y/df.u], [df.u]], ylabels=['angle[deg]','gain [deg/%PWM]','input [%PWM]'], titles=['System Response', 'Gain Y/U', 'Control output'], labels=['y','y/u','u'], savepath='multiplot_response.pdf')
