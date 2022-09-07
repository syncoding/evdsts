"""evdsts Defined Custom Types"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "1.0rc3"
__internal__ = "0.0.1"


from datetime import datetime
from typing import Any, Union, Dict, List

from pandas import Timestamp, DataFrame, Series

#* Define a JSON type for annotating raw returns.
JSONType = Union[str, int, float, bool, None, List[Any], Dict[str, Any]]

#* Define a DateLike type for date/time operations
DateLike = Union[None, str, datetime, Timestamp]

#* Define a FrameLike for data which can be represented as a DataFrame
FrameLike = Union[Dict, Series, DataFrame]
