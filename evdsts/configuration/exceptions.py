"""evdsts Defined Exceptions"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "1.0rc1"


class SubCategoryNotFoundException(Exception):
    """Raisess when a sub-category is not found"""


class GroupNotFoundException(Exception):
    """ Raisess when a group of sub-category is not found"""


class SeriesNotFoundException(Exception):
    """ Raisess when a series is not found"""


class APIServiceConnectionException(Exception):
    """Raisess when an API key, API Server, API Request and network based exceptions is occured"""


class WrongAPIKeyException(Exception):
    """Raisess when used EVDS Service API Key is wrong"""


class WrongDateFormatException(Exception):
    """Raisess when a given date format can not be identified"""


class WrongDateRangeException(Exception):
    """Raisess if given date is out of range"""


class UndefinedFrequencyException(Exception):
    """Raisess when a given or API returned time series frequency can not be identified"""


class UndefinedTransformationFunctionException(Exception):
    """Raises when an undefined transformation function is given as a parameter"""


class UndefinedAggregationFunctionException(Exception):
    """Raises when an undefined aggregation function is given as a parameter"""


class AmbiguousFunctionMappingException(Exception):
    """Raises if transformation and aggregation functions are applied at the same time"""


class AmbiguousOutputTypeException(Exception):
    """Raises if raw and dictionary types are requested at once"""


class AmbiguousFunctionParameterException(Exception):
    """Raises if a function takes an ambiguous parameter set"""


class UnmatchingParameterSizeException(Exception):
    """Raises when given parameters sizes don't match each other"""


class UnmatchingFieldSizeException(Exception):
    "Raisess when given series names count is different than API returned series count"


class UnknownTimeSeriesIdentifierException(Exception):
    """Raisess when a given series name is not found on API server"""


class InsufficientSampleSizeException(Exception):
    """Raisess if a process needs a larger size sample than provided"""

class OptionalPackageRequiredException(Exception):
    """Raisess if a required optional package is not found on environment"""
