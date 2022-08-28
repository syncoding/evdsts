"""evdsts IndexBuilder Class"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "1.0rc2"


import json
from json import JSONDecodeError
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Any, List, Optional, Dict

from evdsts.configuration.cfg import EVDSTSConfig
from evdsts.base.connecting import Connector
from evdsts.utils.general import delete_file, progress, write_json


class IndexBuilder:

    """EVDS Time Series Index Builder Class"""

    def __init__(
                 self,
                 key: Optional[str] = None,
                 language: str = "TR",
                 proxy_servers: Optional[Dict[str, str]] = None,
                 verify_certificates: bool = True
                 ) -> None:

        """EVDS (EDDS) Search Index Builder.

        Args:
            - key (str): API key supplied by EVDS (EDDS) service.
            - language (str, optional): Interface language (if available). Defaults to "TR".
            - proxy_servers (Optional[Dict[str, str]], optional): Proxies for accesing the EVDS
            over them. Defaults to None
            - verify_certificates (bool, optional): Enabling/Disabling of SSL security certificate
            checking during connection.
                - True: Check SSL sertificate is valid.
                - False: No security check (use the option if you encounter connection problems
                despite the API service is actually on-line)
            Defaults to True.
        """

        self.cfg: EVDSTSConfig = EVDSTSConfig()

        self.key: str = key if key else self._load_key()
        self.index_file: str = ""
        self.connector = Connector(
            key=self.key,
            language=language,
            proxy_servers=proxy_servers,
            verify_certificates=verify_certificates
        )

        self.language: str = language

    @property
    def language(self) -> str:

        """Returns language code"""

        return self._language

    @language.setter
    def language(self, val: str) -> None:

        """Sets Indexing language"""

        if not self.cfg.defined_languages.get(val.strip(), None):
            raise ValueError(f"{val.strip()} is not a defined language.")

        self._language = val.strip()

        self._language_changed(self._language)

    @property
    def index_age_in_days(self) -> int:

        """Returns the age of the search index file in days.

        Returns:
            int: age of serch index file (in days)
        """

        if not Path(self.index_file).is_file():
            return -1

        modification_time_stamp: float = Path(self.index_file).stat().st_mtime
        modification_date: datetime = datetime.fromtimestamp(modification_time_stamp)
        age_days: int = (datetime.now() - modification_date).days

        return age_days

    def _language_changed(self, language: str) -> None:

        """Things that must be reloaded when the language is changed.

        Args:
            language (str): selected language
        """

        # reload when the language is chenged
        self.index_file = self._set_index_file(language)
        self.connector.language = language

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
                "API key using 'save_key()' method of EVDSConnector in order not to provide\na key "
                "every time when you create an instance of IndexBuilder."
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

    def _set_index_file(self, language: str) -> str:

        """Sets search index file corresponding to given language

        Returns:
            - str: index file name
        """

        if language == "TR":
            return self.cfg.index_file_tr
        else:
            return self.cfg.index_file_en

    def _get_series(self, wait: int) -> Dict[str, Any]:

        """Downloads indexing data from the API Service

        Args:
            - wait (int): waiting time in seconds before each new connection is established.
                - can not be set less then 5 secs. in order not to overload the API service.

        Returns:
            Dict[str, Any]: All available series on EVDS service.
        """

        index: Dict[str, Any] = {}

        main_categories: Dict[int, str] = self.connector.get_main_categories(as_dict=True)
        main_category_ids: List[int] = main_categories.keys()
        size: int = len(main_category_ids)

        progress(0, size)
        exit_: bool = False

        for idx, id_ in enumerate(main_category_ids):
            sub_categories: Dict[str, Any] = (
                self.connector.get_sub_categories(id_, as_dict=True).keys()
            )
            try:
                for group in sub_categories:
                    series_group: Dict[str, Any] = self.connector.get_groups(group, as_dict=True)
                    index.update(series_group)
                    sleep(wait)
            except KeyboardInterrupt:
                exit_ = True

            progress(idx, size)

            if exit_:
                print('\nAborted !')
                break

        return index

    def _write_index(self, index: Dict[str, Any]) -> None:

        """Writes created index to the disk.

        Args:
            index (Dict[str, Any]): provided created index dictionary.
        """

        write_json(self.index_file, reference_dict=index)

    def build_index(self, wait: float = 5) -> None:

        """Builds a new search index that is required by in-situ searches.

        Args:
            - wait (int): waiting time in seconds before each new connection is established.
                - can not be set less then 5 secs. in order not to overload the API service.
        """

        if wait < 5:
            print(
                "Connecting the server intensively could cause a service overload.\n"
                "waiting time before a new connection is established must be at least 5 sec."
            )
            return

        index_age: int = self.index_age_in_days

        if index_age != -1:
            print(f"\nCurrent index is {index_age} days old.")
        else:
            print("\nNo prior built index is found.")
        print("Rebuilding the index will take around 30 minutes.\n")

        accept: str = input("Are you sure to continue? [Y/N]\n")
        if accept.lower() not in ('y', 'yes'):
            print("\nAborted!")
            return

        print("\n(1/2) creating index... (ctrl+C to abort)\n")
        index: Dict[str, Any] = self._get_series(wait)
        print(f"\n(2/2) writing index -> {self.index_file}\n")
        self._write_index(index)
        print("done...\n")
        print(
            "The search index is created with most up-to-date entries from EVDS service.\n"
            "You can now search series in this updated index."
        )
