from setuptools import setup, find_packages

setup(
    name='audio_analysis_node',
    version='0.0.1',
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'scikit-learn',
        'joblib',
        'pywavelets'
    ],
    description='Audio processing utilities for ROS',
)
