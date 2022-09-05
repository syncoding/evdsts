"""evdsts Transformator Class"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "1.0rc3"
__internal__ = "0.0.1"

from itertools import combinations
from typing import Dict, List, Sequence, Tuple, Optional, Type, Union

import numpy as np
import pandas as pd


from evdsts.configuration.exceptions import (
    InsufficientSampleSizeException, OptionalPackageRequiredException
)
from evdsts.utils.general import is_numeric


def _quantize_float(
                    vector: np.ndarray,
                    precision: int,
                    preserve_int: bool = True
                    ) -> np.ndarray:

    """Quantizes a floating-point number (or int) vector to given precision

    Args:
        - vector (np.ndarray): a floating-point (or integer) numbers array.
        - precision (int): precision requested
        - preserve_int (optional, bool): Integer values are returned untouched if True.
        Defaults to True.

    Returns:
        - np.ndarray[np.float32, np.int8, np.int16, np.int32, np.int64]:
        quantized (or original) number
    """

    # types must be preserved.
    if preserve_int and vector.dtype in (np.int8, np.int16, np.int32, np.int64):
        return vector

    if precision == 0:
        return np.rint(vector)

    return np.float32(np.around(vector, precision))


def _set_precision(
                   series: pd.DataFrame,
                   precision: int,
                   inplace: bool = False
) -> Union[pd.DataFrame, None]:

    """Sets the floating-point numbers precisions of series in given DataFrame and return it
    back

    Args:
        - series (pd.DataFrame): A DataFrame made up of numerical series
        - precision (int): percision to be fixed
        - inplace(bool, optional): mutates the original series given if True. Defaults to False

    Returns:
        pd.DataFrame: precision fixed data frame if inplace=False or None.
    """
    if precision is None:
        return series
    if isinstance(precision, str):
        if precision.isnumeric():
            precision = int(precision)
        else:
            raise TypeError("Precision must be an integer!")

    fixed_series: pd.DataFrame = series.apply(_quantize_float, precision=precision, raw=True)

    if inplace:
        series.update(fixed_series)
        return

    return fixed_series


class Transformator:

    """A data transformations class for data manipulations on EVDS series"""

    @staticmethod
    def _convert_to_df(series: Union[Dict, pd.Series, pd.DataFrame]) -> pd.DataFrame:

        """Converts compatible types intp pandas DataFrame

        Args:
            series (Union[Dict, pd.Series, pd.DataFrame]): Data provided.

        Raises:
            TypeError: If provided data is not a convertible type
            ValueError: If provided data structure is not convertible

        Returns:
            pd.DataFrame: Series in DataFrame
        """

        if not isinstance(series, (Dict, pd.Series, pd.DataFrame)):
            raise TypeError(
                f"Series shold be either a dictionary or a pandas DataFrame or pandas DataFrame!\n"
                f"Provided type is {type(series)}"
            )

        if isinstance(series, pd.DataFrame):
            return series
        if isinstance(series, pd.Series):
            return series.to_frame()
        if isinstance(series, Dict):
            try:
                df: pd.DataFrame = pd.DataFrame(series)
                df.index.name = "Date"
                return df
            except Exception:
                raise ValueError("Given dictionary could not be converted to a DataFrame") from None

    @staticmethod
    def _prepare_for_return(
                            original: pd.DataFrame,
                            stats: pd.DataFrame,
                            rename: bool = True,
                            suffix_1: Optional[str] = None,
                            suffix_2: Optional[str] = None,
                            precision: Optional[int] = None,
                            keep_originals: bool = True
    ) -> pd.DataFrame:

        """Prepares data for the last return.

        Args:
            - original (pd.DataFrame): original observations DataFrame
            - stats (pd.DataFrame): stats computed DataFrame
            - rename (bool, optional): renames the stats. Defaults to True.
            - suffix_1 (Optional[str], optional): 1st suffix for renaming. Defaults to None.
            - suffix_2 (Optional[str], optional): 2nd suffix for renaming. Defaults to None.
            - precision (int, optional): precision to be truncated stats values. Defaults to None.
            - keep_originals (bool, optional): returns the original as well if True.
            Defaults to True.

        Returns:
            - pd.DataFrame: prepared data.
        """

        if rename:
            if not suffix_2:
                if suffix_1:
                    stats.columns = [str(name) + "_" + str(suffix_1) for name in stats.columns]
            else:
                if suffix_1:
                    stats.columns = [
                        str(name) + "_" + suffix_1 + "_" + str(suffix_2) for name in stats.columns
                        ]

        stats = Transformator.set_precision(stats.iloc[::], precision=precision)

        if not keep_originals:
            return stats

        originals: pd.DataFrame = original.copy(deep=True)
        joint: pd.DataFrame = Transformator._join(originals, stats)

        return joint

    @staticmethod
    def _join(*series: pd.DataFrame, axis: int = 1) -> pd.DataFrame:

        """Joins DataFrames together"""

        return pd.concat(series, axis=axis)

    @staticmethod
    def _z(vector: np.ndarray) -> np.ndarray:

        """Returns Z-Scores for a given vector.

        Args:
            vector (np.ndarray): A numpy NDArray vector

        Returns:
            np.ndarray: Z values
        """
        mean: float = np.nanmean(vector)
        std: float = np.nanstd(vector)
        if np.isclose(std, 0, rtol=1e-05, atol=1e-08, equal_nan=False):
            raise ValueError(f"All observations in series is the same: {mean}!")

        z: np.ndarray = (vector - mean) / std

        return z

    @staticmethod
    def _mad(vector: np.ndarray, constant: float = 1.4826) -> np.ndarray:

        """Returns median absulete deviations for given values in vector

        Args:
            vector (np.ndarray): time series vector

        Returns:
            np.ndarray: median absolute deviation (mad)
        """

        # 1/q(norm(0.75)) = 1.4826

        mad_socre: np.float64 = np.nanmedian(np.absolute(vector - np.nanmedian(vector))) * constant
        if np.isclose(mad_socre, 0, rtol=1e-05, atol=1e-08, equal_nan=False):
            raise ValueError(
                f"At least %50 of observations in series is the same: mad_score={mad_socre}!"
            )

        mad_: np.ndarray = (vector - np.nanmedian(vector)) / mad_socre

        return mad_

    @staticmethod
    def _normalize(vector: np.ndarray, method: str) -> np.ndarray:

        """Returns normalized vector of given vector.

        Args:
            vector (np.ndarray): a vector to be normalized

        Method:
            - the normalization method
                - simple
                - min-max
                - mean
                - median
                - median absolute deviation
                - z

        Returns:
            - np.ndarray: normalized vector
        """

        if method == "simple":
            normal: np.ndarray = vector / (np.nanmax(vector) + 1)
        elif method == "min-max":
            normal: np.ndarray = (
                (vector - np.nanmin(vector)) / (np.nanmax(vector) - np.nanmin(vector))
            )
        elif method == "mean":
            normal: np.ndarray = (vector - np.nanmean(vector)) / (np.nanmax(vector) + 1)
        elif method == 'median':
            normal: np.ndarray = (vector - np.nanmedian(vector)) / (np.nanmax(vector) + 1)
        elif method == "mad":
            normal: np.ndarray = Transformator._mad(vector)
        elif method == "z":
            normal: np.ndarray = Transformator._z(vector)

        return normal

    @staticmethod
    def _time_trend(
                    vector: np.ndarray,
                    degree: int = 1,
                    min_sample: int = 5,
                    min_different: int = 5,
    ) -> np.ndarray:

        """Returns the deterministic time trend for given vector

        Args:
            - vector (np.ndarray): A vector consists of numerical values.
            - degree (int, optional): Degree of deterministic trend. Defaults to 1.
            - min_sample (int, optional): Minimum sample size to compute the trend. Defaults to 5.
            - min_different (int, optional): Minimum number of different observations.
            Defaults to 5.

        Raises:
            - InsufficientSampleSizeException: If the observations are insufficient.
            - InsufficientSampleSizeException: If the different observations are insufficient.
            - ValueError: If given polynom degree is not appropriate.

        Returns:
            - np.ndarray: deterministic time trend for the given vector.
        """

        n: int = len(vector)

        if n < min_sample:  # there should be at least min_sample samples
            raise InsufficientSampleSizeException(
                f"one of the series has got insufficient observations in it!\n"
                f"The minimum allowed sample size is {min_sample}, but one of them has got {n} "
                f"values in it."
            )
        if len(set(vector)) < min_different:  # there should be at min_diff different samples.
            raise InsufficientSampleSizeException(
                f"one of the series has got insufficient number of different observations in it!\n"
                f"{min_different} number of different observations must be in each series but one "
                f"of them has got {len(set(vector))} different values currently."
            )

        if degree < 1:
            raise ValueError("Degree must be greater than 1!")

        if degree > 2:
            print(
                "Warning: High order polynoms can oscillate wildly if they're not a good "
                "representative of given data"
            )

        # y = Bn*Trend^n + Bn-1*Trend^n-1 + B0*Trend^0 + e,   n: n, n-1, ... n-n
        trend: np.ndarray = np.arange(1, n + 1)   # deterministic trend vector X
        y: np.ndarray = vector  # Series vector Y

        pred: np.ndarray = np.isfinite(trend) & np.isfinite(y)  # just a precaution for NAN values

        coefficients: np.ndarray = np.polyfit(trend[pred], y[pred], degree)  # LS estimator

        predictions = 0
        for degree, coeff in enumerate(coefficients, 1):
            predictions += (trend ** degree) * coeff if degree != len(coefficients) else coeff

        trend_vector: np.ndarray = predictions

        return trend_vector

    @staticmethod
    def _dummy(
            vector: np.ndarray,
            threshold: Union[float, Sequence[float]],
            condition: str,
            fill_true: float,
            fill_false: float
    ) -> np.ndarray:

        """Converts given vector to a dummy vector.

        Args:
            vector (np.ndarray): A np.array containing numbers
            threshold (Union[float, Sequence[float, float]]): cutoff point(s) for dummy creation
            condition (str): creation condition
            fill_true (float): fill if condition is True
            fill_false (float): fill if condition is False

        Returns:
            np.ndarray: Dummy Vector
        """

        # need to be copied or originals are lost since it is manupilating the column itself.
        vector_copy: np.ndarray = np.copy(vector)

        if condition == ">":
            vector_copy[vector_copy > threshold] = fill_true
        elif condition == ">=":
            vector_copy[vector_copy >= threshold] = fill_true
        elif condition == "<":
            vector_copy[vector_copy < threshold] = fill_true
        elif condition == "<=":
            vector_copy[vector_copy <= threshold] = fill_true
        elif condition == "()":
            vector_copy[(vector > np.min(threshold)) & (vector < np.max(threshold))] = fill_true
        elif condition == "[]":
            vector_copy[(vector >= np.min(threshold)) & (vector <= np.max(threshold))] = fill_true

        vector_copy[vector_copy != fill_true] = fill_false

        return vector_copy

    @staticmethod
    def _rolling_window_check(window: Union[float, int, str]) -> Tuple[Union[int, str], int]:

        """Checks rolling window compatibility"""

        if isinstance(window, (int, float)):
            window = round(window)
            min_periods = 0
            if window < 2:
                raise ValueError('window must be greater than 1.')
        elif isinstance(window, str):
            min_periods = 0

        return window, min_periods

    @staticmethod
    def _parse_parameters(
                          parameter: Union[None, int, str, Sequence[int]],
                          type_: Type = int
    ) -> Tuple[Union[int, float, str]]:

        """Parses given various types of parameters to required parameters format.

        Args:
            parameter (Union[None, int, str, Sequence[int]]]): parameter

        Returns:
            Tuple[int]: parsed parameters
        """

        if not parameter:
            return tuple()

        parsed_parameter: Tuple[Union[int, float]] = tuple()

        if isinstance(parameter, Sequence):

            if isinstance(parameter, str):
                if type_ is float:
                    parsed_parameter = tuple(
                        (type_(val.strip()) for val in parameter.split(',') if is_numeric(val.strip()))
                    )
                elif type_ is int:
                    parsed_parameter = tuple(
                        (type_(val.strip()) for val in parameter.split(',') if val.strip().isnumeric())
                    )
                elif type_ is str:
                    parsed_parameter = tuple(
                        (type_(val.strip()) for val in parameter.split(','))
                    )
            else:
                parsed_parameter = tuple(parameter)
        elif type_ is int and isinstance(parameter, type_):
            parsed_parameter = (parameter, )
        elif type_ is float and isinstance(parameter, (int, type_)):
            parsed_parameter = (parameter, )
        else:
            raise TypeError(f"Parameter type is wrong: {parameter}")

        return parsed_parameter

    @staticmethod
    def _unique_parameters(
                           seq_lags: Union[Tuple[int], None],
                           range_lags: Union[int, None]
    ) -> List[int]:
        """Returns a unique parameter set from given parameters set

        Args:
            seq_lags (Union[Tuple[int], None]): sequential type lags
            range_lags (Union[int, None]): integer lags

        Returns:
            List[int]: _description_
        """

        raw_lags: List[int] = []

        if seq_lags and range_lags:
            raw_lags = [lag for lag in range(1, range_lags + 1)] + [lag for lag in seq_lags]
        elif range_lags:
            raw_lags = [lag for lag in range(1, range_lags + 1)]
        elif seq_lags:
            raw_lags = [lag for lag in seq_lags]

        unique_lags: List[int] = sorted(list(set(raw_lags)))

        return unique_lags

    @staticmethod
    def join(*series: pd.DataFrame) -> pd.DataFrame:

        """Joins given series (all must be indexed the same)

        Raises:
            ValueError: Under different conditions
            TypeError: If given series are not DataFrame or Series types.

        Returns:
            pd.DataFrame: Joint series.
        """

        if len(series) < 2:
            raise ValueError("There must be at least 2 DataFrames to be joined!")
        check: bool = all(
            (isinstance(data, (pd.DataFrame, pd.Series)) for data in series)
        )
        if not check:
            raise TypeError("All given series must be either a DataFrame or Series objects!")

        check = all(
        (True if idx == len(series) - 1 else
                True if data.index.equals(series[idx + 1].index) else False
                    for idx, data in enumerate(series))
    )
        if not check:
            raise ValueError("The indexes of given series is not equal to each others!")

        joint: pd.DataFrame = Transformator._join(*series)

        return joint

    @staticmethod
    def set_precision(
                      series: pd.DataFrame,
                      precision: int,
                      inplace: bool = False
    ) -> Union[pd.DataFrame, None]:

        """Sets the floating-point numbers precisions of series in given DataFrame and return it
        back

        Args:
            - series (pd.DataFrame): A DataFrame made up of numerical series
            - precision (int): percision to be floating-point numbers fixed
            - inplace (optional, bool): mutates the provided series if True. Defaults to False

        Returns:
            pd.DataFrame: precision fixed data frame if 'inplace=False' or None.
        """

        fixed_series: pd.DataFrame = _set_precision(series, precision=precision, inplace=inplace)

        return fixed_series

    def __init__(self, global_precision: Optional[int] = None) -> None:

        """The transformation processes for any kind of data manupilations related to evdsts

        Args:
            - global_precision (Optional[int], optional): Sets a global precision for floating-point
            numbers returned by all kind of transformation functions. Defaults to None.
                - if None given: No global precision is set. Each transformation function uses its
                own default precision if an explicit precision is not supplied with 'precision=n'
                parameter while calling the transformator function.
                - integer number given: Global default precision for every transformation function
                is set as given precision. That means they use this global default precision
                instead of their own individual defaults if an explicit precision is not given with
                'precision=n' parameter while calling the transformator function.

        Notes:
            - Explicitly given 'precision' parameter while calling any transformation functions
            overrides the 'global_precision' and the functions' own default precision.
            - 'global_precision' overrides the functions' own default precision if an explicit
            precision is not given with 'precision=n' parameter while calling the transformator
            function.
        """

        self.global_precision: Union[None, int] = global_precision

    @property
    def global_precision(self) -> Union[None, int]:

        """Returns the precision of floating-point numbers for all transformators"""

        return self._global_precision

    @global_precision.setter
    def global_precision(self, val: Union[None, int]) -> None:

        """Sets the precision of floating-point numbers for all transformators as a global default
        """

        if val is None:
            self._global_precision = None
            return
        if not isinstance(val, int):
            raise TypeError(
                "Global precision can be either an integer number or None (for default)"
            )

        self._global_precision = val

    def _decide_precision(self, precision: Union[None, int]) -> Union[None, int]:

        """Decides whichever precision is to be used for the process

        Returns:
            Union[None, int]: precision decided.
        """

        if precision is not None:
            return precision
        else:
            if self.global_precision:
                return self.global_precision

        return None

    def ln(
        self,
        series: pd.DataFrame,
        precision: Optional[int] = None,
        keep_originals: bool = True,
        rename: bool = True
    ) -> pd.DataFrame:

        """Returns natural logarithm series.

        Args:
            - series [pd.DataFrame]: A Dataframe includes series to be processed.
            - precision (int, optional): Precision of returned values. Defaults to None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame if
            True. Defaults to True.
            - rename(bool, optional): renames the column names appropriately. Defaults to True.

        Returns:
            pd.DataFrame: LN(Series).
        """

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)
        transformed: pd.DataFrame = np.log(series)

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=transformed, rename=rename, suffix_1='LN',
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def diff(
            self,
            series: pd.DataFrame,
            order: int = 1,
            precision: Optional[int] = None,
            keep_originals: bool = True,
            rename: bool = True
    ) -> pd.DataFrame:

        """Returns difference series in given order.

        Args:
            - series [pd.DataFrame]: A Dataframe includes series to be processed.
            - order (int, optional): Order for difference operator.
            Defaults to 1 (1st Difference).
            - precision (int, optional): Precision of returned values. Defaults to None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame if.
            True. Defaults to True.
            - rename(bool, optional): renames the column names appropriately. Defaults to True.

        Returns:
            - pd.DataFrame: (Series, order)L
        """

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)
        transformed: pd.DataFrame = series - series.shift(order)

        if rename:
            transformed.columns = [
                name + "_DIFF" if order == 1 else str(name) + "_DIFF_" + str(order)
                    for name in transformed.columns
            ]

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=transformed, rename=False,
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def lndiff(
            self,
            series: pd.DataFrame,
            order: int = 1,
            precision: Optional[int] = None,
            keep_originals: bool = True,
            rename: bool = True
    ) -> pd.DataFrame:

        """Returns differences of natural logarithms for given order. This is a symmetric returns
        that; if you get 0.2 ln difference in time t, and -0.2 ln difference in time t + 1 then you
        get back to where you were, that is, its total efect is 0. Notice the symmetry as a
        different charecter of ln difference than regular growth since a %20 growth in time t,
        and %-20 growth in time t + 1 is equal to net %-4 growth.

        Args:
            - series [pd.DataFrame]: A Dataframe includes series to be processed.
            - order (int, optional): Order for difference operator.
            Defaults to 1 (1st Log Difference).
            - precision (int, optional): Precision of returned values. None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame if
            True. Defaults to True.
            - rename(bool, optional): renames the column names appropriately. Defaults to True.

        Returns:
            - pd.DataFrame: (LN(Series), order)L
        """

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)
        transformed: pd.DataFrame = np.log(series / series.shift(order))

        if rename:
            transformed.columns = [
                name + "_LNDIFF" if order == 1 else name + "_LNDIFF_" + str(order)
                    for name in transformed.columns
            ]

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=transformed, rename=False,
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def deterministic_trend(
                            self,
                            series: pd.DataFrame,
                            degree: int = 1,
                            precision: Optional[int] = None,
                            keep_originals: bool = True,
                            rename: bool = True
    ) -> pd.DataFrame:

        """Returns deterministic time series trend for given series

        Args:
            - series [pd.DataFrame]: A Dataframe includes series to be processed.
            - degree (int, optional): Degree of the deterministic trend. Defaults to 1.
            - precision (int, optional): Precision of returned values. Defaults to None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame
            if True. Defaults to True.
            - rename(bool, optional): renames the column names appropriately. Defaults to True.

        Returns:
            - pd.DataFrame: deterministic trend
        """

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)
        trend_series: pd.DataFrame = series.apply(
            Transformator._time_trend, degree=degree, raw=True
        )

        if rename:
            trend_series.columns = [
                str(name) + "_LINTR" if degree == 1 else str(name) + "_PLYTR_" + str(degree)
                    for name in trend_series.columns
            ]

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=trend_series, rename=False,
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def sma(
            self,
            series: pd.DataFrame,
            window: Union[int, str],
            precision: Optional[int] = None,
            keep_originals: bool = True,
            rename: bool = True
    ) -> pd.DataFrame:

        """"Returns simple moving averages of series in given DataFrame.

        Args:
            - series (pd.Series): DataFrame made up of time series.
            - window Union[int, str]: The window for averaging as fixed period or time based.
                - can be anchored to observations: 5 means exactly 5 observations regardless of
                time.
                - can be anchored to time: "5d" means observations that comprising exactly 5 days.
            - precision (int, optional): Precision of returned values. Defaults to None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame if
            True. Defaults to True
            - rename(bool, optional): renames the column names appropriately. Defaults to True.

        Raises:
            - ValueError: if an inappropriate window is provided

        Returns:
            - pd.DataFrame: simple moving averages of series in given dataframe
        """

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)
        window, min_periods = Transformator._rolling_window_check(window)

        ma_: pd.DataFrame = series.rolling(window=window, min_periods=min_periods).mean()

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=ma_, rename=rename, suffix_1="SMA", suffix_2=window,
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def ema(
            self,
            series: pd.DataFrame,
            window: Optional[float]= None,
            alpha: Optional[float] = None,
            precision: Optional[int] = None,
            keep_originals: bool = True,
            rename: bool = True
    ) -> pd.DataFrame:

        """Returns exponential moving averages of series in given DataFrame.

        Args:
            - series (pd.Series): DataFrame made up of time series.
            - window (float): The window (or span) for averaging as fixed period.
                - can be given only as fixed values: 5 means exactly 5 observations regardless
                of time.
            - alpha (float, optional): The smoothing factor given directly.
                - should be in range (0, +1)
            - precision (int, optional): Precision of returned values. Defaults to None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame if
            True. Defaults to True
            - rename(bool, optional): renames the column names appropriately. Defaults to True.

        Raises:
            - ValueError: if an inappropriate window is provided

        Returns:
            - pd.DataFrame: exponential moving averages of series in given dataframe
        """

        if not (window or alpha):
            raise ValueError(
                "You should provide either a smoothing 'window' or 'alpha' to calculate the EMA"
            )

        if window and alpha:
            raise ValueError(
                "Providing both the smoothing factor 'alpha' and smoothing 'window' is an ambigious"
                "statement. You must provide either the 'window' or the 'alpha' but not both"
                f"You provide both alpha= {alpha} and window= {window}"
            )

        if window and window < 2:
            raise ValueError(
                f"Averaging period window must be greater than 1"
                f"You provide window= {window}"
            )

        if alpha and not (0 < alpha < 1):
            raise ValueError(
                f"Smoothing parameter alpha should meet the condition 0 < alpha < 1\n"
                f"You provide apha= {alpha}"
            )

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)
        alpha = alpha if alpha else 2.0 / (1 + window)

        ema_: pd.DataFrame = series.ewm(alpha=alpha,
                                        min_periods=0,
                                        adjust=False,
                                        ignore_na=False).mean()

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=ema_, rename=rename, suffix_1="EMA",
            suffix_2= window if window else "A" + str(alpha).replace(".", "_"),
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def rolling_var(
                    self,
                    series: pd.DataFrame,
                    window: int,
                    precision: Optional[int] = None,
                    keep_originals: bool = True,
                    rename: bool = True
    ) -> pd.DataFrame:

        """"Returns rolling variances of series in given dataframe to easliy spot
        possible structural breaks.

        Args:
            - series (pd.Series): DataFrame made up of time series.
            - window (int): The window or period for rolling variance.
                - can be only fixed observations: 5 means exactly 5 observations regardless of time.
            - precision (int, optional): Precision of returned values. Defaults to None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame if
            True. Defaults to True
            - rename(bool, optional): renames the column names appropriately. Defaults to True.

        Raises:
            - ValueError: if an inappropriate window is provided

        Returns:
            - pd.DataFrame: rolling variances of series in given dataframe
        """

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)
        window, min_periods = Transformator._rolling_window_check(window)

        rollvar: pd.DataFrame = series.rolling(window=window, min_periods=min_periods).var()

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=rollvar, rename=rename, suffix_1="ROLVAR", suffix_2=window,
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def rolling_corr(
                    self,
                    series: pd.DataFrame,
                    window: int,
                    precision: Optional[int] = None,
                    keep_originals: bool = True,
                    rename: bool = True
    ) -> pd.DataFrame:

        """"Returns binary rolling correlations of given series. Rolling Correlations in a time
        period (window) can be a good indication of unstable or spurious relitionships in series.
        Rolling correlations are especially useful for observing deviations from the long-term
        linear relitionships in provided series. Sever swings in observed correlations
        (especially sign changes) could indicate that the linear relitionship of two series is not
        stable in time, that is, no stable long-term relitionship is engaged in subject series and
        seeming long-term relitionship between the series could possible be unstable or spurious.

        Args:
            - series (pd.Series): DataFrame made up of time series.
            - window (int): The window (or period) for rolling correlations.
                - can be only fixed observations: 5 means exactly 5 observations regardless of time.
            - precision (int, optional): Precision of returned values. Defaults to None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame if
            True. Defaults to True
            - rename(bool, optional): renames the column names appropriately. Defaults to True.

        Raises:
            - ValueError: if an inappropriate window is provided

        Returns:
            - pd.DataFrame: binary rolling correlations of series in given dataframe
        """

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)
        window, min_periods = Transformator._rolling_window_check(window)

        rcorr: pd.DataFrame = (
            series
            .rolling(window=window, min_periods=min_periods)
            .corr()
            .iloc[:,:]
         )

        names: List[str] = rcorr.columns.to_list()
        combs: List[str] = list(combinations(names, 2))
        result: pd.DataFrame = pd.DataFrame()

        for s1, s2 in combs:
            corrs: pd.DataFrame = (
                rcorr.loc[(slice(None), s1), s2]
                .drop(columns=s1)
                .reset_index(drop=True)
            )
            result = pd.concat([result, corrs], axis=1)

        result.columns = ['_'.join(name) for name in combs]
        result.index = series.index

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=result, rename=rename, suffix_1="RLCR", suffix_2=window,
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def z_score(
                self,
                series: pd.DataFrame,
                precision: Optional[int] = None,
                keep_originals: bool = True,
                rename: bool = True
    ) -> pd.DataFrame:

        """Returns Z scores (x-mu)/sigma(x) for series in given DataFrame. A good measure for
        spotting deviations from the expected values for a series which is normally distributed
        y:~N(m, s)

        Args:
            - series (pd.DataFrame): Series z-scores to be calculated.
            - precision (int, optional): Precision of returned values. Defaults to None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame if
            True. Defaults to True
            - rename(bool, optional): renames the column names appropriately. Defaults to True.

        Returns:
            - pd.DataFrame: z-scores
        """

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)
        z: pd.DataFrame = series.apply(Transformator._z, raw=True)

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=z, rename=rename, suffix_1="Z",
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def mad(
            self,
            series: pd.DataFrame,
            precision: Optional[int] = None,
            keep_originals: bool = True,
            rename: bool = True
    ) -> pd.DataFrame:

        """Returns Median Absolute Deviation median(|y(t) - median(yt)|) for series in given
        DataFrame. Notice: the median absolute deviation is a robust statistic, even for data drawn
        from non normal populations and could be used instead of z-score for measuring deviations
        from the expectations as a substitute.

        Args:
            - series (pd.DataFrame): Series to be MAD calculated.
            - precision (int, optional): Precision of returned values. Defaults to None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame if
            True.
            - rename(bool, optional): renames the column names appropriately. Defaults to True.

        Returns:
            - pd.DataFrame: Median Absolule Deviation
        """

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)
        mad_: pd.DataFrame = series.apply(Transformator._mad, raw=True)

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=mad_, rename=rename, suffix_1="MAD",
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def decompose(
                  self,
                  series: pd.DataFrame,
                  degree: int = 1,
                  source: str = "trend",
                  method: str = "subtract",
                  precision: Optional[int] = None,
                  keep_originals: bool = True,
                  rename: bool = True
    ) -> pd.DataFrame:

        """Returns detrended series in line with provided source and method. Extracting time based
        deterministic trends from the series could be a good way to create stationary series from the
        non-stationary ones. The most important caveat for this process is that modelling with
        de-trended series can not represent long-term relitionships with variables since de-trending
        process cause the series loose their long-term memories.

        Args:
            - series (pd.DataFrame): A DataFrame consists of series to be detrended
            - degree (int, optional): Degree of deterministic trend or window for (e/s)ma.
            Defaults to 1.
                - means polinomial degree of deterministic trend if the source is given as 'trend'.
                for instance: 1 means linear trend, and 2 means quadratic trend, etc.
                - means window of (e/s)ma if the source is given as 'sma' or 'ema'
            - source (str, optional): source of detrending process. Defaults to "trend".
                - trend: detrended series = series (- or /) trend(series, given_degree)
                - sma: detrended series = series (- or /) sma(series, window=degree)
                - ema: detrended series = series (- or /) ema(series, window=degree)
            - method (str, optional): method to be used as detrending operator. Defaults to
            "subtract".
                - subtract: series - source
                - divide: series / source
            - keep_originals (bool, optional): Includes original series in returned DataFrame if
            True. Defaults to True.
            - precision (int, optional): precision of values in detrended series. Defaults to None.
            - rename(bool, optional): renames the column names appropriately. Defaults to True.

        Raises:
            - TypeError: If source or method is provided inappropriately.
            - ValueError: If provided source is unknown
            - ValueError: If provided method is unknown

        Returns:
            - pd.DataFrame: de-trended series
        """

        defined_sources: List[str] = ["trend", "sma", "ema"]
        defined_methods: List[str] = ["subtract", "divide"]

        if not (isinstance(source, str) and isinstance(method, str)):
            raise TypeError("Source and method must be strings")

        source = source.lower()
        method = method.lower()

        if source not in defined_sources:
            raise ValueError(f"Source must be in {defined_sources}")
        if method not in defined_methods:
            raise ValueError(f"method must be in {defined_methods}")

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)

        detrended_series: pd.DataFrame = pd.DataFrame()
        if source == "trend":
            trend_series = series.apply(Transformator._time_trend, degree=degree, raw=True)
            if method == "subtract":
                detrended_series = series - trend_series
            elif method == "divide":
                detrended_series = series / trend_series.replace({0: np.nan})
        elif source == "sma":
            ma_: pd.DataFrame = self.sma(
                series=series, window=degree, precision=None, keep_originals=False, rename=False
            )
            if method == "subtract":
                detrended_series = series - ma_
            elif method == "divide":
                detrended_series = series / ma_.replace({0: np.nan})
        elif source == "ema":
            ema_: pd.DataFrame = self.ema(
                series=series, window=degree, precision=None, keep_originals=False, rename=False
            )
            if method == "subtract":
                detrended_series = series - ema_
            elif method == "divide":
                detrended_series = series / ema_.replace({0: np.nan})

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=detrended_series, rename=rename, suffix_1="DET",
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def normalize(
                  self,
                  series: pd.DataFrame,
                  method: str = "mad",
                  precision: Optional[int] = None,
                  keep_originals: bool = True,
                  rename: bool = True
    ) -> pd.DataFrame:

        """Returns normalized series in given DataFrame

        Args:
            - series (pd.DataFrame): Series to be z-score calculated.
            - method (str): normalization method. Defaults to 'mad'
                - simple: x / (max(x) + 1) -> range: [0, +1)
                - min - max: (x - min(x)) / (max(x) - min(x)) -> range: (0, 1]
                - mean: (x - mu(x)) / (max(x) + 1) -> range: [-1, +1)
                - median: (x - median(x)) / (max(x) + 1) -> range: [-1, +1)
                - mad: (x - median(x)) / (median(abs(x - median(x))) * 1.4826) -> range: (-inf, +inf)
                - z: (x- mu(x)) / sigma(x) -> range: (-inf, +inf)
            - precision (int, optional): Precision of returned values. Defaults to None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame if
            True.
            - rename(bool, optional): renames the column names appropriately. Defaults to True

        Returns:
            - pd.DataFrame: normalized series
        """

        defined_methods: List[str] = ['simple', "min-max", 'mean', 'median', 'mad', 'z']

        if not isinstance(method, str):
            raise TypeError(f"'method' must be a string type in {defined_methods}")

        method = method.lower()

        if method not in defined_methods:
            raise ValueError(f"'method' must be a value in {defined_methods}")

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)

        normalized: pd.DataFrame = pd.DataFrame()
        normalized = series.apply(Transformator._normalize, method=method, raw=True)

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=normalized, rename=rename, suffix_1="NORM",
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def dummy(
              self,
              series: pd.DataFrame,
              condition: str,
              threshold: Union[float, str, int, Sequence[Union[float, str, int]]],
              fill_true: float = 1,
              fill_false: float = 0,
              precision: Optional[int] = None,
              keep_originals: bool = True,
              rename: bool = True
    ) -> pd.DataFrame:

        """Retruns a dummy series of given series

        Args:
            - series (pd.DataFrame): Series DataFrame
            - condition (str): Evaluation condition for cutoff or bounds.
                - '>' : greater than threshold
                - '>=': greater than or equals to threshold
                - '<' : smaller than threshold
                - '<=': smaller than or equals to threshold
                - '()': greater than lower bound and smaller than upper bound (closed bounds).
                - '[]': greater than or equal to lower bound and smaller than or equal to upper
                bound (open bounds).
            - threshold Union[float, str, Sequence[Union[float, str]]]: The cutoff or bound points
            for dummy creation (e.g: 5 for x > 5 condition or "1, 4", (1, 4) pr [1, 4] for
            1 < x < 4 condition)
            - fill_true (float, optional): Value to be filled if the given condition is True.
            Defaults to 1.
            - fill_false (float, optional): Value to be filled if the given condition is False.
            Defaults to 0.
            - precision (int, optional): Precision of returned values. Defaults to None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame if
            True
            Defaults to True.
            - rename (bool, optional): renames the column names appropriately. Defaults to True

        Returns:
            - pd.DataFrame: Dummy series that satisfy the given condition.
        """

        defined_conditions: List[str] = [">", ">=", "<", "<=", "()", "[]"]

        if not ((isinstance(condition, str)) and (condition in defined_conditions)):
            raise TypeError(f"Condition must be a a string an in {defined_conditions}")
        condition = condition.strip()

        if condition in ("()", "[]") and not isinstance(threshold, Sequence):
            raise ValueError(
                f"Provided threshold is wrong for condition: '{condition}'\n"
                "Upper and Lower thresholds must be given in a comma separated string, Tupl or List"
                "like '3, 5', (3, 5) or [3, 5]"
            )

        if condition not in ("()", "[]"):
            if isinstance(threshold, str):
                if is_numeric(threshold):
                    threshold = float(threshold)
                else:
                    raise TypeError(
                        f"Threshold must be an integer or floating-number number for "
                        f"given condition: '{condition}'"
                    )
            else:
                if not isinstance(threshold, (int, float)):
                    raise TypeError(
                        f"Threshold must be an integer or floating-number number for "
                        f"given condition: '{condition}'"
                    )
        else:
            threshold = Transformator._parse_parameters(threshold, type_=float)
            if len(threshold) != 2:
                raise ValueError(
                    f"Length of bounds should be 2 as consisting of upper and lower bounds.\n"
                    f"Bounds can be given as a Tuple or List like (3, 5) or [3, 5] for condition "
                    f"'{condition}'.\nThe lenght of provided bounds {threshold} is {len(threshold)}"
                )


        suffix_map: Dict[str, str] = {
            ">": f"GTT_{threshold}",
            ">=": f"GOET_{threshold}",
            "<": f"SMT_{threshold}",
            "<=": f"SOET_{threshold}",
            "()": f"CBOUND",
            "[]": f"OBOUND"
        }

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)

        dummy_series: pd.DataFrame = series.apply(
                                    Transformator._dummy, threshold=threshold, condition=condition,
                                    fill_true=fill_true, fill_false=fill_false, raw=True
                                    )

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=dummy_series, rename=rename, suffix_1=suffix_map[condition],
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def laggeds(
                self,
                series: pd.DataFrame,
                range_lags: Optional[int] = None,
                lags: Optional[Union[int, Sequence, str]] = None,
                precision: Optional[int] = None,
                keep_originals=True
    ) -> pd.DataFrame:

        """Returns the lagged series of given series.

        Args:
            - series (pd.DataFrame): DataFrame object containing series
            - range_lags (Optional[int], optional): An integer number indicating lags in range.
            Defaults to None.
                - given 'n' means all lags in 1....n.
                - for instance; '5' means: y(t-1), y(t-2), y(t-3), y(t-4), y(t-5)
            - lags (Optional[Union[int, Sequence, str], optional): Individual lag values.
            Defaults to None.
                - given 'n' means only the nth. lag.
                - for instance; '5' means: y(t-5)
                - can be given in a Sequence type container like (3, 6, 9, 12) or [3, 6, 9, 12]
                indicating: y(t-3), y(t-6), y(t-9), y(t-12)
                - can be given as a comma separated string like "3, 4" indicating: y(t-3), y(t-4)
            - precision (int, optional): Precision of returned values. Defaults to None.
            - keep_originals (bool, optional): Includes original series in returned DataFrame if
            True
            Defaults to True.

        Raises:
            ValueError: If given lags is not integer values

        Returns:
            pd.DataFrame: Lagged Series
        """

        series = Transformator._convert_to_df(series)

        if not (isinstance(range_lags, int) or range_lags is None):
            raise TypeError("'range_lags' must be an integer number representing the lags 1....n")

        parsed_lags: Tuple[int] = Transformator._parse_parameters(lags)

        if not (range_lags or parsed_lags):
            raise ValueError(
                "At least one of the parameters shuld be provided: 'range_lags' or 'lags'"
            )

        precision = self._decide_precision(precision=precision)

        unique_lags: List[int] = Transformator._unique_parameters(parsed_lags, range_lags)

        lagged_series: List[pd.DataFrame] = []

        for lag in unique_lags:
            lagged: pd.DataFrame = series.copy(deep=True).shift(lag)
            lagged.columns = [name + "_LAG_" + str(lag) for name in lagged.columns]
            lagged_series.append(lagged)

        lagged_joint: pd.DataFrame = Transformator._join(*lagged_series)

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=lagged_joint, rename=False,
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def corr(
             self,
             series: pd.DataFrame,
             method: str = 'pearson',
             precision: Optional[int] = None
    ) -> pd.DataFrame:

        """Returns correlation coefficients between series in given DataFrame. This is especially
        important for easily detecting possible multi co-linearity problem in considering model.
        Significant correlations (ro > 0.6 or ro < -0.6 in general) between considering independent
        variables for a model indicate that the considering model will probably suffer from
        multi co-linearity problem.

        Args:
            - series (pd.DataFrame): A DataFrame consist of only one series (such as usdtry)
            - method (optional, str): Method of correlation computations. Defaults to 'pearson'
                - pearson : standard Pearson correlation coefficients
                - kendall : Kendall Tau correlation coefficients.
                - spearman : Spearman rank correlation coefficients
            - precision (int, optional): precision to be used to truncate floatings.
            Defaults to None.

        Raises:
            - ValueError: If given DataFrame is made up of less than 2 series.

        Returns:
            - pd.DataFrame: Correlation coefficients of given series.
        """

        defined_methods: List[str] = ["pearson", "kendall", "spearman"]

        if not isinstance(method, str):
            raise TypeError(f"'method' must be a string in {defined_methods}")

        method = method.lower()

        if method not in defined_methods:
            raise ValueError(
                f"{method} is not a defined method. It must be one of {defined_methods}"
            )

        series = Transformator._convert_to_df(series)

        if len(series.columns) < 2:
            raise ValueError("Provided DataFrame should consist of more than 1 series.")

        precision = self._decide_precision(precision=precision)

        try:
            corr_: pd.DataFrame = Transformator.set_precision(
                series.corr(method=method), precision=precision
            )
        except ModuleNotFoundError:
            if method == "kendall":
                raise OptionalPackageRequiredException(
                    "\nCalculating Kendall's Tau requires 'scipy' package to be installed.\n\n"
                    "for pip users: pip install scipy\n\n"
                    "for Anaconda or Miniconda users: conda install scipy\n\n"
                    "In Jupyter Notebook:\n\n"
                    "for pip users (in Jupyter Notebook):\n"
                    "%pip install scipy\n\n"
                    "for Anaconda or Miniconda users (in Jupyter Notebook):\n"
                    "%conda install scipy"
                ) from None
            raise

        return corr_

    def autocorr(
                self,
                series: pd.DataFrame,
                range_lags: Optional[int] = None,
                lags: Optional[Union[int, Sequence, str]] = None,
                method: str = 'pearson',
                column: Optional[Union[str, int]] = None,
                precision: Optional[int] = None
    ) -> pd.DataFrame:

        """Returns autocorrelations between the original series and given lags of them.
        The autocorrelations could provide you a very quick insight about the stationary state of
        the series provided. Significant correlations (ro > 0.6 or ro < -0.6 in general) between the
        series and its laggeds indicates that the observations are highly dependent on their prior
        values in time, and therefore, that would indicate that the mean of the series depends on
        and changes through time (a possible stochastic trend flag).

        Args:
            - series (pd.DataFrame): A DataFrame consist of only one series (such as usdtry)
            - range_lags (Optional[int], optional): An integer number indicating lags in range.
            Defaults to None.
                - given 'n' means all lags in 1....n.
                - for instance; '5' means: y(t-1), y(t-2), y(t-3), y(t-4), y(t-5)
            - lags (Optional[Union[int, Sequence, str], optional): Individual lag values.
            Defaults to None.
                - given 'n' means only the nth. lag.
                - for instance; '5' means: y(t-5)
                - can be given in a Sequence type container like (3, 6, 9, 12) or [3, 6, 9, 12]
                indicating: y(t-3), y(t-6), y(t-9), y(t-12)
                - can be given as a comma separated string like "3, 4" indicating: y(t-3), y(t-4)
            - method (optional, str): Method of correlation computations. Defaults to 'pearson'
                - pearson : standard Pearson correlation coefficients
                - kendall : Kendall Tau correlation coefficients.
                - spearman : Spearman rank correlation coefficients
            - column (Optional[Union[str, int]], optinal): column name for DataFrames including
            series more than 1. Defaults to None.
                - string: column name
                - integer: column index (starting with 0)
            - precision (int, optional): precision to be used to truncate floatings.
            Defaults to None.

        Raises:
            - ValueError: If given DataFrame is made up of more than 1 series.
            - ValueError: If neither 'range_lags' not 'lags' is provided.
            - TypeError:  If 'range_lags' is not given as an integer number.

        Returns:
            - pd.DataFrame: Autocorrelations.
        """

        series = Transformator._convert_to_df(series)

        if len(series.columns) > 1:
            if column is None:
                raise ValueError(
                    "Provided DataFrame consists of more than 1 series\nPlese provide a column "
                    "name using 'column' parameter."
                )
            else:
                if isinstance(column, str):
                    try:
                        series = series.loc[:, column.strip()]
                    except KeyError:
                        try:
                            series = series.loc[:, column.strip().upper()]
                        except KeyError:
                            try:
                                series = series.loc[:, column.strip().lower()]
                            except KeyError:
                                raise KeyError(
                                    f"Given column {column} is not found in DataFrame"
                                ) from None
                elif isinstance(column, int):
                    try:
                        series = series.iloc[:, column]
                    except IndexError:
                        raise IndexError(
                            f"The column index you provide ({column}) is out of bounds\n"
                            f"The frame has {len(series.columns) - 1} columns starting from 0"
                        ) from None
                else:
                    raise TypeError("'column' must be a real column name or index of the column")

        lagged_series: pd.DataFrame = self.laggeds(
            series, lags=lags, range_lags=range_lags, precision=None
        )

        try:
            auto_corr: pd.DataFrame = Transformator.set_precision(
                lagged_series.corr(method=method), precision=precision
            )
        except ModuleNotFoundError:
            if method == "kendall":
                raise OptionalPackageRequiredException(
                    "\nCalculating Kendall's Tau requires 'scipy' package to be installed.\n\n"
                    "for pip users: pip install scipy\n\n"
                    "for Anaconda or Miniconda users: conda install scipy\n\n"
                    "In Jupyter Notebook:\n\n"
                    "for pip users (in Jupyter Notebook):\n"
                    "Import sys\n"
                    "!{sys.executable} -m pip install scipy\n\n"
                    "for Anaconda or Miniconda users (in Jupyter Notebook):\n"
                    "Import sys\n"
                    "!conda install --prefix {sys.prefix} scipy"
                ) from None
            raise

        return auto_corr

    def serial_corr(
                    self,
                    series: pd.DataFrame,
                    hold: Union[str, int],
                    range_lags: Optional[int] = None,
                    lags: Optional[Union[int, Sequence, str]] = None,
                    method: str = 'pearson',
                    precision: Optional[int] = None
    ) -> pd.DataFrame:

        """Returns a serial correlation vector between the constant and the others. The vector could
        provide you a very quick insight about linear relitionships between a constant series and
        the others including their lags.

        Args:
            - series (pd.DataFrame): A DataFrame consist of series (such as usdtry, eurtry)
            - column (Optional[Union[str, int]], optinal): the constant column (like a dependent
            variable for a model)
                - string: column name
                - integer: column index (starting with 0)
            - range_lags (Optional[int], optional): An integer number indicating lags in range.
            Defaults to None.
                - given 'n' means all lags in 1....n.
                - for instance; '5' means: y(t-1), y(t-2), y(t-3), y(t-4), y(t-5)
            - lags (Optional[Union[int, Sequence, str], optional): Individual lag values.
            Defaults to None.
                - given 'n' means only the nth. lag.
                - for instance; '5' means: y(t-5)
                - can be given in a Sequence type container like (3, 6, 9, 12) or [3, 6, 9, 12]
                indicating: y(t-3), y(t-6), y(t-9), y(t-12)
                - can be given as a comma separated string like "3, 4" indicating: y(t-3), y(t-4)
            - method (optional, str): Method of correlation computations. Defaults to 'pearson'
                - pearson : standard Pearson correlation coefficients
                - kendall : Kendall Tau correlation coefficients.
                - spearman : Spearman rank correlation coefficients
            - precision (int, optional): precision to be used to truncate floatings.
            Defaults to None.

        Raises:
            - ValueError: If given DataFrame is made up of more than 1 series.
            - ValueError: If neither 'range_lags' not 'lags' is provided.
            - TypeError:  If 'range_lags' is not given as an integer number.

        Returns:
            - pd.DataFrame: Autocorrelations.
        """

        series = Transformator._convert_to_df(series)

        if len(series.columns) < 2:
            raise ValueError(
                    "Provided DataFrame consists of less than 2 series\nPlese provide a "
                    "DataFrame made up of at least 2 series to see corr connections."
                )

        exclude: List[str] = []
        if isinstance(hold, str):
            exclude = [hold.strip()]
            try:
                series[exclude].empty
            except KeyError:
                exclude = [hold.strip().upper()]
                try:
                    series[exclude].empty
                except KeyError:
                    exclude = [hold.strip().lower()]
                    try:
                        series[exclude].empty
                    except KeyError:
                        raise KeyError(f"Given column ({hold}) is not found in DataFrame") from None
        elif isinstance(hold, int):
            try:
                exclude = [series.columns[hold]]
            except IndexError:
                raise IndexError(
                    f"The column index you provide ({hold}) is out of bounds"
                    f"The frame has {len(series.columns) - 1} columns starting from 0"
                ) from None
        else:
            raise TypeError("'hold' must be a real column name or index of the column")

        if not (isinstance(range_lags, int) or range_lags is None):
            raise TypeError("'range_lags' must be an integer number representing the lags 1....n")

        parsed_lags: Tuple[int] = Transformator._parse_parameters(lags)

        if not (range_lags or parsed_lags):
            raise ValueError(
                "At least one of the parameters shuld be provided: 'range_lags' or 'lags'"
            )

        precision = self._decide_precision(precision=precision)
        included: pd.DataFrame = series.copy().loc[:, ~series.columns.isin(exclude)]
        lagged_series: pd.DataFrame = self.laggeds(included, lags=lags, range_lags=range_lags, precision=None)
        dataset: pd.DataFrame = self.join(series[exclude], lagged_series)

        try:
            corr_connect: pd.DataFrame = Transformator.set_precision(
                                            dataset.corr(method=method), precision=precision
                                         ).iloc[:, 0].to_frame()

        except ModuleNotFoundError:
            if method == "kendall":
                raise OptionalPackageRequiredException(
                    "\nCalculating Kendall's Tau requires 'scipy' package to be installed.\n\n"
                    "for pip users: pip install scipy\n\n"
                    "for Anaconda or Miniconda users: conda install scipy\n\n"
                    "In Jupyter Notebook:\n\n"
                    "for pip users (in Jupyter Notebook):\n"
                    "Import sys\n"
                    "!{sys.executable} -m pip install scipy\n\n"
                    "for Anaconda or Miniconda users (in Jupyter Notebook):\n"
                    "Import sys\n"
                    "!conda install --prefix {sys.prefix} scipy"
                ) from None
            raise

        return corr_connect

    def outliers(
                self,
                series: pd.DataFrame,
                method: str = 'mad',
                critical_upper: float = 3.0,
                critical_lower: float = -3.0,
                precision: Optional[int] = None,
                keep_originals: bool = True,
                rename: bool = True
    ) -> pd.DataFrame:

        """Returns dummy series for detected outliers.

        Args:
            - series (pd.DataFrame): DataFrame consists of series to be evaluated.
            - method (str, optional): outliers detection method. Defaults to 'mad'.
                - 'mad': outliers are detected using 'mean absolute deviation' this is the preferred
                method for the series that are not normally distributed since the detection
                algorithm is still robust.
                - 'z': outliers are detected using deviations from 'standard normal distribution'.
                This could be the preferable way for the series which are normally distributed.
            - critical_upper (float, optional): upper critical value for deviations.
            Defaults to 3.0.
            - critical_lower (float, optional): lower critical value for deviations.
            Defaults to -3.0.
            - precision (int, optional): precision to be used for dummies. Defaults to None.
            - keep_originals (bool, optional):  Includes original series in returned DataFrame if
            True
            Defaults to True.
            - rename (bool, optional): renames the column names appropriately. Defaults to True

        Explanation:
            Returned dummy series consist of 0s and 1s indicating:
            - 1: an outlier values is detected in corresponding date.
            - 0: the value is in the bound of expectations.

        Raises:
            - TypeError: If provided method is not a string
            - ValueError: If provided method is not defined
            - TypeError: If upper or lower critical value is not a number.

        Returns:
            - pd.DataFrame: Detected outliers
        """

        defined_methods: List[str] = ['mad', 'z']
        if not isinstance(method, str):
            raise TypeError(f"'method must be a string in {defined_methods}")

        method = method.lower()

        if method not in defined_methods:
            raise ValueError(
                f"given method ({method}) is unknown. 'method' must be in {defined_methods}"
            )
        if not (
            isinstance(critical_lower, (int, float)) and isinstance(critical_upper, (int, float))
           ):
            raise TypeError("'critical_lower' and 'critical_upper' must be both numbers!")

        series = Transformator._convert_to_df(series)
        precision = self._decide_precision(precision=precision)

        if method == "z":
            score: pd.DataFrame = self.z_score(
                series, precision=None, keep_originals=False, rename=False
            )
        elif method == "mad":
            score: pd.DataFrame = self.mad(series, precision=None, keep_originals=False, rename=False)

        outliers_ub: pd.DataFrame = self.dummy(
            score, threshold=critical_upper, condition=">",
            keep_originals=False, rename=False, fill_false=np.nan
        )
        outliers_lb: pd.DataFrame = self.dummy(
            score, threshold=critical_lower, condition="<", keep_originals=False, rename=False
        )
        outliers_: pd.DataFrame = outliers_ub.combine_first(outliers_lb)

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=outliers_, rename=rename, suffix_1="OUT",
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def smooth(
               self,
               series: pd.DataFrame,
               method: str = 'mad',
               critical_upper: float = 3.0,
               critical_lower: float = -3.0,
               smooth_method: str = 'ema',
               smooth_window: int = 2,
               precision: Optional[int] = None,
               keep_originals: bool = True,
               rename: bool = True
    ) -> pd.DataFrame:

        """Returns outliers smoothed series.

        Args:
            - series (pd.DataFrame): DataFreme consists of series to be evaluated.
            - method (str, optional): outliers detection method. Defaults to 'mad'.
                - 'mad': outliers are detected using 'mean absolute deviation' this is the preferred
                method for the series that are not normally distributed since the detection
                algorithm is still robust.
                - 'z': outliers are detected using deviations from 'standard normal distribution'.
                This could be the preferable way for the series which are normally distributed.
            - critical_upper (float, optional): upper critical value for deviations.
            Defaults to 3.0.
            - critical_lower (float, optional): lower critical value for deviations.
            Defaults to -3.0.
            - smooth_method (str, optional): method that is used for smoothing the detected outliers.
            Defaults to 'ema'
                - can be used either 'sma' or 'ema'
            - smooth_window (int, optional): e(ma) window
            (how many values will be used for smoothing) Defaults to 2
            - precision (int, optional): precision to be used for dummies. Defaults to 0.
            - keep_originals (bool, optional):  Includes original series in returned DataFrame if
            True
            Defaults to True.
            - rename (bool, optional): renames the column names appropriately. Defaults to True

        Explanation:
            Returned series consists of:
            - Smoothed Values: For detected outliers.
            - Original Observations: For inbound values.
            - smoothing is done using ema(2)

        Raises:
            - TypeError: If provided method is not a string
            - ValueError: If provided method is not defined
            - TypeError: If upper or lower critical value is not a number.

        Returns:
            - pd.DataFrame: Outliers smoothed series.
        """

        series = Transformator._convert_to_df(series)

        smoothing_methods: List[str] = ['sma', 'ema']

        if not isinstance(smooth_method, str):
            raise TypeError("Smoothing method must be a string: ma or ema?")

        smooth_method = smooth_method.lower()

        if smooth_method not in smoothing_methods:
            raise ValueError(f"{smooth_method} is unknown. Did you mean ma or ema?")

        if not isinstance(smooth_window, int):
            raise TypeError(
                f"Smoothing window must be an integer number. You provided {smooth_window}"
            )

        series_copy = series.copy()

        outliers_ = self.outliers(
            series=series,
            method=method,
            critical_lower=critical_lower,
            critical_upper=critical_upper,
            precision=None,
            keep_originals=False,
            rename=False
        )

        joint: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=outliers_, rename=True, suffix_1="OUTLIERS_INTERNAL",
            precision=None, keep_originals=True
        )

        out_columns: List[str] = (
            joint.columns[joint.columns.str.contains("_OUTLIERS_INTERNAL")].to_list()
        )

        if not out_columns:
            return series

        for col_idx, column in enumerate(out_columns):

            idx = joint[column][joint[column] != 0].index

            if smooth_method == 'ema':
                new_vals = self.ema(
                    series.iloc[:, col_idx], precision=None, keep_originals=False, window=smooth_window
                ).loc[idx]
            elif smooth_method == 'sma':
                new_vals = self.sma(
                    series.iloc[:, col_idx], precision=None, keep_originals=False, window=smooth_window
                ).loc[idx]

            new_vals = new_vals.iloc[:, 0]
            new_vals.name = series.iloc[:, col_idx].name

            series_copy.update(new_vals)

        ready_to_return: pd.DataFrame = Transformator._prepare_for_return(
            original=series, stats=series_copy, rename=rename, suffix_1="SMOOTH",
            precision=precision, keep_originals=keep_originals
        )

        return ready_to_return

    def rename(
               self,
               series: pd.DataFrame,
               names: Union[str, Sequence[str]],
               inplace: bool = False
    ) -> Union[pd.DataFrame, None]:

        """Renames series names in given DataFrame

        Args:
            - series (pd.DataFrame): A DataFrame object consists of series.
            - names (Union[str, Sequence[str]]): New names for series in same order with originals.
                - can be given as comma separated string: "usdtry, eurtry, corr_usdtry, corr_eurtry"
                - can be given as a Tuple: ("usdtry", "eurtry", "corr_usdtry", "corr_eurtry")
                - can be given as a List: ["usdtry", "eurtry", "corr_usdtry", "corr_eurtry"]
            - inplace (bool, optional): Renames the given series instead of creating and returning
            new ones.

        Raises:
            - ValueError: If lenght of given names doesn't match with length of series in DataFrame

        Returns:
             Union[pd.DataFrame, None]: Renamed copy of given DataFrame if 'inplace=False' or None
        """

        names = Transformator._parse_parameters(names, type_=str)
        if len(names) != len(series.columns):
            raise ValueError(
                f"Lenght of given names ({len(names)}) doesn't match with length of series "
                f"({len(series.columns)})"
            )

        if inplace:
            series.columns = names
            return

        verbatim: pd.DataFrame = series.copy()
        verbatim.columns = names

        return verbatim

    def __repr__(self) -> str:

        return (f"\n*{self.__class__.__name__}*:\n\n"
                f"Global Precision: {self.global_precision}\n")
