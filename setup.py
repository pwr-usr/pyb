from setuptools import setup, find_packages

setup(
    name='pyb',
    version='0.1.0',
    description='A package for retrieving fundamental data',
    author='Your Name',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'download_fundamental=pyb.scripts.download_fundamental:main',
            'download_stock_info=pyb.scripts.download_stock_info:main',
            'retrieve_fundamental_data=pyb.scripts.retrieve_fundamental_data:main'
        ]
    },
) 