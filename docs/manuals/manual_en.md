# <img src="https://github.com/syncoding/evdsts/blob/master/docs/images/evdsts.png?raw=true" width="5%"/> evdsts

## USER MANUAL - EN - V.1.R.0

- ## [__Getting an API Key from the EDDS__](#getting-an-api-key-from-edds)
- ## [__The Connector Basics__](#the-basics-1)
    - ### [__Importing the Connector and Creating an Instance__](#importing-connector)
    - ### [__Saving Your API Key for Future Use__](#save-the-key)
    - ### [__Searching Into Database for Series Name Definition of EDDS__](#searching-into-database)
    - ### [__Listing Main Data Categories on EDDS__](#listing-main-cat)
    - ### [__Listing Sub-Categories in Main Categories__](#listing-sub-cat)
    - ### [__Listing Groups Belong to Sub-Categories__](#listing-groups)
    - ### [__Retrieving Singular Time Series__](#getting-singular)
    - ### [__Retrieving Multi-Dimentional Time Series__](#getting-multi)
- ## [__Advanced Features__](#the-advanced-1)
    - ### [__Time Series Indexing__](#ts-indexing)
    - ### [__Selecting Different Frequency for Time Series Requested__](#selecting-different-frequency)
    - ### [__Selecting Transformation Function(s) for Time Series Requested__](#selecting-transformation)
    - ### [__Selecting Aggregation Function(s) for Time Series Requested__](#selecting-aggregation)
    - ### [__Retrieving Raw Data in JSON Format__](#retrieving-raw-data)
    - ### [__Assigning New Names for Retrieved Time Series__](#assigning-new-names)
        - ### [__Assigning New Names for Bare Series Requests__](#assigning-new-names-bare)
        - ### [__Assigning New Names for Transformed or Aggregated Series Requests__](#assigning-new-names-transagg)
    - ### [__Writing Series on Disk__](#writing-series)
    - ### [__Updating Local Search Index__](#updating-index)
- ## [__Using Reference Names to Retrieve Time Series__](#using-reference-names)
    - ### [__Saving Reference Name While Retrieving Time Series__](#saving-reference-name)
    - ### [__Saving Reference Names Directly__](#saving-names-directly)
    - ### [__Transferring Given Reference Names to Other Projects__](#transferring-reference-names)
- ## [__The Transformator__](#the-transformator-1)
    - ### [__Renaming Series Names with Transformator__](#rename-series)
    - ### [__Fixing The Floating-Point Numbers Precision with Transformator__](#trans-precision)
    - ### [__Differentiation: D(y<sub>t</sub>, i) = y<sub>t</sub> - y<sub>t-i</sub> = (1-L)<sup>i</sup>y<sub>t</sub>__](#regular-diff)
    - ### [__Natural Logarithmic Transformation: ln(y<sub>t</sub>)__](#log-transform)
    - ### [__Logarithmic Difference (LogReturn): D(ln(y<sub>t</sub>), i) = ln(y<sub>t</sub>) - ln(y<sub>t-i</sub>) = (1-L)<sup>i</sup>ln(y<sub>t</sub>)__](#logaritmic-diff)
    - ### [__Deterministic Trend: y<sub>t</sub> = β<sub>0</sub> + β<sub>1</sub>Trend + β<sub>2</sub>Trend<sup>2</sup> + ... β<sub>n</sub>Trend<sup>n</sup> + ε<sub>t</sub>__](#deterministic-trend)
    - ### [__Decompose: y<sub>t</sub> - (β<sub>0</sub> + β<sub>1</sub>Trend + β<sub>2</sub>Trend<sup>2</sup> + ... β<sub>n</sub>Trend<sup>n</sup> + ε<sub>t</sub>)__](#de-trend)
    - ### [__Simple Moving Average: MA<sub>t</sub> = (y<sub>t</sub> + y<sub>t-1</sub> ... y<sub>t-n</sub>) / n__](#smooth-sma)
    - ### [__Exponential Moving Average: EMA<sub>t</sub> = αy<sub>t</sub> + (1-α)EMA<sub>t-1</sub>__](#smooth-ema)
    - ### [__Rolling Var: ROLVAR<sub>t</sub> = σ<sup>2</sup>(y<sub>t</sub>, y<sub>t-1</sub> ... y<sub>t-n</sub>)__](#detect-rollvar)
    - ### [__Rolling Correlations: ROLCORR<sub>t</sub> = ρ(y<sub>t-n</sub>, x<sub>t-n</sub>)__](#detect-rollcorr)
    - ### [__Cumulative Sum: Cusum<sub>t</sub> = 𝚺(y<sub>t</sub>, y<sub>t-1</sub> ... y<sub>t-n</sub>)__](#get-cusum)
    - ### [__Z-Score: Z<sub>t</sub> = (y<sub>t</sub> - ȳ) / σ<sub>y</sub>__](#get-z-score)
    - ### [__Median Absolute Deviation: MAD<sub>t</sub> = median(|y<sub>t</sub> - median(y<sub>t</sub>)|)__](#get-mad)
    - ### [__Normalized Series: y<sub>t, normal</sub> = F(y<sub>t</sub>)__](#get-normalized)
    - ### [__Dummy Series: D<sub>n</sub>__](#get-dummies)
    - ### [__Lagged Series: y<sub>t-1</sub>, y<sub>t-2</sub> ... y<sub>t-n</sub>__](#get-laggeds)
    - ### [__Correlation Coefficients: ρ(y<sub>t</sub>, x<sub>t</sub>)__](#get-corr)
    - ### [__Autocorrelation Coefficients: AUTOCORR<sub>t</sub> = ρ<sub>t, t-n</sub>__](#get-auto-corr)
    - ### [__Serial Correlation Coefficients: SERIALCORR<sub>t</sub> = ρ<sub>t, x-n</sub>__](#get-serial-corr)
    - ### [__Outliers__](#get-outliers)
    - ### [__Smoothed Series__](#get-smoothed)
## [__Joining The Connector and Transformator Methods__](#joining-methods)
## [__Defined Exceptions__](#defined-exceptions-1)


<a id="getting-an-api-key-from-edds"></a>

### __Getting an API Key from EDDS__

Please follow the below instructions to obtain the required API key to connect EVDS:


