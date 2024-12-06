"""evdsts EVDSConfig Class"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "1.0rc5"
__internal__ = "0.0.1"


#? could also be implemented using:
# 1: json: not very useful and error prone.
# 2: yaml: more useful than json but needs an external package to be installed to implement.
# 3: dataclasses: requires Python > 3.6 (trying to stay in 3.6)
# 4: omegaconf: could be the best for the project but needs an external package.
# 5: pydantic: needs an external package. (trying to stay in just pandas and requests)
# 6: hydra: needs an external package and too complex for a project like this.

from typing import Dict, List, Tuple

from evdsts.configuration.globals import (
    URL_MAIN_CATEGORIES, URL_SUB_CATEGORIES, URL_GROUPS, URL_SERIES, URL_SIGN_UP, DEFINED_LANGUAGES,
    NOT_AVAILABLE_CATEGORIES, FREQUENCY_MAP, CATEGORY_ID, TRANSFORMATIONS_MAP, AGGREGATIONS_MAP,
    ENGLISH_FREQUENCY_MAP, REFERENCE_FILE, DATAGROUP_CODE, DATAGROUP_NAME, FREQUENCY_STR,
    START_DATE, END_DATE, SERIES_NAME, SERIES_CODE, TOPIC_TITLE, UNIXTIME, YEARWEEK, INDEX_FILE_TR,
    INDEX_FILE_EN, KEY_FILE, DATE_SEPARATORS, FREQUENCY_REGEXES, RAW_ITEMS
)


class EVDSTSConfig:

    """Config class for global variables all over the evdsts"""

    # can be converted to a dataclass with just a decorator.

    url_main_categories: str = URL_MAIN_CATEGORIES
    url_sub_categories: str = URL_SUB_CATEGORIES
    url_groups: str = URL_GROUPS
    url_series: str = URL_SERIES
    url_sign_up: str = URL_SIGN_UP
    defined_languages: Dict[str, str] = DEFINED_LANGUAGES
    not_available_categories: List[int] = NOT_AVAILABLE_CATEGORIES
    frequency_map: Dict[Tuple[str, str, str, int], str] = FREQUENCY_MAP
    category_id: str = CATEGORY_ID
    transformations_map: Dict[Tuple[str, str, int], str] = TRANSFORMATIONS_MAP
    aggregations_map: Dict[Tuple[str, str, int], str] = AGGREGATIONS_MAP
    english_frequency_map: Dict[str, str] = ENGLISH_FREQUENCY_MAP
    reference_file: str = REFERENCE_FILE
    datagroup_code: str = DATAGROUP_CODE
    datagroup_name: str = DATAGROUP_NAME
    frequency_str: str = FREQUENCY_STR
    start_date: str = START_DATE
    end_date: str = END_DATE
    series_name: str = SERIES_NAME
    series_code: str = SERIES_CODE
    topic_title: str = TOPIC_TITLE
    unixtime: str = UNIXTIME
    yearweek: str = YEARWEEK
    index_file_tr: str = INDEX_FILE_TR
    index_file_en: str = INDEX_FILE_EN
    key_file: str = KEY_FILE
    date_separators: List[str] = DATE_SEPARATORS
    frequency_regexes: Dict[str, List[str]] = FREQUENCY_REGEXES
    raw_items: str = RAW_ITEMS
