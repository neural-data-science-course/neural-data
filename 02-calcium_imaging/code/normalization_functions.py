'''
Rutines for normalize caiman calcium imaging traces using SNR

Author: zbarry
'''

import numpy as np
from scipy.ndimage import percentile_filter

from caiman.utils.stats import df_percentile
from caiman.source_extraction.cnmf.deconvolution import estimate_parameters


def detrend_trace(trace, trend_window_length):
    """
    Detrend a trace to make an even baseline before deconvolving with OASIS.
    This is very useful for trace drift to decrease spurious spike events.
    Uses skimage percentile filtering with automatic quantile estimation via
    CaImAn.
    :param trace: A single raw fluorescence trace which can be constructed from
        `C(trace) + YrA(trace)`
    :param trend_window_length: The number of timepoints to use for a window
        from which the percentile for a region is calculated. Keep much longer
        than the longest non-sparse groups of spike trains to avoid them getting
        highly decreased in size and distorting the fluorescence trace.
    :return: The trace after detrending.
    """

    quantile_min, _ = df_percentile(
        trace[np.newaxis, :trend_window_length], axis=1
    )

    perc_trace = percentile_filter(trace, quantile_min, trend_window_length)

    trace = trace - perc_trace

    return trace


def calc_ar_props(
        trace,
        ar_p,
        sn=None,
        g=None,
        noise_range=(0.25, 0.5),
        noise_method="mean",
        lags=5,
        fudge_factor=0.96,
):
    """
    Calculate the AR process coefficients & noise from a fluorescence trace.
    :param trace: A single raw fluorescence trace which can be constructed from
        `C(trace) + YrA(trace)`
    :param ar_p: Order of autoregressive process
    :param sn: SNR which is calculated from PSD by CaImAn. Leave as None to calc
        in this function.
    :param g: autoregressive process coefficient. Leave as None to calc in this
        function.
    :param noise_range: fraction range of the trace sampling frequency /
        framerate to average the PSD over to calculate noise.
    :param noise_method: noise_method used in `estimate_parameters`.
    :param lags: number of lags used in `estimate_parameters` to estimate AR
        coefficients from the trace autocovariance.
    :param fudge_factor: regularization constant on AR coefficients used in
        `estimate_parameters`.
    :return: Tuple of:
        1) The autoregressive coefficients.
        2) Signal-to-noise ratio - the "white noise" component of the AR
           process.
        3) The standard deviation of the AR process, which can be used to
           normalize traces.
    """

    g, sn = estimate_parameters(
        trace,
        p=ar_p,
        sn=sn,
        g=g,
        range_ff=noise_range,
        method=noise_method,
        lags=lags,
        fudge_factor=fudge_factor,
    )

    if ar_p == 1:
        std_ar = np.sqrt(sn ** 2 / (1 - float(g[0]) ** 2))

    elif ar_p == 2:
        std_ar = np.sqrt(
            (1 - g[1])
            * sn ** 2
            / ((1 + g[1]) * (1 - g[0] - g[1]) * (1 + g[0] - g[1]))
        )

    else:
        raise ValueError("AR process parameter p must be 1 or 2.")

    return g, sn, std_ar


def normalize_traces(
        cmn_c, cmn_yra, cmn_s, ar_p, offset_method="denoised_floor"
):
    """
    Normalize calcium traces based on a calculation of signal-to-noise ratio.
    The white noise of the AR process is calculated by taking the average power
    across the higher frequency regions of the trace's power spectral density.
    The final standard deviation of the "noise" is based on the AR process
    theoretical variance which varies by the AR order (1 or 2 supported).
    :param cmn_c: The "C" matrix of denoised traces from the CNMF analysis
    :param cmn_yra: "YrA" matrix of residuals from CNMF analysis
    :param cmn_s: "S" matrix of residuals from CNMF analysis
    :param ar_p: Order of the autoregressive process.
    :param offset_method:
        'denoised_floor': use the minimum of the denoised trace as the zeroing
            point for z-scoring
    :return: Tuple of:
        1) The raw traces [component index x timepoint] z-scored to the noise
        2) The "denoised" [component index x timepoint] (i.e., AR model-applied)
            traces z-scored
        3) Normalized residual traces.
        4) Normalized S / 'activity' traces.
        5) Vector of the AR process "noise" that the traces were normed to.
    """

    noise_levels = np.zeros(cmn_c.shape[0], dtype=cmn_c.dtype)

    raw_traces_normed = np.zeros_like(cmn_c)
    denoised_traces_normed = np.zeros_like(cmn_c)
    residuals_normed = np.zeros_like(cmn_c)
    s_normed = np.zeros_like(cmn_c)

    for trace_idx, (c_indiv, yra_indiv, s_indiv) in enumerate(
            zip(cmn_c, cmn_yra, cmn_s)
    ):
        f_indiv = c_indiv + yra_indiv  # "raw" trace for this component

        _, sn, std_ar = calc_ar_props(f_indiv, ar_p=ar_p)

        if offset_method == "denoised_floor":
            c_offset = np.min(c_indiv)
            f_offset = c_offset
        else:
            raise ValueError(f"Unknown offset calculation: {offset_method}")

        norm_raw_trace = (f_indiv - f_offset) / std_ar
        norm_denoised_trace = (c_indiv - c_offset) / std_ar
        norm_residual = yra_indiv / std_ar
        norm_s = s_indiv / std_ar

        noise_levels[trace_idx] = std_ar

        raw_traces_normed[trace_idx, :] = norm_raw_trace
        denoised_traces_normed[trace_idx, :] = norm_denoised_trace
        residuals_normed[trace_idx, :] = norm_residual
        s_normed[trace_idx, :] = norm_s

    return (
        raw_traces_normed,
        denoised_traces_normed,
        residuals_normed,
        s_normed,
        noise_levels,
    )