"""evdsts IndexBuilder Class"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "0.1.0"
__internal__ = "0.0.2"


import json
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path
from time import sleep
from typing import Any

from tqdm import tqdm

from evdsts.base.connecting import Connector
from evdsts.configuration.cfg import EVDSTSConfig
from evdsts.utils.general import delete_file, write_json


class IndexBuilder:
    """EVDS Time Series Index Builder Class"""

    def __init__(
        self,
        key: str | None = None,
        language: str = "TR",
        proxy_servers: dict[str, str] | None = None,
        verify_certificates: bool = True,
        secure: bool = True,
    ) -> None:
        """EVDS (EDDS) Search Index Builder.

        Args:
            - key (str): API key supplied by EVDS (EDDS) service.
            - language (str, optional): Interface language (if available). Defaults to "TR".
            - proxy_servers (dict[str, str] | None, optional): Proxies for accesing the EVDS
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
            verify_certificates=verify_certificates,
            secure=secure,
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
            - dict[str, str]: name references
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
                key: str = json.load(f)["key"]
            except JSONDecodeError:
                print("JSON file that keeps the API KEY can not be decoded and is removed!")
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

    def _estimate_total_series(self) -> int:
        """Estimates total series count from the existing index file.

        Returns:
            int: estimated number of series entries, or 0 if no index exists.
        """
        try:
            with open(self.index_file, "r", encoding="utf-8") as f:
                return len(json.load(f))
        except (FileNotFoundError, JSONDecodeError, ValueError):
            return 0

    def _get_series(self, wait: int) -> dict[str, Any]:
        """Downloads indexing data from the API Service

        Args:
            - wait (int): waiting time in seconds before each new connection is established.
                - can not be set less then 5 secs. in order not to overload the API service.

        Returns:
            dict[str, Any]: All available series on EVDS service.
        """

        index: dict[str, Any] = {}

        main_categories: dict[int, str] = self.connector.get_main_categories(as_dict=True)
        all_cats = self.connector._all_categories
        if not all_cats.empty and "UST_CATEGORY_ID" in all_cats.columns:
            parent_ids: set = set(int(x) for x in all_cats["UST_CATEGORY_ID"].unique() if x != -1)
            leaf_category_ids: list[int] = [
                id_ for id_ in main_categories.keys() if int(id_) not in parent_ids
            ]
        else:
            leaf_category_ids: list[int] = list(main_categories.keys())

        estimated_total: int = self._estimate_total_series()

        pbar = tqdm(
            total=estimated_total,
            desc="Building index",
            unit=" series",
            dynamic_ncols=True,
        )
        exit_: bool = False

        for id_ in leaf_category_ids:
            try:
                sub_categories: dict[str, Any] = self.connector.get_sub_categories(
                    id_, as_dict=True
                ).keys()
            except Exception:
                sleep(wait)
                continue
            sleep(wait)
            try:
                for group in sub_categories:
                    series_group: dict[str, Any] = self.connector.get_groups(group, as_dict=True)
                    index.update(series_group)
                    pbar.update(len(series_group))
                    sleep(wait)
            except KeyboardInterrupt:
                exit_ = True
            except Exception:
                sleep(wait)

            if exit_:
                break

        pbar.total = len(index)
        pbar.n = len(index)
        pbar.refresh()
        pbar.close()

        if exit_:
            print("\nAborted !")

        return index

    def _write_index(self, index: dict[str, Any]) -> None:
        """Writes created index to the disk.

        Args:
            index (dict[str, Any]): provided created index dictionary.
        """

        write_json(self.index_file, reference_dict=index)

    def build_index(self, wait: float = 5, confirm: bool = True) -> None:
        """Builds a new search index that is required by in-situ searches.

        Args:
            - wait (int): waiting time in seconds before each new connection is established.
                - can not be set less then 5 secs. in order not to overload the API service.
            - confirm (bool): whether to ask for user confirmation before building.
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
        print("Rebuilding the index will take around 60 minutes.\n")

        if confirm:
            accept: str = input("Are you sure to continue? [Y/N]\n")
            if accept.lower() not in ("y", "yes"):
                print("\nAborted!")
                return

        print("(1/2) creating index... (ctrl+C to abort)\n")
        index: dict[str, Any] = self._get_series(wait)
        print(f"\n(2/2) writing index -> {self.index_file}\n")
        self._write_index(index)
        print("done...\n")
        print(
            "The search index is created with most up-to-date entries from EVDS service.\n"
            "You can now search series in this updated index."
        )
