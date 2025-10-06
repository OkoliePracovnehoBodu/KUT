import qplot as qplt
import pandas as pd
import numpy as np
import seaborn as sns
from numpy.polynomial import Polynomial
import datautils as dutil

FILE_PATH = './DATA/ss_char.csv'

# sns.set_theme(style="ticks", palette="gray", context="paper")  # clean look
# sns.set_context("paper", font_scale=1.2)
qplt.set_paper_style(single_column=True)


df = pd.read_csv(FILE_PATH)
df.columns = df.columns.str.strip()


du = df.u.diff()/df.dt
duind = du > 0
mask = duind.to_numpy().astype(bool)
dtind = df.t[mask]
dtind_diff = dtind.diff()

print("Columns: ", df.columns, ' | count: ', df.t.count())
print(dtind_diff.agg(['std', 'mean', 'max', 'min']))

qplt.plot(df.t, signals=[df.y], xlabel='t [s]', ylabel=r'$\varphi [^\circ]$', title='System Response', labels=[r'$\varphi$'], savepath='measurement.pdf')


qplt.scatter(df.u, signals=[df.y], xlabel='u [%PWM]', ylabel=r'$\varphi [^\circ]$', title='Control response', labels=['data'], size=5, savepath='gain_response.pdf')
qplt.subplots(df.t, signals=[[df.y], [df.y/df.u], [df.u]], ylabels=[r'$\varphi [^\circ]$', r'$\frac{\varphi}{u} [^\circ/\%PWM]$','u [%PWM]'], xlabels=['t [s]'], titles=['System Response', r'$\frac{\varphi}{U}$ response', 'Control output'], labels=['y','y/u','u'], savepath='multiplot_response.pdf')

# Plot the derivative of the y response signal
dy = df.y.diff()/df.dt
dystd = 10 * dy.std()
tline = [0, df.t.iloc[-1]]
stdline = [dystd, dystd]

nsamples_remove = 10 # number of sample to remove, before enormous change in dy
sigmaindx = np.where(dy > dystd)[0][0] - nsamples_remove
dfre = pd.DataFrame({"t": df.t.iloc[:sigmaindx], "y": df.y.iloc[:sigmaindx], "u": df.u.iloc[:sigmaindx], "dt": df.dt.iloc[:sigmaindx], "df_plant": df.dt_plant.iloc[:sigmaindx]})


time_to_zoom = 60 # the time to take for the zoom effect in seconds
indx = np.where(df.t <= time_to_zoom)

nsamples_zoom = len(indx[0])

t_zoom = dfre.t[:nsamples_zoom]
y_zoom = dfre.y[:nsamples_zoom]
u_zoom = dfre.u[:nsamples_zoom]
dt_zoom = dfre.dt[:nsamples_zoom]

dfzoom = pd.DataFrame({"t": t_zoom, "y": y_zoom, "u": u_zoom, "dt": dt_zoom})
dfzoom.to_csv("zoomed_measurement.csv", index=False)
print("✅ Zoomed data saved to zoomed_measurement.csv")

dy_zoom = np.diff(y_zoom)/dfzoom["dt"][:-1]

du_zoom_idx, du_zoom_std_threshold = dutil.make_change_threshold_indices(u_zoom, 5)
_, du_zoom_ranges = dutil.make_intervals(du_zoom_idx)

# print(du_zoom_idx, du_zoom_ranges)

t_du_zoom = [t_zoom[0], t_zoom.iloc[-1]]
u_std_zoom = [du_zoom_std_threshold, du_zoom_std_threshold]

df_zoom_stable = pd.concat([dfzoom.iloc[start:end] for start, end in du_zoom_ranges])

qplt.plot([t_zoom[:-1]], signals=[dy_zoom], title="Zoomed dY", xlabel='t [s]', ylabel=r'$\omega [^\circ/s]$', labels=[r'$\omega$'], savepath="zoomed_dy.pdf")

qplt.plot(t_zoom, signals=[y_zoom, u_zoom], scatter_signals=[(df_zoom_stable.t, df_zoom_stable.y, "steady")], reference_signal=u_zoom, labels=[r'$\varphi$','u'], xlabel='t [s]', ylabel=r'$\varphi [^\circ]$', title='Measurement zoom', savepath='measurement_zoom.pdf')


