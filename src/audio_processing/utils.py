import numpy as np
import pywt
import time

def one_dimensional_binary_pattern(signal):
    """
    Convert a 1D signal to its binary pattern representation.
    """
    # Calculate the binary pattern by comparing each sample with the next
    binary_pattern = np.where(np.diff(signal) > 0, 1, 0)
    return binary_pattern

def wavelet_transform(signal, wavelet='db4', level=4):
    """
    Perform a wavelet transform on the signal and return coefficients up to the specified level.
    """
    coeffs = pywt.wavedec(signal, wavelet, level=level)
    return coeffs

def feature_extraction(signal):
    """
    Extract features from a single audio signal chunk.
    """
    # Perform wavelet transform on the audio chunk
    coeffs = wavelet_transform(signal, wavelet='db4', level=4)

    # Calculate the binary pattern for each wavelet level and normalize the concatenated features
    binary_patterns = [one_dimensional_binary_pattern(level) for level in coeffs]
    bp_features = np.concatenate(binary_patterns)
    bp_features_norm = bp_features / np.linalg.norm(bp_features)
    
    return bp_features_norm