1. Open EDDS website. [__EDDS__](https://evds2.tcmb.gov.tr/index.php?/evds/login)
2. You can change the website language by clicking __`EN`__ on the upper right bar.
3. Click __`SIGN UP`__ button on current page.
4. Fill up the form with requested information and register.
5. Check for incoming mails from the inbox that belongs to e-mail address you used for  
   EDDS membership, and verify your e-mail address via the received e-mail.
6. Open the same page and log into your account.
7. Click on your username and then click __`Profile`__ on opened sliding menu.
8. You can get your API key by clicking __`API Key`__ on newly opened page.


<a id="the-basics-1"></a>

## __The Connector Basics__

`evdsts` is comprised of two important classes:  
1. __`Connector`__: Responsible for connecting to EDDS, and retrieving time series.
2. __`Transformator`__: Responsible for making useful transformations and other manipulations on
retrieved data.

Here we're going to tackle with basic data fetching and related processes with `evdsts`, and therefore
the `Connector`


<a id="importing-connector"></a>

### [__Importing the Connector and Creating an Instance__](#connector-instance)
### [__Saving Your API Key for Future Use__](#save-the-key)
### [__Searching Into Database for Series Name Definition of EDDS__](#searching-into-database)
### [__Listing Main Data Categories on EDDS__](#listing-main-cat)
### [__Listing Sub-Categories in Main Categories__](#listing-sub-cat)
### [__Listing Groups Belong to Sub-Categories__](#listing-groups)
### [__Retrieving Singular Time Series__](#getting-singular)
### [__Retrieving Multi-Dimentional Time Series__](#getting-multi)


<a id="connector-instance"></a>

### __Importing the Connector and Creating an Instance__

You'll need to import __`Connector`__ class from `evdsts` into your project in order to retrieve
time series from EDDS.

```python
from evdsts import Connector
```
and then you can create an instance of `Connector` using your API key like below:

```python
connector = Connector('YOUR_API_KEY', language='EN')  # Default language is TR
```
several additional parameters can be used while instantiating the `Connector` class. The full
fingerprint of the class initialization options is given below:

```python
def __init__(
                key: Optional[str] = None,
                language: str = "TR",
                show_links: bool = False,
                proxy_servers: Optional[Dict[str, str]] = None,
                verify_certificates: bool = True,
                jupyter_mode: bool = False,
                precision: Optional[int] = None
) -> None:

```

1. `key`: API key supplied by __EVDS (EDDS)__
2. `language`: Interface language (if available).
    - Current supported languages are:
        - Turkce: `TUR`, `tur`, `TR`, `tr`
        - English: `ENG`, `eng`, `EN`, `en`  
    Defaults to `TR`
3. `show_links`: shows the current URL to be connected. Defaults to `False`
4. `proxy_servers`: for users who would like to connect the service behind a proxy server.
Proxy servers must be given in a `dict` container like:   
`{"http": "127.0.0.1", "https": "127.0.0.1"}`  
Defaults to `None`
5. `verify_certificates`: A `True/False` flag for Enabling/Disabling of SSL security certificate
checking of the server during connection. Defaults to `True`
6. `jupyter_mode`: Enables/Disables `Jupyter Notebook` mode for better representation on-screen.
    - `True`:
        - screen floating-point precision: __2__  
        (note this only affects the precision of screen representation. The internal operational
        precision either comes from the EDDS service itself, or the internal precision is eqaul to
        user provided precision if a fixed precision is given by the `precision` parameter.
        - Maximum `pandas` `DataFrame` object columns to be showed on screen: __6__
    - `False`: No screen representation optimizations.  
    Defaults to `None`
7. `precision`: The operational precision of floating-point numbers.
    - integer value: floating-point precisions are set to given value. for instance:
    `1907.72231162012281817` is truncated to `1907.72` if the given precision is `2`, or, `72.1907`
    is truncated to `72` if the given precision is `0`
    - None: precision is set to original precision returned from the EDDS.
    Defaults to `None`

__Cases__:

```python
# simple initialization
connector = Connector('YOUR_API_KEY', language='EN')

# Shows the url the connector tries to connect
connector = Connector('YOUR_API_KEY', language='EN', show_links=True)

# connection behind a proxy
proxies = {"http": "127.0.0.1", "https": "127.0.0.1"}
connector = Connector('YOUR_API_KEY', language='EN', proxy_server=proxies)

# Disables SSL certificate verification for connected server
connector = Connector('YOUR_API_KEY', language='EN', verify_certificates=False)

# Jupyter Notebook mode for better screen representations on Jupyter. This only affects screen
# representations.
connector = Connector('YOUR_API_KEY', language='EN', jupyter_mode=True)

# sets precision to 2 for all retrieved series. This affects both screen representation and also
# internal calculations.
connector = Connector('YOUR_API_KEY', language='EN', precision=2)
```


<a id="save-the-key"></a>

### __Saving Your API Key for Future Use__

You don't need to use your API Key for everytime you start your application. You can save your api
key on disk in order not to use the api key for further initializations of the `Connector`. You
can use `save_key()` method to save your current key on disk.

```python
connector = Connector('YOUR_API_KEY', language='EN')
connector.save_key()  # now you don't need to use your api key for your current project anymore.
```

you can instantiate a `Connector` class without using your api key once you save your key to disk.

```python
connector = Connector(language='EN')  # your key is read from the disk here.
```


<a id="searching-into-database"></a>

### __Searching Into Database for Series Name Definition of EDDS__

You don't need to visit the EDDS website to find out what is the name identification of the EDDS
for the series you would like to retrieve. You can search series names by keywords without leaving
the `evdsts` thanks to `where()` method.

The fingerprint of the `where()` method is:

```python
def where(keyword: str, n: int = 5, verbose: bool = True) -> Dict[str, str]
```

1. `keyword`: words to be searched (for instance: consumer price index)
2. `verbose`: Shows the results on screen if `True`. Defaults to `True`.
3. `n`: Number of maxiumum related results to be returned . Defaults to `5`.


__Cases (EN)__:

```python
connector = Connector(language="EN")    # Assuming you have already saved your API Key on disk.
connector.where("consumer price index") # search takes around 0.5 seconds.
```

The search above gives the below output:

```
5 most relevant results for 'consumer price index' are shown below.

                                                 Search Results                                                 
----------------------------------------------------------------------------------------------------------------
Series Code          Series Name                                                     Frequency        Start Date 
----------------------------------------------------------------------------------------------------------------
TP.FE.OKTG01         Consumer Price Index                                            MONTHLY          01-01-2003 
TP.MK.F.BILESIK.TUM  (PRICE INDICES) BIST All Shares-100 Index (XTUMY), According to BUSINESS DAILY   02-01-2009 
TP.MK.G.BILESIK.TUM  (RETURN INDICES) BIST All Shares-100 Index (XTUMY_CFNNTLTL), Ac BUSINESS DAILY   02-01-2009 
TP.FG.T63            Istanbul Wholesale Price Index (1963=100)(ICC)                  MONTHLY          01-01-1963 
TP.FG.T68            Istanbul Wholesale Price Index (1968=100)(ICC)                  MONTHLY          01-01-1968 
----------------------------------------------------------------------------------------------------------------
```

> The __5__ closest results are shown as default when you look up series names, however you can set `n`
> parameter to see the `n` closest results. For instance; `connector.where("consumer price index", 10)`
> shows the 10 closest results for the statement: _consumer price index_.

> `where()` method also returns a `dict` object consists of all results of the performed search
> without any truncation.

```python
# all search results are assigned to 'all_results' variable without any truncation. This is a
# dictionary mades up of Dict[Series Code, List[Series Name, Series Frequency, Series Start Date]]
all_results = connector.where("consumer price index")
```

__Cases (TR)__:

```python
connector = Connector()                   # Assuming you have already saved your API Key on disk.
connector.where("tüketici fiyat endeksi") # search takes around 0.5 seconds.
```

```
5 most relevant results for 'tüketici fiyat endeksi' are shown below.

                                                 Search Results                                                 
----------------------------------------------------------------------------------------------------------------
Series Code          Series Name                                                     Frequency        Start Date 
----------------------------------------------------------------------------------------------------------------
TP.FE.OKTG01         Tüketici Fiyat Endeksi (Genel)                                  AYLIK            01-01-2003 
TP.MK.F.BILESIK.TUM  (FİYAT) BİST Tüm-100 Endeksi (XTUMY), Kapanış Fiyatlarına Göre  İŞ GÜNÜ          02-01-2009 
TP.MK.F.HIZMET       (FİYAT) BİST Hizmet Endeksi (XUHIZ), Kapanış Fiyatlarına Göre ( İŞ GÜNÜ          02-01-1997 
TP.MK.F.TEKNOLOJI    (FİYAT) BİST Teknoloji Endeksi (XUTEK), Kapanış Fiyatlarına Gör İŞ GÜNÜ          30-06-2000 
TP.TUFE1YI.T1        1.Yurt İçi Üretici Fiyat Endeksi                                AYLIK            01-01-1982 
----------------------------------------------------------------------------------------------------------------
```

This output is returned as a `Dict` without any truncation on results which can be assigned into a
variable.

```python
# all search results are assigned to 'all_results' variable without any truncation. This is a
# dictionary mades up of Dict[Series Code, List[Series Name, Series Frequency, Series Start Date]]
all_results = connector.where("tüketici fiyat endeksi")
```

<a id="listing-main-cat"></a>

### __Listing Main Data Categories on EDDS__

You can use `get_main_categories()` method to retrieve main data categories of all data which are
stored in EDDS database. The returned type defaults to pandas `DataFrame`, however, you can get the
main categories in a `dict` or as `json` format if you prefer to.

The fingerprint of `get_main_categories` is:

```python
def get_main_categories(
                        as_dict: bool = False,
                        raw: bool = False,
) -> Union[pd.DataFrame, JSONType, Dict]:
```

1. `as_dict`: Returns main categories as a dictionary
        - forming {CATEGORY_ID: category_name}.
Defaults to False.
2. `raw`: returns untouched `JSON` object retrieved from EVDS Service instead of processed types.
Defaults to `False`

__Cases__:

```python
main_categories = connector.get_main_categories()
print(main_categories)

# this gives you a pandas DataFrame object representing below.
```

|Index| CATEGORY ID|                       TITILE                                    |
|:---: |:---:       |----------------------------------------------------------------|
|0	   |     1	    | MARKET STATISTICS                                              |
|1	   |     2	    | EXCHANGE RATES                                                 |
|2	   |     3	    | INTEREST RATES                                                 |
|3	   |     4	    | MONEY AND BANKING STATISTICS                                   |
|4	   |     5	    | WEEKLY SECURITIES STATISTICS                                   |
|5	   |     12	    | FINANCIAL STATISTICS                                           |
|6	   |     13	    | CBRT BALANCE SHEET DATA                                        |
|7	   |     14	    | PRICE INDICES                                                  |
|8	   |     15	    | SURVEYS                                                        |
|9	   |     18	    | BALANCE OF PAYMENTS INTERNATIONAL INVESTMENT POSITION          |
|10    |     19	    | FOREIGN TRADE STATISTICS                                       |
|11    |     20	    | PUBLIC FINANCE                                                 |
|12    |     21	    | PRODUCTION STATISTICS                                          |
|13    |     22	    | PAYMENT SYSTEMS AND EMISSION                                   |
|14    |     23	    | EMPLOYMENT STATISTICS                                          |
|15    |     6	    | EXTERNAL DEBT                                                  |
|16    |     7	    | DEPOSITS AND PARTICIPATION FUNDS SUBJECT TO REQUIRED RESERVES  |
|17    |     24	    | BIS COMPARATIVE COUNTRY STATISTICS                             |
|18    |     25	    | GOLD STATISTICS                                                |
|19    |     26	    | HOUSING AND CONSTRUCTION STATISTICS                            |
|20    |     27	    | FINANCIAL ACCOUNTS                                             |
|21    |     28	    | TOURISM STATISTICS                                             |
|22    |     95	    | EVDS USAGE STATISTICS                                          |


Main categories can be also requested as processed Python dictionaries or JSON strings. You can set
`as_dict` flag `True`to get the retrieved data in `Dict` type, or similarly, you can use `raw` flag
to get the main categories as a JSON string.

```python
# dictionary
main_dict = connector.get_main_categories(as_dict=True)

# JSON string
main_raw = connector.get_main_categories(raw=True)
```


<a id="listing-sub-cat"></a>

### __Listing Sub-Categories in Main Categories__

sub-categories can be listed by supplying main category IDs or main category names to the
`get_sub_categories()` method. sub-categories are returned as pandas `DataFrames` in its default
setting, however, you can get the sub-categories in a `dict` or as `json` format if you prefer to.

The fingerprint of `get_sub_categories()` is:

```python
def get_sub_categories(
                        main_category: Union[int, str],
                        as_dict: bool = False,
                        raw: bool = False,
                        verbose: bool = False,
) -> Union[pd.DataFrame, JSONType, Dict]:
```

1. `main_category`: Could be a main category ID or an actual main category name.
        - integer number: returns sub-categories which given value corresponds to main category ID.
        - string: returns sub-categories which belongs to given main category name.
2. `as_dict`: Returns a dictionary forming {datagroup_code: datagroup_name}
Defaults to `False`
3. `raw`: returns untouched JSON object retrieved from EVDS Service instead of processed types.
Defaults to `False`
4. `verbose`: a detailed version of retrieved data. Defaults to `False`.

__Cases__:

```python
# (2 = EXCHANGE RATES) according to Category ID section of main categories table.
exchange_rates_sub = connector.get_sub_categories(2)

```

This gives you a `DataFrame` representin below:

|DATAGROUP_CODE  | CATEGORY_ID  |...    |START_DATE	|END_DATE   |
|----------------|--------------|-------|-----------|-----------|
|	bie_dkdovytl  |	    2	    |...	|1950-01-02	|2022-08-01 |
|	bie_dkefkytl  |	    2	    |...	|1990-01-02	|2022-08-01 |
|	bie_dkkurbil  |	    2	    |...	|2009-04-02	|2021-12-21 |
|	bie_rktufey   |	    2	    |...	|1994-01-01	|2022-06-01 |
|	bie_rkufey    |	    2	    |...	|1994-01-01	|2022-06-01 |
|	bie_redkurigm |	    2	    |...	|2003-01-01	|2021-01-01 |

> Note: above table includes more columns but is truncated for data to be fitted the screen.

or as an alternative you can use the main category names to get the same sub-categories data.

```python
exchange_rates_sub = connector.get_sub_categories("EXCHANGE RATES")

```
> __Please note that the process is case-sensitive, therefore, the category names must be used__
> __exactly as appeared in main categories.__

sub-categories can be returned as `dictionary` objects, raw `JSON` or as a detailed version of
the `DataFrame` sheet.

```python
# as dictionary
sub_dict = connector.get_sub_categories("PRODUCTION STATISTICS", as_dict=True)

# as raw JSON
sub_raw = connector.get_sub_categories("PRODUCTION STATISTICS", raw=True)

# # as a more detailed version of DataFrame that includes all information on EDDS
sub_detailed = connector.get_sub_categories("PRODUCTION STATISTICS", verbose=True)

# and a combined version of above.
rates_all = connector.get_sub_categories("EXCHANGE RATES", as_dict=True, verbose=True)
```


<a id="listing-groups"></a>

### __Listing Groups Belong to Sub-Categories__

Groups belong to sub-categories can be called by giving related sub-category name as parameter to the
`get_groups()` method. Groups are returned as pandas `DataFrames` in its default setting,
however, you can get the sub-categories in a `dict` or as `json` format if you prefer to.

The fingerprint of `get_groups()` is:

```python
def get_groups(
                data_group_code: str,
                as_dict: bool = False,
                raw: bool = False,
                verbose: bool = False,
                parse_dt: bool = False
) -> Union[pd.DataFrame, JSONType, Dict]:
```

1. `data_group_code`: Code of the sub-category the data requested for.
2. `as_dict`: Returns a dictionary forming {series_code: series_name}  
            Defaults to `False`
3. `raw`: returns untouched JSON object retrieved from EVDS Service instead of processed types.  
Defaults to `False`
4. `verbose`: A very detailed version of the group data.  
Defaults to False.
5. `parse_dt`: The option for date-time fields representation.
    - `True`: datetime fields in returned dictionary are converted to Python date object.
    - `False`: datetime fields in returned dictionary are returned as is (string)  
Defaults to `False`

__Cases__:

```python
group_effectives = connector.get_groups("bie_dkdovytl")
```

|SERIE_NAME_ENG	            |SERIE_CODE	    |FREQUENCY_STR    |START_DATE   |END_DATE  |
|---------------------------|---------------|-----------------|-------------|----------|
|(USD) US Dollar (Buying)	|TP.DK.USD.A.YTL|	DAILY	      |1950-01-02	|2022-08-01|
|(USD) US Dollar (Selling)	|TP.DK.USD.S.YTL|	DAILY	      |1950-01-02	|2022-08-01|
|(EUR) Euro (Buying)	    |TP.DK.EUR.A.YTL|	DAILY	      |1999-01-04	|2022-08-01|
|(EUR) Euro (Selling)	    |TP.DK.EUR.S.YTL|	DAILY	      |1999-01-04	|2022-08-01|

> Note: above table includes more rows but is truncated for data to be fitted the screen.

Groups can also be requested as `dict` type objects or `JSON` type raw data. In addition, a more detailed
data belong to groups can be retrieved with the flag `verbose`.

```python
# as dictionary
groups_dict = connector.get_groups("bie_gsyhgycf", as_dict=True)

# as JSON
groups_raw = connector.get_groups("bie_gsyhgycf", raw=True)

# a more detailed version of groups data can be requested with 'verbose' flag.
detailed_groups = connector.get_groups("bie_gsyhgycf", verbose=True)

# groups can also be requested as a detailed dict supplying both 'verbose' and 'as_dict' flags
# together.
detailed_dict = connector.get_groups("bie_gsyhgycf", as_dict=True, verbose=True)
```


<a id="getting-singular"></a>

### __Retrieving Singular Time Series__

Retrieving singular time series data is done with `get_series()` method:

> `evdsts` ensures that all returned data can be used for mathematical operations instantly. That is
> guaranteed through applying a series of transformations to the retrieved data before returning it
> to the user. in other words, `evdsts` never returns a `string` (or `object` in pandas' terms) type
> data which actually represents a floating-point or an integer number. All `floating` data are
> transformed to `float32` type before they are returned. As for `strings` that don't represent
> actual numbers; they are all transformed to `NaN`'s that doesn't affect mathematical integrity.
> This approach provides a great advantage in practice since all series returned from the `evdsts`
> can instantly be used for mathematical operations without a need of any further process.

The fingerpring of the `get_series()` is:

```python
def get_series(
                series: Union[str, Sequence[str]],
                start_date: Optional[Union[str, datetime]] = None,
                end_date: Optional[Union[str, datetime, pd.Timestamp]] = None,
                period: Optional[str] = None,
                aggregations: Optional[Union[str, List[str], Tuple[str]]] = None,
                transformations: Optional[Union[str, List[str], Tuple[str]]] = None,
                keep_originals: bool = True,
                frequency: Optional[Union[str, int]] = None,
                new_names: Optional[Sequence[str]] = None,
                keep_references: bool = False,
                time_series: bool = True,
                ascending: bool = True,
                raw: bool = False,
                as_dict: bool = False,
                convert_to_bd: bool = True
) -> Union[pd.DataFrame, JSONType, Dict]:
```

1. `series`: Time Series names that are requested from the EVDS API server.
    - Series names can be provided as original EVDS service assigned names or reference names that
    was saved as name references before.
        - names can be given in several ways:
            - Comma separated string: "usdtry, eurtry"
            - Space separated string: "usdtry eurtry"
            - In a Sequence type container like a list or tuple: ["usdtry", eurtry] or ("usdtry", "eurtry")
2. `start_date`: The date the time series data are started from. Defaults to `None`
    - `None` or not specified: `start_date` will be set to current date.
    - Could be given as a string in fromat `dd-mm-YYYY`, `dd.mm.YYYY`, `dd/mm/YYYY`
    - Could be given as a Python `datetime` object.
    - Could be given as a Pandas `TimeStamp` object
3. `end_date`: The last observation date for requested time series. Defaults to `None`
    - `None` or not specified: `end_date` will be set to current date.
    - Could be given as a string in fromat `dd-mm-YYYY`, `dd.mm.YYYY`, `dd/mm/YYYY`
    - Could be given as a Python `datetime` object.
    - Could be given as a Pandas `TimeStamp` object.
4. `period`: A period string represents a period from current date. Defaults to `None`.
    - period strings consist of a num and a date identifier part. Num part can be any
    integer number and the date part is a letter reflecting day, week, month and year.
    The letters are the first letters of Turkish and English period identifiers.`period` can not be
    used together with `start_date` or `end_date`.
    - `1d` or `1g` -> represent the period: from 1 day ago - today, examples: `2d`, `7d`, `30d`
    - `1w` or `1h` -> represent the period: from 1 week ago - today, examples: `2w`, `7w`, `30w`
    - `1m` or `1a` -> represent the period: from 1 month ago - today, examples: `2m`, `7m`, `12m`
    - `1y` -> represent the period: from 1 year ago - today, examples: `2y`, `7y`, `30y`
5. `aggregations`: Aggregation functions wich will be applied to time series before returning.
Defaults to `None`
    - `None` or not specified: No aggregation function is applied to time series.
    - Given as `string`: Same aggregation function is applied to all given time series.
    - Given as `List` or `Tuple` types: Different aggregation functions are applied to the time series
    in given order.
        - Available aggregation functions:
            - Mean: `avg`
            - Minimum: `min`
            - Maximum: `max`
            - First: `first`
            - Last: `last`
            - Cumulative Sum: `sum`
6. `transformations`: Transformation functions that will be applied to time series before returning.
Defaults to `None`
    - `None` or not specified: No transformation is applied to time series.
    - Given as `string`: Same transformation is applied to all given time series.
    - Given as `List` or `Tuple` types: Different transformations are applied to the time series in
    given order.
        - Available transformation functions:
            - Level: `level`
            - Percentage change: `percent`
            - Difference: `diff`
            - Yearly Percentage Change: `ypercent`
            - Yearly Difference: `ydiff`
            - Year to Date Percentage Change: `ytdpercent`
            - Year to Date Difference: `ytddiff`
            - Moving Average: `mov`
            - Moving Total: `movsum`
7. `keep_originals` (bool, optional): Sets the state of the original series when an aggregation or
transformation function is applied to the series. Defaults to `True`
    - `True`: Keep original series when a transformation function is applied to time series.
    - `False`: Drop original series when a transformation function is applied to time series.
8. `frequency` Frequence of requested time series. Defaults to `None` (as is)
    - Available frequencies:
        - Daily: `daily` or `D`
        - Business Daily: `bdaily` or `B`
        - Weekly: `weekly` or `W`
        - semimonthly: `semimonthly` or `SM`
        - Monthly: `monthly` or `M`
        - Quarterly: `quarterly`, `Q`
        - Semiyearly: `semiyearly` or `6M`
        - Yearly: `yearly` or `Y`
9. `new_names`: Changes teh created `DataFrame` column names with given ones. Defaults to `None`
10. `keep_references`: Stores given new column names (if supplied) as references to real series names
on EVDS API service. The reference names can not be stored if a transformation or aggregation
function is applied to requested series. Defaults to `False`.
11. `time_series`: Tries to parse string dates into DateRanges corresponding to returned frequency of
time series. That is especially useful (and mostly required) for time series analysis since string
dates are converted to sortable, indexable, sliceable, differentiable real dates. Defaults to `True`
12. `ascending`: Sort direction of the index.
    - `True`: Oldest data first.
    - `False`: Newest data first. Defaults to `True`
13. `raw`: Returns retrieved `JSON` data untouched. Defaults to `False`
14. `as_dict`: Returns retrieved data as dictionary type. Defaults to `False`
15. `convert_to_bd`: Checks start_date and end_date and returns the nearest business
date if any of them encounters in weekend. Defaults to `True`.


__Cases__:

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL")
```
The result is the most up-to-date value of data when a series name is supplied to the `get_series()`
without providing any parameter. The return type defaults to a pandas `DataFrame` object unless
otherwise is requested. Starting and ending dates for requested series are given through `start_date`
and `end_date` parameters of `get_series()` method. The date is made equal to current date if any of
them is not provided. The requested time series data are retrieved from the given start date to the
current date if just a start date is provided to the connector.

`start_date` (and `end_date` that is mentioned further) can be provided as below formats.

1. `d.m.y` -> 01.07.2022 or 1.7.2022
2. `d-m-y` -> 01-07-2022 or 1-7-2022
3. `d/m/y` -> 01/07/2022 or 1/7/2022
4. Python's `datetime` type -> datetime(2022, 7, 1)
5. pandas' `Timestamp` type -> pd.Timestamp(2002, 7, 1)

```python
# 'end_date' is made equal to current date for all below examples since it's not proveded.

# string dates
usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date="1.7.2022")  # OK
usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date="1-7-2022")  # OK
usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date="1/7/2022")  # OK

