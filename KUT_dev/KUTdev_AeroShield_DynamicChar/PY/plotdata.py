import qplot as qplt
import pandas as pd
import numpy as np
import seaborn as sns
from numpy.polynomial import Polynomial

FILE_PATH = './DATA/dyn_char.csv'

sns.set_theme(style="ticks", palette="gray", context="paper")  # clean look
sns.set_context("paper", font_scale=1.2)

qplt.set_paper_style(single_column=True)


df = pd.read_csv(FILE_PATH)
df.columns = df.columns.str.strip()

print("Columns: ", df.columns, ' | count: ', df.t.count())

# Plot the response in a subplot
qplt.subplots(df.t, signals=[[df.y], [df.u]], xlabels=['t [s]'], ylabels=[r'$\varphi [^\circ]$', 'u [%PWM]'], titles=['System Response', 'Input Signal'], labels=['y','u'], savepath='dyn_char_measurement.pdf')

# Split the data into segments where u is changing after stable period
# Find the first change in control input after getting to the U_PB

du = df.u.diff()/df.dt
du_avg = du.std() * 2  # 2sigma threshold

qplt.plot([df.t, [df.t.iloc[0], df.t.iloc[-1]]], signals=[du, [du_avg, du_avg]], xlabel='t [s]', ylabel='du', title='Input derivative', labels=['du'], savepath='dyn_char_du.pdf')

mask_2sig = (abs(du) > du_avg).astype(bool)
t_2sig = df.t[mask_2sig]
u_2sig = df.u[mask_2sig]
y_2sig = df.y[mask_2sig]

change_points = pd.DataFrame({"t": t_2sig, "u": u_2sig, "y": y_2sig, "data_mask": mask_2sig[mask_2sig].index})
change_points.to_csv('dyn_char_changepoints.csv', index=False)
print("✅ Change points saved to dyn_char_changepoints.csv")

t_2sig_inv = df.t[~mask_2sig]
u_2sig_inv = df.u[~mask_2sig]
y_2sig_inv = df.y[~mask_2sig]

df_inv = pd.DataFrame({"t": t_2sig_inv, "u": u_2sig_inv, "y": y_2sig_inv, "data_mask": (~mask_2sig)[~mask_2sig].index})
df_inv.to_csv('dyn_char_nosteps.csv', index=False)
print("✅ Raw data without step changes saved to dyn_char_nosteps.csv")

qplt.scatter([df_inv.t, change_points.t], signals=[df_inv.u, change_points.u], reference=df_inv.u, xlabel='t [s]', ylabel='u [%PWM]', title='Input changes', labels=['u','change points'], size=15, savepath='dyn_char_u_changes.pdf')

# Remove the data for stabilization periods (removing all the data before the first change)
df_clean = df.copy().loc[change_points["data_mask"].iloc[0]:].reset_index(drop=True)
df_clean['data_mask'] = change_points["data_mask"].copy().reset_index(drop=True)
df_clean.data_mask = df_clean.data_mask - df_clean.data_mask.iloc[0]  # reset index to 0
df_clean.t = df_clean.t - df_clean.t.iloc[0]  # reset time to 0
df_clean.to_csv('dyn_char_clean.csv', index=False)
print("✅ Cleaned data saved to dyn_char_clean.csv")

qplt.subplots(df_clean.t, signals=[[df_clean.y], [df_clean.u]], xlabels=['t [s]'], ylabels=[r'$\varphi [^\circ]$', 'u [%PWM]'], titles=['Cleaned System Response','Cleaned input signal'], labels=[r'$\varphi$','u'], savepath='dyn_char_u_clean.pdf')

change_points_clean = change_points["data_mask"].copy().reset_index(drop=True)
change_points_clean = change_points_clean - change_points_clean.iloc[0]  # reset index to 0

# Split the data into segments based on the change points
ranges = list(zip(change_points_clean.shift(1).fillna(0).astype(int), change_points_clean.astype(int)))[1:] # skip the first range (0, first change point)

# No overlapping steps
for i, (rmin, rmax) in enumerate(ranges):
	STEP_SIZE = df.u[change_points.data_mask.iloc[i]] - df.u[change_points.data_mask.iloc[i] - 1]
	seg = df_clean.loc[rmin:rmax-1].reset_index(drop=True)
	seg['step_size'] = STEP_SIZE
	seg.drop(columns=['data_mask'], inplace=True)
	seg.to_csv(f'dyn_char_step_{i:02d}.csv', index=False)
	qplt.subplots(seg.t, signals=[[seg.y], [seg.u]], xlabels=['t [s]'], ylabels=[r'$\varphi [^\circ]$', 'u [%PWM]'], titles=[f'Step {i:02d} - Size: {STEP_SIZE}', 'Control Input'], labels=['y','u'], savepath=f'dyn_char_step_{i:02d}.pdf')
	print(f"✅ Step {i:02d} saved to dyn_char_step_{i:02d}.csv")

# Overlapping steps (include the change point in both steps)
# overlap_count = 10  # number of samples to overlap
# for i, (rmin, rmax) in enumerate(ranges):
# 	STEP_SIZE = df.u[change_points.data_mask.iloc[i]] - df.u[change_points.data_mask.iloc[i] - 1]
# 	seg = df_clean.loc[(rmin if i == 0 else rmin - overlap_count):rmax - 1].reset_index(drop=True)
# 	seg['step_size'] = STEP_SIZE
#	seg.drop(columns=['data_mask'], inplace=True)
# 	seg.to_csv(f'dyn_char_step_ov_{i:02d}.csv', index=False)
# 	qplt.subplots(seg.t, signals=[[seg.y], [seg.u]], xlabels=['t [s]'], ylabels=['output [deg]', 'u [%PWM]'], titles=[f'Step {i:02d} (overlap)', 'Control Input'], labels=['y','u'], savepath=f'dyn_char_step_ov_{i:02d}.pdf')
# 	print(f"✅ Step {i:02d} (overlap) saved to dyn_char_step_ov_{i:02d}.csv")

print("All done!")