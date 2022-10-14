"""
DOCSTRING
"""

from pywt import scale2frequency
from pywt import cwt
from scipy.signal import butter
from scipy.signal import sosfilt
import numpy as np


def bandpass_filter(signal, low_f, high_f, sampling_rate=1.0, filter_order=5):
    '''
    Band pass filter based on the scipy implementation of butterwirth filtering.

    Returns the filtered signal in the specified frequency band.

    Parameters
    ----------
    signal : array-like
        the signal to filter

    low_f : float
        lower bound of the frequency band

    high_f : float
        higher bound of the frequency band

    sampling_rate : float
        sampling rate of the signal, defaults to 1 if not specified

    filter_order : int
        order of the butterwirth filter, defaults to 15 if not specified

    Returns
    -------
    filtered_signal : array-like
        filtered signal

    '''
    filter = butter(filter_order, [low_f, high_f],
                    btype='band', output='sos', fs=sampling_rate)
    filtered_signal = sosfilt(filter, signal)
    return filtered_signal


def morlet_transform(signal, low_f, high_f, n_freqs=20, sampling_rate=1.0):
    """
    Morlet transforms the signal in a given frequency band, with given frequency resolution

    Parameters
    ---------------------
    signal

    low_f

    high_f

    n_freqs

    sampling_rate

    Returns
    ---------------------
    C:
    freq:
    """
    frequencies = np.linspace(low_f, high_f, n_freqs)/sampling_rate
    scales = scale2frequency('cmor1-0.5', frequencies)
    C, freq = cwt(signal, wavelet='cmor1-0.5', scales=scales,
                  sampling_period=1.0/sampling_rate)
    return C, freq


def power(signal, low_f, high_f, sampling_rate=1.0, n_freqs=20):
    '''
    '''
    C, freq = morlet_transform(
        signal, low_f, high_f, sampling_rate=sampling_rate, n_freqs=n_freqs)
    power = np.mean(abs(C), axis=0)
    return power
