from setuptools import setup
from setuptools import find_packages

with open('README_EN.md', "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name= "evdsts",
    author= "Burak Celik",
    author_email= "synertic@gmail.com",
    license= "MIT",
    version= "1.0rc4",
    description= "A Python implementation for retrieving and transforming macroeconomic time series data from TCMB EVDS (CBRT EDDS) API.",
    long_description= long_description,
    long_description_content_type='text/markdown',
    url= "",
    install_requires= [
        "pandas>=2.0.0",
        "requests>=2.12.5"
    ],
    keywords="macroeconomics, finance, econometrics, evds, edds, api, time series",
    packages=find_packages(exclude=['test*']),
    package_data={
        "evdsts.data": ['*.json']
    },
    exclude_package_data={"evdsts": ['*.json']},
    classifiers= [
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Turkish",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13"
    ],
    python_requires= ">=3.8"
)
