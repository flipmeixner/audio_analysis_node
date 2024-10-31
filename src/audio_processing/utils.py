#!/home/flip/python_envs/rover_env/bin/python
import numpy as np
import pywt
import librosa

import sys
print("Python interpreter:", sys.executable)

def one_dimensional_binary_pattern(signal):
    """
    Convert a 1D signal to its binary pattern representation.
    """
    # Calculate the binary pattern (compare each sample with the next)
    binary_pattern = np.where(np.diff(signal) > 0, 1, 0)

    return binary_pattern

def wavelet_transform(signal, wavelet='haar', level=1):
    """
    Perform a wavelet transform on the signal.
    """
    # Perform the wavelet transform
    coeffs = pywt.wavedec(signal, wavelet, level=level)

    return coeffs

def feature_extraction(filepath):
    features = []
    for file in filepath:
        signal, sr = librosa.load(file, sr=None)
        L1, L2, L3, L4, L5 = wavelet_transform(signal, wavelet='db4', level=4)
        # Calculate the binary pattern for each level
        bp_L1 = one_dimensional_binary_pattern(L1)
        bp_L2 = one_dimensional_binary_pattern(L2)
        bp_L3 = one_dimensional_binary_pattern(L3)
        bp_L4 = one_dimensional_binary_pattern(L4)
        bp_L5 = one_dimensional_binary_pattern(L5)

        bp_features = np.concatenate([bp_L1, bp_L2, bp_L3, bp_L4, bp_L5])
        bp_features_norm = bp_features / np.linalg.norm(bp_features)
        features.append(bp_features_norm)
    return features