# datetime classes
from datetime import datetime
from pandas import Timestamp

# datetime instances
d_date = datetime(2022, 7, 1)
p_date = Timestamp(2022, 7, 1)

usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date=d_date)  # OK
usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date=p_date)  # OK
```

`end_date` accepts the same type of date entries for determining in which date last data ends for
the time series requested. `end_date` is made equal to current date when nothing is supplied.

```python
# end_date parameter is not provided and therefore is automatically assigned to the current date.
usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date="1.7.2022")

# daily USDTRY series belongs to June of 2022 period.
usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date="01.06.2022", end_date="30.06.2022")
```

Alternatively, you can use `period` parameter of the `get_series()` method to indicate a time period
from the current date. `period` takes a period string to identify the period you would like to
retrieve the series.

Period string consists of two part; the first one is an integer number and the second one is a date
period such as; day, week, month and year.

|period identifier  | example parameter | means                                 |
|-------------------|-------------------|---------------------------------------|
| `d` or `g`        |    `27d` or `27g` | 27 days ago from today -  today       |
| `w` or `h`        |   `19w` or `19h`  | 19 weeks ago from today - today       |
| `m` or `a`        |   `2m` or `2a`    | 2 months ago from today - today       |
| `y`               |   `27y`           | 27 years ago from today - today       |

> Notice that `start_date` or `end_date` cannot be used together with `period` because it creates an ambiguous
> request. An exception is raised if you try to use these parameters together.


<a id="getting-multi"></a>

### __Retrieving Multi-Dimentional Time Series__

Retrieving multi-dimentional data can be done using one of the belows:

1. series can be provided to `get_series()` method as strings in a sequence type container like a `List` or `Tuple`.
2. series can be provided to `get_series()` method as comma separated `string`s.
3. series can be provided to `get_series()` method as space separated `string`s.

__Cases__:

```python
# list or tuple
series = ["TP.DK.USD.A.YTL", "TP.DK.EUR.A.YTL"]
exchange_rates = connector.get_series(series,                              # OK
                                      start_date="01.06.2022",
                                      end_date="07.06.2022")

# comma separated strings
exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",  # OK
                                      start_date="01.06.2022",
                                      end_date="07.06.2022")

# space separated strings
exchange_rates = connector.get_series("TP.DK.USD.A.YTL TP.DK.EUR.A.YTL",   # OK
                                      start_date="01.06.2022",
                                      end_date="07.06.2022")
```


<a id="the-advanced-1"></a>

## __Advanced Features__

Here we'll look through some of the advanced features of `evdsts` we can gather as below;

### [__Time Series Indexing__](#ts-indexing)
### [__Selecting Different Frequency for Time Series Requested__](#selecting-different-frequency)
### [__Selecting Transformation Function(s) for Time Series Requested__](#selecting-transformation)
### [__Selecting Aggregation Function(s) for Time Series Requested__](#selecting-aggregation)
### [__Retrieving Raw Data in JSON Format__](#retrieving-raw-data)
### [__Assigning New Names for Retrieved Time Series__](#assigning-new-names)
### [__Writing Series on Disk__](#writing-series)
### [__Updating Local Search Index__](#updating-index)


<a id="ts-indexing"></a>

### __Time Series Indexing__

`evdsts`, transforms all series that are retrieved from EDDS service to real time series.
This behavior is controlled by `time_series` flag of the `get_series()` method and can be set as
`True` or `False`. It defaults to `True`.

__Cases__:

```python
# this call returns a `DataFrame` without time series indexing.
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.06.2022",
                              end_date="30.06.2022",
                              time_series=False)
```

> __Disabling time series indexing cause many useful features to be lost. Therefore, it would better
> kept enabled unless a certain need emerges.__

Time series indexing enables us to get slices like below.  

Let's take a sllice from `usdtry` that comprise the range from 1st of June, 2022 - 7th of June, 2022

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.06.2022",
                              end_date="30.06.2022")

usdtry_slice = usdtry.loc["2022-06-01": "2022-06-07"]
```

We see one of the advantages of time series indexing that we could get a range comprising 01-07
June despite we didn't know which original index number (EDDS originally returns the series indexed
by 0 to n) it corresponds to.  

Likewise, assume we suspect a date (15.06.2022) which possibly can be a beginning of a structural
break for our `usdtry` series.

```python
structural_break = datetime(2022, 6, 15)
usdtry_after_break = usdtry.loc[usdtry.index > structural_break]
usdtry_before_break = usdtry.loc[usdtry.index <= structural_break]
```

We can easily split the series as before and after the break thanks to time series indexing.

Or assume that we need a dummy variable that represents `Mondays` for our model. We had to know
which days were corresping to Mondays in the current range if we wouldn't use time series indexing,
however, we can easily create a new series like below thanks to time series indexing.

```python

# day of week -> Monday: 0 - Sunday: 6
import pandas as pd

usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.06.2022",
                              end_date="30.06.2022")

usdtry_mondays = usdtry.loc[usdtry.index.day_of_week == 0]

dummy_monday = pd.DataFrame(index=usdtry.index)
dummy_monday = dummy_monday.combine_first(usdtry_mondays)
dummy_monday = dummy_monday.fillna(0)
dummy_monday[dummy_monday > 0] = 1

```

Let's get yearly slices from the series we retrieved as an other example:

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2020",
                              end_date="31.12.2021")

# maybe we need data just belongs to 2020.
usd_20 = usdtry.loc["2020"]

# or maybe between 2020 and 2021.
usd_21_22 = usdtry.loc["2020": "2021"]
```

we'have just seen some of the advantages of `evdsts`' time series conversions above, however, these were
just a little portion of what you can achieve while you are working on real time series. You can visit
[Pandas Time Series](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html) page
for getting more information about working with time series.


<a id="selecting-different-frequency"></a>

### __Selecting Different Frequency for Time Series Requested__

The `frequency` parameter of the `get_series()` method is used for selecting the frequency of time
series you request from the API service. you can use `show_frequency_references()` method of the
`Connector` instance in order to see defined frequencies.

```python
connector.show_frequency_references()
```

```python
                 References Table                 
--------------------------------------------------
Reference Name Represents -> Original Frequency Names on EVDS
--------------------------------------------------
default or level or 0   ---> 
daily or D or 1         ---> 1
bdaily or B or 2        ---> 2
weekly or W or 3        ---> 3
semimonthly or SM or 4  ---> 4
monthly or M or 5       ---> 5
quarterly or Q or 6     ---> 6
semiyearly or 6M or 7   ---> 7
yearly or Y or 8        ---> 8
--------------------------------------------------
```
Let's retrieve `usdtry` series in business daily frequency which are originally observed in daily frequency.
According to table above, you can provide `bdaily`, `B`, or `2` to the `frequency`` parameter to do
that.

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2020",
                              end_date="31.12.2021",
                              frequency="bdaily")
```

Dates corresponding to Saturdays and Sundays should no longer be included in returned series index
when you set the frequency as business daily.

> Note that; the public holidays don't correspond to weekends are represented as `NaN`s in this
> frequency.


<a id="selecting-transformation"></a>

### __Selecting Transformation Function(s) for Time Series Requested__

A set of defined transformation functions can be applied to series before retrieving them from the
service. These defined functions are determined by `transformations` parameter of the `get_series()`
method. You can use `show_transformation_references()` method of the `Connector` instance in order to
see all EDDS service pre-defined functions.

__Cases__:

```python
connector.show_transformation_references()
```

```python
                 References Table                 
--------------------------------------------------
Reference Name Represents -> Original Transformation Function Names on EVDS
--------------------------------------------------
level or 0              ---> 0
percent or 1            ---> 1
diff or 2               ---> 2
ypercent or 3           ---> 3
ydiff or 4              ---> 4
ytdpercent or 5         ---> 5
ytddiff or 6            ---> 6
mov or 7                ---> 7
movsum or 8             ---> 8
--------------------------------------------------
```

Identifications of transformation functions given on above table are:  

|   parameter       |   explanation                                             |
|:-----------------:|-----------------------------------------------------------|
| `level`           |    _Level Series_                                         |
| `percent`         |    _Percentage (return) Series_                           |
| `diff`            |    _Difference Series_                                    |
| `ypercent`        |    _Yearly Percentage (return) Series_                    |
| `ydiff`           |    _Yearly Difference Series_                             |
| `ytdpercent`      |    _Year to Date (end_date) Percentage (return) Series_   |
| `ytddiff`         |    _Year to Date (end_date) Difference Series_            |
| `mov`             |    _Moving Average Series_                                |
| `movsum`          |    _Moving Sum Series_                                    |

Let's transform our originally daily observed time series to weekly series and then
add the percentage (return) series to this series as an instance.

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="W",
                              transformations="percent")

# the return will be: USDTRY and USDTRY% in weekly frequency.
# USDTRY% = (USDTRY-USDTRY(t-1)) / USDTRY(t-1)
```

Transformations can be applied by two different ways when multi-dimensional series are requested.

1. Given transformation function is applied to all series requested if only one function is provided.
For instance, if only `t` function is given for series `s1` and `s2`, then the transformed series are
`t(s1)` and `t(s2)`
2. Given transformation functions are applied to series respectively if individual transformation
functions are provided for each time series in request. For instance, if `t1` and `t2` functions are
given for series `s1` and `s2`, then the transformed series are `t1(s1)` and `t2(s2)`

```python
exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="W",
                                      transformations="percent")

# the return will be; USDTRY, EURTRY, USDTRY%, and EURTRY% since only one transformation
# function (percent) is provided for both series.
```

> If otherwise is explicitly requested, the original series are preserved and returned in frame when
> transformation or aggregation functions are applied to them. This behavior is controlled by
> `keep_originals` flag of the `get_series()` method and defaults to `True`. You can set it `False`
> when calling if you would not like the original series to be returned together with transformed ones.

```python
exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="W",
                                      transformations="percent",
                                      keep_originals=False)

# the return will be USDTRY% and EURTRY% since the 'keep_originals' flag is set 'False'.
```

As for below sample, `percent` is applied to TP.DK.USD.A.YTL (USDTRY) and `diff` is applied to
TP.DK.EUR.A.YTL (EURTRY) respectively since two individual transformation functions are provided
for two requested time series.

```python
exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="W",
                                      transformations="percent, diff")

# the return will be; USDTRY, EURTRY, USDTRY% and D(EURTRY) time series.
# USDTRY% = (USDTRY-USDTRY(t-1)) / USDTRY(t-1)
# D(EURTRY) = (EURTRY(t) - EURTRY(t-1))
```

Individual transformation functions can be provided by different ways shown below:

1. with a comma separated `string`
2. with a space separated `string`
3. with individual strings in a sequence type container like a `List` or `Tuple`

