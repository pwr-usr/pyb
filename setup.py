"""
Setup file for financial_analysis package.
"""

from setuptools import setup, find_packages

setup(
    name="financial_analysis",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "bt>=0.2.9",
        "pyb",  # Add appropriate version if known
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A modular package for financial ratio analysis",
    keywords="finance, ratio, analysis, backtest",
    python_requires=">=3.6",
) 