dtind_max = np.concatenate([np.where(mask)[0] - 1, [df.t.count() - 1]])

# print(dtind_max, np.diff(dtind_max))

dtind_min = np.floor(dtind_max - np.diff(np.concatenate([[0], dtind_max])) * 0.5).astype(np.int32)



iseries = pd.DataFrame({"v": range(df.t.count())})
imask = pd.Series(False, iseries.index)

means = []
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
ys = df.y[tind_filt]
y_filt = df.y[imask]
t_filt = df.t[imask]

ss_df = pd.DataFrame({"t": ts, "u": us, "y": ys, "y_mean": means})
ss_df.to_csv('ss_char_processed.csv', index=False)
print("✅ Processed data saved to ss_char_processed.csv")


# exit(0)
# print(df.u[tind_filt])

qplt.plot([df.t, t_filt, ts, ts], signals=[df.y, y_filt, means, us], reference_signal=df.y, xlabel='t [s]', ylabel='du', title='Static Characteristic', labels=['y', 'y_filt', 'y_mean', 'u_mean'], savepath='ss_char.pdf')

qplt.scatter(us, signals=[means], xlabel='u [%PWM]', ylabel=r'$\varphi [^\circ]$', title='Static Characteristic', labels=['data'], savepath='ss_char_gain.pdf')

fit_range = (4, 96)
us_fit_find = us[fit_range[0]:fit_range[1]]
ys_fit_find = means[fit_range[0]:fit_range[1]]
ts_fit_find = ts[fit_range[0]:fit_range[1]]

fit_df = pd.DataFrame({"t": ts_fit_find, "u": us_fit_find, "y": ys_fit_find})
fit_df.to_csv('ss_char_fitdata.csv', index=False)
print("✅ Fit data saved to ss_char_fitdata.csv")

qplt.scatter([us, fit_df['u']], signals=[means, fit_df['y']], xlabel='u [%PWM]', ylabel=r'$\varphi [^\circ]$', title='Static Characteristic Comparison', labels=['data','data zoom'], savepath='ss_char_linear_gain.pdf')

poly = None
MSE = float('inf')

# Fit a n degree polynomial to us vs means
for pol in range(1, 4):
	newpoly = Polynomial.fit(fit_df["u"], fit_df["y"], pol)
	means_fit = newpoly(fit_df["u"])
	newMSE = np.mean((np.array(fit_df["y"]) - newpoly(np.array(fit_df["u"])))**2)
	print(f"Poly deg: {pol:2d} | MSE: {newMSE:3.4f}")
	if newMSE < MSE:
		poly = newpoly
		MSE = newMSE

if poly is None:
	raise ValueError("Polynomial fitting failed!")

# Generate fitted values for plotting
us_fit = np.linspace(min(fit_df["u"]), max(fit_df["u"]), 100)
means_fit = poly(us_fit)

MSE = np.mean((np.array(fit_df["y"]) - poly(np.array(fit_df["u"])))**2)
print("Mean Squared Error of the fit:", MSE)

# Plot the fitted curve
qplt.plot(us_fit, signals=[means_fit], markers=['.'], scatter_signals=[(fit_df['u'], fit_df["y"], r'real', 'red', 10, 'x')], xlabel='u [%PWM]', ylabel=r'$\varphi [^\circ]$', title=f'Poly Fit {poly.degree()}: Static Characteristic = {MSE:3.4f} MSE', labels=['data'], linewidth=1, savepath='ss_char_polyfit.pdf')

print("Fitted polynomial coefficients:", poly.convert().coef, f" (degree {poly.degree()})")
print("Polynomial fit equation: y =", " + ".join([f"{coef:.6g}*u^{i}" for i, coef in enumerate(poly.convert().coef)]))

pcoefs = pd.DataFrame(poly.convert().coef, index=[f'a{i}' for i in range(len(poly.convert().coef))], columns=['value'])
pcoefs.to_csv('ss_char_polyfit_coefs.csv')
print("✅ Coefficients saved to ss_char_polyfit_coefs.csv")