```python
transformations = ["percent", "diff"]

exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2022",
                                      transformations=transformations)    # OK

exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2022",
                                      transformations="percent, diff")    # OK

exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2022",
                                      transformations="percent diff")     # OK
```


<a id="selecting-aggregation"></a>

### __Selecting Aggregation Function(s) for Time Series Requested__

A set of defined aggregation functions can be applied to series before retrieving them from the
service. These defined functions are determined by `aggregations` parameter of the `get_series()` method.
You can use `show_aggregation_references()` method of the `Connector` instance in order to see all
EDDS service pre-defined functions.

__Cases__:

```python
connector.show_aggregation_references()
```

```python
                 References Table                 
--------------------------------------------------
Reference Name Represents -> Original Aggregation Function Names on EVDS
--------------------------------------------------
avg or 1                ---> avg
min or 2                ---> min
max or 3                ---> max
first or 4              ---> first
last or 5               ---> last
sum or 6                ---> sum
--------------------------------------------------
```

Identifications of aggregation functions given on above table are:  

|   parameter   |   explanation                             |
|:--------------|-------------------------------------------|
| `avg`         |average (mean) value in selected frequency |
| `min`         |minimum value in selected frequency        |
| `max`         |maximum value in selected frequency        |
| `first`       |first value in selected frequency          |
| `last`        |last value in selected frequency           |
| `sum`         |sum of values in selected frequency        |

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="W",
                              aggregations="max")

# the output will be USDTRY and the maximum observed values for USDTRY in a given week
# in range (01.01.2021 - 31.12.2021)
# in other words, it's equals to USDTRY and max(USDTRY, W).
```

Aggregations can be applied by two different ways when multi-dimensional series are requested.

1. Given aggregation function is applied to all series requested if only one function is provided.
For instance, if only `a` function is given for series `s1` and `s2`, then the transformed series are
`a(s1)` and `a(s2)`
2. Given aggregation functions are applied to series respectively if individual aggregation
functions are provided for each time series in frame. For instance, if `a1` and `a2` functions are
given for series `s1` and `s2`, then the transformed series are `a1(s1)` and `a2(s2)`

```python
exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="W",
                                      aggregations="max")

# the return will be; USDTRY, EURTRY, max(USDTRY, W) and max(EURTRY, W) since only one aggregation
# function is provided for all series.
```

> Note that the original time series are preserved and returned with the aggregated series since
> `keep_originals` flag defaults to `True`.

As for below sample, `max` is applied to TP.DK.USD.A.YTL (USDTRY) and `min` is applied to
TP.DK.EUR.A.YTL (EURTRY) respectively since two individual transformation functions are provided
for two time series. Corollary, the aggregated series are equals to max(USDTRY) and min(EURTRY)
in requested frequencies.

```python
exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="W",
                                      aggregations="max, min")

# the output will be USDTRY, EURTRY, the maximum observed values for USDTRY, and the minimum observed
# values for EURTRY in a given week in range (01.01.2021 - 31.12.2021)
# in other words, it's equals to USDTRY, EURTRY, max(USDTRY, W), min(EURTRY, W).
```

Individual aggregation functions can be provided by different ways shown below:

1. with a comma separated `string`
2. with a space separated `string`
3. with individual strings in a sequence type container like a `List` or `Tuple`

```python
aggregations = ["max", "min"]

exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2022",
                                      aggregations=aggregations)          # OK

exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2022",
                                      aggregations="min, max")            # OK

exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2022",
                                      aggregations="min max")             # OK
```

> __Please not that; for preventing ambiguity, `evdsts` doesn't allow the transformations and__
> __aggregations are applied to series at once.__


<a id="retrieving-raw-data"></a>

### __Retrieving Raw Data in Other Formats__

You can use `raw` flag of the `get_series()` method to retrieve untouched JSON data which is
returned from the API service.

```python
exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2020",
                                      end_date="31.12.2021",
                                      frequency="Y",
                                      transformations="percent",
                                      raw=True)
```

likewise, you can use `as_dict` parameter to retrive the data as a `Dict` object.

```python
exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2020",
                                      end_date="31.12.2021",
                                      frequency="Y",
                                      transformations="percent",
                                      as_dict=True)
```


<a id="assigning-new-names"></a>

### __Assigning New Names for Retrieved Time Series__

You can assing new column names for the series retrieved by `new_names` parameter of the
`get_sereies()` method. New names for `DataFrame` columns are set respectively for the
series requested.

### [__Assigning New Names for Bare Series Requests__](#assigning-new-names-bare)
### [__Assigning New Names for Transformed or Aggregated Series Requests__](#assigning-new-names-transagg)


<a id="assigning-new-names-bare"></a>

### __Assigning New Names for Bare Series Requests__

The below example shows how to give new names for retrieved series. Names are provided respectively
that maps `TP.DK.USD.A.YTL = USDTRY`, and `TP.DK.EUR.A.YTL = EURTRY` in below, therefore, the column
names of returned `DataFrame` are `USDTRY` and `EURTRY` instead of `TP.DK.USD.A.YTL` and `TP.DK.EUR.A.YTL`

__Cases__:

```python
exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="W",
                                      new_names="USDTRY, EURTRY")
```

New series names can be provided by different ways shown below:

1. with a comma separated `string`
2. with a space separated `string`
3. with individual strings in a sequence type container like a `List` or `Tuple`

```python
new_names = ["USDTRY", "EURTRY"]

exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="W",
                                      new_names=new_names)                 # OK

exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="W",
                                      new_names="USDTRY, EURTRY")          # OK

exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="W",
                                      new_names="USDTRY EURTRY")          # OK
```


<a id="assigning-new-names-transagg"></a>

### __Assigning New Names for Transformed or Aggregated Series Requests__

If the original time series are requested with transformed or aggregated series as well, that is,
`keep_originals = True`  
then new names must be given in below order:

__`names for original series then names for transformed/aggregated series`__

Hence, if for instance; USDTRY is requested with a `percent` transformation, then the new names must be
given as below because the returned `DataFrame` includes both `USDTRY` and `USDTRY%` series since
`keep_originals` is set `True` and the original series are returned together with percentages as well.

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="W",
                              transformations="percent",
                              new_names="USDTRY, P_USDTRY")

# since the returned dataframe made up of USDTRY, USDTRY% (because 'keep_originals' = True as default)
# new names is provided as USDTRY, P_USDTRY.
```

> Tip: an `UnmatchingFieldSizeException` raises when you give a mismatched number of new names and
> you can figure out how many new names you should have been provided from the error message.

if the original series are not requested in returned data (`keep_originals = False`) then the new
names are given for just transformed or aggregated series.

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="W",
                              transformations="percent",
                              keep_originals=False,
                              new_names="USDTRY_P")

# just USDTRY is given as new name since the returned data includes just USDTRY% because
# keep_originals flag is False
```

similarly,

```python
exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="6M",
                                      aggregations="max, min",
                                      new_names="USDTRY, EURTRY, USDTRY_MAX, EURTRY_MIN")

# the returned data includes USDTRY, EURTRY, max(USDTRY), min(EURTRY), and therefore
# the new names are provided accordingly.
```

and,

```python
exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="6M",
                                      aggregations="max, min",
                                      new_names="USDTRY_MAX, EURTRY_MIN",
                                      keep_originals=False)

# the returned data includes just max(USDTRY) and min(EURTRY), therefofe
# the new names are provided accordingly.
```


<a id="writing-series"></a>

### __Writing Series on Disk__

All data returned from `evdsts` can be written on disk by `to_file()` method of the `Connector` instance.
You can write data in; `JSON`, `CSV` or `XLS` (requires `openpyxl` package) formats in order to store them
for further use.

`to_file()` method takes two important parameters:  

a. `data`: the data itself to be written on disk  
b. `data_format`: determines the output format like `csv`, `json`, `xls`

The fingerprint of `to_file()` is:

```python
def to_file(
            data: Optional[Union[pd.DataFrame, JSONType, Dict]] = None,
            data_format: str = "csv",
            filename: Optional[str] = None,
            delimiter: str = ";",
) -> None:
```

1. `data`: The data to be written on disk.
    - can be given in Pandas `DataFrame`
    - can be given in `JSONType` raw data
    - can be given in Pyton `Dict`.
2. `data_format`: Output format. Defaults to `csv`
    - for csv file format: `csv`
    - for Excel format: `excel`, `xls`, or `xlsx`
    - for raw format: `raw` or `json`
3. `filename`: Output filename. Defaults to `None`
    - The bare filename for output. Output file is always saved on current working directory.
    Therefore, the given filename shoul be just the bare filename like "cppi" or "unemployment".
        - if not given, the outputfile name is set to: `data_year_month_day_hours_minutes_seconds`
4. `delimiter`: Fields delimiter for csv format. Defaults to `;`

__Cases__:

Let's write main categories on disk:

```python

main_dict = connector.get_main_categories()
connector.to_file(data=main_dict, data_format='csv')

```
```python
Given data have been written on g:\My Drive\Dev\Active\evdsts\data_2022_07_19_213945.csv
```

Likewise,

```python
sub_categories_df = connector.get_sub_categories("EXCHANGE RATES")
connector.to_file(data=sub_categories_df, data_format='json')

```
```python
Data is written on g:\My Drive\Dev\Active\evdsts\data_2022_08_12_214320.json
```

> `evdsts` can write all `dict`, `JSON`, and `DataFrame` types of data to disk in provided formats.


<a id="updating-index"></a>

### __Updating Local Searh Index__

`evdsts` uses a local index to search series names in EDDS. The local index possibly be outdated
after several months from creation date because of the series updates done in EDDS itself. You can
update the local index every several months in order its to be in sync with EDDS.

__Cases__:

```python

# You need the IndexBuilder class of evdsts for updating the local search index.
from evdsts import IndexBuilder

# create a builder instance like below.
builder = IndexBuilder('YOUR_API_KEY', language="EN")

# you can check how old the local index is in days.
print(builder.index_age_in_days)

# rebuild the index if it's been a long time (like months) since it's created.
builder.build_index()
```

> __Please note that rebuilding the local search index takes around 30 minutes because the builder waits__
> __a reasonable amount of time (min. 5 secs.) between every new connection it establishes in order__
> __not to overload the API service with frequent requests.__



<a id="using-reference-names"></a>

## __Using Reference Names to Retrieve Time Series__

The most important reason that negatively affects the productivity when you work on series identified
in EDDS database is the complex series name identifications of EDDS. This cause you to find the
original series names on EDDS whenever you would like to get data from the service. `evdsts` solves
the issue introducing reference names which can be used as a proxy names for real series names in
EDDS database while retrieving data from the service.

Reference names can be given in two different ways which are shown below;

1. You can give new names to the series and save them as reference names using `keep_references` flag
if you request just original series, that is, when neither a transformation nor an aggregations function
is requested with original series.
2. You can use `save_name_references()` method of the `Connector` instance to save reference names directly.

### [__Saving Reference Name While Retrieving Time Series__](#saving-reference-name)
### [__Saving Reference Names Directly__](#saving-names-directly)
### [__Transferring Given Reference Names to Other Projects__](#transferring-reference-names)


<a id="saving-reference-name"></a>

### __Saving Reference Names While Retrieving Time Series__

The first way to save reference names is shown below block. You can use `keep_references` flag since
neither a transformation nor an aggregation function is applied to the requested series. The reference
name `usdtry` is saved as indicating `usdtry -> TP.DK.USD.A.YTL` permanently.

__Cases__:

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="Q",
                              new_names="usdtry",
                              keep_references=True)
```

A notification are shown on screen whenever you save a reference name for a series. That means you
can use this reference name for retrieving data later on.

```python
Below references map have been created for further use. You can use reference series names instead of original ones
when retrieving data from the EVDS API service. Reference names are permanent unless this reference mapping is deleted
or changed.

                 References Table                 
--------------------------------------------------
Reference Name Represents -> Original Series Names on EVDS
--------------------------------------------------
usdtry          ---> TP.DK.USD.A.YTL
--------------------------------------------------
```

Let's make the same request now.

```python
usdtry = connector.get_series("usdtry",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="Q")
# you don't need to know or provide the original series name from now on!
```

Let's save more than one reference names in a call.

```python
exchange_rates = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="Q",
                                      new_names="usdtry, eurtry",
                                      keep_references=True)
```

```python
Below references map have been created for further use. You can use reference series names instead of original ones
when retrieving data from the EVDS API service. Reference names are permanent unless this reference mapping is deleted
or changed.

                 References Table                 
--------------------------------------------------
Reference Name Represents -> Original Series Names on EVDS
--------------------------------------------------
eurtry          ---> TP.DK.EUR.A.YTL
usdtry          ---> TP.DK.USD.A.YTL
--------------------------------------------------
```

You can see all the reference names you've given for your current project using `show_name_references()`
method.

```python
Below references map have been created for further use. You can use reference series names instead of original ones
when retrieving data from the EVDS API service. Reference names are permanent unless this reference mapping is deleted
or changed.

                 References Table                 
--------------------------------------------------
Reference Name Represents -> Original Series Names on EVDS
--------------------------------------------------
cpi             ---> TP.FE.OKTG01
eurtry          ---> TP.DK.EUR.A.YTL
usdtry          ---> TP.DK.USD.A.YTL
--------------------------------------------------
```

Let's retrieve multi-dimentional time series using above reference names.

```python
exchange_rates = connector.get_series("usdtry, eurtry",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="Q")
```

You can also change reference names with this method like below:

```python
exchange_rates = connector.get_series("usdtry, eurtry",
                                      start_date="01.01.2021",
                                      end_date="31.12.2021",
                                      frequency="Q",
                                      new_names="dollar_tl, euro_tl",
                                      keep_references = True)
# old reference names 'usdtry' and 'eurtry' are changed with 'dollar_tl' and 'euro_tl'
```

> Returned `DataFrame` columns are named automatically with reference names if a reference name
> has been given for any series in requested ones. Therefore, you don't need to use `new_names`
> parameter to rename columns for the series which reference names are already assigned.


<a id="saving-names-directly"></a>

