"""evdsts SearchEngine Class"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "1.0rc1"


from collections import Counter
from datetime import datetime
from itertools import permutations
import json
from json import JSONDecodeError
from pathlib import Path
from pprint import pprint
import re
from time import perf_counter
from typing import List, Dict, Tuple

from evdsts.configuration.cfg import EVDSTSConfig
from evdsts.utils.general import delete_file


class SearchEngine:

    """A simple search engine created for EVDS index searching"""

    def __init__(self, language: str) -> None:

        """A simple search engine originally developed for evdsts series code search.

        Args:
            language (str): index language
        """
        self.cfg: EVDSTSConfig = EVDSTSConfig()
        self.index_file: str = ""
        self.language: str = language
        self.index: Dict[str, str] = {}

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

        # change language dependent features.
        self._language_changed(self._language)

    @property
    def index_age_in_days(self) -> int:

        """Returns the age of the search index file in days.

        Returns:
            int: age of serch index file (in days)
        """

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
        self.index = {}

    def _set_index_file(self, language: str) -> str:

        """Sets search index file corresponding to given language

        Returns:
            - str: index file name
        """

        if language == "TR":
            return self.cfg.index_file_tr
        else:
            return self.cfg.index_file_en

    def _load_index(self) -> None:

        """Loads series index"""

        # load index on demand in order not to allocate memory unnecessarily.
        corrupted_file: bool = False
        check: bool = Path(self.index_file).is_file()
        if not check:
            return

        with open(self.index_file, "r", encoding="utf-8") as f:
            try:
                self.index = json.load(f)
            except JSONDecodeError:
                print('JSON file that keeps the series index can not be decoded and is removed!')
                corrupted_file = True

        if corrupted_file:
            delete_file(self.index_file)

    def _show_search_results(self, results: Dict[str, List[str]]) -> None:

        """Writes series search results to screen.

        Args:
            - results (Dict[str, List[str]]): search results
        """

        print("{:^112}".format("Search Results"))
        print("-" * 112)
        print(
            "{:20}".format('Series Code'),
            "{:63}".format('Series Name'),
            "{:16}".format('Frequency'),
            "{:11}".format('Start Date')
        )

        print("-" * 112)

        for series_name, informations in results.items():
            try:
                print(
                    "{:20.20}".format(series_name),
                    "{:63.63}".format(informations[0]),
                    "{:16.16}".format(informations[1]),
                    "{:11.11}".format(informations[2])
                )
            except KeyError:
                # nevertheless show what is going on.
                pprint(results)
                break

        print("-" * 112)

    def _get_keyword_vector(self, keyword: str, separator: str = " ") -> List[str]:

        """Returns a vector from given literal

        Args:
            keyword (str): literal
            separator (str, optional): sepator for words in literal " ".

        Returns:
            List[str]: keyword vector
        """

        vector: List[str] = keyword.strip().split(separator)

        return vector

    def _create_regex_patterns(
                               self,
                               keyword: str,
                               max_word_vector_length: int = 8
    ) -> Tuple[Tuple[str, int]]:

        """Creates regex patterns for series searching.

        Args:
            - keyword (str): words to be searched.
            - max_word_vector_lenght(int): maxiumum lenght of words separeted with a separator.

        Returns:
            - List[str]: list of created regex patterns.
        """

        # First, make a regexes list which consist of possible permutations of given words from 1
        # to len(given words). The order is not important since the individual words can be
        # appeared in different order.

        if not keyword:
            return []

        keywords: List[str] = self._get_keyword_vector(keyword)

        # very long expressions can take too long time to calculate permutations.
        if len(keywords) > max_word_vector_length:
            keywords = keywords[:max_word_vector_length]

        keywords = [
            word for i in range(len(keywords) + 1)
                for word in list(permutations(keywords, i)) if i > 0
        ]
        patterns: List[List[str]] = [
            r'\b' + possibility[0] + r'\b' if len(possibility) == 1 else
                (word + r"\s+.*" for word in possibility)
                    for possibility in keywords
        ]

        regexes: List[str] = [
        str.rstrip(''.join((regex for regex in pattern)), r"\s+.*") for pattern in patterns
        ]
        # add patterns to difficulty to match in order not to call len and split functions every
        # time to determine difficulty in scoring step
        regexes = tuple((regex, len(regex.split(r"\s+.*"))) for regex in regexes)

        return regexes

    def _search_score(
                      self,
                      keyword: str,
                      overtime: float = 4.0,
    ) -> Tuple[Counter, bool]:

        """Calculates search reasult for given patterns

        Args:
            - keyword (str): keywords to be searched
            - overtime (float): defines how long the scoring process can takes maximum in seconds.


        Returns:
            - Tuple[Counter, bool]:
                - list of matching keys and their scores
                - a flag for providing information if the search was interceped due to timeover.
        """

        # and second use a scoring schema that gives scores to the matches according to difficulty
        # of matching.

        counter_list: List[str] = []
        exclude_list: List[str] = []
        time_over: bool = False

        patterns: Tuple[Tuple[str, int]] = self._create_regex_patterns(keyword)

        start: float = perf_counter()

        # not a readibility focused but performance.
        # info[0] is actual names of the series'.
        # regexes comes in order by difficulty from _create_regex_patterns.
        for key, info in self.index.items():
            score = 0
            exclude_list = []
            for regex, difficulty in patterns:
                # first check 1 word long regexes
                if difficulty == 1:
                    evaluate = re.search(regex, info[0], re.IGNORECASE)
                    if evaluate:
                        score += difficulty
                    else:
                        # not matched so all aliases of the word will be excluded from furter
                        # searches
                        exclude_list += [regex.strip(r'\b')]
                else:
                    break

            if exclude_list:
                # exclude not matching individual words.
                new_keyword: str = ' '.join(
                    (word for word in keyword.strip().split(" ") if word not in exclude_list)
                )
                new_patterns: Tuple[Tuple[str, int]] = self._create_regex_patterns(new_keyword)

            else:
                # everyone onf them is matched
                new_keyword = keyword
                new_patterns = patterns

            for regex, difficulty in new_patterns:
                # check regexes only longer the 1 word
                if difficulty > 1:
                    if re.search(regex, info[0], re.IGNORECASE):
                        score += difficulty

                if (perf_counter() - start) > overtime:
                    time_over = True
                    break

            if score:
                counter_list.extend([key] * score)

        result: Counter = Counter(counter_list)

        return result, time_over

    def where(
              self,
              keyword: str,
              n: int = 5,
              verbose: bool = True,
    ) -> Dict[str, str]:

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

        if not self.index:
            self._load_index()
            if not self.index:
                print(
                    "There is no index found to be searched!\n"
                    "Use IndexBuilder to build one to search in."
                )
                return

        if not keyword:
            raise ValueError("Keyword can not be None type.")

        overtime: float = 4.0
        score, time_over = self._search_score(keyword, overtime=overtime)
        most_commons: List[Tuple[str, int]] = score.most_common(n)
        result: Dict[str, str] = {k: self.index[k][:3] for k, _ in most_commons}

        if verbose:
            if result:
                print(f"{len(result)} most relevant results for '{keyword}' are shown below.\n")
                self._show_search_results(result)
            else:
                print(f"Nothing found for {keyword}")

        if time_over:
            print(
                f"Warning: searching took more time than {overtime} seconds and intercepted!\n"
                "Please try to search using less words (max. 6 words are ideal in general) if you "
                "don't find the series names you're looking for."
            )

        return result
