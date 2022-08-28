"""evdsts General Utils Module"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "1.0rc2"

import csv
from datetime import datetime, date
from io import StringIO
import json
from json import JSONDecodeError, JSONEncoder
from pathlib import Path
import shutil
import sys
from typing import Any, Dict, List, Optional, Sequence, Union, TextIO


import pandas as pd


from evdsts.configuration.exceptions import (
    UnmatchingFieldSizeException, OptionalPackageRequiredException
)
from evdsts.configuration.types import JSONType


def is_numeric(string: str) -> bool:

    """Returns if given number is an int or float

    Args:
        string (str): string to be checked.

    Returns:
        bool: is numeric
    """
    try:
        float(string)
    except ValueError:
        return False

    return True


def copy_file(source: Union[str, Path], target: Union[str, Path], verbose: bool = True) -> None:

    """Copies a file from source to target.

    Args:
        source (Union[str, Path]): source file name
        target (Union[str, Path]): target file name
        verbose (bool, optional): text output for result. Defaults to True.
    """

    if isinstance(source, Path):
        source = str(source.absolute())

    if isinstance(target, Path):
        target = str(target.absolute())

    try:
        shutil.copy2(source, target)
    except FileNotFoundError:
        print(f"\nCopy failed! Are you sure the file {source} exists?\n")
        raise
    except Exception:
        print("\nAn unknown exception has been occured please read the output!\n")
        raise

    if verbose:
        print(f'\nsuccess: {source} --> {target}')


def delete_file(fname: str, raise_errors: bool = False) -> None:

    """Clears name references.

    Args:
        - fname (str): file to be deleted.
        - raise_errors (bool, optional): Raise or pass if an error is occured.
            - True: raise
            - False: pass
        Defaults to False.
    """

    try:
        Path(fname).unlink()
    except Exception as ex:
        if not raise_errors:
            pass
        print(ex)
        raise


def write_json(fname: str, reference_dict: Dict[str, str]) -> None:

    """Writes reference file to disk.

    Args:
        fname (str): file name to be written.
        reference_dict (Dict[str, str]): Dictionary to be written.
    """

    class CustomEncoder(JSONEncoder):

        """A custom JSON encoder for serializing datetime fields in given dictionary"""

        def __init__(self, *args, **kwargs) -> None:

            super().__init__(
                            skipkeys=True,
                            allow_nan=True,
                            ensure_ascii=False
                            )

        def default(self, arg: Any) -> str:

            if isinstance(arg, (datetime, date)):
                return arg.isoformat()
            else:
                return super().default(arg)

    with open(fname, "w", encoding="utf-8") as f:
        json.dump(
            reference_dict,
            f,
            ensure_ascii=False,
            skipkeys=True,
            allow_nan=True,
            cls=CustomEncoder
        )


def load_json(text: Union[str, bytes], field: Optional[str] = None) -> JSONType:

    """Returns JSON data from a given literal.

    Args:
        - text (Union[str, bytes]): A string or byte object.
        - field (Optional[str]): a specific field to be returned.

    Returns:
        - JSONType: JSON type object.
    """
    try:
        json_val: JSONType = json.loads(text)
    except JSONDecodeError:
        print(f"{text!r} is not a correct JSON data type.")
        raise

    if field:
        try:
            return json_val[field]
        except KeyError:
            print(f"Given field ({field}) is not a key in JSONType data!")
            raise

    return json_val


def write_excel(
                df: pd.DataFrame,
                fname: Path,
                sheet_name: str = "evds_data",
                float_format: str = "%.4f",
                verbose: bool = False
                ) -> bool:

    """Writes a Pandas DataFrame object on disk in MS Excel Format.

    Args:
        - df (pd.DataFrame): DataFrame object to be written
        - fname (Path): A Pathlike object
        - sheet_name (str, optional): Excel Sheet name. Defaults to "evds_data".
        - verbose (bool, optional): Text information after done. Defaults to False.

    Returns:
        - bool: Result of the operation
    """

    try:
        df.to_excel(fname, float_format=float_format, sheet_name=sheet_name)
    except ModuleNotFoundError:
        raise OptionalPackageRequiredException(
            "\nWriting excel files requires 'openpyxl' package to be installed.\n\n"
            "for pip users: pip install openpyxl\n\n"
            "for Anaconda or Miniconda users: conda install openpyxl\n\n"
            "In Jupyter Notebook:\n\n"
            "for pip users (in Jupyter Notebook):\n"
            "%pip install openpyxl\n\n"
            "for Anaconda or Miniconda users (in Jupyter Notebook):\n"
            "%conda install openpyxl"
        ) from None

    if verbose:
        print(f"DataFrame has been written to -> {str(fname)}")

    return True


def write_data(
               data: Union[pd.DataFrame, JSONType, Dict],
               data_format: str = "csv",
               filename: Optional[str] = None,
               delimiter: str = ";",
               ) -> None:

    """Tries hard to save the given data on disk in various formats.

    Args:
        - data ([Union[pd.DataFrame, JSONType, Dict]]): The data to be written on disk.
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

    frame_data: bool = False
    json_data: bool = False
    dict_data: bool = False

    if isinstance(data, (pd.DataFrame, pd.Series)):
        if data.empty:
            print(
                'Given DataFrame is empty or nothing has been gotten from the API service yet...'
            )
            return
        frame_data = True
    elif isinstance(data, (str, bytes, list)):
        try:
            test_cast: JSONType = json.dumps(data, skipkeys=True, allow_nan=True, ensure_ascii=False)
        except Exception:
            raise TypeError('Given data is not a writable JSONType') from None
        json_data = True
    elif isinstance(data, dict):
        dict_data = True

    if data_format not in ("excel", "xls", "xlsx", "raw", "json", "csv"):
        print(
            f"Given data format {data_format} is not supported."
            f"Allowed formats: [csv, excel, json] "
        )
        return

    written: bool = False

    data_format = data_format.lower()
    dt: str = datetime.now().strftime('%Y_%m_%d_%H%M%S')
    name: str = "data" + "_" + dt if not filename else filename.split(".")[0]
    fname: Path = Path.cwd() / name

    if data_format in ("raw", "json"):

        fname = fname.with_suffix(".json")
        if json_data:
            json_str: JSONType = json.dumps(
                data, skipkeys=True, allow_nan=True, ensure_ascii=False
            )
            stream_like: TextIO = StringIO(json_str)
            df: pd.DataFrame = pd.read_json(stream_like, encoding="utf-8")
            df.to_json(fname)
            written = True
        elif frame_data:
            data.to_json(fname)
            written = True
        elif dict_data:
            try:
                df: pd.DataFrame = pd.DataFrame(data)
                df.to_json(fname)
                written = True
            except Exception:
                with open(fname, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, skipkeys=True, allow_nan=True)
                written = True

    elif data_format == "csv":

        fname = fname.with_suffix(".csv")
        if frame_data:
            data.to_csv(fname, sep=delimiter, encoding="utf-8", float_format="%.4f")
            written = True
        if json_data:
            json_str: JSONType = json.dumps(
                data, skipkeys=True, allow_nan=True, ensure_ascii=False
            )
            stream_like: TextIO = StringIO(json_str)
            df: pd.DataFrame = pd.read_json(stream_like, encoding="utf-8")
            df.to_csv(fname, sep=delimiter, encoding="utf-8", float_format="%.4f")
        if dict_data:
            try:
                df: pd.DataFrame = pd.DataFrame(data)
                df.to_csv(fname, sep=delimiter, encoding="utf-8", float_format="%.4f")
            except Exception:
                with open(fname, "w", encoding="utf-8") as f:
                    writer: csv.DictWriter = csv.DictWriter(
                        f, fieldnames=data.keys(), delimiter=delimiter, quoting=csv.QUOTE_MINIMAL
                    )
                    writer.writeheader()
                    writer.writerow(data)
                written = True

    elif data_format in ("excel", "xls", "xlsx"):

        fname = fname.with_suffix(".xlsx")
        if frame_data:
            written = write_excel(df, fname, float_format="%.4f", sheet_name="evds_data")
        if json_data:
            json_str: JSONType = json.dumps(
                data, skipkeys=True, allow_nan=True, ensure_ascii=False
            )
            stream_like: TextIO = StringIO(json_str)
            df: pd.DataFrame = pd.read_json(stream_like, encoding="utf-8")
            written = write_excel(df, fname, float_format="%.4f", sheet_name="evds_data")
        if dict_data:
            try:
                df: pd.DataFrame = pd.DataFrame(data)
            except Exception:
                print(f'failed: {data} is not an Excel convertable structure')
                return
            written = write_excel(df, fname, float_format="%.4f", sheet_name="evds_data")
            written = True

    if written:
        print(f"Given data have been written on {str(fname)}")
    else:
        print("failed: something went wrong while the data is being written.")


