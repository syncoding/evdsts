# <img src="https://github.com/syncoding/evdsts/blob/master/docs/images/evdsts.png?raw=true" width="5%"/> evdsts

 [![PyPI version](https://badge.fury.io/py/evdsts.svg)](https://pypi.org/project/evdsts/)
 [![PyPI - Downloads](https://img.shields.io/pypi/dm/evdsts)](https://pypistats.org/packages/evdsts)
 [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/evdsts)](https://pypi.org/project/evdsts/)
 [![PyPI - Status](https://img.shields.io/pypi/status/evdsts)](https://pypi.org/project/evdsts/)
 [![GitHub - License](https://img.shields.io/github/license/syncoding/evdsts)](https://github.com/syncoding/evdsts/blob/master/LICENSE)
 [![GitHub issues](https://img.shields.io/github/issues-raw/syncoding/evdsts)](https://github.com/syncoding/evdsts/issues)
 [![GitHub top language](https://img.shields.io/github/languages/top/syncoding/evdsts)](https://github.com/syncoding/evdsts)
 [![GitHub Fork](https://img.shields.io/github/forks/syncoding/evdsts?style=social)](https://img.shields.io/github/forks/syncoding/evdsts?style=social)

## __The Purpose__

`evdsts` is a Python implementation for retrieving and transforming macroeconomic time series data from
__The Central Bank of Republic of Türkiye__ __Electronic Data Delivery System__ __(EDDS)__ API.
`evdsts` is designed for making both data retrieving and also time series analysis easy thanks to its
time series analysis ready outputs and other useful transformations.

## __The Overview__

`evdsts` is mainly designed for preparing the time series analysis ready datasets from the data
retrieved from __EDDS__. `evdsts` both makes the data retrieving easy and also allows you to start
working on data instantly with its advanced features that gives you complete control over the
retrieved data.

`evdsts` is consisted of two important classes:
1. `The Connector`: Responsible for processes such as; connecting to EDDS, data retrieving, data
renaming, etc.
2. `The Transformator`: Works co-integrated with the `Connector` and responsible for making some
useful transformations which can provide you a preliminary undestanding about the series you're
dealing with.

Some key features of `evdsts` are listed below:

- `evdsts` can perform instant transformations on retrieved data thanks to its `Transformator` class.
The Transformator is designed to co-work with `Connector` and perform a set of frequently used
transformations on retrieved data such as; z-score calculation, dummy series creation, outliers
detection, differentiation and others.
- You can search series by keywords in `evdsts` without any need for visiting EDDS website to find
series definitions you would like to retrieve from the service. Searches are done locally and gives
you instant results.
- `evdsts` ensures that all returned data can be used for mathematical operations instantly. That
guarantees no any `string` type is returned for a data type which actually represents a `datetime`,
`float` or `int` type.
- All retrieved data are converted to real time series automatically (optional, can be disabled)
- Requesting data from the API doesn't require remembering the complex series names definitions of
the original EDDS database to retrieve them. `evdsts` allows you to assign meaningful names to
the series such as; _cppi_, _ir_, _gdp_ and _usdtry_, and these assigned names can be used when
retrieving data from the EDDS later on. User assigned names are called reference names, and they
are permanent once they are assigned to series unless they're changed or deleted. Additionally,
current reference names in a project can be transferred to new projects easily.
- All parameters belong to transformation and aggregation functions and frequencies are renamed in
a meaningful manner like `daily`, `quarterly`, `percent`, `diff`, `max`, etc. and these definitions
are used as parameters for retrieving data from the API service. Therefore, there is no need to know
original API's complex parameter definitions for transformation or aggregation functions or time
series frequencies anymore.
- `evdsts` detects many kinds of errors and warns you before a connection request is made.
This allows you to know why the data would not be able to be retrieved with provided parameters, or,
about emerged ambiguities which are arisen from the provided parameter sets.
- `evdsts` allows you to make useful data transformations such as higher order differentiations
or log-returns that are originally not supported by the API, but is used for time series analysis
frequently.
- All types of retrieved data can be returned in `DataFrame`, `JSON` or `dict` types optionally.
- All retrieved data can be written on disk in `JSON`, `CSV` and `XLS` formats in order to store and
use them later, or in other softwares such as R, EViews, SAS or RATS.
- All functions and class methods are fully annotated and you can get peak hints for everything you
need to use while working with Spyder IDE, Pycharm, VS Code or Jupyter.
- All types in source code are annotated (and commented) to make working easy on source code for
developers.

## __Documentation__

Please see [__THE USER MANUAL__](https://github.com/syncoding/evdsts/blob/master/docs/manuals/manual_en.md) for detailed explanations about how to get an API key from the EDDS and use `evdsts`

## __Examples__ [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/syncoding/evdsts/blob/master/examples/examples.ipynb)

Please download the [__Jupyter Notebook Application__](https://github.com/syncoding/evdsts/blob/master/examples) that covers the main use cases of `evdsts`,
or alternatively open it on __Google Colab__ by clicking the _Open in Colab_ link above.

## __Dependencies__

`evdsts` is a __Python 3__ only project and depends on below packages:

1. cpython >= 3.6.15 (or equivalent PyPy distribution)
1. pandas >= 0.25.3
2. requests >= 2.12.5

## __Additional Requirements__

[openpyxl](https://pypi.org/project/openpyxl/) is required if you would like to write data on disk
in MS Excel format. openpyxl is not required if you don't think working with MS Excel files.

## __Installation__

Stable version of `evdsts` is available on GitHub, PyPI and conda-forge and can be installed
following one of the below ways:

### __PyPI__

```
pip install evdsts
```

### __GitHub__

```
pip install git+https://github.com/syncoding/evdsts.git
```

### __Conda__

```
conda install evdsts -c conda-forge
```

## __Source Code__

[GitHub](https://github.com/syncoding/evdsts/evdsts)

## __Changelog__

[__Changelog__](https://github.com/syncoding/evdsts/blob/master/CHANGELOG.md)

## __License__

[__MIT__](https://github.com/syncoding/evdsts/blob/master/LICENSE.txt)

## __Contact__

<a href="mailto:synertic@gmail.com?"><img src="https://img.shields.io/badge/gmail-%23DD0031.svg?&style=for-the-badge&logo=gmail&logoColor=white"/></a>