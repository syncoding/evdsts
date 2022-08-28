"""evdsts Time Related Utils Module"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "1.0rc2"

from datetime import datetime, timedelta
import re
from typing import Callable, Optional, Tuple, Union, Sequence, List, Dict

import numpy as np
import pandas as pd
from pandas import Timestamp

from evdsts.configuration.cfg import EVDSTSConfig
from evdsts.configuration.exceptions import (
    UndefinedFrequencyException, WrongDateFormatException, WrongDateRangeException
)
from evdsts.configuration.globals import DATE_SEPARATORS
from evdsts.configuration.types import DateLike

config: EVDSTSConfig = EVDSTSConfig()


def find_current_date(as_dt: bool = False) -> Union[str, datetime]:

    """Returns current date in a format that can be used as an EVDS API parameter.

    Args:
        - as_dt (bool, optional): returns the current date as Python datetime object instead of
        string type.

    Returns:
        - str: Current date as string which is formatted in dd-aa-YYYY, or
        - datetime: current date
    """
    now: datetime = datetime.now().date()
    if as_dt:
        return now
    str_now: str = now.strftime('%d-%m-%Y')

    return str_now


def parse_dates(
                str_date: str,
                fmt: str = '%d-%m-%Y',
                ignore_errors: bool = False,
                only_date: bool = True
                ) -> datetime:

    """Returns a date or datetime object from a given string

    Args:
        - str_date (str): A string indicates a date in given format.
        - fmt (str, optional): A date format string. Defaults to '%d-%m-%Y'.
        - ignore_errors (bool, optional): raise or ignore errors. Defaults to False.
            - True: returns datetime object if it can be parsed or otherwise the string date
            supplied.
        - only_date(bool, optional): returns excluding the time part of the date.

    Returns:
        - datetime: a  datetime object consists of date and time or just date
    """

    try:
        parsed_date = datetime.strptime(str_date, fmt)
        if only_date:
            parsed_date = parsed_date.date()
    except (ValueError, TypeError):
        if ignore_errors:
            return str_date
        raise

    return parsed_date


def correct_date(datelike: DateLike, use_separator: str = "-") -> str:

    """Retruns a corrected date from a given date as complying with EVDS API requirements

    Args:
        - datelike (Union[str, datetime, TimeStamp]): A date like object in any format.
            - String Dates: To be corrected with correct_delimiter if it's not separated by
            this charecter.
            - datetime objects: To be corrected as strings that compliying the format
            'dd-mm-YYY'
            - TimeStamp objects: To be corrected as strings that compliying the format
            'dd-mm-YYY'
        - use_delimniter (str): Any separator supplied for parsing date fields in given date.

    Raises:
        - WrongDateFormatException: If the given datelike object can not be parsed into
        a string in required format.

    Returns:
        str: A date string that EVDS API requires.
    """

    corrected_date: str = ""

    if datelike is None:
        return find_current_date()

    if isinstance(datelike, str):
        check_separator: int = sum(1 if char == use_separator else 0 for char in datelike)

        if check_separator == 2:
            corrected_date = datelike
        else:
            for separator in DATE_SEPARATORS:
                check_separator = sum(1 if char == separator else 0 for char in datelike)
                if check_separator == 2:
                    corrected_date = datelike.replace(separator, use_separator)
                    break
    else:
        # try to parse whatever is given:
        try:
            # strftime is not used because the below can any possible date format correctly.
            date_list: List[str] = []
            date_list.append(str(datelike.day) if datelike.day > 9 else "0" + str(datelike.day))
            date_list.append(
                str(datelike.month) if datelike.month > 9 else "0" + str(datelike.month)
            )
            date_list.append(str(datelike.year))
            corrected_date = '-'.join(date_list)
        except Exception:
            pass

    if not corrected_date:
        raise WrongDateFormatException(
            f'Given date {datelike} is not in a correct format.\n'
            f'use a string formed as dd-mm-YY (gg-aa-YYY) or a datetime object'
        )

    # check if any of them is a further date then now
    current_date: datetime = find_current_date(as_dt=True)
    try:
        dt_corrected_date: datetime = datetime.strptime(corrected_date, "%d-%m-%Y").date()
    except ValueError:
        raise WrongDateRangeException(
            f"Day or Month in {corrected_date} is out of range!\n"
            f"Please check the calender and make sure the given date actually exists."
        ) from None

    if dt_corrected_date > current_date:
        # given time is further than now
        corrected_date = find_current_date()

    return corrected_date


def get_period(period: str) -> Tuple[str, str]:

    """Returns a string date period from a given period string

    Args:
        period (str): period string: a number + [d, w, m, y, g, a] (order is not importrant)

    Raises:
        ValueError: If given period string can not be parsed
        ValueError: If converter function can not be found
        ValueError: If period string is not a string type

    Returns:
        Tuple[str, str]: string date period
    """

    if not isinstance(period, str):
        raise ValueError(
            "period parameter must be a string such as '2y' for indicating last 2 year."
    )

    # English and Turkish date identifiers for: day, week, month, year
    date_strings: List[str] = ["d", "w", "m", "y", "g", "h", "a"]

    period = period.lower().strip()

    num_pattern: re.Pattern = re.compile(r'\d+')
    str_pattern: re.Pattern = re.compile(f'{date_strings}', flags=re.IGNORECASE)

    num_match: re.Match = num_pattern.search(period)
    str_match: re.Match = str_pattern.search(period)

    if not (num_match and str_match):
        raise ValueError(
            f"Intended period can not be identified from given pattern: {period}\n"
            f"Please be sure the provided pattern is consisting of a number and a string which is\n"
            f"one of the identified date strings: {date_strings}"
        )

    period_map: Dict[str, Callable[[int], str]] = {

        "d": lambda val: correct_date(find_current_date(as_dt=True) - timedelta(days=val)),
        "w": lambda val: correct_date(find_current_date(as_dt=True) - timedelta(weeks=val)),
        "m": lambda val: correct_date(find_current_date(as_dt=True) - timedelta(days=val * 31)),
        "y": lambda val: correct_date(find_current_date(as_dt=True) - timedelta(days=val * 366)),
        "g": lambda val: correct_date(find_current_date(as_dt=True) - timedelta(days=val)),
        "h": lambda val: correct_date(find_current_date(as_dt=True) - timedelta(weeks=val)),
        "a": lambda val: correct_date(find_current_date(as_dt=True) - timedelta(days=val * 31))
    }

    num_part: int = int(num_match.group(0))
    str_part: str = str_match.group(0)

    converter: Callable[[int], str] = period_map.get(str_part, None)

    if not converter:
        raise ValueError(
            f"Intended period can not be identified from given string.\n"
            f"string part should be in: {date_strings}"
        )

    start_date: str = converter(num_part)
    end_date: str = find_current_date()

    return start_date, end_date


def convert_to_business_date(datelike: DateLike, use_separator: str = "-") -> str:

    """Checks given date if it's a business date and converts to nearest bdate if not.

    Args:
        - datelike (DateLike): A datelike object: str, datetime, pd.TimeStamp
            - string dates must be in d m Y format.
        - use_separator (str, optional): Date separator to be used. Defaults to "-".

    Raises:
        - ValueError: If given date string is in wrong date format.

    Returns:
        - str: nearest business date to given date.
    """

    if not datelike:
        return datelike

    format_ = f'%d{use_separator}%m{use_separator}%Y'
    if isinstance(datelike, str):
        try:
            check_datelike: datetime = datetime.strptime(datelike, format_).date()
        except ValueError as ex:
            print("Date string format or the date itself is wrong! Check given date!\n")
            raise ex

    check: bool = bool(len(pd.bdate_range(check_datelike, check_datelike)))
    if check:
        return correct_date(datelike, use_separator=use_separator)

    while not check:
        check_datelike = check_datelike - timedelta(days=1)
        check = bool(len(pd.bdate_range(check_datelike, check_datelike)))

    return correct_date(check_datelike, use_separator=use_separator)


def as_real(
            df: pd.DataFrame,
            dtype: str,
            columns: Optional[Union[str, Sequence[str]]] = None,
            convert_to_na: Optional[Union[str, Sequence[str]]] = "ND",
            exclude_columns: Optional[Union[str, Sequence[str]]] = ('tarih', 'date', 'yearweek')
            ) -> pd.DataFrame:

    """Returns a DataFrame as casting all number like values into a given real number type
    for whole DataFrame or for only given column. It guarantees all types can be casted into
    the dtype is converted to given dtype befeore returning. The datelike fields in DataFrame
    are excluded from casting in case of them to applied special date parsing operations.

    Args:
        - df (pd.DataFrame): A DataFrame object which it's fields will be cast into
        given data type.
        - dtype (str): The data type that will be used to cast into.
            - 'int8', 'int16', 'int32', 'int64'
            - 'float16', 'float32', 'float64'
        - columns (Optional[Union[str, Sequence[str]]], optional): A specific column or columns
        of the given
        DataFrame object. Could be given as string or a Sequence type like List or Tuple.
        Defaults to None.
        - convert_to_na (Optional[Union[str, Sequence[str]]]): Strings that are converted to np.na
        as a floating number.
            - can be given as a string
            - can be given as a sequence of strings.
        - exclude_columns (Optional[Union[str, Sequence[str]]]): Exclude columns from type casting
            - can be given as a string
            - can be given as a sequence of strings

    Raises:
        - TypeError:  If columns or exclude_columns is not an expected type.
        - ValueError: If given 'dtype' is not an accepted type to cast.

    Returns:
        - pd.DataFrame: Transformed DataFrame object.
    """

    def cast_type(column: pd.Series):

        """the mapping function that guarantees all the series can be cast into given type is
        converted."""

        try:
            # try type casting into given dtype.
            casted: pd.Series = column.astype(dtype, errors='raise')
            return casted
        except Exception:
            # not successfull return the same Series object.
            return column

    accepted_types: List[str] = ['int8', 'int16', 'int32', 'int64', 'float16', 'float32', 'float64']

    if dtype not in accepted_types:
        raise ValueError(
            f"dtype must be in {accepted_types}, but you've given {dtype}"
        )

    if convert_to_na:
        if isinstance(convert_to_na, str):
            convert_to_na = [convert_to_na]
        elif isinstance(convert_to_na, Sequence):
            convert_to_na = list(convert_to_na)
        else:
            raise TypeError("convert_to_na must be either a string or a sequence of strings")

    if exclude_columns:
        if isinstance(exclude_columns, str):
            exclude_columns = [exclude_columns]
        elif isinstance(exclude_columns, Sequence):
            exclude_columns = [name.lower() for name in exclude_columns]
        else:
            raise TypeError("exclude_columns must be either a string or a sequence of strings")

    if not columns:
        # change unspecified API returns into a type that can be casted into a float or int.
        # API may return 'ND' for differenciated or not observed values of series.
        # Don't touch date identifier fields because trying to cast them to another type can
        # mistakenly be success.
        if convert_to_na:
            df = df.where(~df.isin(convert_to_na), other=np.nan)

        if exclude_columns:
            columns_restricted: List[str] = [
                name for name in list(df.columns)
                    if name.lower() not in exclude_columns
            ]
            # cast all except datelikes to given dtype
            df[columns_restricted] = df[columns_restricted].iloc[::].apply(cast_type)
        else:
            df = df.astype(dtype, errors="ignore")
    else:
        # cast the given specific column or colums to given type
        columns = [columns] if isinstance(columns, str) else list(columns)
        if convert_to_na:
            df[columns] = df[columns].where(~df[columns].isin(convert_to_na))
        df[columns] = df[columns].astype(dtype, errors='ignore')

    return df


def find_datelike_columns(df: pd.DataFrame) -> pd.DataFrame:

    """Returns columns which possibly represents index of a time series.

    Args:
        - df (pd.DataFrame): A DataFrame object.

    Returns:
        - pd.DataFrame: Columns that could be time series indexes.
    """

    date_identifiers: List[str] = ['tarih', 'date']
    datelikes: List[str] = [col for col in df if col.lower() in date_identifiers]
    datelike_columns: pd.DataFrame = df[datelikes]

    return datelike_columns


def crete_ts_index(df: pd.DataFrame, method: str) -> pd.Series:

    """Returns a date range that it's frequency exactly fits in the supplied DataFrame.

    Args:
        - df (pd.DataFrame): A DataFrame which will be examined to find it's frequencies.
        - method (str): The sniffing for the series to detect their possible frequencies.

    Returns:
        - pd.Series: _description_
    """

    #! this can be easliy done with UNIXTIME but I'm working on another thing that consists of
    #! only string indexes. Therefore, I'm going to use this converter instead of using UNIXTIME
    #! against future compatibilities.

    def sniff_format(column: pd.Series) -> List[str]:

        """Returns possible frequencies that may belong to given series' as sniffing
        supplied data to detect it's frequency.

        Args:
            - column (pd.Series): datelike series objects.

        Returns:
            - List[str]: A list of possible frequencies that given series could be fit.
        """

        test_series: pd.Series
        test: bool = False
        # get a small sample from time series to sniff date format.
        sample: pd.Series = column.dropna(how='all').head(10)
        # try to sniff date format from that sample using all defined regex patterns.
        # an API returned series can be matched with more than one format like;
        # daily frequency can be matched with both daily, business daily, weekly, etc.
        # detect all possible formats for the data in question.
        possible_formats: List[str] = []
        for key, patterns in regexes.items():
            for pattern in patterns:
                test_series = sample.apply(
                    lambda datelike, pattern=pattern: bool(re.match(pattern, str(datelike)))
                )
                # greedy sniff looks for any value in series is matched to given pattern
                if method == 'greedy':
                    test = test_series.any()
                # lazy sniff chacks if all values in series are matched to given pattern
                else:
                    test = test_series.all()
                if test:
                    possible_formats.append(key)

        return possible_formats

    # load all sniffing regexes that can detect EVDS API returned date identifiers.
    regexes: Dict[str, List[str]] = config.frequency_regexes
    # create possible formats as sniffing them using a small sample of data.
    # aggregate all results for individual datelike series that could possibly be time series.
    possible_date_frequencies: pd.Series = df.agg(sniff_format)

    index: pd.Series = pd.Series(dtype="object")
    first: str = None  # first record of series
    last: str = None  # last record of series
    splitted_first: List[str] = []  # splitted first record of series by date separator
    splitted_last: List[str] = []  # splitted last record of series by date separator
    start: str = None  # starting date of date range
    end: str = None  # ending date of date range
    # date range frequencies corresponding to determined frequencies.
    frequency_map: Dict[str, str] = dict(
        daily="D", bdaily="B", weekly="W", semimonthly="SM",
        monthly="M", quarterly="Q", semiyearly="6M", yearly="Y"
    )

    # iterate through all sniffed date formats to determine which one is correct.
    # we can't just create a daterange with period equaling to length of the given data
    # because that would mean fitting the to the created frequency. On contrary, we need
    # to fit our date range to data to determine the correct frequency.
    # name: pd.Series name, frequencies: a list of sniffed formats from the sample data.
    for name, frequencies in possible_date_frequencies.iteritems():
        # iterate through all sniffed frequencies to determine which one is actually suitable
        # for the data that is returned from the EVDS API.
        for frequency in frequencies:
            # find a right frequency key to create a date range object.
            freq: str = frequency_map.get(frequency, None)

            if not freq:
                raise UndefinedFrequencyException(
                    f"Returned '{frequency}' is not a defined frequency in {frequency_map}"
                )

            # start and end dates of the given data
            first = str(df[name].iat[0])
            last = str(df[name].iat[-1])

            # For yearly data, just take first and last + 1 to creta a suitable date range.
            if freq == "Y":
                start = str(first)
                end = str(int(last) + 1)

            # for semiyearly data, find first half and create a half more of the last
            # to include current half
            if freq == '6M':
                # check for all possible date separators in case of the API changes
                # in the future.
                for separator in config.date_separators:
                    splitted_first = first.split(separator)
                    splitted_last = last.split(separator)
                    if len(splitted_first) == len(splitted_last) == 2:
                        break
                else:
                    continue

                # extract digits from the half identifier.
                extract_half_pattern: str = r"\d+"
                # for start
                extract_half: List[str] = re.findall(extract_half_pattern, splitted_first[1])
                if len(extract_half):
                    start = splitted_first[0] + "-" + str(extract_half[0])
                else:
                    continue
                # for end
                extract_half = re.findall(extract_half_pattern, splitted_last[1])
                if str(extract_half[0]) in ("01", "1"):
                    end = str(int(splitted_last[0])) + "-2"
                elif str(extract_half[0]) in ("02", "2"):
                    end = str(int(splitted_last[0]) + 1) + "-1"
                else:
                    continue
            # same idea with semiyearly data
            if freq == "Q":
                # check for all possible date separators in case of the API changes
                # in the future.
                for separator in config.date_separators:
                    splitted_first = first.split(separator)
                    splitted_last = last.split(separator)
                    if len(splitted_first) == len(splitted_last) == 2:
                        break
                else:
                    continue

                extract_half_pattern: str = r"\d+"
                # for start
                extract_half: List[str] = re.findall(extract_half_pattern, splitted_first[1])
                if len(extract_half):
                    start = splitted_first[0] + "-Q" + str(extract_half[0])
                else:
                    continue
                # for end
                extract_half = re.findall(extract_half_pattern, splitted_last[1])
                if str(extract_half[0]) in ("01", "1", "02", "2", "03", "3"):
                    end = str(int(splitted_last[0])) + "-Q" + str(int(extract_half[0]) + 1)
                elif str(extract_half[0]) in ("04", "4"):
                    end = str(int(splitted_last[0]) + 1) + "-Q1"
                else:
                    continue
            # same idea with semiyearly data
            if freq == "M":
                for separator in config.date_separators:
                    splitted_first = first.split(separator)
                    splitted_last = last.split(separator)
                    if len(splitted_first) == len(splitted_last) == 2:
                        break
                else:
                    continue

                extract_half_pattern: str = r"\d+"
                # for start
                extract_half: List[str] = re.findall(extract_half_pattern, splitted_first[1])
                if len(extract_half):
                    start = splitted_first[0] + "-" + str(extract_half[0])
                else:
                    continue
                # for end
                extract_half = re.findall(extract_half_pattern, splitted_last[1])
                if str(extract_half[0]) in (
                    "01", "1", "02", "2", "03", "3", "04", "4", "05", "5", "06", "6",
                    "07", "7", "08", "8", "09", "9", "10", "11"
                ):
                    end = str(int(splitted_last[0])) + "-" + str(int(extract_half[0]) + 1)
                elif str(extract_half[0]) in ("12",):
                    end = str(int(splitted_last[0]) + 1) + "-1"
                else:
                    continue
            # below are all in format dd-mm-yyy. Therefore start and end is created in line
            # with the same idea but with a little tunning required by the individual periods.
            if freq in ("SM", "W", "B", "D"):
                # check for all possible date separators in case of the API changes
                # in the future.
                for separator in config.date_separators:
                    splitted_first = first.split(separator)
                    splitted_last = last.split(separator)
                    if len(splitted_first) == len(splitted_last) == 3:
                        break
                else:
                    continue

                # create Timestamps from the string dates.
                day: int = int(splitted_first[0])
                month: int = int(splitted_first[1])
                year: int = int(splitted_first[2])
                start = Timestamp(year, month, day)
                day: int = int(splitted_last[0])
                month: int = int(splitted_last[1])
                year: int = int(splitted_last[2])

                if freq not in ("D", "B"):
                    # Add one day to guarantee that it includes the period the last data
                    # currently in.
                    end = Timestamp(year, month, day) + timedelta(days=1)
                else:
                    # Don't do that if the frequency is daily.
                    end = Timestamp(year, month, day)

            # start or end can not be set somehow, so, continue for other snifffed frequencies.
            if not start or not end:
                continue
            # Weekly series is announced on every Friday
            freq = "W-FRI" if freq == "W" else freq
            # create a date range comprising the determined range start - end
            test_index: pd.DatetimeIndex = pd.date_range(start, end, freq=freq)
            # test if given time series exactly fit into the created range.
            if len(test_index) == len(df[name]):
                # success.
                index = test_index
                break

        start, end = None, None

    return index


def convert_to_time_series(
                           df: pd.DataFrame,
                           method: str = 'greedy'
                           ) -> pd.DataFrame:

    """Tries to convert given DataFrame to time series and returns it.

    Args:
        - df (pd.DataFrame): DataFrame to be tried converting into time series.
        - method (str, optional): Methods of convert. Defaults to 'greedy'.
            - 'greedy' : a more eager algorithm for trying to convert given ordered series into
            time series.
            - 'lazy': a more shy algorithm for trying to convert given series in time series.

    Returns:
        - pd.DataFrame: Time series converted DataFrame.
    """

    # which columns of given data could be time series?
    datelike_columns: pd.DataFrame = find_datelike_columns(df)

    if datelike_columns.empty:
        # not any datelike is in there.
        return df
    # try to create a time series index complying with these columns.
    index = crete_ts_index(datelike_columns, method=method)

    if not index.empty:
        # time series index is created successfully.
        df.set_index(index, inplace=True)
        df.drop(datelike_columns.columns, axis=1, inplace=True)
        df.index.name = 'Date'

    return df