### __Saving Reference Names Directly__

As a second way, you can save reference names directly using `save_names_references()` method
of the `Connector` instance like below.

The fingerprint of the `save_name_references()` is:

```python
def save_name_references(
                         series_names: Union[str, Sequence[str]],
                         reference_names: Union[str, Sequence[str]],
                         old_reference_names: Optional[List[str]] = None,
                         verbose: bool = True,
                         check_names: bool = True
) -> None:
```

1. `series_names`: Original series name(s) on EVDS API. or names that currently saved as references.
    - Can be given as a string for one series or in a Sequence type like. a `List` or `Tuple`.
    `[seriesname1, seriesname2,...]`
2. `reference_names`: reference names for series.
    - Can be given as a string for one series or in a Sequence type like a `List` or `Tuple`.
    `[reference_name_1, reference_name_2,...]`
    - Reference names must be made up of standard `Latin` chars `[A-Za-z]`, digits `[0-9]` and
    underscore charecter (`_`)
3. `old_reference_names`: Mostly for internal use. Defaults to `None`
4. `verbose`: Gives text output for the result. Defaults to `True`.
5. `check_names`: Checks if given series names are correct identifiers on EVDS API server.
Defaults to `True`


__Cases__:

```python
connector.save_name_references('TP.FE.OKTG01', 'cpi')
```

or you can save more than one reference names at once like below;

```python
connector.save_name_references('TP.FE.OKTG01, TP.DK.USD.A.YTL', 'cpi, usdtry')
```

You can save reference names with different ways:

1. with a comma separated `string`
2. with a space separated `string`
3. with individual strings in a sequence type container like a `List` or `Tuple`

```python
series = ["TP.DK.USD.A.YTL", "TP.DK.EUR.A.YTL"]
references = ["usdtry", "eurtry"]

connector.save_name_references("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL", "usdtry, eurtry", verbose=False)  # OK
connector.save_name_references("TP.DK.USD.A.YTL TP.DK.EUR.A.YTL", "usdtry eurtry", verbose=False)    # OK
connector.save_name_references(series, references, verbose=False)                                    # OK

# verbose controls the on screen output
```
> Tip: you can use `verbose` flag almost every function for enabling or disabling the on-screen
> representation of the results.

You can also change the old reference names with new ones. Let's assume we would like to change the
reference name we already assigned as `usdtry` to `usdlira`

```python
connector.save_name_references("usdtry", "usdlira")
```

```python
Below references map have been created for further use. You can use reference series names instead of
original ones when retrieving data from the EVDS API service. Reference names are permanent unless
this reference mapping is deleted or changed.

                 References Table                 
--------------------------------------------------
Reference Name Represents -> Original Series Names on EVDS
--------------------------------------------------
usdlira          ---> TP.DK.USD.A.YTL
--------------------------------------------------
```


<a id="transferring-reference-names"></a>

### __Transferring Given Reference Names to Other Projects__

You can transfer your reference names between projects through transferring `evds_series_references.json`
file to the projects' current working directories.

_Where is the current reference names file?_

```python
print(connector.references_file)

# gives 'g:\\My Drive\\Dev\\Active\\evdsts\\evds_series_references.json'
```

or just `print` the `Connector` instance to see reference file location together with other details.

```python
print(connector)
```

_How can I transfer that names to the new project I'm currently working on?_

1. Create a new `Connector` instance in your new project. Say, `connector`
2. Use `import_name_references()` method giving the reference name file path which you got from the
other project.

The fingerprint of `import_name_references()` method is:

```python
def import_name_references(source: Union[str, Path]) -> None:
```

1. `source`: absolute path for the name references file.

__Cases__:

```python
connector.import_name_references('g:\\My Drive\\Dev\\Active\\evdsts\\evds_series_references.json')
```


<a id="the-transformator-1"></a>

## __The Transformator__

`Transformator` is the second important part of the `evdsts` that responsible for manipulating the
retrieved data in order to ease the time series analysis process. You need to create an instance of
`Transformator` class in order to perform defined transformations.

> __Please note that the most of `Transformator` methods depend on '_time series indexing_' and__
> __'_ascending ordering_'. This is already the return default of the `Connector`, but the integrity__
> __of the results are not guaranteed if you use__;
> __`time_series = False`__ and/or
> __`ascending = False`__
> __flags when retrieving the data using `Connector`'s __`get_series()`__ method__.

The fingerprint of `Transformator` class is:

```python
def __init__(global_precision: Optional[int] = None) -> None:
```

1. `global_precision`: Sets a global precision for floating-point numbers returned by all kind of
transformation functions. Defaults to `None`
    - if `None` given: No global precision is set. Each transformation function uses its own default
    precision if an explicit precision is not supplied with `precision=n` parameter while calling the
    transformator function.
    - integer number given: Global default precision for every transformation function is set as
    given precision. That means they use this global default precision instead of their own individual
    defaults if an explicit precision is not given with `precision=n` parameter while calling the
    transformator function.

    - Notes:
        - Explicitly given `precision` parameter while calling any transformation functions always
        overrides the `global_precision` and the functions' own default precision.
        - `global_precision` overrides the functions' own default precision if an explicit precision
        is not given with `precision=n` parameter while calling the transformator function.

__Cases__:

You can create an instance of `Transformator` class like below;

Firstly, you need to import the `Transformator` class from `evdsts`

```python
from evdsts import Transformator
```

and then, you can create an instance of the class like below;

```python
transformator = Transformator()
```

or you can define a global floating-point number precision in order to be used by all `Transformator`
methods by default. The floating-point number precision of below `transformator` object is set to `4`
as an instance.

```python
transformator = Transformator(4)  # This sets the default floating-point numbers precision to 4 for all methods.
```

### [__Renaming Series Names with Transformator__](#rename-series)
### [__Fixing The Floating-Point Numbers Precision with Transformator__](#trans-precision)
### [__Differentiation: D(y<sub>t</sub>, i) = y<sub>t</sub> - y<sub>t-i</sub> = (1-L)<sup>i</sup>y<sub>t</sub>__](#regular-diff)
### [__Natural Logarithmic Transformation: ln(y<sub>t</sub>)__](#log-transform)
### [__Logarithmic Difference (LogReturn): D(ln(y<sub>t</sub>), i) = ln(y<sub>t</sub>) - ln(y<sub>t-i</sub>) = (1-L)<sup>i</sup>ln(y<sub>t</sub>)__](#logaritmic-diff)
### [__Deterministic Trend: y<sub>t</sub> = β<sub>0</sub> + β<sub>1</sub>Trend + β<sub>2</sub>Trend<sup>2</sup> + ... β<sub>n</sub>Trend<sup>n</sup> + ε<sub>t</sub>__](#deterministic-trend)
### [__Decompose: y<sub>t</sub> - (β<sub>0</sub> + β<sub>1</sub>Trend + β<sub>2</sub>Trend<sup>2</sup> + ... β<sub>n</sub>Trend<sup>n</sup> + ε<sub>t</sub>)__](#de-trend)
### [__Simple Moving Average: MA<sub>t</sub> = (y<sub>t</sub> + y<sub>t-1</sub> ... y<sub>t-n</sub>) / n__](#smooth-sma)
### [__Exponential Moving Average: EMA<sub>t</sub> = αy<sub>t</sub> + (1-α)EMA<sub>t-1</sub>__](#smooth-ema)
### [__Rolling Var: ROLVAR<sub>t</sub> = σ<sup>2</sup>(y<sub>t</sub>, y<sub>t-1</sub> ... y<sub>t-n</sub>)__](#detect-rollvar)
### [__Rolling Correlations: ROLCORR<sub>t</sub> = ρ(y<sub>t-n</sub>, x<sub>t-n</sub>)__](#detect-rollcorr)
### [__Cumulative Sum: Cusum<sub>t</sub> = 𝚺(y<sub>t</sub>, y<sub>t-1</sub> ... y<sub>t-n</sub>)__](#get-cusum)
### [__Z-Score: Z<sub>t</sub> = (y<sub>t</sub> - ȳ) / σ<sub>y</sub>__](#get-z-score)
### [__Median Absolute Deviation: MAD<sub>t</sub> = median(|y<sub>t</sub> - median(y<sub>t</sub>)|)__](#get-mad)
### [__Normalized Series: y<sub>t, normal</sub> = F(y<sub>t</sub>)__](#get-normalized)
### [__Dummy Series: D<sub>n</sub>__](#get-dummies)
### [__Lagged Series: y<sub>t-1</sub>, y<sub>t-2</sub> ... y<sub>t-n</sub>__](#get-laggeds)
### [__Correlation Coefficients: ρ(y<sub>t</sub>, x<sub>t</sub>)__](#get-corr)
### [__Autocorrelation Coefficients: AUTOCORR<sub>t</sub> = ρ<sub>t, t-n</sub>__](#get-auto-corr)
### [__Serial Correlation Coefficients: SERIALCORR<sub>t</sub> = ρ<sub>t, x-n</sub>__](#get-serial-corr)
### [__Outliers__](#get-outliers)
### [__Smoothed Series__](#get-smoothed)


<a id="rename-series"></a>

### __Renaming Series Names with Transformator__

You can rename using `rename()` function if you would not like to use series names assigned
automatically by the `Transformator`.

The fingerprint of `rename()` function is:

```python
def rename(
            self,
            series: pd.DataFrame,
            names: Union[str, Sequence[str]],
            inplace: bool = False
) -> Union[pd.DataFrame, None]:
```

1. `series`: A DataFrame object consists of series.
2. `names`: New names for series in same order with originals.
    - can be given as comma separated string: `"usdtry, eurtry, corr_usdtry, corr_eurtry"`
    - can be given as a Tuple: `("usdtry", "eurtry", "corr_usdtry", "corr_eurtry")`
    - can be given as a List: `["usdtry", "eurtry", "corr_usdtry", "corr_eurtry"]`
3. `inplace`:  mutates the provided series if `True`. Defaults to `False`

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python
connector = Connector(language="EN")  # assuming you already have saved your API Key on disk.

# an instance of Transformator
transformator = Transformator()

# get series using reference names
series = connector.get_series("usdtry, eurtry",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="M")

lag_2s = transformator.laggeds(series, "1, 2") # get lag series including originals for instance

# this returns a copy renaming all series in lag_2s
# (usdtry, eurtry, usdtry_lag_1, eurtry_lag_1, usdtry_lag_2, eurtry_lag_2)
# notice that the original series still preserved here.

# new names must be provided in the same order with original ones in lag_2s
lag_2s_renamed = transformator.rename(lag_2s, "utr, eutr, utrl1, eutrl1, utrl2, eutrl2")

# Below usages are also valid. With a List
new_names = ["utr", "eutr", "utrl1", "eutrl1", "utrl2", "eutrl2"]
lag_2s_renamed = transformator.rename(lag_2s, new_names)

# or with a Tuple
new_names = ("utr", "eutr", "utrl1", "eutrl1", "utrl2", "eutrl2")
lag_2s_renamed = transformator.rename(lag_2s, new_names)

# This renames the series in lag_2s itself returning nothing.
transformator.rename(lag_2s, "utr, eutr, utrl1, eutrl1, utrl2, eutrl2", inplace=True)

```


<a id="trans-precision"></a>

### __Fixing The Floating-Point Numbers Precision with Transformator__

You can truncate floating-point numbers in your data anytime you would like using the
`set_precision()` method.

The fingerprint of `set_precision()` function is:

```python
def set_precision(
                    series: pd.DataFrame,
                    precision: int,
                    inplace: bool = False
) -> Union[pd.DataFrame, None]:
```

1. `series`: A DataFrame made up of numerical series.
2. `precision`: percision to be floating-point numbers fixed.
3. `inplace`: mutates the provided series if `True`. Defaults to `False`

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python
connector = Connector(language="EN")  # assuming you already have saved your API Key on disk.
transformator = Transformator()

# assuming you already have saved the reference name 'eurtry' for 'TP.DK.EUR.A.YTL'.
eurtry = connector.get_series("eurtry",
                              start_date="01.06.2022",
                              end_date="30.06.2022",
                              frequency="B")

# this returns a new series in which the exchange rates precisions are fixed to 2
eurtry_p4 = transformator.set_precision(eurtry, 2)

# this mutates the 'usdtry' variable itself as fixing the flotaing-number precisions to 2
transformator.set_precision(eurtry, 2, inplace=True)
```


<a id="regular-diff"></a>

### __Differentiation: Δ(y<sub>t</sub>, i) = y<sub>t</sub> - y<sub>t-i</sub> = (1-L)<sup>i</sup>y<sub>t</sub>__

You can use `diff()` method of `Transformator` to get difference series of given series.
You can use `diff()` method of `Transformator` to get difference series of given series.
Difference series are commonly used for making stationary series from non-stationary ones.
The most important caveat for this process is that modelling with difference series can not represent long-term relitionships with variables since differentiating process cause the series loose their long-term memories.

The fingerprint of `diff()` method is:

```python
def diff(
        series: pd.DataFrame,
        order: int = 1,
        precision: Optional[int] = None,
        keep_originals: bool = True,
        rename: bool = True
) -> pd.DataFrame:
```

1. `series` : A `DataFrame` includes series to be processed.
2. `order`: Order for difference operator. Defaults to `1` (1st Difference).
3. `precision`: Precision of returned values. Defaults to `None`
4. `keep_originals`: Includes original series in returned DataFrame if `True` Defaults to `True`
5. `rename`: renames the column names appropriately. Defaults to `True`

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__

```python

connector = Connector(language="EN")  # assuming you already have saved your API Key on disk.
transformator = Transformator(4)      # precision of the results will be 4 if otherwise is explicitly
                                      # given to the method

usdtry = connector.get_series("usdtry",
                              start_date="01.06.2022",
                              end_date="30.06.2022",
                              frequency="B")

# this gives you usdtry and the first difference of usdtry in a frame
diff_with_originals_included = transformator.diff(usdtry)
```