def join_sequentials(series: Sequence[str], delimiter: str = "-") -> str:

    """Returns a joined string which is created from given list and delimiter.

    Args:
        - series (Sequence[str]): A Sequence type like a List or Tuple that contains strings.
        - delimiter (str): Delimiter char that will be used for joining the elements.

    Returns:
        - str: Joined string.
    """

    return delimiter.join(series)


def set_column_names(
                     df: pd.DataFrame,
                     column_names: Sequence[str],
                     all_uppercase: bool = True,
                     double_size: bool = False
                     ) -> pd.DataFrame:

    """Returns the same DataFrame object as changing column names with given ones.

    Args:
        - df (pd.DataFrame): DataFrame object to be altered.
        - column_names (Sequence[str]): column names to be set as DataFrames' column names.
        - all_uppercase (bool, optional): makes all given names in uppercase
        - double_size = to determine if the names comes from a recursive operation (aggregations)

    Raises:
        - TypeError: If given name container is not a Sequence type.
        - UnmatchingFieldSizeException: If lenght of the given names doesn't match with number
        of columns in DataFrame.

    Returns:
        - pd.DataFrame: DataFrame
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"A Pandas DataFrame object must be supplied to df variable.\n"
            f"You sent {type(df)}"
    )

    try:
        given_size: int = len(column_names)
    except Exception:
        raise TypeError(
            'Column names must be strings in a Sequence type container like a List or Tuple'
        ) from None
    column_size: int = len(df.columns)
    if given_size != column_size:
        raise UnmatchingFieldSizeException(
            f"Given size of new names ({given_size if not double_size else given_size * 2}) is "
            f"different from DataFrame's columns size "
            f"({column_size if not double_size else column_size * 2})"
        )

    new_names: List[str] = column_names

    if all_uppercase:
        new_names = [name.upper() for name in new_names]

    df.columns = new_names

    return df


def drop_na_columns(df: pd.DataFrame) -> pd.DataFrame:

    """Returns the same DataFrame as dropping columns which are all NaN

    Args:
        df (pd.DataFrame): DataFrame to be NaN columns dropped.

    Returns:
        pd.DataFrame: DataFrame cleared from NaNs
    """
    df.dropna(axis=1, how='all', inplace=True)

    return df


def drop_columns(
                 df: pd.DataFrame,
                 columns: Optional[Sequence] = None,
                 ignore_errors: bool = True
                 ) -> pd.DataFrame:

    """Returns DataFrame clearing it from predetermined and given fields.

    Args:
        - df (pd.DataFrame): DataFrame to be altered.
        - columns (Sequence, optional): Columns to be dropped.
        - ignore_errors (bool, optional): Ignores the errors for not found columns.
        Defaults to True.

    - Returns:
        pd.DataFrame: DataFreame freed from obsolote fields.
    """

    if isinstance(columns, str):
        clear_list = [columns]
    elif isinstance(columns, Sequence):
        clear_list = [name for name in columns]
    else:
        raise TypeError("Columns must be a single string or a sequence of strings.")

    if ignore_errors:
        df.drop(columns=clear_list, inplace=True, errors='ignore')
    else:
        df.drop(columns=clear_list, inplace=True)

    return df


def progress(current: int, maximum: int, real_end: bool = False) -> None:

    """A simple progressbar implementation

    Args:
        current (int): current step
        maximum (int): maxmium step
        real_end (bool, optional): Maxiumum is real or a max of range(s, e). Defaults to False.
    """

    progress_: int = 0
    if not real_end:
        progress_ = round(100 * current / (maximum - 1))
    else:
        progress_ = round(100 * current / maximum)

    # should be divided by 100
    denominator: int = 2
    step: int = int(progress_ / denominator)
    rebuild: int = int(100 / denominator)

    show: str = f"Progress: {progress_}% - [" + "|" * step + " " * (rebuild - step) + "]"

    if progress_ < 100:
        sys.stdout.write(f"{show}\r")
    else:
        sys.stdout.write(f"{show}\n")

    sys.stdout.flush()
