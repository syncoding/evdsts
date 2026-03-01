<p align="center">
  <img src="https://github.com/syncoding/evdsts/blob/master/docs/images/evdsts.png?raw=true" width="120"/>
</p>

<h1 align="center">evdsts</h1>

<p align="center">
  <strong>Macroeconomic time series toolkit for TCMB EVDS (CBRT EDDS)</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/evdsts/"><img src="https://badge.fury.io/py/evdsts.svg" alt="PyPI version"></a>
  <a href="https://pypistats.org/packages/evdsts"><img src="https://img.shields.io/pypi/dm/evdsts" alt="Downloads"></a>
  <a href="https://pypi.org/project/evdsts/"><img src="https://img.shields.io/pypi/pyversions/evdsts" alt="Python Version"></a>
  <a href="https://pypi.org/project/evdsts/"><img src="https://img.shields.io/pypi/status/evdsts" alt="Status"></a>
  <a href="https://github.com/syncoding/evdsts/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/syncoding/evdsts" alt="License"></a>
  <a href="https://github.com/syncoding/evdsts/issues"><img src="https://img.shields.io/github/issues-raw/syncoding/evdsts" alt="Issues"></a>
  <a href="https://github.com/syncoding/evdsts"><img src="https://img.shields.io/github/languages/top/syncoding/evdsts" alt="Top Language"></a>
  <a href="https://github.com/syncoding/evdsts"><img src="https://img.shields.io/github/forks/syncoding/evdsts?style=social" alt="Forks"></a>
</p>

---

## The Purpose

`evdsts` is a Python implementation for retrieving and transforming macroeconomic time series data from
**The Central Bank of Republic of Turkiye** **Electronic Data Delivery System** **(EDDS)** API.
`evdsts` is designed for making both data retrieving and also time series analysis easy thanks to its
time series analysis ready outputs and other useful transformations.

## Overview

`evdsts` is mainly designed for preparing the time series analysis ready datasets from the data
retrieved from **EDDS**. `evdsts` both makes the data retrieving easy and also allows you to start
working on data instantly with its advanced features that gives you complete control over the
retrieved data.

`evdsts` is consisted of two important classes:

| Class | Responsibility |
|:------|:---------------|
| **Connector** | Connecting to EDDS, data retrieving, data renaming, etc. |
| **Transformator** | Co-integrated transformations such as z-score, dummies, outliers, differencing and more. |

### Key Features

- **In-situ search** -- search series by keywords without leaving Python; results are instant and local.
- **Analysis-ready outputs** -- every returned value is guaranteed to be a proper numeric or datetime type, never a raw string.
- **Auto time-series indexing** -- retrieved data are converted to real pandas DatetimeIndex series automatically (optional).
- **Reference names** -- assign memorable aliases like `usdtry` or `cppi` to complex EDDS codes; aliases are permanent and portable across projects.
- **Human-readable parameters** -- use `daily`, `quarterly`, `percent`, `diff`, `max` instead of cryptic API codes.
- **Pre-flight validation** -- many parameter errors are caught before any network request is made.
- **Extended transformations** -- log-returns, higher-order differences and other operations not natively supported by the API.
- **Flexible output** -- get results as `DataFrame`, `JSON` or `dict`; write to disk as CSV, JSON or XLS.
- **CLI support** -- rebuild search indexes from the command line with `evdsts build-index`.
- **Fully annotated** -- type hints and docstrings everywhere for IDE autocompletion and quick help.

## Quick Start

```python
from evdsts import Connector

connector = Connector("YOUR_API_KEY", language="EN")

# search for a series
connector.where("consumer price index")

# retrieve data
cpi = connector.get_series("TP.FE.OKTG01", start_date="01.01.2020")

# retrieve multiple series
rates = connector.get_series(
    "TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
    start_date="01.01.2023",
    frequency="M",
    transformations="percent",
)
```

## CLI Usage

```bash
# rebuild the search index
evdsts build-index --language ENG -y

# see all options
evdsts build-index --help
```

## Documentation

Please see [**THE USER MANUAL**](https://github.com/syncoding/evdsts/blob/master/docs/manuals/manual_en.md) for detailed explanations about how to get an API key from the EDDS and use `evdsts`.

## Examples [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/syncoding/evdsts/blob/master/examples/examples.ipynb)

Download the [**Jupyter Notebook Application**](https://github.com/syncoding/evdsts/blob/master/examples) that covers the main use cases of `evdsts`,
or alternatively open it on **Google Colab** by clicking the *Open in Colab* badge above.

## Installation

Stable version of `evdsts` is available on GitHub, PyPI and conda-forge.

```bash
# PyPI
pip install evdsts

# GitHub
pip install git+https://github.com/syncoding/evdsts.git

# Conda
conda install evdsts -c conda-forge
```

## Dependencies

| Package | Version |
|:--------|:--------|
| Python | >= 3.13 |
| pandas | >= 3.0.0 |
| requests | >= 2.32.5 |
| tqdm | >= 4.67.3 |

> [openpyxl](https://pypi.org/project/openpyxl/) is additionally required if you want to write data in MS Excel format.

## Links

| | |
|:--|:--|
| Source Code | [GitHub](https://github.com/syncoding/evdsts/blob/master/evdsts) |
| Changelog | [CHANGELOG.md](https://github.com/syncoding/evdsts/blob/master/CHANGELOG.md) |
| License | [MIT](https://github.com/syncoding/evdsts/blob/master/LICENSE.txt) |

## Contact

<a href="mailto:synertic@gmail.com?"><img src="https://img.shields.io/badge/gmail-%23DD0031.svg?&style=for-the-badge&logo=gmail&logoColor=white"/></a>
