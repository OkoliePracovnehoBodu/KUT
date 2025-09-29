import qplot as qplt
import pandas as pd
import numpy as np
import seaborn as sns
from numpy.polynomial import Polynomial

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

print("Columns: ", df.columns, ' | count: ', df.t.count())
print(dtind_diff.agg(['std', 'mean', 'max', 'min']))

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

# qplt.plot([df.t, t_filt, ts, ts], signals=[df.y, y_filt, means, us], reference_signal=df.y, xlabel='t [s]', ylabel='du', title='Static Characteristic', labels=['y', 'y_filt', 'y_mean', 'u_mean'], savepath='ss_char.pdf')

qplt.scatter(us, signals=[means], xlabel='u [%PWM]', ylabel='angle [deg]', title='Static Characteristic', labels=['y'], savepath='ss_char_gain.pdf')

fit_range = (4, 90)
us_fit_find = us[fit_range[0]:fit_range[1]]
ys_fit_find = means[fit_range[0]:fit_range[1]]
ts_fit_find = ts[fit_range[0]:fit_range[1]]

fit_df = pd.DataFrame({"t": ts_fit_find, "u": us_fit_find, "y": ys_fit_find})
fit_df.to_csv('ss_char_fitdata.csv', index=False)
print("✅ Fit data saved to ss_char_fitdata.csv")

poly = None
MSE = float('inf')

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
# Fit a 2nd degree polynomial (quadratic) to us vs means

# Generate fitted values for plotting
us_fit = np.linspace(min(fit_df["u"]), max(fit_df["u"]), 100)
means_fit = poly(us_fit)

MSE = np.mean((np.array(fit_df["y"]) - poly(np.array(fit_df["u"])))**2)
print("Mean Squared Error of the fit:", MSE)

# Plot the fitted curve
qplt.scatter([fit_df["u"], us_fit], signals=[fit_df["y"], means_fit], reference=fit_df["y"], xlabel='u [%PWM]', ylabel='angle [deg]', title=f'Poly Fit {poly.degree()}: Static Characteristic = {MSE:3.4f} MSE', labels=['data','fit'], savepath='ss_char_polyfit.pdf')

print("Fitted polynomial coefficients:", poly.convert().coef, f" (degree {poly.degree()})")
print("Polynomial fit equation: y =", " + ".join([f"{coef:.6g}*u^{i}" for i, coef in enumerate(poly.convert().coef)]))
pcoefs = pd.DataFrame(poly.convert().coef, index=[f'a{i}' for i in range(len(poly.convert().coef))], columns=['value'])
pcoefs.to_csv('ss_char_polyfit_coefs.csv')
print("✅ Coefficients saved to ss_char_polyfit_coefs.csv")

# qplt.plot(df.t, signals=[df.y], xlabel='t [s]', ylabel='angle [deg]', title='System Response', labels=['y'], savepath='measurement.pdf')
# qplt.plot(df.u, signals=[df.y], xlabel='u [%PWM]', ylabel='angle [deg]', title='Gain response', savepath='gain_response.pdf')
# qplt.subplots(df.t, signals=[[df.y], [df.y/df.u], [df.u]], ylabels=['angle[deg]','gain [deg/%PWM]','input [%PWM]'], titles=['System Response', 'Gain Y/U', 'Control output'], labels=['y','y/u','u'], savepath='multiplot_response.pdf')