Differentiated series are returned including the original series as default. You can use
`keep_originals` flag if you would not like the original series returned with the differentiated
ones. In addition, you can use `order` parameter to get 2nd, 3rd, 4th,...nth difference of the
series. For instance, you can get 2nd difference providing `order=2` to the `diff()` method.

```python
# This gives you only the 2nd difference of the usdtry
only_diff_2 = transformator.diff(usdtry, order=2, keep_originals=False)
```

```python
# this gives you the third diff
second_diff = transformator.diff(usdtry, order=3)
```

<a id="log-transform"></a>

### __Natural Logarithmic Transformation: ln(y<sub>t</sub>)__

You can use `ln()` method to get natural logarithmics of given series. Likewise, `keep_originals` flags
controls if the returned dataframe includes the original series. Log transformation can ease modelling problems
arisen from high series variances.

The fingerprint of `ln()` method is:

```python
def ln(
       series: pd.DataFrame,
       precision: Optional[int] = None,
       keep_originals: bool = True,
       rename: bool = True
) -> pd.DataFrame:
```

1. `series` : A `DataFrame` includes series to be processed.
2. `precision`: Precision of returned values. Defaults to `None`
3. `keep_originals`: Includes original series in returned DataFrame if `True` Defaults to `True`
4. `rename`: renames the column names appropriately. Defaults to `True`

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python

usd_and_ln_usd = transformator.ln(usdtry)   # this gives you usdtry and ln(usdtry)

ln_usd = transformator.ln(usdtry, keep_originals=False)   # this gives you only ln(usdtry)

```

<a id="logaritmic-diff"></a>

### __Logarithmic Difference (LogReturn): Δ(ln(y<sub>t</sub>), i) = ln(y<sub>t</sub>) - ln(y<sub>t-i</sub>) = (1-L)<sup>i</sup>ln(y<sub>t</sub>)__

You can use `lndiff()` method to get logarithmic differences (log returns) of series.
Likewise, `keep_originals` flags controls if the returned frame includes the original series. This is
a symmetric return series so that; if you get `0.2` ln difference in time `t`, and `-0.2` ln difference in
time `t + 1`, then you get back to where you were, that is, its total efect is `0`. Notice the symmetry as a
different charecter of ln difference than regular growth since a `%20` growth in time `t`, and `%-20` growth in
time `t + 1` is equal to net `%-4` growth.

The fingerprint of `lndiff()` method is:

```python
def lndiff(
           series: pd.DataFrame,
           order: int = 1,
           precision: Optional[int] = None,
           keep_originals: bool = True,
           rename: bool = True
) -> pd.DataFrame:
```

1. `series` : A `DataFrame` includes series to be processed.
2. `order`: Order for difference operator. Defaults to `1` (1st Log Difference).
3. `precision`: Precision of returned values. Defaults to `None`
4. `keep_originals`: Includes original series in returned DataFrame if `True` Defaults to `True`
5. `rename`: renames the column names appropriately. Defaults to `True`

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__


```python

usd_log_return = transformator.lndiff(usdtry)           # this gives you 1st logarithmic differences (log returns)

usd_2nd_lndiff = transformator.lndiff(usdtry, order=2)  # this gives you 2nd logarithmic differences

only_log_return = transformator.lndiff(usdtry, keep_originals=False)  # this gives you just the log returns

```

<a id="deterministic-trend"></a>

### __Deterministic Trend: y<sub>t</sub> = β<sub>0</sub> + β<sub>1</sub>Trend + β<sub>2</sub>Trend<sup>2</sup> + ... β<sub>n</sub>Trend<sup>n</sup> + ε<sub>t</sub>__

You can use `deterministic_trend()` method to get the forecast series taken from the deterministic
trend model for given series. Likewise, `keep_originals` flags controls if the returned frame
includes the original series.

Deterministic trend model is defined below:

 y<sub>t</sub> = β<sub>0</sub> + β<sub>1</sub>Trend + β<sub>2</sub>Trend<sup>2</sup> + ... β<sub>n</sub>Trend<sup>n</sup> + ε<sub>t</sub>

Notice the deterministic trend is a phenomenon that satisfies the condition σ<sup>2</sup>y<sub>t</sub> = σ<sup>2</sup>,
that is, the variance of the trend doesn't change with the time. Such a process is called a _trend stationary_ process
and the stationary can be provided by removing that trend from the original series. This, sometimes called as
`decomposition` as well.

The fingerprint of the `deterministic_trend()` method is:

```python
def deterministic_trend(
                        series: pd.DataFrame,
                        degree: int = 1,
                        precision: Optional[int] = None,
                        keep_originals: bool = True,
                        rename: bool = True
) -> pd.DataFrame:
```

1. `series`: A Dataframe includes series to be processed.
2. `degree`: Degree of the deterministic trend. Defaults to `1`.
3. `precision`: Precision of returned values. Defaults to `None`.
4. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`.
5. `rename`: renames the column names appropriately. Defaults to `True`.

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Casees__:

```python
# this gives you the forecasts of the linear trend model
dt_forecast = transformator.deterministic_trend(usdtry)

# this gives you the forecasts of the quadratic trend model
dt_quadratic_forecast = transformator.deterministic_trend(usdtry, degree=2)
```

> High order polynoms can oscillate wildly if they're not a good representative of given series.
> Therefore, use the higher degree trend models if you're sure that the process is follows that
> order in a deterministic manner (eg: some kind of seasonality charecter).

<a id="de-trend"></a>

### __Decompose: y<sub>t</sub> - (β<sub>0</sub> + β<sub>1</sub>Trend + β<sub>2</sub>Trend<sup>2</sup> + ... β<sub>n</sub>Trend<sup>n</sup> + ε<sub>t</sub>)__

You can decompose (de-trend) retrieved series using `decompose()` method. Extracting time based deterministic trends
from the original series could be a good way to create stationary series from the non-stationary (or trend stationary) ones.
Decomposition (or de-trending) is especially an appropriate way to reach stationary series if the subject
series have a deterministic trend as one of the components.

Decomposition can be done through one of the ways below;

- Removing deterministic trend
    - subtracting
    - dividing
- Removing Simple/Exponential Moving Averages
    - subtracting
    - dividing

Deterministic trend model is defined below:

 y<sub>t</sub> = β<sub>0</sub> + β<sub>1</sub>Trend + β<sub>2</sub>Trend<sup>2</sup> + ... β<sub>n</sub>Trend<sup>n</sup> + ε<sub>t</sub>

Simple Moving Average process is defined as below;

MA<sub>t</sub> = (y<sub>t</sub> + y<sub>t-1</sub> ... y<sub>t-n</sub>) / n

Exponential Moving Average process is defined as below;

EMA<sub>t</sub> = αy<sub>t</sub> + (1-α)EMA<sub>t-1</sub>

The fingerprint of `detrend()` method is:

```python
def decompose(
              series: pd.DataFrame,
              degree: int = 1,
              source: str = "trend",
              method: str = "subtract",
              precision: Optional[int] = None,
              keep_originals: bool = True,
              rename: bool = True
) -> pd.DataFrame:
```

1. `series`: A DataFrame consists of series to be detrended
2. `degree`: Degree of deterministic trend or window for (e/s)ma. Defaults to `1`.
    - means polinomial degree of deterministic trend if the source is given as `trend`.
    for instance: `1` means linear trend, and `2` means quadratic trend, etc.
    - means window of `(e/s)ma` if the source is given as `sma` or `ema`
3. `source`: source of detrending process. Defaults to `trend`.
    - `trend`: detrended series = series (- or /) trend(series, given_degree)
    - `sma`: detrended series = series (- or /) sma(series, window=degree)
    - `ema`: detrended series = series (- or /) ema(series, window=degree)
4. `method`: method to be used as detrending operator. Defaults to `subtract`
    - `subtract`: `series` - `source`
    - `divide`: `series` / `source`
5. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`
6. `precision`: precision of values in detrended series. Defaults to `None`
7. `rename`: renames the column names appropriately. Defaults to `True`.

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python
# this gives you [usdtry - (usdtry_forecast = b0 + b1Trend*usdtry)]
det_usdtry = transformator.decompose(usdtry, degree=1, source='trend', method='subtract')

# this gives you [usdtry - (usdtry_forecast = b0 + b1Trend*usdtry + b2Trend^2*usdtry)]
det_usdtry_2 = transformator.decompose(usdtry, degree=2, source='trend', method='subtract')

# this gives you [usdtry / (usdtry_forecast = b0 + b1Trend*usdtry)]
det_usdtry_dv = transformator.decompose(usdtry, degree=1, source='trend', method='divide')

# this gives you [usdtry - simple moving average(usdtry, window=2)]
# degree parameter is representing the sma window here
det_usdtry_sma = transformator.decompose(usdtry, degree=2, source='sma', method='subtract')

# this gives you [usdtry - exponential moving average(usdtry, window=2)]
# degree parameter is representing the ema window here
det_usdtry_ema = transformator.decompose(usdtry, degree=2, source='ema', method='subtract')
```

<a id="smooth-sma"></a>

### __Simple Moving Average: MA<sub>t</sub>(n) = (y<sub>t</sub> + y<sub>t-1</sub> ... y<sub>t-n</sub>) / n__

You can get _Simple Moving Average_ smoothed series through `sma()` method of `Transformator`. Moving
Averages, in general, are good for observing the main streams in series discarding the high frequency
oscillations (can be seen as noises) around the expected values of the series since it smooths out the
excess volatilities. __SMA__ gives the same weights to the observations for given time window and can
be seen as an insensitive process to excess recent value deviations in time.

The full fingerprint of the process is;

MA<sub>t</sub>(n) = (y<sub>t</sub> + y<sub>t-1</sub> ... y<sub>t-n</sub>) / n

The fingerprint of the `sma()` method is:

```python
def sma(
        series: pd.DataFrame,
        window: Union[int, str],
        precision: Optional[int] = None,
        keep_originals: bool = True,
        rename: bool = True
) -> pd.DataFrame:
```

1. `series`: A DataFrame made up of time series.
2. `window`: The window for averaging process (as fixed period or time based).
    - can be anchored to observations: `5` means exactly 5 observations regardless of
    time.
    - can be anchored to time: `5d` means observations that comprising exactly `5` days.
3. `precision`: Precision of returned values. Defaults to `None`
4. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`
5. `rename`: renames the column names appropriately. Defaults to `True`.

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python
# this gives you sma(5)
usdtry_sma5 = transformator.sma(usdtry, window=5)
```


<a id="smooth-ema"></a>

### __Exponential Moving Average: EMA<sub>t</sub>(n) = αy<sub>t</sub> + (1-α)EMA<sub>t-1</sub>__

You can get _Exponential Moving Average_ smoothed series through `ema()` method of `Transformator`.
Moving Averages, in general, are good for observing the main streams in series discarding the high
frequency oscillations (can be seen as noises) around the expected values of the series since it
smooths out the excess volatilities. __EMA__ gives more weights to recent observations for given time
window (or called span) and, therefore can be seen a sensitive process to excess recent value
deviations in time. That may help to detect regime shifs (or structural changes) earlier than SMA
can do.

The full fingerprint of the proces is:

EMA<sub>0</sub> = y<sub>0</sub>  
EMA<sub>t</sub>(n) = αy<sub>t</sub> + (1-α)EMA<sub>t-1</sub>, t: 1...t  
α = 2 / (1 + n)

The fingerprint of the `ema()` method is:

```python
def ema(
        series: pd.DataFrame,
        window: Optional[float]= None,
        alpha: Optional[float] = None,
        precision: Optional[int] = None,
        keep_originals: bool = True,
        rename: bool = True
) -> pd.DataFrame:
```

1. `series`: A DataFrame made up of time series.
2. `window`: The window (or span) for averaging as fixed period.
    - can be given only as fixed values: `5` means exactly `5` observations regardless of time.
3. `alpha`: The smoothing factor given directly.
    - should be in range (0, +1)
3. `precision`: Precision of returned values. Defaults to `None`
4. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`
5. `rename`: renames the column names appropriately. Defaults to `True`.

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python
# this gives you ema(5)
usdtry_ema5 = transformator.ema(usdtry, window=5)

# this also gives you ema(5) since alpha = 2 / (1 + n)
usdtry_ema5 = transformator.ema(usdtry, alpha=0.333)

```

<a id="detect-rollvar"></a>

### __Rolling Vars: ROLVAR<sub>t</sub>(n) = σ<sup>2</sup>(y<sub>t</sub>, y<sub>t-1</sub> ... y<sub>t-n</sub>)__

_Rolling Variances_ in a fixed time period (window) can be a good indication of regime or structural
changes in series. A regime/structural change can be suspected for the series in qustion
once an uncexpected shift is obeserved in the rolling variance. You can get rolling variances for given time
period using `rolling_var()` method.

The fingerprint of the `rolling_var()` method is:

```python
def rolling_var(
                series: pd.DataFrame,
                window: int,
                precision: Optional[int] = None,
                keep_originals: bool = True,
                rename: bool = True
) -> pd.DataFrame:
```

1. `series`: A DataFrame made up of time series.
2. `window`: The window (or period) for rolling variance.
    - can be given only as fixed values: `5` means exactly `5` observations regardless of time.
3. `precision`: Precision of returned values. Defaults to `None`
4. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`
5. `rename`: renames the column names appropriately. Defaults to `True`.

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python
# this gives you rolling variances for 10 daily periods.
usdtry_rolvar_10 = transformator.rolling_var(usdtry, window=10)
```

<a id="detect-rollcorr"></a>

### __Rolling Correlations: ROLCORR<sub>t</sub>(n) = ρ(y<sub>t</sub>, y<sub>t-1</sub> ... y<sub>t-n</sub>)__

_Rolling Correlations_ in a time period (window) can be a good indication of unstable or spurious relitionships
in series. Rolling correlations are especially useful for observing deviations from the long-term linear relitionships
in provided series. Sever swings in observed correlations (especially sign changes) could indicate that
the linear relitionship of two series is not stable in time, that is, no stable long-term relitionship
is engaged in subject series and seeming long-term relitionship between the series could possible be
unstable or spurious. You can get rolling correlations for given time period using `rolling_corr()` method.

