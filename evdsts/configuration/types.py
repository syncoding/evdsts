"""evdsts Defined Custom Types"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "1.0rc4"
__internal__ = "0.0.2"


from datetime import datetime
from typing import Any, Union, Dict, List
from urllib3.poolmanager import PoolManager

from pandas import Timestamp, DataFrame, Series
from requests.adapters import HTTPAdapter

#* Define a JSON type for annotating raw returns.
JSONType = Union[str, int, float, bool, None, List[Any], Dict[str, Any]]

#* Define a DateLike type for date/time operations
DateLike = Union[None, str, datetime, Timestamp]

#* Define a FrameLike for data which can be represented as a DataFrame
FrameLike = Union[Dict, Series, DataFrame]


class EVDSHttpAdapter (HTTPAdapter):

    """A tailored HTTP adapter to use for security layer connections """

    def __init__(self, ssl_context: Any = None, **kwargs: Any):

        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    # override
    def init_poolmanager(self,
                         connections: int,
                         maxsize: Any,
                         block: bool | None = False
                         ) -> None:

        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context
        )