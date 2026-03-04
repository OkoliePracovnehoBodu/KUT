

dF_raw = pd.read_csv(
    datasetPath + files_dict[selectedFile]['filename'],
    sep=',',
    decimal='.',
    header=0,
)

# tp    time stamp from embedded system [sec]
# y     output of the system [degrees]


# y shift needed to correct for zero steady-state position

# use mean of first 0.33 seconds as initial y (fallback to last sample)

if 'tp' in dF_raw.columns and not dF_raw['tp'].isna().all():
    first_t = dF_raw['tp'].iloc[0]
    mask_first_033 = dF_raw['tp'] <= (first_t + 0.33)
    steady_y_val = dF_raw.loc[mask_first_033, 'y'].mean() if mask_first_033.any() else dF_raw['y'].iloc[-1]
else:
    steady_y_val = dF_raw['y'].iloc[-1]

dF_raw['y'] = dF_raw['y'] - steady_y_val



# -------------------------------------------
# create mask_event_range


mask_event_range = (dF_raw['tp'] <= files_dict[selectedFile]['endtime'])
# -------------------------------------------



dF_range = dF_raw.loc[mask_event_range]


# add dy column (derivative of y) with zero padding at the beginning
dF_range = dF_range.copy()
dF_range['dy'] = (dF_range['y'].diff() / dF_range['tp'].diff()).fillna(0)


dF_range['tp'] = dF_range['tp'] - dF_range['tp'].iloc[0]





workdata_t = dF_range['tp'].to_numpy()
workdata_y = dF_range['y'].to_numpy()
workdata_dy = dF_range['dy'].to_numpy()

# workdata_y_init = - assumed_init_y_val