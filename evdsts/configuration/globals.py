"""evdsts Defined Global Variables"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "1.0rc5"
__internal__ = "0.0.1"


from pathlib import Path
from typing import Dict, List, Tuple

#* Define constants that doesn't change by instance to make further code refactoring easy
#* and independent on class.

#* Define URLs.
URL_MAIN_CATEGORIES: str = 'https://evds2.tcmb.gov.tr/service/evds/categories/'
URL_SUB_CATEGORIES: str = 'https://evds2.tcmb.gov.tr/service/evds/datagroups/'
URL_GROUPS: str = 'https://evds2.tcmb.gov.tr/service/evds/serieList/'
URL_SERIES: str = 'https://evds2.tcmb.gov.tr/service/evds/'
URL_SIGN_UP: str = 'https://evds2.tcmb.gov.tr/index.php?/evds/login'

#* Define languages
DEFINED_LANGUAGES: Dict[str, str] = {

    "TR": "TR",
    "TUR": "TR",
    "tr": "TR",
    "tur": "TR",
    "ENG": "ENG",
    "EN": "ENG",
    "eng": "ENG",
    "en": "ENG",
}

#* Define constant fields in API Service returned data.

CATEGORY_ID: str = "CATEGORY_ID"
DATAGROUP_CODE: str = "DATAGROUP_CODE"
DATAGROUP_NAME: str = "DATAGROUP_NAME"
FREQUENCY_STR: str = "FREQUENCY_STR"
TOPIC_TITLE: str = "TOPIC_TITLE"
SERIES_CODE: str = "SERIE_CODE"
SERIES_NAME: str = "SERIE_NAME"
START_DATE: str = "START_DATE"
END_DATE: str = "END_DATE"
UNIXTIME: str = "UNIXTIME"
YEARWEEK: str = "YEARWEEK"

#* Define not available categories.
NOT_AVAILABLE_CATEGORIES: List[int] = [17]

#* Define separators that is currently used or will possible used by the EVDS API to separate
#* date fields each other.
DATE_SEPARATORS = ["-", ".", "/"]

#* Define frequency detection regexes for time series convertions.
#* Use a future proof approch like allowing (-,./ and \)
#* for separating dates or Ç and H for determining quarterly and semiyearly frequency.
#* weekly data can include YEARWEEK field so create a regex for that structure too.
FREQUENCY_REGEXES: Dict[str, List[str]] = {

    "daily": [r"\b(?:[0]*[1-9]|[1-2][0-9]|[3][0-1])(?:-|\.|/|\\)(?:[0]*[1-9]|[1][0-2])(?:-|\.|/|\\)\d{4}\b"],
    "bdaily": [r"\b(?:[0]*[1-9]|[1-2][0-9]|[3][0-1])(?:-|\.|/|\\)(?:[0]*[1-9]|[1][0-2])(?:-|\.|/|\\)\d{4}\b"],
    "weekly": [r"\b(?:[0]*[1-9]|[1-2][0-9]|[3][0-1])(?:-|\.|/|\\)(?:[0]*[1-9]|[1][0-2])(?:-|\.|/|\\)\d{4}\b"],
    "semimonthly": [r"\b(?:15|28|29|30|31)(?:-|\.|/|\\)(?:[0]*[1-9]|[1][0-2])(?:-|\.|/|\\)\d{4}\b"],
    "monthly": [r"\b\d{4}(?:-|\.|/|\\)(?:[0]*[1-9]|[1][0-2])\b"],
    "quarterly": [r"\b\d{4}(?:-|\.|/|\\)(?:Q|q|Ç|ç)0*[1-4]\b"],
    "semiyearly": [r"\b\d{4}(?:-|\.|/|\\)(?:S|s|H|h)0*[1-2]\b"],
    "yearly": [r"^\b(?:19[0-9][0-9]|2[0-9][0-9][0-9])\b$"],
}

#* Define a frequency map that all keys can be used for getting corresponding identifier as
#* API parameter.
FREQUENCY_MAP: Dict[Tuple[str, str, str, int], str] = {

    ("default", "level", "0", 0): "",
    ("daily", "D", "1", 1): "1",
    ("bdaily", "B", "2", 2): "2",
    ("weekly", "W", "3", 3): "3",
    ("semimonthly", "SM", "4", 4): "4",
    ("monthly", "M", "5", 5): "5",
    ("quarterly", "Q", "6", 6): "6",
    ("semiyearly", "6M", "7", 7): "7",
    ("yearly", "Y", "8", 8): "8",
}

#* Define a transformation functions map that all keys can be used for getting
#* corresponding identifier as API parameter.
TRANSFORMATIONS_MAP: Dict[Tuple[str, str, int], str] = {

    ("level", "0", 0): "0",
    ("percent", "1", 1): "1",
    ("diff", "2", 2): "2",
    ("ypercent", "3", 3): "3",
    ("ydiff", "4", 4): "4",
    ("ytdpercent", "5", 5): "5",
    ("ytddiff", "6", 6): "6",
    ("mov", "7", 7): "7",
    ("movsum", "8", 8): "8",
}

#* Define an aggregation functions map that all keys can be used for getting
#* corresponding identifier as API parameter.
AGGREGATIONS_MAP: Dict[Tuple[str, str, int], str] = {

    ("avg", "1", 1): "avg",
    ("min", "2", 2): "min",
    ("max", "3", 3): "max",
    ("first", "4", 4): "first",
    ("last", "5", 5): "last",
    ("sum", "6", 6): "sum",
}

ENGLISH_FREQUENCY_MAP: Dict[str, str] = {

    "0": "UNKNOWN",
    "GÜNLÜK": "DAILY",
    "İŞ GÜNÜ": "BUSINESS DAILY",
    "HAFTALIK": "WEEKLY",
    "HAFTALIK(CUMA)": "WEEKLY (FRIDAY)",
    "AYLIK": "MONTHLY",
    "ÜÇ AYLIK": "QUARTERLY",
    "ALTI AYLIK": "SIX MONTHLY",
    "YILLIK": "YEARLY"
}

#* API Key file path to save and load API Key.
KEY_FILE: str = str(Path.cwd() / Path("evds_api_key.json"))

#* Name references file path to save and load references.
REFERENCE_FILE: str = str(Path.cwd() / Path("evds_series_references.json"))

#* Series index file path to search operations.
INDEX_FILE_TR: str = str(Path(__file__).parent.parent / Path("data") / Path("evds_index_tr.json"))
INDEX_FILE_EN: str = str(Path(__file__).parent.parent / Path("data") / Path("evds_index_en.json"))

#* Define raw JSONType data related variables.
RAW_ITEMS: str = "items"
