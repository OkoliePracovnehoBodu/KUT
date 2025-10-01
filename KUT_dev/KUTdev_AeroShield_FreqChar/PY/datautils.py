import numpy as np

def make_intervals(ends: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Create intervals from an array of end indices.
    
    Example:
        ends = [0, 150, 300]
        -> ranges = [75, 150, 225, 300]
        -> intervals = [(75, 150), (225, 300)]
    """
    ends = np.asarray(ends)
    if len(ends) < 2:
        raise ValueError("Need at least two endpoints to form intervals")
    
    # compute midpoints between consecutive ends
    midpoints = (ends[:-1] + ends[1:]) // 2
    
    # combine midpoints with ends, but skip the very first 0
    ranges = np.r_[midpoints, ends[1:]]
    ranges.sort()
    
    # build pairs (0,1), (2,3), ...
    intervals = [(ranges[i], ranges[i+1]) for i in range(0, len(ranges), 2)]
    
    return ranges, intervals


def make_change_threshold_indices(x: np.ndarray, std_sigma_threshold: float = 5.0, append_first_zero: bool = True) -> tuple[np.ndarray, float]:
    dx = np.diff(x)
    dx_std = np.std(dx)
    dx_threshold = std_sigma_threshold * dx_std
    changes = np.r_[np.where(dx > dx_threshold)[0].astype(int), len(x)]
    if append_first_zero and changes[0] != 0:
        changes = np.r_[0, changes]
    return changes, dx_threshold