The fingerprint of the `rolling_corr()` method is:

```python
def rolling_corr(
                 series: pd.DataFrame,
                 window: int,
                 precision: Optional[int] = None,
                 keep_originals: bool = True,
                 rename: bool = True
) -> pd.DataFrame:
```

1. `series`: A DataFrame made up of time series.
2. `window`: The window (or period) for rolling correlations.
    - can be given only as fixed values: `5` means exactly `5` observations regardless of time.
3. `precision`: Precision of returned values. Defaults to `None`
4. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`
5. `rename`: renames the column names appropriately. Defaults to `True`.

__Availability__:
Can be used for multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python

rates = connector.get_series("usdtry, eurtry",
                             start_date="01.06.2022",
                             end_date="30.06.2022",
                             frequency="B")

# this gives you rolling correlations between usdtry and eurtry for 10 daily periods.
rates_rolcorr_10 = transformator.rolling_corr(rates, window=10)

rates = connector.get_series("usdtry, eurtry, gbptry",
                             start_date="01.06.2022",
                             end_date="30.06.2022",
                             frequency="B")

# this gives you rolling correlations between usdtry-eurtry, usdtry-gbptry and eurtry-gbptry for 10 daily periods
rates_rolcorr_10 = transformator.rolling_corr(rates, window=10)
```

<a id="get-z-score"></a>

### __Z-Score: Z<sub>t</sub> = (y<sub>t</sub> - ȳ) / σ<sub>y</sub>__

The _Z-Score_ describes the position of a raw score in terms of its distance from the mean, when measured
in standard deviation units. Z-Score is a good measure for spotting deviations from the expected values
for a series which is normally distributed y:~N(μ, σ). Observing z-scores bigger than `+3` or smaller
than `-3` can be a good indication that the subject value is a suspected outlier even if the series are
not normally distributed under the assumptions of big sample size. You can get z-scores for provided
series using `z_score()` method.

The fingerprint of the `z_score()` method is:

```python
def z_score(
            series: pd.DataFrame,
            precision: Optional[int] = None,
            keep_originals: bool = True,
            rename: bool = True
) -> pd.DataFrame:
```

1. `series`: A DataFrame made up of time series.
2. `precision`: Precision of returned values. Defaults to `None`
3. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`
4. `rename`: renames the column names appropriately. Defaults to `True`.

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python
# this gives you all z-scores for all observations in all series provided.
usdtry_z = transformator.z_score(usdtry, precision=2)
```


<a id="get-mad"></a>

### __Median Absolute Deviation: median(|y<sub>t</sub> - median(y<sub>t</sub>)|)__

The _Median Absolute Deviation_ (__MAD__) describes the position of a median score in terms of its
distance from the median, when measured in absolute terms. It is very useful for describing the
variability of series with outliers. The median absolute deviation is a robust statistic, even for data
drawn from non-normal populations and could be used instead of z-score for measuring deviations from
the expectations as a substitute. Observing MADs bigger than `+3` or smaller than `-3` can be a good
indication that the subject value is a suspected outlier even if the series are not normally
distributed under the assumptions of big sample size. You can get MADs for provided series using
`mad()` method.

The fingerprint of the `mad()` method is:

```python
def mad(
        series: pd.DataFrame,
        precision: Optional[int] = None,
        keep_originals: bool = True,
        rename: bool = True
) -> pd.DataFrame:
```

1. `series`: A DataFrame made up of time series.
2. `precision`: Precision of returned values. Defaults to `None`
3. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`
4. `rename`: renames the column names appropriately. Defaults to `True`.

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python
# this gives you all median absoulte deviations for all observations in all series provided.
usdtry_mad = transformator.mad(usdtry, precision=2)
```

<a id="get-normalized"></a>

### __Normalized Series: y<sub>t, normal</sub> = F(y<sub>t</sub>)__

You can get nomralized series for given series to use them as inputs for other processes such as
machine learning algorithms. You can use `normalize()` method to get normalized series.

There are `6` normalization methods are defined in order to be used in normalization process, and
these are:

