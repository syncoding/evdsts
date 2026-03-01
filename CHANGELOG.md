# <img src="https://github.com/syncoding/evdsts/blob/master/docs/images/evdsts.png?raw=true" width="5%"/> evdsts

## evdsts Changelog

### V.0.1.0
 - Doc Fix


### V.0.1.0
 - Searching logic enhanced as lowering the archive series scores
 - Searching returns the most 100 similar series as default
 - ´serialize´ parameter added to `get_main_categories´, ´get_sub_categories´, ´get_groups´ and ´get_series´



### V.0.1.0
 - EVDS 3.0 Compatibility
 - Turkish User Manual Added
 - Python 3.11 and 3.12 support has been dropped
 - Dependency Update: pandas >= 3.0.0
 - Dependenct Update: requests >= 2.32.5
 - New Dependency: tqdm (for index building progress monitoring)
 - Auto Resolve Level 1-2-3 Categories
 - Series Searching Enhanced
 - Building Duplicate Index Entries Fixed
 - Indexing Refactored (since the API keeps rate limiting the requests)
 - pandas int16 cast was returning negative category id's because of the overflow, fixed: int32
 - Index Building CLI script
 - Connection and Read Timeouts are Increased Again
 - Index Update
 - New Style Type Hinting
 - Various Small Bug Fixes


### V.1.0rc6
 - Python 3.8, 3.9 and 3.10 support has been dropped
 - Config has been migrated from setup.py to pyproject.toml
 - Index Update


### V.1.0rc5
 - Connection and read timeouts are increased


### V.1.0rc4
 - API SSL handshake fix
 - Pandas 2.0 method calls fix
 - Index update
 - Experimental Class LSModeller to perform LS Modelling, ADF and Cointegration tests

### V.1.0rc3
 - Reference tables fix
 - Internal class versioning
 - transformations and aggregations parsing fix


### V.1.0rc2
- Bug Fixes in documentation
- A Bug Fix in setup.py
- A small fix in Connector

### V.1.0rc1
- First release candidate.
