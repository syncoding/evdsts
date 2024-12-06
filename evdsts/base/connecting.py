"""evdsts Connector Class"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "1.0rc5"
__internal__ = "0.0.3"


from datetime import datetime, timedelta
import json
from json import JSONDecodeError
from pathlib import Path
from string import ascii_letters, digits
from typing import Optional, Sequence, Union, Any, List, Tuple, Dict
from urllib.error import HTTPError
import webbrowser
import ssl


import pandas as pd
import requests
from requests import Timeout
from requests.exceptions import RequestException

from evdsts.base.searching import SearchEngine
from evdsts.base.transforming import _set_precision
from evdsts.configuration.cfg import EVDSTSConfig
from evdsts.configuration.types import JSONType, EVDSHttpAdapter
from evdsts.configuration.exceptions import (
    AmbiguousFunctionMappingException, APIServiceConnectionException, SubCategoryNotFoundException,
    UndefinedAggregationFunctionException, UndefinedFrequencyException,
    UndefinedTransformationFunctionException, UnknownTimeSeriesIdentifierException,
    UnmatchingParameterSizeException, WrongAPIKeyException, GroupNotFoundException,
    AmbiguousOutputTypeException, SeriesNotFoundException, AmbiguousFunctionParameterException
)
from evdsts.utils.general import (
    copy_file, delete_file, drop_columns, drop_na_columns, join_sequentials, load_json,
    set_column_names, write_data, write_json
)
from evdsts.utils.time_series import (
    as_real, convert_to_business_date ,convert_to_time_series, correct_date, find_current_date,
    get_period, parse_dates
)


class Connector:

    """TCMB (CBRT) EVDS (EDDS) API Service Connector Class."""

    @classmethod
    def request_key(cls, language="ENG") -> None:

        """Instructions to get API Key from EVDS API Service"""

        if language.lower() in ("tr", "turkce"):
            instructions: str = (
                "\nEVDS baglantisi icin gereken API anahtarini almak icin lutfen "
                "asagidaki yonergeleri izleyin:\n\n1. EVDS web sitesini acin. (otomatik "
                "olarak acilacaktir)\n2. Acilan sayfada 'KAYIT OLUN' butonuna tiklayin. "
                "\n3. Formda istenen bilgileri girip EVDS'ye kayit olun.\n4. Girdiginiz e-mail "
                "adresine ait olan gelen kutusunu kontrol edin ve gelen e-mail üzerinden e-mail "
                "adresinizi dogrulayin.\n5. Ayni sayfayi acin ve hesabiniza giris yapin.\n"
                "6. Kullanici adiniza tiklayin ve acilir menuden 'Profil' sekmesine tiklayin.\n"
                "7. Acilan menude 'API Anahtari' butonuna tiklayarak baglanti icin gereken API "
                "anahtarinizi gorebilirsiniz."
            )
        elif language.lower() in ("eng", "en", "english"):
            instructions = (
                "\nPlease follow below instructions to obtain the required API key to "
                "connect EDDS:\n1. Open EVDS website. (it will be opened automatically) "
                "\n2. You can change the website language by clicking 'EN' on the upper right bar "
                "\n3. Click 'SIGN UP' button on current page.\n4. Fill up the form with requested "
                "information and register.\n5. Check for incoming mails from the inbox that "
                "belongs to e-mail address you used for\n   EDDS membership, and verify your "
                "e-mail address via the received e-mail.\n6. Open the same page and log into your "
                "ccount.\n7. Click on your username and then click 'Profile' on opened sliding "
                "menu.\n8. You can get your API key by clicking 'API Key' on newly opened page "
            )
        else:
            raise ValueError("Language must be either TR or ENG")

        print(instructions)
        webbrowser.open(EVDSTSConfig.url_sign_up, new=2)

    def __init__(
                 self,
                 key: Optional[str] = None,
                 language: str = "TR",
                 show_links: bool = False,
                 proxy_servers: Optional[Dict[str, str]] = None,
                 verify_certificates: bool = True,
                 secure: bool = True,
                 jupyter_mode: bool = False,
                 precision: Optional[int] = None
    ) -> None:

        """EVDS (EDDS) API Service Connection Interface.

        Args:
            - `key` (str): API key supplied by EVDS (EDDS) service.
            - `language` (str, optional): Interface language (if available). Defaults to `TR`.
            Current supported languages are:
                - Turkce: `TUR`, `tur`, `TR`, `tr`
                - English: `ENG`, `eng`, `EN`, `en`
            - `show_links` (bool, optional): Shows which urls are connected. Defaults to `False`
            - `proxy_servers` (Optional[Dict[str, str]], optional): Proxies for accesing the EVDS
            over them. Defaults to `None`.
            - `verify_certificates` (bool, optional): Enabling/Disabling of SSL security certificate
            checking during connection.
                - `True`: Check SSL sertificate is valid.
                - `False`: No security check (use the option if you encounter connection problems
                despite the API service is actually on-line)
            Defaults to `True`.
            - `jupyter_mode` (bool, optional): Enable/Disable Jupyter Notebook mode for better
            representation on-screen. Defaults to `False`.
                - `True`:
                    - floating-point precision: 2 (note this just affects the precision of screen
                representation. The real operational precision is either comes from the EVDS or
                is eqaul to given precision if a fixed precision is given by 'precision' parameter.
                    - Maximum pandas DataFrame columns to be showed: `6`
                - False: No screen representation optimizations.
            - `precision` (Optional[int], optional): The operational precision of floating-point
            numbers.
                - integer value: floating-point precisions are set to given value. for instance:
                `1907.72231162012281817` is truncated to `1907.72` if the given precision is `2`,
                or, `72.1907` is truncated to `72` if the given precision is `0`
                - None: precision is equal to original precision returned from the EVDS.
                Defaults to `None`
        """

        self.cfg: EVDSTSConfig = EVDSTSConfig()
        self.api_key: str = key if key else self._load_key()
        self.show_links: bool = show_links
        self.jupyter_mode: bool = jupyter_mode
        self.precision: Union[None, int] = precision
        self.main_categories: pd.DataFrame = pd.DataFrame()
        self.session: requests.Session = self._create_session(secure=secure)
        self.data: pd.DataFrame = pd.DataFrame()
        self.first_request: bool = True
        self.internal_references_file_call = True
        self.references_file = self.cfg.reference_file

        self.name_cache: Dict[str, str] = self._load_references()
        self.proxy_servers: Dict[str, str] = proxy_servers
        self.verify_certificates: bool = verify_certificates
        self.secure: bool = secure

        self.search_engine: SearchEngine = SearchEngine(language=language)
        self.language: str = language

    @property
    def api_key(self) -> str:

        """Returns API Key"""

        return self._api_key

    @api_key.setter
    def api_key(self, key: str) -> None:
        """Sets API Key"""

        self._api_key = key

    @property
    def language(self) -> str:

        """Returns language code"""

        return self._language

    @language.setter
    def language(self, code: str) -> None:

        """Sets interface language and language related attributes"""

        self._language = self.cfg.defined_languages.get(code.strip(), None)
        if not self._language:
            raise ValueError(f"{code} is not a defined language")
        # change language dependent features.
        self._language_changed(self._language)

    @property
    def proxy_servers(self) -> Dict[str, str]:

        """Returns proxy servers"""

        return self._proxy_servers

    @proxy_servers.setter
    def proxy_servers(self, servers: Dict[str, str]) -> None:

        """Sets proxy servers"""

        if servers is None:
            self.session.proxies = {}
            self._proxy_servers = {}
            return

        if not isinstance(servers, dict):
            raise TypeError('Proxies must be given as a dict like {http: 127.0.0.1}')

        self._proxy_servers = servers
        self.session.proxies = servers

    @property
    def verify_certificates(self) -> bool:

        """Returns certificate verification status"""

        return self._verify_certificates

    @verify_certificates.setter
    def verify_certificates(self, flag: bool) -> None:

        """Sets certificate verification True/False"""

        if flag is True:
            self._verify_certificates = True
            self.session.verify = True
        else:
            self._verify_certificates = False
            self.session.verify = False

    @property
    def jupyter_mode(self) -> bool:
        """ Returns the Jupyter Notebook Mode state"""
        return self._jupyter_mode

    @jupyter_mode.setter
    def jupyter_mode(self, switch: bool):

        """Enables/Disables Jupyter Notebook Represenatation Mode. This mode only affects the
        screen representation of data.

        Args:
            - switch (bool): Can be set True/False
                - True: Max columns to be shown in screen: 5, float precision: 2
                - False: Pandas Defaults
        """

        if switch:
            #* Better screen representation for Jupyter Notebook users.
            pd_options: Dict[str, Any] = {
                                        'display.max_columns': 6,
                                        'display.float_format': '{:.2f}'.format,
            }

            for k, v in pd_options.items():
                pd.set_option(k, v)

            self._jupyter_mode = True
        else:
            #* Normal mode
            pd.reset_option('display.float_format')
            pd.reset_option('display.max_columns')

            self._jupyter_mode = False

    @property
    def precision(self) -> Union[None, int]:

        """Returns the precision of floating-point numbers"""

        return self._precision

    @precision.setter
    def precision(self, val: Union[None, int]) -> None:

        """Sets the precision of floating-point numbers"""

        if val is None:
            self._precision = None
            return
        if not isinstance(val, int):
            raise TypeError(
                "Precision can be either an integer number or None (for EVDS default)"
            )

        self._precision = val

    @property
    def references_file(self) -> str:

        """Returns reference file location"""

        return self._references_file

    @references_file.setter
    def references_file(self, fname: str) -> None:

        if self.internal_references_file_call:
            self._references_file = fname
            self.internal_references_file_call = False
            return

        check: bool = Path(fname).is_file()
        if not check:
            raise ValueError(f"{fname} is not found on disk!")
        with open(fname, "r", encoding="utf-8") as f:
            try:
                check = json.load(f)
            except Exception:
                raise TypeError(
                    f"Given file ({fname}) is not a valid name reference file"
                ) from None

        self._references_file = fname

    def _create_session(self, secure: bool) -> requests.Session:

        """_summary_

        Args:
            secure (bool): _description_

        Returns:
            requests.Session: _description_
        """

        session: requests.Session = requests.Session()
        if secure:
            session.adapters.pop("https://", None)
            context: ssl.SSLContext = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.options |= 0x4
            session.mount('https://', EVDSHttpAdapter(context))

        return session

    def _language_changed(self, language: str) -> None:

        """Variables that must be reloaded when the language is changed.

        Args:
            - language (str): selected language
        """

        # reload when the language is changed
        self.main_categories = self._get_main_categories()
        self.search_engine.language = language

    def _load_references(self) -> Dict[str, str]:

        """Load name references into memory from the references file.

        Returns:
            - Dict[str, str]: name references
        """

        corrupted_file: bool = False

        if not Path.is_file(Path(self.references_file)):
            return {}

        with open(self.references_file, "r", encoding="utf-8") as f:
            try:
                references: Dict[str, str] = json.load(f)
            except JSONDecodeError:
                print('JSON file that keeps the references can not be decoded and is removed!')
                corrupted_file = True

        if corrupted_file:
            delete_file(self.references_file)
            return {}

        return references

    def _load_key(self) -> None:

        """Load name references into memory from the references file.

        Returns:
            - Dict[str, str]: name references
        """

        corrupted_file: bool = False

        if not Path.is_file(Path(self.cfg.key_file)):
            raise ValueError(
                f"\nYou need to provide a key either with 'key=YOUR_API_KEY' or have a file on\n "
                f"{self.cfg.key_file} that holds the key that you saved before.\nYou can save your "
                "API key using 'save_key()' method in order not to provide a key every time\nwhen "
                "you create an instance of EVDSConnector."
            )

        with open(self.cfg.key_file, "r", encoding="utf-8") as f:
            try:
                key: str = json.load(f)['key']
            except JSONDecodeError:
                print('JSON file that keeps the API KEY can not be decoded and is removed!')
                corrupted_file = True

        if corrupted_file:
            delete_file(self.cfg.key_file)
            raise ValueError(
                f"The file {self.cfg.key_file} was corrupted and deleted!\n You can save your key "
                "using 'save_key() method now if you would like to."
            )

        return key

    def _clear_referencs_in_memory(self) -> None:

        """Clears references in memory"""

        self.name_cache = {}

    def _get_main_categories(self) -> pd.DataFrame:

        """Returns main categories of EVDS Service Database.

        Returns:
           - DataFrame: Main categories of EVDS database.
        """

        extensions: Dict[str, str] = dict(key=self.api_key, type='json')
        response: bytes = self._get_response(
            self.cfg.url_main_categories,
            extensions=extensions,
            type_="main_categories"
            )

        id_field: str = self.cfg.category_id
        title_field: str = self.cfg.topic_title + "_" + self.language
        nas: List[str] = self.cfg.not_available_categories
        index_name: str = "Index"

        main_categories_json: JSONType = load_json(response)
        required_columns: List[str] = [id_field, title_field]
        main_categories: pd.DataFrame = pd.DataFrame(main_categories_json)[required_columns]
        main_categories = as_real(main_categories, "int16", id_field)
        main_categories.index.name = index_name
        available_main_categories: pd.DataFrame = main_categories[
            ~main_categories[id_field].isin(nas)
        ]
        return available_main_categories

    def _find_sub_category(
                           self,
                           main_category: Union[int, str] = None
    ) -> Dict[str, Union[str, int]]:

        """Returns sub category parameters for given main category.

        Args:
           - main_category (Union[int, str]]): Main category name or Main Category ID.

        Raises:
           - SubCategoryNotFoundException: When the category is not found.
           - ValueError: When an unappropriate category identifier is given.

        Returns:
           - Dict[str, Union[str, int]]: Parameter extensions for request.
        """

        extensions: Dict[str, Union[str, int]] = {}
        title: str = self.cfg.topic_title + "_" + self.language
        id_: str = self.cfg.category_id

        if str(main_category).isnumeric():
            main_category = int(main_category)

        if isinstance(main_category, int):
            available_ids: List[int] = list(self.main_categories[id_])
            if main_category in available_ids:
                extensions = dict(key=self.api_key, mode=2, code=main_category, type='json')
        elif isinstance(main_category, str):
            try:
                code: int = self.main_categories[
                    self.main_categories[title].str.contains(main_category)
                ][id_].iat[0]
            except Exception:
                raise SubCategoryNotFoundException(
                    f"Given main category name ({main_category}) is not found in EVDS "
                    f"Main Categories."
                ) from None

            extensions = dict(key=self.api_key, mode=2, code=code, type='json')

        else:
            raise ValueError(
                "Main category must be an integer representing the main category code "
                "or a string which is an actual main category name."
            )

        if not extensions:
            raise SubCategoryNotFoundException(
                f"Given main category ID {main_category} is not found on EVDS Main Categories."
            )

        return extensions

    def _create_trans_agg_param(
                                self,
                                functions: List[Union[str, int]],
                                series_count: int,
                                type_: str,
                                delimiter: str = "-",
    ) -> str:

        """Returns request parameters for transformation and aggregation functions.

        Args:
            - functions List[Union[str, int]]: Transformation or Aggregation Functions given.
                - None or not given: No any transformation/aggregation function is applied to
                requested data.
                - List or Tuple: Individual transformation/aggregation functions for every series
                requested.
                - String or int: The same transformation/aggregation function for all given series.
            - series_count (int): Lenght of the given series.
            - type_ (str): Type of the function(s) to be definition checked:
                - "transformation" for Transformation Functions.
                - "aggregation" for Aggregation Functions.
            - delimiter (str): Delimiter char that will be used for joining the elements.
            Defaults to "-"

        Returns:
            - str: Transformation/Aggregation function parameters for API request.
        """

        functions_param: str = ''

        if not all(functions):
            # Default transformation/aggregation function (None)
            return ''

        if series_count != len(functions):
            if len(functions) != 1:
                raise UnmatchingParameterSizeException(
                    f'{type_.title()} functions count (given: {len(functions)}) must be equal '
                    f'to series count (given: {series_count}) if {type_.title()} functions '
                    f'are given individualy for each series.'
                )
            else:
                # The same transformation/aggregation function for all series
                functions_param = join_sequentials(
                    [str(function) for function in functions for i in range(series_count)],
                    delimiter=delimiter
                )
        else:
            functions_param = join_sequentials(
                [str(function) for function in functions],
                delimiter=delimiter
            )

        return functions_param

    def _find_real_trans_agg_functions(
                                       self,
                                       given_functions: List[Union[str, int]],
                                       type_: str
    ) -> List[str]:

        """Checks the definition status of given transformation or aggregation function(s) and
        returns related values corresponding to them.

        Args:
            - given_functions List[Union[str, int]]:
            Given transformation or aggregation function(s).
            - type_ (str): Type of the function(s) to be definition checked:
                - "transformation" for Transformation Functions.
                - "aggregation" for Aggregation Functions.

        Raises:
            - ValueError: If given type_ parameter is undefined.
            - UndefinedTransformationFunctionException: Given string or int transformation function
            is not defined.
            - UndefinedAggregationFunctionException: Given string or int aggregation function
            is not defined.
            - UndefinedTransformationFunctionException: Given list or tuple transformation functions
            are not defined.
            - UndefinedAggregationFunctionException: Given list or tuple aggregation functions
            are not defined.

        Returns:
            List[str]: API's function definition key(s) for given functions.
        """

        functions: Union[str, List[str]] = []

        if not all(given_functions):
            return ['']

        if type_ == "transformation":
            # ensure all types are str
            defined_functions = self.cfg.transformations_map
        elif type_ == "aggregation":
            defined_functions = self.cfg.aggregations_map
        else:
            raise ValueError('type_ parameter must be either "transformation" or "aggregation"')

        if isinstance(given_functions, Sequence):
            str_functions: List[str] = [str(val) for val in given_functions]
            for function in str_functions:
                for t in defined_functions:
                    if function in t:
                        functions.append(defined_functions[t])
            if len(functions) != len(given_functions):
                if type_ == "transformation":
                    self.show_transformation_references()
                    raise UndefinedTransformationFunctionException(
                        f'One (or more) of the transformation function(s) in {given_functions} is '
                        f'undefined. Plese check above transformation functions map.'
                    )
                elif type_ == "aggregation":
                    self.show_aggregation_references()
                    raise UndefinedAggregationFunctionException(
                        f'One (or more) of the aggregation function(s) in {given_functions} is '
                        f'undefined. Plese check above aggregation functions map.'
                    )

        return functions

    def _find_real_frequency(self, given_frequency: Union[None, str, int]) -> str:

        """Returns a series frequency that is currently identified on EVDS API server.

        Args:
            - given_frequency (Union[None, str, int]): Can be in various types.
                - None: The default frequency is returned.
                - String: The matching frequency is returned.
                    - ""  if not anything given or given string is "default" or "0"
                    - "1" if given string is "daily" or "1"
                    - "2" if given string is "workday" or "2"
                    - "3" if given string is "weekly" or "3"
                    - "4" if given string is "semimonthly" or "4"
                    - "5" if given string is "monthly" or "5"
                    - "6" if given string is "quarterly" or "6"
                    - "7" if given string is "semiyearly" or "7"
                    - "8" if given string is "yearly" or "8"
                - Integer: Same as above string mapping.

        Raises:
            - UndefinedFrequencyException: If the frequency of data could not be determined using
            given string or integer.

        Returns:
            str: Data frequency
        """
        frequency: str = None

        if given_frequency is None or given_frequency == "":
            return ""

        if isinstance(given_frequency, (str, int)):
            search: str = str(given_frequency)
            for t in self.cfg.frequency_map:
                if search in t:
                    frequency = self.cfg.frequency_map[t]

        if frequency is None:
            self.show_frequency_references()
            raise UndefinedFrequencyException(
                f"Given frequency ({given_frequency}) is not defined. Please check above "
                f"frequency map."
            )

        return frequency

    def _parse_series_names(
                            self,
                            series: Union[str, Sequence[str]],
                            check_references: bool = True
    ) -> Tuple[List[str], List[str]]:

        """Checks given series names and returns a list of series if it could be done.

        Args:
            - series (Sequence[str]): Any Sequence type consisting of strings.
            - check_references(bool, optional): checks if the given series are defined in name
            references (if they're reference names) and returns original series names if reference
            names are detected.

        Raises:
            - TypeError: If given container can not be converted into a list.

        Returns:
            Tuple[List[str], List[str]]: A tuple consisting of
            (real_series_names, given_series_names)
        """

        real_series: List[str] = []
        if isinstance(series, str):
            names: str = series.strip().split(",")
            if len(names) == 1:
                names = series.strip().split(" ")
                if len(names) == 1:
                    names = [series]
            real_series = [name.strip() for name in names]
        elif isinstance(series, Sequence):
            real_series = list(series)
        else:
            raise TypeError(
                "series names must be given either comma or space separated string like;\n"
                "'usdtry, cppi' or\n'usdtry cppi\nor in a Sequence type container "
                "like list or tuple"
            )

        # store given names as old names for further use like managing references deleting.
        given_names: List[str] = real_series

        # check references
        if check_references:
            real_series = [
                name if name not in self.name_cache else self.name_cache[name]
                    for name in real_series
            ]

        return real_series, given_names

    def _parse_trans_agg_names(
                               self,
                               functions: Union[str, None, Sequence[str]],
    ) -> List[str]:
        """Returns parsed transformation or aggregation functions names from given ones.

        Args:
            - functions (Union[str, None, Sequence[str]]):
            given transformation/aggregation functions

        Raises:
            - TypeError: If an unsupported type of names is given.

        Returns:
            - List[str]: List of parsed aggregation or transformation functions.
        """

        if functions is None:
            return ['']

        real_functions: List[str] = []
        if isinstance(functions, str):
            names: str = functions.strip().split(",")
            if len(names) == 1:
                names = functions.strip().split(" ")
                if len(names) == 1:
                    names = [functions]
            real_functions = [name.strip() for name in names]
        elif isinstance(functions, int):
            real_functions = [functions]
        elif isinstance(functions, Sequence):
            real_functions = list(functions)
        else:
            raise TypeError(
                "function names must be given either comma or space separated string like;\n"
                "'percent, diff' or\n'percent diff'\nor in a Sequence type container "
                "like List or Tuple"
            )

        return real_functions

    def _insert_originals(
                       self,
                       series: List[str],
                       functions: List[str]
    ) -> Tuple[List[str], List[str]]:

        """Returns Transformation/Aggregation parameters adding original series to them
        if it's not included.

        Raises:
            - UnmatchingParameterSizeException: If given transformation/aggregation
            function size doesn't match with series size.

        Returns:
            _type_: Parameters including original series.
        """
        # series has been already checked and assured that it's a Sequence type except string.
        # functions can be both transformation and aggregation functions types.

        extended_functions: List[str] = []
        extended_series: List[str] = []

        if not all(functions):
            return extended_series, extended_functions

        if len(functions) != 1 and len(functions) != len(series):
            raise UnmatchingParameterSizeException(
                f'Transformation/Aggregations functions count (given: {len(functions)}) '
                f'must be equal to series count (given: {len(series)}) if transformation '
                f'or aggregation functions are given individualy.'
            )

        # orginal api parameters comes here so, need to check just "0"
        functions = [function for function in functions if function != "0"]
        # check if all is given as 'level'
        if not functions:
            functions = ["0" for i in range(len(series))]
            return series, functions

        if len(functions) == len(series):
            # individual transformations for given series
            extended_functions = ["0" for i in range(len(series))] + functions
            extended_series = series * 2
        else:
            # same transformation for all given series.
            extended_series = series * 2
            extended_functions = [
                "0" if i < len(series) else function
                    for function in functions
                        for i in range(len(extended_series))
            ]

        if not (extended_series and extended_functions):
            raise UnmatchingParameterSizeException(
                f'Transformation/Aggregations functions count (given: {len(functions)}) '
                f'must be equal to series count (given: {len(series)}) if transformation '
                f'or aggregation functions are given individualy.'
            )

        return extended_series, extended_functions

    def _get_response(self, url: str, extensions: Dict[str, str], type_: str) -> bytes:

        """Makes a GET request towards the API server and returns the response given.

        Args:
            - url (str): Base API URL to be connected.
            - extensions (Dict[str, str]): url extensions which specifies the requested data and
            its frequency/transformations/aggregations/etc.

        Raises:
            - WrongAPIKeyException: for APIKEY related issues.
            - APIServiceConnectionException: for Connection Timeouts.
            - APIServiceConnectionException: for Network (Internet) related issues.
            - APIServiceConnectionException: for Unknown issues.

        Returns:
            - bytes: The response gotten from the API Server.
        """

        url_extensions: str = self._generate_url_extensions(extensions)
        api_url: str = url + url_extensions

        if self.show_links:
            print(f"request: {api_url}")

        try:
            request: requests.Response = self.session.get(api_url,
                                                          timeout=(5, 5),
                                                          headers={"key":self.api_key}
            )
        except Timeout as ex:
            print("url: ", api_url)
            raise APIServiceConnectionException(
                "A connection timeout has occured. Please check your network status and "
                "be sure the EVDS website is currently on-line"
            ) from ex
        except RequestException as ex:
            print("url: ", api_url)
            raise APIServiceConnectionException(
                "An unknown connection error has occured while your request is processed. "
                "Please check your network status and be sure the EVDS website is currently on-line"
            ) from ex
        except HTTPError as ex:
            print("url: ", api_url)
            raise APIServiceConnectionException(
                "A network error is occured while your request is processed."
            ) from ex

        if request.status_code == 404:
            raise APIServiceConnectionException(
                "EVDS API Server is currently down. Please retry later."
            )

        if not request.status_code == 200:
            print(f'request: {api_url}\nreturn:{request.status_code}\n')

            if self.first_request:
                if request.status_code == 500:
                    raise WrongAPIKeyException(
                        f"Given api key {self.api_key} is wrong!\n"
                        f"Please check your key and try connection again."
                    )
            else:
                if type_ == "series":
                    raise SeriesNotFoundException(
                        "The series you requested is not found on EVDS!\n"
                        "Are you sure you provided the original or correct reference series names?"
                    )
                elif type_ == "groups":
                    raise GroupNotFoundException(
                        "The group you requested is not found on EVDS!\n"
                        "Are you sure you provided a correct group name?"
                    )
                elif type_ == "sub_categories":
                    raise GroupNotFoundException(
                        "The sub-category you requested is not found on EVDS!\n"
                        "Are you sure you provided a correct sub-category name?"
                    )
            raise APIServiceConnectionException(
                f"\nEVDS API server didn't respond OK for the request above.\n"
                f"The response given by the server is: {request.status_code}\n"
                f"Please make sure you requested correct original EVDS API series names "
                f"or correct reference names you saved before."
            )
        self.first_request = False

        return request.content

    def _generate_url_extensions(self, param_dict: Dict[str, str]) -> str:

        """Returns extension text for the base API url.

        Args:
            - param (Dict[str, str]): Parameters dictionary.

        Returns:
            - str: string parameters that will be added to base API url as extension.
        """

        url_extensions: str = ''.join(
            [str(k) + '=' + str(v) + "&" if idx < len(param_dict) - 1 else str(k) + '=' + str(v)
                    for idx, (k, v) in enumerate(param_dict.items())]
        )

        return url_extensions

    def _auto_save_name_references(
                                   self,
                                   old_names: Sequence[str],
                                   new_names: Sequence[str],
                                   original_names: Sequence[str]
    ) -> None:

        """Saves given reference names as mappings for real series names"""

        # API replaces "." with "_" in its JSON response therefore must be reversed back.
        original_names: List[str] = [str(name).replace("_", ".") for name in original_names]
        # given names maybe already a reference_name so it must also be checked
        # in order to remove them from the cache
        old_names = list(old_names)
        # new names given
        new_names = list(new_names)

        self.save_name_references(
                                  series_names=original_names,
                                  reference_names=new_names,
                                  old_reference_names=old_names,
                                  check_names=False
        )

    def _auto_rename_columns(
                             self,
                             df: pd.DataFrame,
                             names: List[str],
                             transformations: str = '',
                             aggregations: str = '',
                             functions_separator: str = "-"
    ) -> pd.DataFrame:

        """Assigns reference names to columns if there are set before

        Args:
            - df (pd.DataFrame): created DataFrame with series in.
            - names (List[str]): real series name from EVDS API.
            - transformations (str, optional): Applied Transformations. Defaults to ''.
            - aggregations (str, optional): Applied Aggregations. Defaults to ''.
            - functions_separator (str, optional): Pararmeters separator. Defaults to "-".

        Returns:
            - pd.DataFrame: DataFrame column names changed with assigned reference names.
        """

        auto_names: List[str] = []

        # need a reverse lookup
        reversed_references: Dict[str, str] = {v: k for k, v in self.name_cache.items()}
        # if real series names have been referenced before?
        ref_names: List[str] = [
            name if name not in reversed_references else reversed_references[name]
            for name in names
        ]

        if transformations or aggregations:

            if transformations:
                ftype = transformations.split(functions_separator)
                reversed_funcs = {v: k for k, v in self.cfg.transformations_map.items()}
                ftype = [reversed_funcs[key][0] for key in ftype]

            if aggregations:
                ftype = aggregations.split(functions_separator)
                reversed_funcs = {v: k for k, v in self.cfg.aggregations_map.items()}
                ftype = [reversed_funcs[key][0] for key in ftype]

            auto_names = [
                name.upper() + "_" + func.upper() if func != "level" else name.upper()
                for name, func in zip(ref_names, ftype)
            ]

            # just a precaution because they should be equal.
            if len(df.columns) == len(auto_names):
                df.columns = auto_names

        else:

            if len(df.columns) == len(ref_names):
                auto_names = [name.upper() for name in ref_names]
                df.columns = auto_names

        return df

    def _show_references(
                         self,
                         references,
                         reference_type: Optional[str] = "series"
    ) -> None:

        """Screen representation of series, transformation, and aggregation functions'
        reference names stored on disk."""

        if not references:
            print("No reference names has been stored yet...")
            return

        if reference_type == "series":
            sorted_keys: List[str] = sorted(references, key=lambda key: key[0])
            references: Dict[str, str] = {k: references[k] for k in sorted_keys}

            print(
                "\nBelow references map have been created for further use. You can use reference "
                "series names instead of original ones when retrieving data from the EVDS API "
                "service. Reference names are permanent unless this reference mapping is "
                "deleted or changed.\n"
            )

        print("{:^60}".format("References Table"))
        print("-" * 60)
        print(f"Reference Name Represents -> Original {reference_type.title()} Names on EVDS")
        print("-" * 60)

        for reference_name, original_name in references.items():
            if reference_type == "series":
                print(
                    "{:15}".format(reference_name),
                    "--->",
                    original_name,
                )
            else:
                representation: str = ' or '.join(
                    (reference for reference in reference_name if isinstance(reference, str))
                )
                print(
                    "{:23}".format(representation),
                    "--->",
                    original_name,
                )
        print("-" * 60)
        print("\n")

    def _get_series(
                    self,
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
                    convert_to_bd: bool = True
    ) -> pd.DataFrame:

        """A dummy function for get_series"""

        if transformations and aggregations:
            raise AmbiguousFunctionMappingException(
                "Using transformation and aggregation function mappings at the same time is an "
                "ambiguous process that can change the result by applying order. Please use them "
                "applying one at a time."
            )

        series, old_names = self._parse_series_names(series)
        if new_names:
            new_names, _ = self._parse_series_names(new_names, check_references=False)

        transformations = self._parse_trans_agg_names(transformations)
        aggregations = self._parse_trans_agg_names(aggregations)

        transformations: Union[str, List[str]] = (
            self._find_real_trans_agg_functions(transformations, type_='transformation')
        )
        aggregations: Union[str, List[str]] = (
            self._find_real_trans_agg_functions(aggregations, type_='aggregation')
        )
        frequency = self._find_real_frequency(frequency)

        if keep_originals and all(transformations):
            series, transformations = self._insert_originals(series, transformations)

        str_series: str = join_sequentials(series)

        if period and (start_date or end_date):
            raise AmbiguousFunctionParameterException(
                "start_date and/or end_date and period parameters can not be provided at the same "
                "time.\nPlease use either start_date and end_date parameters or just period "
                "parameter."
            )

        if period:
            start_date, end_date = get_period(period)

        start_date = correct_date(start_date)
        end_date = correct_date(end_date)

        start_date = convert_to_business_date(start_date) if convert_to_bd else start_date
        end_date = convert_to_business_date(end_date) if convert_to_bd else end_date

        series_count: int = len(series)
        aggregations_param: str = self._create_trans_agg_param(
            functions=aggregations, series_count=series_count, type_="aggregation"
        )
        transformations_param: str = self._create_trans_agg_param(
            functions=transformations, series_count=series_count, type_="transformation"
        )

        params: Dict[str, str] = dict(
            key=self.api_key, series=str_series, startDate=start_date, endDate=end_date,
            type='json', formulas=transformations_param, aggregationTypes=aggregations_param,
            frequency=frequency
        )

        data: bytes = self._get_response(url=self.cfg.url_series, extensions=params, type_="series")
        json_data: JSONType = load_json(data, field=self.cfg.raw_items)

        # Convert to DataFrame
        df: pd.DataFrame = pd.DataFrame(json_data)
        # Clear unnecessary fields
        df = drop_columns(df, [self.cfg.unixtime, self.cfg.yearweek])
        # Ensure all numerical fields are represented as float32 type in DataFrame
        df = as_real(df, 'float32')
        # Convert to time series
        if time_series:
            df = convert_to_time_series(df)
        else:
            df.rename(columns={'Tarih': 'Date'}, errors='ignore', inplace=True)
        # Drop columns consisting of all NAs
        df = drop_na_columns(df)
        # Sort values
        df.sort_index(ascending=ascending, inplace=True)
        # add to references (must always be done before renaming columns with reference names)
        if (new_names and keep_references) and not (all(transformations) or all(aggregations)):
            # series names can be misleading if any transformation or aggregation is applied to
            # original series.
            #if not (transformations and aggregations):
            self._auto_save_name_references(
                                            old_names=old_names,
                                            new_names=new_names,
                                            original_names=df.columns
            )
        # Change column names if supplied
        if new_names and time_series:
            double_size: bool = False
            if all(aggregations) and keep_originals:
                # adding originals to aggregations is a two step process and cause giving
                # wrong type of size information when the size of given series names and actual
                # columns size of the DataFrame is different. double_size acts as just an
                # information correction flag.
                double_size = True

            df = set_column_names(df, new_names, double_size=double_size)
        else:
            # auto rename columns if there are reference names assigned before
            self._auto_rename_columns(df, series, transformations_param, aggregations_param)

        self.data = df

        return df

    def save_key(self, key: Optional[str] = None) -> None:

        """Saves provided key to disk that is loaded automatically while instantiation if any other
        key is not supplied explicitly.

        Args:
            key (str): Your EVDS API Key
        """
        if not key:
            if self.api_key:
                key = self.api_key
            else:
                raise ValueError("You need to supply an EVDS Key to save")
        else:
            self.api_key = key

        write_json(self.cfg.key_file, dict(key=key))

        print(f"{key} has been saved to -> {self.cfg.key_file}")

    def show_transformation_references(self) -> None:

        """Shows current transformation functions map that is used by EVDS API
        to determine the frequency of a series.
        """
        self._show_references(
                              references=self.cfg.transformations_map,
                              reference_type="transformation function"
        )

    def show_aggregation_references(self) -> None:

        """Shows current aggregation functions map that is used by EVDS API
        to determine the frequency of a series.
        """
        self._show_references(
                              references=self.cfg.aggregations_map,
                              reference_type="aggregation function"
        )

    def show_frequency_references(self) -> None:

        """Shows current frequency reference mapping."""

        self._show_references(
                              references=self.cfg.frequency_map,
                              reference_type="frequency"
        )

    def show_name_references(self) -> None:

        """Shows current series names reference mapping."""

        self._show_references(
                              references=self.name_cache,
                              reference_type="series"
        )

    def get_main_categories(
                            self,
                            as_dict: bool = False,
                            raw: bool = False,
    ) -> Union[pd.DataFrame, JSONType, Dict]:

        """Returns main data categories defined on EVDS in different formats

        Args:
            - as_dict (bool, optional): Returns main categories as a dictionary
            - forming{CATEGORY_ID: category_name}. Defaults to False.
            - raw (bool, optional): returns untouched JSON object retrieved from EVDS Service
            - instead of processed types. Defaults to False

        Raises:
            - AmbiguousOutputTypeException: If both as_dict and as_raw is given True

        Returns:
            - Union[pd.DataFrame, JSONType, Dict]: EVDS Service Main Categories.
        """

        if as_dict and raw:
            raise AmbiguousOutputTypeException(
                "Output type is ambiguous. Please select either 'raw' or 'dict' type."
            )

        if not (as_dict or raw):
            return self.main_categories

        original_dict: Dict[Dict[int, int], Dict[int, str]] = self.main_categories.to_dict()
        category_id: str = self.cfg.category_id
        title: str = self.cfg.topic_title + "_" + self.language
        main_dict: Dict[int, str] = {
            original_dict[category_id][i]: original_dict[title][i]
                for i in range(len(original_dict[category_id]))
        }

        if raw:
            return json.dumps(main_dict, allow_nan=True, ensure_ascii=False)

        return main_dict

    def get_sub_categories(
                           self,
                           main_category: Union[int, str],
                           as_dict: bool = False,
                           raw: bool = False,
                           verbose: bool = False,
    ) -> Union[pd.DataFrame, JSONType, Dict]:

        """Returns sub-categories of main categories as DataFrame (or other types supported).

        Args:
            - main_category (Union[int, str]]): Could be a main category ID
            or an actual main category name.
                - integer: returns sub-categories which given value corresponds to main category ID.
                - string: returns sub-categories which belongs to given main category name.
            - as_dict (bool, optional): Returns a dictionary forming
            {datagroup_code: datagroup_name} Defaults to False
            - raw (bool, optional): returns untouched JSON object retrieved from EVDS Service
            instead of processed types. Defaults to False
            - verbose (bool, optional): a detailed version of retrieved data. Defaults to False.

        Raises:
            - AmbiguousOutputTypeException: If both as_dict and as_raw is given True
            - SubCategoryNotFoundException: If provided sub-category is not found on EVDS

        Returns:
           - Union[pd.DataFrame, JSONType, Dict]: Sub-Categories which given main categories include
           in.
        """

        if as_dict and raw:
            raise AmbiguousOutputTypeException(
                "Output type is ambiguous. Please select either 'raw' or 'dict' type."
            )

        params: Dict[str, Union[str, int]] = self._find_sub_category(main_category)
        sub_categories: bytes = self._get_response(
            url=self.cfg.url_sub_categories,
            extensions=params,
            type_="sub_categories"
        )
        json_sub_categories: JSONType = load_json(sub_categories)

        if not json_sub_categories:
            raise SubCategoryNotFoundException(
            "Requested sub-category is not found on EVDS!\n"
            "Are you sure you provided a correct sub-category name?"
        ) from None

        if raw:
            return json_sub_categories

        datagroup_code: str = self.cfg.datagroup_code
        datagroup_name: str = (
            self.cfg.datagroup_name if self.language == "TR"
                else self.cfg.datagroup_name + "_" + self.language
        )
        datagroup_frequency: str = self.cfg.frequency_str
        datagroup_id: str = self.cfg.category_id
        start_date: str = self.cfg.start_date
        end_date: str = self.cfg.end_date

        if as_dict:
            if not verbose:
                try:
                    # there are some groups that don't have meaning like 'bie_bosluk1' and they can
                    # cause a KeyError when the fields are tried to get.
                    sub_dict: Dict[str, str] = {
                        sub[datagroup_code]: [
                                            sub[datagroup_id], sub[datagroup_name],
                                            sub[datagroup_frequency], sub[start_date],
                                            sub[end_date]
                                            ]
                            for sub in json_sub_categories
                    }

                except KeyError:

                    if self.language == "TR":
                        return {
                            "TANIMSIZ": ["TANIMSIZ" for i in range(5)]
                        }
                    else:
                        return {
                            "UNDEFINED": ["UNDEFINED" for i in range(5)]
                        }
            else:
                sub_dict = {
                    sub[datagroup_code]: [sub[field] for field in sub if field != datagroup_code]
                        for sub in json_sub_categories
                }

            if self.language == "ENG":
                sub_dict = {k: list(map(lambda val: self.cfg.english_frequency_map[val]
                                if val in self.cfg.english_frequency_map else val, v))
                                    for k, v in sub_dict.items()}
            sub_dict = {
                k: list(map(lambda val: parse_dates(val, ignore_errors=True), v))
                    for k, v in sub_dict.items()
            }

            return sub_dict

        df: pd.DataFrame = pd.DataFrame(json_sub_categories)

        if self.language == "ENG":
            df[datagroup_frequency] = pd.Series(
                df.iloc[:, :][datagroup_frequency]
                    ).map(self.cfg.english_frequency_map)

        if verbose:
            return df

        columns: List[str] = [
            datagroup_code, datagroup_id, datagroup_name,
            datagroup_frequency, start_date, end_date
        ]

        df = df[columns].iloc[:, :]

        try:
            # in case of any conversion error the string dates better to be preserved.
            df[start_date] = pd.to_datetime(df[start_date].iloc[:], format='%d-%m-%Y')
            df[end_date] = pd.to_datetime(df[end_date].iloc[:], format='%d-%m-%Y')
        except Exception:
            pass

        return df

    def get_groups(
                   self,
                   data_group_code: str,
                   as_dict: bool = False,
                   raw: bool = False,
                   verbose: bool = False,
                   parse_dt: bool = False
    ) -> Union[pd.DataFrame, JSONType, Dict]:

        """Returns all series names, codes and observations start dates belong to given
        sub-categories as DataFrame (or other supported formats).

        Args:
            - data_group_code (str): Code of the sub-category the data requested for.
            - as_dict (bool, optional): Returns a dictionary forming {series_code: series_name}
            Defaults to False.
            - raw (bool, optional): returns untouched JSON object retrieved from EVDS Service
            instead of processed types. Defaults to False.
            - verbose (bool, optional): A very detailed version of the group data.
            Defaults to False.
            - parse_dt (bool, optional): Defaults to False:
                - True: datetime fields in returned dictionary are converted to Python date object.
                - False: datetime fields in returned dictionary are returned as is (string)

        Raises:
            - AmbiguousOutputTypeException: If both as_dict and as_raw is given True
            - GroupNotFoundException: if provided group is not found on EVDS

        Returns:
           - Union[pd.DataFrame, JSONType, Dict]: Series which given sub-category include in.
        """

        if as_dict and raw:
            raise AmbiguousOutputTypeException(
                "Output type is ambiguous. Please select either 'raw' or 'dict' type."
            )

        params: Dict[str, str] = dict(key=self.api_key, code=data_group_code, type='json')
        series: bytes = self._get_response(
            url=self.cfg.url_groups,
            extensions=params,
            type_="groups"
        )
        json_groups: JSONType = load_json(series)

        if not json_groups:
            raise GroupNotFoundException(
            "Requested group is not found on EVDS!\n"
            "Are you sure you provided a correct group name?"
        ) from None

        if raw:
            return json_groups

        series_name: str = (
            self.cfg.series_name if self.language == "TR"
                else self.cfg.series_name + "_" + self.language
        )
        series_code: str = self.cfg.series_code
        frequency: str = self.cfg.frequency_str
        start_date: str = self.cfg.start_date
        end_date: str = self.cfg.end_date

        if as_dict:
            if not verbose:
                try:
                    sub_dict: Dict[str, str] = {
                        sub[series_code]: [
                                        sub[series_name], sub[frequency],
                                        sub[start_date], sub[end_date]
                                        ]
                            for sub in json_groups
                                for i in range(len(json_groups))
                    }

                except KeyError:

                    if self.language == "TR":
                        return {
                            "TANIMSIZ": ["TANIMSIZ" for i in range(4)]
                        }
                    else:
                        return {
                            "UNDEFINED": ["UNDEFINED" for i in range(4)]
                        }
            else:

                sub_dict = {
                    sub[series_code]: [sub[field] for field in sub if field != series_code]
                        for sub in json_groups
                }

            if self.language == "ENG":
                sub_dict = {k: list(map(lambda val: self.cfg.english_frequency_map[val]
                                if val in self.cfg.english_frequency_map else val, v))
                                    for k, v in sub_dict.items()}
            if parse_dt:
                sub_dict = {
                    k: list(map(lambda val: parse_dates(val, ignore_errors=True), v))
                        for k, v in sub_dict.items()
                }

            return sub_dict

        df: pd.DataFrame = pd.DataFrame(json_groups)

        if self.language == "ENG":
            df[frequency] = df[frequency].iloc[:].map(self.cfg.english_frequency_map)

        try:
            # in case of any conversion error the string dates better to be preserved.
            df[start_date] = pd.to_datetime(df[start_date].iloc[:], format='%d-%m-%Y')
            df[end_date] = pd.to_datetime(df[end_date].iloc[:], format='%d-%m-%Y')
        except Exception:
            pass

        columns: List[str] = [series_name, series_code, frequency, start_date, end_date]

        if verbose:
            return df

        return df[columns]

    def get_series(
                    self,
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

        """Returns requested time series from the EVDS API Service.

        Args:
            - series (Sequence[str]): Time Series names that are requested from the EVDS API server.
                - names can be provided as original EVDS service assigned names or reference names
                that was saved as name references before.
                - names can be given in several ways:
                    - Comma separated string: "usdtry, eurtry"
                    - Space separated string: "usdtry eurtry"
                    - In a Sequence type container like a list or tuple: ["usdtry", eurtry]
                    or ("usdtry", "eurtry")
            - start_date (Optional[Union[str, datetime, pd.Timestamp]]): The date the time series
            data are started from.
                - None or not specified: Will be set to current date.
                - Could be given as a string in fromat 'dd-mm-YYYY', 'dd.mm.YYYY', 'dd/mm/YYYY'
                - Could be given as a Python datetime object.
                - Could be given as a Pandas TimeStamp object
            - end_date (Optional[Union[str, datetime]], optional): The last observation date
            for requested time series. Defaults to None
                - None or not specified: Will be set to current date.
                - Could be given as a string in fromat 'dd-mm-YYYY', 'dd.mm.YYYY', 'dd/mm/YYYY'
                - Could be given as a Python datetime object.
                - Could be given as a Pandas TimeStamp object
            - period (Optional[str]): A period string represents a period from current date.
            Defaults to None.
                - period strings consist of a num and a date identifier part. Num part can be any
                integer number and the date part is a letter reflecting day, week, month and year.
                The letters are the first letters of Turkish and English period identifiers.
                period can not be used together with start_date or end_date
                - 1d or 1g -> represent the period: from 1 day ago - today, examples: 2d, 7d, 30d
                - 1w or 1h -> represent the period: from 1 week ago - today, examples: 2w, 7w, 30w
                - 1m or 1a -> represent the period: from 1 month ago - today, examples: 2m, 7m, 12m
                - 1y -> represent the period: from 1 year ago - today, examples: 2y, 7y, 30y
            - aggregations (Optional[Union[str, List[str], Tuple[str]]], optional):
            Aggregation functions wich will be applied to time series before returning.
            Defaults to None.
                - None or not specified: No aggregation function is applied to time series.
                - Given as string: Same aggregation function is applied to all given time series.
                - Given as List or Tuple: Different aggregation functions are applied to
                the time series in given order.
            Available aggregation functions:
                - Mean: 'avg'
                - Minimum: 'min'
                - Maximum: 'max'
                - First: 'first'
                - Last: 'last'
                - Cumulative Sum: 'sum'
            - transformations (Optional[Union[str, List[str], Tuple[str]]], optional):
            Transformation functions that will be applied to time series before returning.
            Defaults to None.
                - None or not specified: No transformation is applied to time series.
                - Given as string: Same transformation is applied to all given time series.
                - Given as List or Tuple: Different transformations are applied to
                the time series in given order.
            Available transformation functions:
                - Level: 'level'
                - Percentage change: 'percent'
                - Difference: 'diff'
                - Yearly Percentage Change: 'ypercent'
                - Yearly Difference: 'ydiff'
                - Year to Date Percentage Change: 'ytdpercent'
                - Year to Date Difference: 'ytddiff'
                - Moving Average: 'mov'
                - Moving Total: 'movsum'
            - keep_originals (bool, optional): Sets the state of the original series when an
            aggregation or transformation function is applied to the series. Defaults to True.
                - True: Keep original series when a transformation function is applied to
                time series.
                - False: Drop original series when a transformation function is applied to
                time series.
            - frequency (Optional[Union[str, int]], optional): Frequence of requested time series.
            Defaults to None (as is). Available frequencies:
                - Daily: 'daily" or "D"
                - Business Daily: 'bdaily' or 'B'
                - Weekly: 'weekly' or 'W'
                - semimonthly: 'semimonthly' or 'SM'
                - Monthly: 'monthly' or 'M'
                - Quarterly: 'quarterly' or 'Q'
                - Semiyearly: 'semiyearly' or '6M'
                - Yearly: 'yearly' or 'Y'
            - new_names (Optional[Sequence[str]], optional): Changes created DataFrame column names
            with given ones. Defaults to None.
            - keep_references (bool, optional): Stores given new column names (if supplied) as
            references to real series names on EVDS API service. The reference names can not be
            stored if a transformation or aggregation function is applied to requested series.
            Defaults to False.
            - time_series (bool, optional): Tries to parse string dates into DateRanges
            corresponding to returned frequency of time series. That is especially useful
            (and mostly required) for time series analysis since string dates are converted to
            sortable, indexable, sliceable, differentiable real dates. Defaults to True
            - ascending (bool, optional): Sort direction of the index. Defaults to True:
                - True: Oldest data first.
                - False: Newest data first.
            - raw (bool, optional): Returns retrieved JSON data untouched. Defaults to False.
            - as_dict (bool, optional): Returns retrieved data as dictionary type. Defaults to False.
            - convert_to_bd (bool, optional): Checks start_date and end_date and returns the nearest
            business date if any of them encounters in weekend. Defaults to True.

        Raises:
            - AmbiguousOutputTypeException: If both as_dict and as_raw is given True

        Usage:
            - x.get_series(["TP.FE.OKTG01", "TP.DK.USD.A.YTL"], start_date=1-1-2022)

        Returns:
            - Union[pd.DataFrame, JSONType, Dict]: Time Series in requested format.
        """

        if as_dict and raw:
            raise AmbiguousOutputTypeException(
                "Output type is ambiguous. Please select either 'raw' or 'dict' type."
            )

        new_names_1: List[str] = []
        new_names_2: List[str] = []

        if aggregations and keep_originals and time_series and new_names:
            new_names, _ = self._parse_series_names(new_names, check_references=False)
            new_names_1 = [name for idx, name in enumerate(new_names) if idx >= len(new_names) / 2]

        result: pd.DataFrame = self._get_series(
            series=series,
            start_date=start_date,
            end_date=end_date,
            period=period,
            aggregations=aggregations,
            transformations=transformations,
            keep_originals=keep_originals,
            frequency=frequency,
            new_names=new_names_1 if new_names_1 else new_names,
            keep_references=keep_references,
            time_series=time_series,
            ascending=ascending,
            convert_to_bd=convert_to_bd
        )

        # any other operations needed.
        if aggregations and keep_originals and time_series and new_names:
            new_names, _ = self._parse_series_names(new_names, check_references=False)
            new_names_2 = [name for idx, name in enumerate(new_names) if idx < len(new_names) / 2]

        if aggregations and keep_originals and time_series:
            originals: pd.DataFrame = self._get_series(
                series=series,
                start_date=start_date,
                end_date=end_date,
                period=period,
                frequency=frequency,
                new_names=new_names_2 if new_names_2 else new_names,
                time_series=time_series,
                ascending=ascending,
                convert_to_bd=convert_to_bd
        )

            result = pd.concat([originals, result], axis=1)

        if self.precision is not None:
            result = _set_precision(result, self.precision)

        if raw:
            return result.to_json(orient="columns", date_format="iso")

        if as_dict:
            return result.to_dict(orient="dict")

        return result

    def save_name_references(
                             self,
                             series_names: Union[str, Sequence[str]],
                             reference_names: Union[str, Sequence[str]],
                             old_reference_names: Optional[List[str]] = None,
                             verbose: bool = True,
                             check_names: bool = True
    ) -> None:

        """Saves reference names for original series names in order them to be used as
        series names when getting data from the EVDS API server.

        Args:
            - series_names (Union[str, Sequence[str]]): Original series name(s) on EVDS API.
            or names that currently saved as references.
                - Can be given as a string for one series or in a Sequence type like. a list or
                tuple. [seriesname1, seriesname2,...]
            - reference_names (Union[str, Sequence[str]]): reference names for series.
            Can be given as a string for one series or in a Sequence type like
            a list or tuple. [reference_name_1, reference_name_2,...]. Reference names
            must be made up of standard Latin chars [A-Za-z], digits [0-9] and
            underscore charecter (_)
            - old_reference_names: Mostly for internal use. Defaults to None
            - verbose (bool, optional): Gives text output for the result. Defaults to True.
            - check_names (bool, optional): Checks if given series names are correct identifiers on
            EVDS API server. Defaults to True.

        Raises:
            - UnknownTimeSeriesIdentifierException: If series name can not be found on API server.
            - UnmatchingParameterSizeException: If given numbers of series names and
            reference names don't equal.

        Usage:
            - For example: when the cppi series (TP.FE.OKTG01) is saved as 'cppi',
            further EVDS data calls can be made with this reference name 'cppi' to get
            TP.FE.OKTG01 series from the API. The given reference names are stored on disk
            permanently unless the 'evds_series_references.json' file is deleted.
            - x.save_name_references("TP.FE.OKTG01", "cppi") -> saves the reference map:
            "cppi" -> "TP.FE.OKTG01"
            - "TP.FE.OKTG01" can now be retrieved from the API server using:
            x.get_series("cppi"], start=1.1.2022)
            - x.save_name_references(["TP.FE.OKTG01", "TP.DK.USD.A.YTL"], ["cppi", "usdtry"])
            similary saves the reference map:
            "cppi" -> "TP.FE.OKTG01" and "usdtry" -> "TP.DK.USD.A.YTL"
        """

        series_names, _ = self._parse_series_names(series_names, check_references=False)
        reference_names, _ = self._parse_series_names(reference_names, check_references=False)

        if len(series_names) != len(reference_names):
            raise UnmatchingParameterSizeException(
                f"Number of names in series names (given: {len(series_names)}) doesn't equal to "
                f"number of names in reference names (given: {len(reference_names)})"
            )

        allowed_chars: str = ascii_letters + digits + "_"
        check: bool = all(
                            (True if char in allowed_chars else False
                             for reference_name in reference_names
                             for char in reference_name)
        )
        if not check:
            raise ValueError(
                "Reference names must be made up of upper and lower case strings "
                "in standard Latin chars [A-Za-z], digits [0-9] and underscore '_' char"
            )

        if check_names:
            try:
                current_date: datetime = find_current_date(as_dt=True)
                test_date: datetime = current_date - timedelta(days=31)
                check: JSONType = self.get_series(
                                                  start_date=test_date,
                                                  series=series_names,
                                                  keep_references=False,
                                                  raw=True
                )
                if not check:
                    raise UnknownTimeSeriesIdentifierException(
                        f'One or more {series_names} is not found on API server.'
                        f'Are you sure they are original series names or names currently in '
                        f'references?'
                    )
            except Exception:
                raise UnknownTimeSeriesIdentifierException(
                    f'One or more {series_names} is not found on API server.'
                    f'Are you sure they are original series names or names currently in '
                    f'references?'
                ) from None

        # check if given key already exists or value already assigned to other key.
        # delete them both if detected
        if not old_reference_names:
            # key already exists
            old_reference_names = [name for name in series_names if name in self.name_cache]
            # value already mapped to another key
            old_reference_names += [k for k, v in self.name_cache.items() if v in series_names]

        # check if given series name are original names or an old reference_name
        series_names = [
            name if name not in self.name_cache else self.name_cache[name]
            for name in series_names
        ]
        reference_names = [reference_name.strip() for reference_name in reference_names]
        # clear old reference names in name references
        if old_reference_names:
            self.clear_references(keys=old_reference_names, raise_errors=False)

        self.name_cache.update(zip(reference_names, series_names))

        write_json(self.references_file, self.name_cache)

        if verbose:
            new_references: Dict[str, str] = dict(zip(reference_names, series_names))
            self._show_references(references=new_references)

    def import_name_references(self, source: Union[str, Path]) -> None:

        """Imports name references from an another location.

        Args:
            - source (Union[str, Path]): absolute path for the name references file.
        """
        copy_file(source, self.references_file)
        self.name_cache = self._load_references()
        self.show_name_references()

    def clear_references(
                         self,
                         keys: Optional[Sequence[str]] = None,
                         confirm_all: bool = True,
                         raise_errors: bool = True
    ) -> None:

        """Clears all reference names given permanently."""

        if not self.name_cache:
            if raise_errors:
                print("No reference names has been saved yet!")
            return

        if not keys:
            if confirm_all:
                self._show_references(references=self.name_cache)
                confirm: str = input(
                    "Are you sure to clear all name references mapping above? [Y/N]\n"
                )
                if confirm.lower() in ("y", "yes"):
                    delete_file(self.references_file, raise_errors=True)
                    self._clear_referencs_in_memory()
                    print("All name references have been cleared...")
                print("Clearing name references is cancelled...")
                return
            else:
                delete_file(self.references_file, raise_errors=True)
                self._clear_referencs_in_memory()
                print("All name references have been cleared...")
                return

        keys = [keys] if isinstance(keys, str) else keys
        try:
            keys = [key.strip() for key in keys]
            for key in keys:
                self.name_cache.pop(key)
        except KeyError:
            if raise_errors:
                self._show_references(references=self.name_cache)
                print(
                    f"Given reference key ({key}) is not found in references. "
                    f"Please check References Table given above to find current"
                    f"defined references."
                )

        write_json(self.references_file, self.name_cache)

    def to_file(
                self,
                data: Optional[Union[pd.DataFrame, JSONType, Dict]] = None,
                data_format: str = "csv",
                filename: Optional[str] = None,
                delimiter: str = ";",
    ) -> None:

        """Saves the current data on disk in various formats.

        Args:
            - data (Optional[Union[pd.DataFrame, JSONType, Dict]]): The data to be written on disk.
                - can be given in Pandas DataFrame
                - can be given in JSONType raw data
                - can be given in dictionary.
            - data_format (str, optional): Output format. Defaults to "csv".
                - for csv file format: "csv"
                - for Excel format: "excel", "xls", or "xlsx"
                - for raw format: "raw" or "json"
            - filename (Optional[str], optional): Output filename. Defaults to None.
                - The bare filename for output. Output file is always saved on current
                working directory. Therefore, the given filename shoul be just the bare
                filename like "cppi" or "unemployment".
                - if not given, the outputfile name is set to:
                data_year_month_day_hours_minutes_seconds
            - delimiter (str, optional): Fields delimiter for csv format. Defaults to ";".
        """

        write_data(data, data_format, filename, delimiter)

    def where(self, keyword: str, n: int = 5, verbose: bool = True) -> Dict[str, str]:

        """Searches given words to determine related series identifications on EVDS API service.

        Args:
            - keyword (str): words to be searched (for instance: consumer price index)
            - verbose (bool, optional): Shows the results on screen if True. Defaults to True.
            - n (int, optional): Number of maxiumum related results to be returned . Defaults to 5.

        Raises:
            - ValueError: if there is no keyword provided to search.

        Returns:
            Union[None, Dict[str, str]]: Results dictionary.
        """

        return self.search_engine.where(keyword=keyword, n=n, verbose=verbose)

    def purge(self) -> None:

        """Purges all cached data from the memory"""

        self.data = pd.DataFrame()

    def __repr__(self) -> str:

        return (
            f"\n*{self.__class__.__name__}*:\n\n"
            f"key: {self.api_key}\nlanguage: {self.language}\nshow_links: {self.show_links}\n"
            f"proxy servers: {self.proxy_servers}\nverify certificates: {self.verify_certificates}\n"
            f"jupyter mode: {self.jupyter_mode}\nprecision: {self.precision}\n"
            f"references file: {self.references_file}\nname references:\n{self.name_cache}"
        )
