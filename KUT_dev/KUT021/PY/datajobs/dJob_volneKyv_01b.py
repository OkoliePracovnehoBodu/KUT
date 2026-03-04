

dF_raw = pd.read_csv(
    datasetPath + currentFile,
    sep=',',
    decimal='.',
    header=0,
)

# tp    time stamp from embedded system [sec]
# y     output of the system [degrees]


# y shift needed to correct for zero steady-state position

# use mean of last 0.5 seconds as initial y (fallback to last sample)
if 'tp' in dF_raw.columns and not dF_raw['tp'].isna().all():
    last_t = dF_raw['tp'].iloc[-1]
    mask_half_sec = dF_raw['tp'] >= (last_t - 0.5)
    steady_y_val = dF_raw.loc[mask_half_sec, 'y'].mean() if mask_half_sec.any() else dF_raw['y'].iloc[-1]
else:
    steady_y_val = dF_raw['y'].iloc[-1]

dF_raw['y'] = dF_raw['y'] - steady_y_val



# -------------------------------------------
# create mask_event_range

# compute tmp_dy
tmp_dy = dF_raw['y'].diff()

# find dtmp_dy treshold

dy_abs = tmp_dy.abs()
threshold = 0.5
mask = dy_abs > threshold
event_times = dF_raw.loc[mask, 'tp']
start = event_times.iloc[0]
end = event_times.iloc[-1]


# include one row before the first event and 1 second after the last event
first_true_idx = mask.idxmax()
start_idx = max(dF_raw.index.min(), first_true_idx - 1)
max_end = end + 3.0
mask_event_range = (dF_raw.index >= start_idx) & (dF_raw['tp'] <= max_end)
# -------------------------------------------



# dF_range = dF_raw.loc[mask_event_range]
dF_range = dF_raw

# add dy column (derivative of y) with zero padding at the beginning
dF_range = dF_range.copy()
dF_range['dy'] = (dF_range['y'].diff() / dF_range['tp'].diff()).fillna(0)


dF_range['tp'] = dF_range['tp'] - dF_range['tp'].iloc[0]





workdata_t = dF_range['tp'].to_numpy()
workdata_y = dF_range['y'].to_numpy()
workdata_dy = dF_range['dy'].to_numpy()

# workdata_y_init = - assumed_init_y_val