|Method        | Definition                                              | Range         |
|:-------------|:------------------------------------------------------- |:--------------|
|`simple`      |  x / (max(x) + 1)                                       | [0, +1)       |
| `min - max`  | (x - min(x)) / (max(x) - min(x))                        | (0, 1]        |
| `mean`       | (x - x̄) / (max(x) + 1)                                  | [-1, +1)      |
| `median`     | (x - median(x)) / (max(x) + 1)                          | [-1, +1)      |
| `mad`        | (x - median(x)) / (median(\|(x - median(x)\|)) * 1.4826 | (-inf, +inf)  |
| `z`          | (x- x̄) / σ<sub>x</sub>                                  | (-inf, +inf)  |

> 1.4826 is the scale factor and is equal to `1 / QNormal(%75)`

The fingerprint of the `normalize()` method is:

```python
def normalize(
              series: pd.DataFrame,
              method: str = "mad",
              precision: Optional[int] = None,
              keep_originals: bool = True,
              rename: bool = True
) -> pd.DataFrame:
```

1. `series`: A DataFrame made up of time series.
2. `method`: normalization method. Defaults to `mad`
    - `simple`: x / (max(x) + 1) -> range: [0, +1)
    - `min - max`: (x - min(x)) / (max(x) - min(x)) -> range: (0, 1]
    - `mean`: (x - mu(x)) / (max(x) + 1) -> range: [-1, +1)
    - `median`: (x - median(x)) / (max(x) + 1) -> range: [-1, +1)
    - `mad`: (x - median(x)) / (median(abs(x - median(x))) * 1.4826) -> range: [-inf, +inf]
    - `z`: (x- mu(x)) / sigma(x) -> range: (-inf, +inf)
3. `precision`: Precision of returned values. Defaults to `None`
4. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`
5. `rename`: renames the column names appropriately. Defaults to `True`.

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python
# this gives you normalized values (z-scores in this example) by given normalize method.
usdtry_normalized = transformator.normalize(usdtry, method="z")
```

<a id="get-dummies"></a>

### __Dummy Series: D<sub>n</sub>__

You can use `dummy()` method to create dummy series in line with given conditions. Dummy series are
very useful for modelling a structural/regime change or brake, and outliers in some applications.

The fingerprint of the `dummy()` method is:

```python
def dummy(
            series: pd.DataFrame,
            condition: str,
            threshold: Union[float, str, int, Sequence[Union[float, str, int]]],
            fill_true: float = 1,
            fill_false: float = 0,
            precision: Optional[int] = None,
            keep_originals: bool = True,
            rename: bool = True
) -> pd.DataFrame:
```

1. `series`: A DataFrame made up of time series.
2. condition (str): Evaluation condition for cutoff or bounds.
    - `>` : greater than threshold
    - `>=`: greater than or equals to threshold
    - `<` : smaller than threshold
    - `<=`: smaller than or equals to threshold
    - `()`: greater than lower bound and smaller than upper bound (closed bounds).
    - `[]`: greater than or equal to lower bound and smaller than or equal to upper bound (open bounds).
3. threshold: The cutoff or bound points for dummy creation (e.g: `5` for `x > 5` condition or `1, 4`,
`(1, 4)` or `[1, 4]`for `1 < x < 4` condition)
4. `fill_true`: Value to be filled if the given condition is `True` Defaults to `1`.
5. `fill_false`: Value to be filled if the given condition is `False`. Defaults to `0`.
6. `precision`: Precision of returned values. Defaults to `None`
7. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`
8. `rename`: renames the column names appropriately. Defaults to `True`.

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

Conditions to be used;

| condition | explanation
|:---------:|-----------------------------------------------------------------------------------------------|
| `>`       | greater than threshold                                                                        |
| `>=`      | greater than or equals to threshold                                                           |
| `<`       | smaller than threshold                                                                        |
| `<=`      | smaller than or equals to threshold                                                           |
| `()`      | greater than lower bound and smaller than upper bound (closed bounds)                         |
| `[]`      | greater than or equal to lower bound and smaller than or equal to upper bound (open bounds)   |

```python
# this gives you a dummy series that its values are equal to 1 if a value in usdtry is greater than 9 and 0 otherwise.
usdtry_gt9 = transformator.dummy(usdtry, ">", 9)

# this gives you a dummy series that its values are equal to 1 if a value in usdtry is greater than 10 and -1 otherwise.
usdtry_gt10 = transformator.dummy(usdtry, ">", 10, fill_true=1, fill_false=-1)

# this gives you a dummy series that its values are equal to 2 if a value in usdtry is smaller or
# equal than 11 and 1 otherwise.
usdtry_st11 = transformator.dummy(usdtry, "<=", 11, fill_true=2, fill_false=1)

# this gives you a dummy series that its values are equal to 1 if a value in usdtry is greater than 8
# or smaller than 10 (closed bounds).
usdtry_g8_l10 = transformator.dummy(usdtry, "()", "8, 10")

# this gives you a dummy series that its values are equal to 1 if a value in usdtry is equal or greater than 8
# or equal or smaller than 10 (open bounds).
usdtry_g8_l10 = transformator.dummy(usdtry, "[]", "8, 10")

# bounds can be given as lists or tuples as well
open_bounds = [8, 10]
usdtry_g8_l10 = transformator.dummy(usdtry, "[]", open_bounds)

```

<a id="get-laggeds"></a>

### __Lagged Series: y<sub>t-1</sub>, y<sub>t-2</sub> ... y<sub>t-n</sub>__

You can use `laggeds()` method to get lagged series of given series. This series can be useful for
some specific modelling and, correcting the serial correlation problem in general.

The fingerprint of the `laggeds()` method is:

```python
def laggeds(
            series: pd.DataFrame,
            range_lags: Optional[int] = None,
            lags: Optional[Union[int, Sequence, str]] = None,
            precision: Optional[int] = None,
            keep_originals=True
) -> pd.DataFrame:
```

1. `series`: A DataFrame made up of time series.
2. `range_lags`: An integer number indicating lags in range. Defaults to `None`
3. `lags`: lags.
    - given `n` means only the nth. lag. For instance; `5` means: y<sub>t-5</sub>
    - can be given in a `Sequence` type container like `(3, 6, 9, 12)` or `[3, 6, 9, 12]`
    indicating: y<sub>t-3</sub>, y<sub>t-6</sub>, y<sub>t-9</sub>, y<sub>t-12</sub>
    - can be given as a comma separated string like `"3, 4"` indicating: y<sub>t-3</sub>, y<sub>t-4</sub>
4. `precision`: Precision of returned values. Defaults to `None`
5. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`
6. `rename`: renames the column names appropriately. Defaults to `True`.

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python
# this gives you only usdtry(t-2)
usdtry_l2 = transformator.laggeds(usdtry, lags=2)

# this gives you usdtry(t-1), usdtry(t-3) and usdtry(t-5)
usdtry_135 = transformator.laggeds(usdtry, lags="1, 3, 5")

lags = [1, 3, 5]
# this also gives you usdtry(t-1), usdtry(t-3) and usdtry(t-5)
usdtry_135 = transformator.laggeds(usdtry, lags=lags)

# this gives you usdtry(t-1), usdtry(t-2), usdtry(t-3)
usdtry_3 = transformator.laggeds(usdtry, range_lags=3)

# this gives you usdtry(t-1), usdtry(t-2), usdtry(t-6), usdtry(t-12)
usdtry_12612 = transformator.laggeds(usdtry, range_lags=2, lags="6, 12")

```

<a id="get-corr"></a>

### __Correlation Coefficients: ρ(y<sub>t</sub>, x<sub>t</sub>)__

You can use `corr()` method to get correlation coefficients between given series. This is especially
important for easily detecting possible multi co-linearity problem in considering model.
Significant correlations (`ρ > 0.6` or `ρ < -0.6` in general) between considering independent
variables for a model indicate that the considering model will probably suffer from multi co-linearity
problem. You can get `Pearson Linear`, `Kendall Tau`, and `Spearman Rank` correlation coefficients using
`corr()` method.

The fingerprint of the `corr()` method is:

```python
def corr(
         series: pd.DataFrame,
         method: str = "pearson",
         precision: Optional[int] = None,
         rename: bool = True
) -> pd.DataFrame:
```

1. `series`: A DataFrame made up of time series.
2. `method`: Method of correlation computations. Defaults to `pearson`
    - `pearson` : standard Pearson correlation coefficients
    - `kendall` : Kendall Tau correlation coefficients.
    - `spearman` : Spearman rank correlation coefficients
3. `precision`: Precision of returned values. Defaults to `None`

> Notice that computing the Kendall Tau correlation coefficients requires the `scipy` package.

__Availability__:
Can be used for multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python

# get series using reference names
series = connector.get_series("usdtry, eurtry",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="M")

# this gives you the Pearson's linear correlation coeeficient between usdtry and eurtry series
corrs = transformator.corr(series)

# This gives you the Spearman rank correlation coefficients between usdtry and eurtry series
corrs_sp = transformator.corr(series, method='spearman')

```

<a id="get-auto-corr"></a>

### __Autocorrelation Coefficients: AUTOCORR<sub>t</sub> = ρ<sub>t, t-n</sub>__

You can use `autocorr()` method to get autocorrelations between the original series and given lags of
them. The autocorrelations could provide you a very quick insight about the stationary state of the
series provided. Significant correlations (`ρ > 0.6` or `ρ < -0.6` in general) between the series
and its laggeds indicates that the observations are highly dependent on their prior values in time,
and therefore, that would indicate that the mean of the series depends on and changes through time
(a possible stochastic trend flag).

The fingerprint of the `autocorr()` method is:

```python
def autocorr(
            series: pd.DataFrame,
            range_lags: Optional[int] = None,
            lags: Optional[Union[int, Sequence, str]] = None,
            method: str = 'pearson',
            column: Optional[Union[str, int]] = None,
            precision: Optional[int] = None
) -> pd.DataFrame:
```

1. `series`: A DataFrame made up of time series.
2. `range_lags`: An integer number indicating lags in range.
3. `lags`: lags.
    - given `n` means only the nth. lag. For instance; `5` means: y<sub>t-5</sub>
    - can be given in a `Sequence` type container like `(3, 6, 9, 12)` or `[3, 6, 9, 12]`
    indicating: y<sub>t-3</sub>, y<sub>t-6</sub>, y<sub>t-9</sub>, y<sub>t-12</sub>
    - can be given as a comma separated string like `"3, 4"` indicating: y<sub>t-3</sub>, y<sub>t-4</sub>
4. `method`: Method of correlation computations. Defaults to `pearson`
    - `pearson` : standard Pearson correlation coefficients
    - `kendall` : Kendall Tau correlation coefficients.
    - `spearman` : Spearman rank correlation coefficients
5. `column`: column name for DataFrames including series more than `1`. Defaults to `None`.
6. `precision`: Precision of returned values. Defaults to `None`

> Notice that computing the Kendall Tau correlation coefficients requires the `scipy` package.

__Availability__:
Can be used for one (e.g: usdtry) dimentional series.

__Cases__:

```python

# this gives you the aoutocorrelations between usdtry and usdtry(t-1), usdtry(t-2), usdtry(t-3)
autocorrs = transformator.autocorr(usdtry, range_lags=3)

# this gives you the aoutocorrelations between usdtry and usdtry(t-1), usdtry(t-3), usdtry(t-5)
autocorrs = transformator.autocorr(usdtry, lags="1, 3, 5")

# this gives you the aoutocorrelations between;
# usdtry and usdtry(t-1), usdtry(t-2), usdtry(t-3), usdtry(t-4) and usdtry(t-12)
autocorrs = transformator.autocorr(usdtry, range_lags=4, lags=12)

# get series using reference names
series = connector.get_series("usdtry, eurtry",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="M")

# notice the seris are made up of two columns that usdtry and eurtry here.
# this gives you the aoutocorrelations between usdtry and usdtry(t-1), usdtry(t-3), usdtry(t-5)
autocorrs = transformator.autocorr(series, lags="1,3,5", column='usdtry')


rates = connector.get_series("usdtry, eurtry",
                              start_date="01.01.2020",
                              end_date="01.01.2022",
                              frequency="Q")

# you can use 'column' parameter to get autocorrelations for any series in given dataframe
# column can be given as column name or column index (starting from 0)

# this picks eurtry and gives autocorrelations
eurtry_autocorr = transformator.autocorr(rates, column='EURTRY', range_lags=4, precision=4)

# this also picks picks eurtry and gives autocorrelations since the column index of eurtry is 1
eurtry_autocorr = transformator.autocorr(rates, column=1, range_lags=4, precision=4)

```

<a id="get-serial-corr"></a>

### __Serial Correlation Coefficients: SERIALCORR<sub>t</sub> = ρ<sub>t, x-n</sub>__

You can use `serial_corr()` method to get a correlation vector between the constant and the others.
The vector could provide you a very quick insight about linear relitionships between a constant series
and the others including their lags.

The fingerprint of the `serial_corr()` method is:

```python
def serial_corr(
                series: pd.DataFrame,
                hold: Union[str, int],
                range_lags: Optional[int] = None,
                lags: Optional[Union[int, Sequence, str]] = None,
                method: str = 'pearson',
                precision: Optional[int] = None
) -> pd.DataFrame:
```

1. `series`: A DataFrame made up of time series.
2. `hold`: the constant series for the correcation vector
3. `range_lags`: An integer number indicating lags in range.
4. `lags`: lags.
    - given `n` means only the nth. lag. For instance; `5` means: y<sub>t-5</sub>
    - can be given in a `Sequence` type container like `(3, 6, 9, 12)` or `[3, 6, 9, 12]`
    indicating: y<sub>t-3</sub>, y<sub>t-6</sub>, y<sub>t-9</sub>, y<sub>t-12</sub>
    - can be given as a comma separated string like `"3, 4"` indicating: y<sub>t-3</sub>, y<sub>t-4</sub>
4. `method`: Method of correlation computations. Defaults to `pearson`
    - `pearson` : standard Pearson correlation coefficients
    - `kendall` : Kendall Tau correlation coefficients.
    - `spearman` : Spearman rank correlation coefficients
5. `precision`: Precision of returned values. Defaults to `None`



> Notice that computing the Kendall Tau correlation coefficients requires the `scipy` package.

__Availability__:
Can be used for one (e.g: usdtry) dimentional series.

__Cases__:

```python

# get series using reference names
series = connector.get_series("usdtry, eurtry",
                              start_date="01.01.2014",
                              end_date="31.12.2021",
                              frequency="M")

# this gives you the the correlaciton (vector as fixing usdtry) between:
# usdtry and eurtry, usdtry(t-1), usdtry(t-2), usdtry(t-3), usdtry(t-4), usdtry(t-12)
# eurtry(t-1), eurtry(t-2), eurtry(t-3), eurtry(t-4), eurtry(t-12)
sc_vector = transformator.serial_corr(series, hold="usdtry", range_lags=4, lags=12)

# this holds usddtry as the constant since the column index of usdtry=0 and gives the correlations
# with eurtry including given lags.
sc_vector = transformator.serial_corr(series, hold=0, range_lags=4, lags=12)

```

<a id="get-outliers"></a>

### __Outliers__

You can use `outliers()` method to create dummy series for detected outliers in given series.

The fingerprint of the `outliers()` method is:

```python
def outliers(
            series: pd.DataFrame,
            method: str = 'mad',
            critical_upper: float = 3.0,
            critical_lower: float = -3.0,
            precision: Optional[int] = None,
            keep_originals: bool = True,
            rename: bool = True
) -> pd.DataFrame:
```

1. series (pd.DataFrame): DataFrame consists of series to be evaluated.
2. `method`: outliers detection method. Defaults to `mad`.
    - `mad`: outliers are detected using _mean absolute deviation_. This is the preferred
    method for the series that are not normally distributed since the detection
    algorithm is still robust.
    - `z`: outliers are detected using deviations from __standard normal distribution__.
    This could be the preferable way for the series which are normally distributed.
3. `critical_upper`: upper critical value for deviations. Defaults to `3.0`
4. `critical_lower`: lower critical value for deviations. Defaults to `-3.0`
5. `precision`: Precision of returned values. Defaults to `None`
6. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`
7. `rename`: renames the column names appropriately. Defaults to `True`.

__Explanation__:

Returned dummy series consist of `0`s and `1`s indicating:
- `1`: an outlier values is detected in corresponding date.
- `0`: the value is in the bound of expectations.

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python
# this gives you detected outliers in line with mad and -3, +3 critical values bounds.
usdtry_outliers_d = transformator.outliers(usdtry)

# this gives you detected outliers in line with mad and -3, +2 critical values bounds.
usdtry_outliers_d = transformator.outliers(usdtry, critical_upper=2, critical_lower=-3)

# this gives you detected outliers in line with z-score and -3, +3 critical values bounds.
usdtry_outliers_d = transformator.outliers(usdtry, method="z")

```

<a id="get-smoothed"></a>

### __Smoothed Series__

You can use `smooth()` method to get smoothed out series against outlier values in line with given
outliers detection criteria. Removing outliers through smoothing and using smoothed series as a substitute of originals
is a good way for modelling the general behaviors between variables instead of modelling for precise forecasting.

The fingerprint of the `smooth()` method is:

```python
    def smooth(
               series: pd.DataFrame,
               method: str = 'mad',
               critical_upper: float = 3.0,
               critical_lower: float = -3.0,
               smooth_method: str = 'ema',
               smooth_window: int = 2,
               precision: Optional[int] = None,
               keep_originals: bool = True,
               rename: bool = True
    ) -> pd.DataFrame:
```

1. series (pd.DataFrame): DataFrame consists of series to be evaluated.
2. `method`: outliers detection method. Defaults to `mad`.
    - `mad`: outliers are detected using _mean absolute deviation_. This is the preferred
    method for the series that are not normally distributed since the detection
    algorithm is still robust.
    - `z`: outliers are detected using deviations from __standard normal distribution__.
    This could be the preferable way for the series which are normally distributed.
3. `critical_upper`: upper critical value for deviations. Defaults to `3.0`
4. `critical_lower`: lower critical value for deviations. Defaults to `-3.0`
5. `smooth_method`: method that is used for smoothing the detected outliers. Defaults to `ema`
    - can be used either `sma` or `ema`
6. `smooth_window`: e(ma) window (how many values will be used for smoothing) Defaults to `2`
7. `precision`: Precision of returned values. Defaults to `None`
8. `keep_originals`: Includes original series in returned DataFrame if `True`. Defaults to `True`
9. `rename`: renames the column names appropriately. Defaults to `True`.

__Explanation__:

Returned series from `smooth()` method consist of:
- Smoothed Values: For detected outliers.
- Original Observations: For inbound values.
- Smoothing is done using given smooth method (ema or sma) and its window

__Availability__:
Can be used for one (e.g: usdtry) or multi-dimentional (e.g: exchange_rates consists of usdtry and eurtry series) series.

__Cases__:

```python
# get series using reference names
series = connector.get_series("usdtry, eurtry",
                              start_date="01.01.2014",
                              end_date="31.12.2021",
                              frequency="M")

# this gives you smoothed series in which outliers detected in line with mad bounds (-3.0, +3.0)
# and out of bound values (if detected) are smoothed with sma(series, 5) values, whereas, in bound
# values are not touched.
smoothed_mad = transformator.smooth(series, smooth_method='sma', smooth_window=5)

# this gives you smoothed series in which outliers detected in line with z-score bounds (-1.96, +1.96)
# and out of bound values (if detected) are smoothed with ema(series, 2) values, whereas, in bound
# values are not touched.
smoothed_z = transformator.smooth(series, method="z", critical_upper=1.96, critical_lower=-1.96)


# get series using reference names
rates = connector.get_series("usdtry, eurtry",
                              start_date="01.01.2014",
                              end_date="31.12.2021",
                              frequency="M")

# this gives you smoothed rates in which outliers detected in line with z-score bounds (-2.56, +2.56)
# and out of bound values (if detected) are smoothed with ema(series, 3) values, whereas, in bound
# values are not touched.
smoothed_rates = transformator.smooth(
    series=rates,
    method='z',
    critical_lower=-2.56,
    critical_upper=2.56,
    smooth_method='ema',
    smooth_window=3,
    keep_originals=False,
    precision=2
)

```

<a id="joining-methods"></a>

## __Joining The Connector and Transformator Methods__

You can chain both `Connector` and `Transformator` class methods if you would like to do so.

__Cases__:

```Python

connector = Connector()          # assuming you have already saved your API Key on disk.
transformator = Transformator()



# below cases assumes you have already saved reference names like below:
# usdtry -> 'TP.DK.USD.A.YTL'
# eurtry -> 'TP.DK.EUR.A.YTL'


# this gives you smoothed usdtry and eurtry
smoothed_rates = (
    transformator
    .smooth(
            connector
            .get_series("usdtry, eurtry", start_date="01.01.2014", end_date="31.12.2021", frequency="M")
    )
)

# This also gives you smoothed usdtry and eurtry
smoothed_rates = transformator.smooth(
    connector.get_series("usdtry, eurtry", start_date="01.01.2014", end_date="31.12.2021", frequency="M")
)

# This gives you smoothed usdtry and eurtry evaluating with z_score bounds (-1.96, +1.96), but,
# notice the original usdtry and eurtry series is not included in returned smoothed data here
# since the 'keep_originals' flag is set to `False`
smoothed_rates = (
    transformator
    .smooth(
            series=connector.get_series("usdtry, eurtry", start_date="01.01.2014", end_date="31.12.2021", frequency="M"),
            method="z", critical_lower=-1.96, critical_upper=1.96, keep_originals=False
    )
)

# this gives you sma(usdtry, 3), sma(eurtry, 3) and 2 dummy series which are:

# USDTRY_SMA_3_GTT_9:
# 1, if 12 < sma(usdtry, 3) < 10
# 0, otherwise

# EURTRY_SMA_3_GTT_9:
# 1, if 12 < sma(eurtry, 3) < 10
# 0, otherwise

rates_sma_3_dummy = (
    transformator
     .dummy(
        transformator
         .sma(
            connector
                .get_series("usdtry, eurtry", start_date="01.01.2014", end_date="31.12.2021", frequency="M")
         , window=3, keep_originals=False)
     , condition="()", threshold=(10, 12)
     )
)

```

<a id="defined-exceptions-1"></a>

## __Defined Exceptions__

Here you can find the defined custom exceptions and the conditions they are raised.

|Exception                             | Explanation
|--------------------------------------|--------------------------------------------------------------------------------|
|`AmbiguousFunctionMappingException` |Raises if transformation and aggregation functions are applied at the same time   |
|`AmbiguousFunctionParameterException`|Raises if a function takes an ambiguous parameter set|
|`AmbiguousOutputTypeException` |Raises if raw and dictionary types are requested at once|
|`APIServiceConnectionException` |Raises when an API key, API Server, API Request and network based exceptions are occured|
|`GroupNotFoundException` |Raises when a group of sub-category is not found|
|`InsufficientSampleSizeException` |Raises if a process needs a larger size sample than provided|
|`OptionalPackageRequiredException` |Raises if a required optional package is not found on environment|
|`SeriesNotFoundException` |Raises when a series is not found|
|`SubCategoryNotFoundException` |Raises when a sub-category is not found|
|`UndefinedAggregationFunctionException` |Raises when an undefined aggregation function is given as a parameter|
|`UndefinedFrequencyException` |Raises when a given or API returned time series frequency can not be identified|
|`UndefinedTransformationFunctionException` |Raises when an undefined transformation function is given as a parameter|
|`UnknownTimeSeriesIdentifierException` |Raises when a given series name is not found on API server|
|`UnmatchingFieldSizeException` |Raises when given series names count is different than API returned series count|
|`UnmatchingParameterSizeException` |Raises when given parameters sizes don't match each other|
|`WrongAPIKeyException` |Raises when used EDDS Service API Key is wrong|
|`WrongDateFormatException` |Raises when a given date format can not be identified|
|`WrongDateRangeException` |Raises if given date is out of range|
