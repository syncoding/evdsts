"""evdsts Least Squares Modelling Class

A simple least squares linear modelling class aims at using nothing except numpy
(and pandas for representing) with unit root and cointegration testing capabilities.
"""

__author__ = "Burak CELIK"
__copyright__ = "Copyright (c) 2022 Burak CELIK"
__license__ = "MIT"
__version__ = "1.0rc4"
__internal__ = "0.0.1"


import enum
from typing import Dict, List, Tuple, Union, Optional

import numpy as np
from numpy.linalg import LinAlgError
import pandas as pd

from evdsts.configuration.types import FrameLike


class LSELinalg:

    """LS Linear Algebra Calculations Class"""

    @staticmethod
    def _shif_array(arr: np.ndarray, lag: int) -> np.ndarray:

        """Returns the lagged series of given series

        Returns:
            - np.ndarray: Lagged series
        """

        return np.concatenate(([np.nan] * lag, arr[:-lag]))

    @staticmethod
    def _id_variable_matrix(x: np.ndarray, const: bool, trend: bool) -> np.ndarray:

        """Returns independent variable matrix

        Args:
            - x (np.ndarray): independent variable vector
            - const (bool): constant term is included.
            - trend (bool): deterministic trend is included

        Returns:
            - np.ndarray: independent variable matrix
        """

        if const:
            c: np.ndarray = np.ones(len(x))
            x: np.ndarray = np.column_stack([c, x])
        if trend:
            t: np.ndarray = np.arange(0, len(x))
            x: np.ndarray = np.column_stack([x, t])

        return x

    @staticmethod
    def _inverse_xtx(x: np.ndarray) -> np.ndarray:

        """Returns X.T(X)

        Args:
            - x (np.ndarray): independent variable matrix

        Returns:
            - np.ndarray: X.T(X)
        """

        try:
            inv_xtx: np.ndarray = np.linalg.inv(np.dot(x.T, x))
        except LinAlgError:
            print("X'X forms a singular matrix, and therefore not an invertable")
            raise

        return inv_xtx

    @staticmethod
    def _lse_coeffs(y: np.ndarray, x: np.ndarray) -> np.ndarray:

        """Returns least squares estimation coefficients.

        Args:
            - y (np.ndarray): dependent variable vector
            - x (np.ndarray): independent variable matrix

        Returns:
            - np.ndarray: LS equation coefficients
        """

        coeffs: np.ndarray = np.dot(LSELinalg._inverse_xtx(x), np.dot(x.T, y))

        return coeffs

    @staticmethod
    def _forecast(y: np.ndarray, x:np.ndarray, coeffs:np.ndarray) -> np.ndarray:

        """Returns LS forecast series

        Args:
            - y (np.ndarray): dependent variable vector
            - x (np.ndarray): independent variable matrix
            - coeffs (np.ndarray): LS coefficients vector

        Returns:
            - np.ndarray: Forecast series
        """
        forecast: np.ndarray = np.dot(x, coeffs)

        return forecast

    @staticmethod
    def _resids(y: np.ndarray, forecast: np.ndarray) -> np.ndarray:

        """Returns LS forecast residual series

        Args:
            - y (np.ndarray): dependent variable vector
            - forecast (np.ndarray): LS model forecast series

        Returns:
            - np.ndarray: Residual series
        """
        residuals: np.ndarray = y - forecast

        return residuals

    @staticmethod
    def _resid_var(resids: np.ndarray, x: np.ndarray) -> np.floating:

        """Returns variance of residuals

        Args:
            - resids (np.ndarray): residual series
            - x (np.ndarray): independent variable matrix

        Raises:
            - ZeroDivisionError: If degree of freedom equals to 0

        Returns:
            - np.floating: variance of residuals
        """
        n: int = x.shape[0]
        k: int = x.shape[1]
        degree_of_fredom: int = n - k

        if degree_of_fredom == 0:
            raise ZeroDivisionError("Resid Variance: Degree of freedom is 0")

        resid_var: np.floating = (1 / degree_of_fredom) * np.sum(resids ** 2)

        return resid_var

    @staticmethod
    def _beta_varcov_matrix(x: np.ndarray, resids: np.ndarray) -> np.ndarray:

        """Returns Variance-Covariance matrix of the LS model coefficients

        Args:
            - x (np.ndarray): independent variable matrix
            - resids (np.ndarray): residual series

        Returns:
            - np.ndarray: Var-Cov matrix of Beta coefficients
        """
        inv_xtx: np.ndarray = LSELinalg._inverse_xtx(x)
        resid_var: np.floating = LSELinalg._resid_var(resids, x)

        b_var_cov: np.ndarray = resid_var * inv_xtx

        return b_var_cov

    @staticmethod
    def _rss(resids: np.ndarray) -> np.floating:

        """Returns residual sum of squares

        Args:
            - resids (np.ndarray): residual series

        Returns:
            - np.floating: RSS
        """
        rss: np.floating = np.nansum(resids ** 2)

        return rss

    @staticmethod
    def _ess(y:np.ndarray, forecast:np.ndarray) -> np.floating:

        """Returns explained sum of squares

        Args:
            - y (np.ndarray): dependent variable vector
            - forecast (np.ndarray): forecast series

        Returns:
            - np.floating: ESS
        """

        return np.nansum((forecast - np.nanmean(y)) ** 2)

    @staticmethod
    def _tss(y:np.ndarray) -> np.floating:

        """Returns total sum of squares

        Args:
            - y (np.ndarray): dependent variable vector

        Returns:
            - np.floating: TSS
        """

        return np.nansum((y - np.nanmean(y)) ** 2)

    @staticmethod
    def _r2(y: np.ndarray, resids: np.ndarray) -> np.floating:

        """Returns determination coefficient

        Returns:
            - np.floating: R-squarred
        """

        return 1 - np.divide(LSELinalg._rss(resids), LSELinalg._tss(y))

    @staticmethod
    def _adj_r2(y: np.ndarray, x:np.ndarray, resids:np.ndarray) -> np.floating:

        """Returns adjusted determination coefficient

        Args:
            - y (np.ndarray): dependent variable vector
            - x (np.ndarray): independent variable matrix
            - resids (np.ndarray): residual series

        Raises:
            - ValueError: if degree of freedom equals to 0

        Returns:
            - np.floating: adj-R-squarred
        """

        r2: np.floating = LSELinalg._r2(y, resids)

        n: int = x.shape[0]
        k: int = x.shape[1]

        nominator: int = k - 1
        denominator: int = n - k

        if denominator == 0:
            raise ValueError("Adj R2: Degree of freedom is 0")

        return r2 - (1 - r2) * (nominator / denominator)

    @staticmethod
    def _mse(resids: np.ndarray) -> np.floating:

        """Returns mean squarred errors

        Args:
            - resids (np.ndarray): residual series

        Returns:
            - np.floating: MSE
        """

        mse: np.floating = LSELinalg._rss(resids) / len(resids)

        return mse

    @staticmethod
    def _loglikelihood(resids: np.ndarray) -> np.floating:

        """Return the result of log-likelihood function

        Args:
            - resids (np.ndarray): residual series

        Returns:
            - np.floating: LLF(residuals)
        """

        rss: np.floating = LSELinalg._rss(resids)
        n: int = len(resids)
        loglikelihood: np.floating = (
            (-n / 2) * np.log(2 * np.pi) - (n / 2) * np.log(rss / n) - (n / 2)
        )

        return loglikelihood

    @staticmethod
    def _aic(resids: np.ndarray, k: int) -> np.floating:

        """Returns Akaike Information Criterion

        Akaike, H. (1969), "Fitting Autoregressive Models for Prediction". Annals of the
        Institute of Statistical Mathematics, 21, 243-247.

        Args:
            - resids (np.ndarray): residual series
            - k (int): number of LS model parameters

        Returns:
            - np.floating: AIC
        """

        loglikelihood: np.floating = LSELinalg._loglikelihood(resids)
        aic: np.floating = -2 * loglikelihood + 2 * k

        return aic

    @staticmethod
    def _bic(resids: np.floating, k: int) -> np.floating:

        """Returns Schwarz Bayesian Criterion
        Schwarz, G. (1978), "Estimating the Dimension of a Model". Annals of Statistics,
        6, 461-464.

        Args:
            - resids (np.floating): residual series
            - k (int): number of LS model parameters

        Returns:
            - np.floating: BIC
        """

        n: np.floating = len(resids)
        loglikelihood: np.floating = LSELinalg._loglikelihood(resids)
        bic: np.floating = - 2 * loglikelihood + k * np.log(n)

        return bic

    @staticmethod
    def _dw(resids: np.ndarray) -> np.floating:

        """Returns Durbin-Watson Test Stats
        Durbin, J.; Watson, G. S. (1950). "Testing for Serial Correlation in Least Squares Regression,
        I". Biometrika. 37 (3-4): 409-428.

        Args:
            - resids (np.ndarray): residual series

        Returns:
            - np.floating: DW test stats
        """

        dw: np.floating = (
            np.nansum((resids - LSELinalg._shif_array(resids, 1)) ** 2) / np.nansum(resids ** 2)
        )

        return dw

    @staticmethod
    def _beta_variances(var_cov_matrix: np.ndarray) -> np.ndarray:

        """Variances of LS Model Beta coefficients

        Args:
            - var_cov_matrix (np.ndarray): Variance-Covariance Matrix of Beta coefficients

        Returns:
            - np.ndarray: _description_
        """

        return var_cov_matrix.diagonal()

    @staticmethod
    def _beta_standard_errors(var_cov_matrix: np.ndarray) -> np.ndarray:

        """Standard errors of Beta coefficients

        Args:
            - var_cov_matrix (np.ndarray): Variance-Covariance Matrix of LS Model Beta coefficients

        Returns:
            - np.ndarray: Beta Standard Errors
        """

        return np.sqrt(LSELinalg._beta_variances(var_cov_matrix))

    @staticmethod
    def _t_stats(coeffs: np.ndarray, standard_errors: np.ndarray) -> np.ndarray:

        """t stats of LS model Beta coefficients

        Args:
            - coeffs (np.ndarray): LS Model Beta coefficients vector
            - standard_errors (np.ndarray): Standard errors of Beta vector

        Returns:
            - np.ndarray: _description_
        """

        return np.divide(coeffs, standard_errors)

    @staticmethod
    def _variable_matrixes(
                           series: pd.DataFrame,
                           y: Union[str, int]
    ) -> Tuple[np.ndarray, np.ndarray]:

        """Returns dependent variable vector and independent variable matrix

        Args:
            - series (pd.DataFrame): series to be splitted
            - y (Union[str, int]): dependent variable. Can be given as
                - Column name of the dependent variable in DataFrame
                - Column index (starting from 0) of dependent variable in DataFrame

        Raises:
            - KeyError: If given column name for dependent variable is not in DataFrame
            - IndexError: If given column index for dependent variable is out of bounds
            - TypeError: If wrong type is given for deternmining dependent variable

        Returns:
            - Tuple[np.ndarray, np.ndarray]: dependent variable vector and independent variable matrix
        """

        if isinstance(y, str):
            try:
                x: np.ndarray = series.drop(columns=y).to_numpy()
                y: np.ndarray = series.loc[:, series.columns == y].to_numpy()[:, 0]
            except KeyError:
                raise KeyError(f"Given column ({y}) is not in DataFrame!") from None
        elif isinstance(y, int):
            try:
                x = series.drop(columns=series.columns[y]).to_numpy()
                y = series.iloc[:, y].to_numpy()
            except IndexError:
                raise IndexError(f"Given column index ({y}) is out of bounds!") from None
        else:
            raise TypeError(
                "Dependent variable y must be given by either the name of the column or column index"
            )

        return y, x

    @staticmethod
    def _model_repr(series: pd.DataFrame, y: Union[str, int], const: bool, trend: bool) -> str:

        """Returns string representation of created LS model

        Args:
            - series (pd.DataFrame): DataFrame object includes dependent and independent variables
            - y (Union[str, int]): dependent variable name or index
                - Column name of the dependent variable in DataFrame
                - Column index (starting from 0) of dependent variable in DataFrame
            - const (bool): model includes constant term
            - trend (bool): model includes deterministic trend

        Raises:
            TypeError: If wrong type is given for deternmining dependent variable

        Returns:
            str: string representation of created model
        """

        model: List[str] = []

        if isinstance(y, str):
            x: pd.DataFrame = series.drop(columns=y)
            y: pd.DataFrame = series.loc[:, series.columns == y]
            if isinstance(x, pd.Series):
                x = x.to_frame()
            if isinstance(y, pd.Series):
                y = y.to_frame()
        elif isinstance(y, int):
            x = series.drop(columns=series.columns[y])
            y = series.iloc[:, y]
            if isinstance(x, pd.Series):
                x = x.to_frame()
            if isinstance(y, pd.Series):
                y = y.to_frame()
        else:
            raise TypeError(
                "Dependent variable y must be given by either the name of the column or column index"
            )

        model.append(f"{y.columns[0]} = ")

        if const:
            model.append("B0")
        for idx, independent in enumerate(x.columns, start=1):
            model.append(f"B{idx}*{independent}")
        if trend:
            model.append(f"B{len(x.columns) + 1}*Trend")

        str_model: str = model[0] + ' + '.join(param for i, param in enumerate(model) if i > 0)

        return str_model


class TestType(enum.IntEnum):

    """An enumeration class determines the type of the test requested"""

    ADF = 0


class TestResult:

    """A test result class returns from different kinds of tests"""

    def __init__(self, stats: np.floating, critical: float, result: bool) -> None:

        self.stats: np.floating = stats
        self.critical: float = critical
        self.result: bool = result

    def __str__(self) -> str:

        return (
            f"Test Stats: {self.stats}, Critical Value: {self.critical}, H0 Rejected: {self.result}"
        )


class Evaluator:

    """Test evalutor class"""

    adf_tau: Dict[str, Dict[int, List[float]]] = {

        "NCNT": {
                #    n     0.01    0.025   0.05     0.1
                    25:  [-2.661, -2.273, -1.955, -1.609],
                    50:  [-2.612, -2.246, -1.947, -1.612],
                    100: [-2.588, -2.234, -1.944, -1.614],
                    250: [-2.575, -2.227, -1.942, -1.616],
                    500: [-2.570, -2.224, -1.942, -1.616],
                    501: [-2.567, -2.223, -1.942, -1.616]
        },

        "CNT": {
                #    n     0.01    0.025   0.05     0.1
                    25:  [-3.724, -3.318, -2.986, -2.633],
                    50:  [-3.568, -3.213, -2.921, -2.599],
                    100: [-3.498, -3.164, -2.891, -2.582],
                    250: [-3.457, -3.136, -2.873, -2.573],
                    500: [-3.443, -3.127, -2.867, -2.570],
                    501: [-3.434, -3.120, -2.863, -2.568]
        },

        "CT": {
                #    n     0.01    0.025   0.05     0.1
                    25:  [-4.375, -3.943, -3.589, -3.238],
                    50:  [-4.152, -3.791, -3.495, -3.181],
                    100: [-4.052, -3.722, -3.452, -3.153],
                    250: [-3.995, -3.683, -3.427, -3.137],
                    500: [-3.977, -3.670, -3.419, -3.132],
                    501: [-3.963, -3.660, -3.413, -3.128]
        },

    }

    def evaluate(
                 self,
                 stats: float,
                 test_type: TestType,
                 n: int,
                 alpha: float,
                 const: bool = False,
                 trend:bool = False
    ) ->TestResult:
        """Evaluates the result as per related test critical value and returns a TestResult object

        Args:
            - stats (float): Calculated statistic for test made
            - test_type (TestType): Type of the test
            - n (int): Sample size
            - alpha (float): Significance level
            - const (bool, optional): Test equation includes constant term. Defaults to False.
            - trend (bool, optional): Test equation includes deterministic trend. Defaults to False.

        Raises:
            - ValueError: If alpha significance level is not determined.

        Returns:
            - TestResult: Result of the evaluation
        """

        defined_sig_levels: List[str] = ["0.01", "0.025", "0.05", "0.1"]

        if str(alpha) not in defined_sig_levels:
            raise ValueError(
                f"Significance level alpha {alpha} is not defined.\n"
                f"Choose one in {defined_sig_levels}"
            )

        sig_index: int = defined_sig_levels.index(str(alpha))
        n_index: int = 0

        if n < 25:
            n_index = 25
        elif 25 <= n < 50:
            n_index = 50
        elif 50 <= n < 100:
            n_index = 100
        elif 100 <= n < 250:
            n_index = 250
        elif 250 <= n < 500:
            n_index = 500
        elif n > 500:
            n_index = 501

        critical: float = 0

        if test_type == TestType.ADF:

            if const and trend:
                critical = self.adf_tau["CT"][n_index][sig_index]
            elif not trend and const:
                critical = self.adf_tau["CNT"][n_index][sig_index]
            elif not (trend or const):
                critical = self.adf_tau["NCNT"][n_index][sig_index]
            else:
                critical = self.adf_tau["CT"][n_index][sig_index]

            if stats < critical:
                return TestResult(stats=stats, critical=critical, result=True)

            return TestResult(stats=stats, critical=critical, result=False)


class LSEModelResults:

    """Least Squares Model Result Class"""

    def __init__(
                 self,
                 model:str,
                 y: np.ndarray,
                 x: np.ndarray,
                 coeffs: np.ndarray,
                 standard_errors: np.ndarray,
                 t_stats: np.ndarray,
                 forecast: np.ndarray,
                 resids: np.ndarray,
                 r2: np.floating,
                 adj_r2: np.floating,
                 aic: np.floating,
                 bic: np.floating,
                 mse: np.floating,
                 rss: np.floating,
                 ess: np.floating,
                 tss: np.floating,
                 dw: np.floating,
                 n: int,
                 k: int,
                 dof: int,
                 const: bool,
                 trend: bool
    ) -> None:

        self.model: str = model
        self.y: np.ndarray = y
        self.x: np.ndarray = x
        self.coeffs: np.ndarray = coeffs
        self.standard_errors: np.ndarray = standard_errors
        self.t_stats: np.ndarray = t_stats
        self.forecast: np.ndarray = forecast
        self.resids: np.ndarray = resids
        self.r2: np.floating = r2
        self.adj_r2: np.floating = adj_r2
        self.aic: np.floating = aic
        self.bic: np.floating = bic
        self.mse: np.floating = mse
        self.rss: np.floating = rss
        self.ess: np.floating = ess
        self.tss: np.floating = tss
        self.dw: np.floating = dw
        self.n: int = n
        self.k: int = k
        self.dof: int = dof
        self.const: bool = const
        self.trend: bool = trend

    def show_model(self, title: str = "LS Model") -> None:

        """Shows the model parameters and other stats

        Args:
            title (str, optional): Title of the table. Defaults to "LS Model".
        """

        print("{:^70}".format(f"{title}"))
        print("-" * 70)
        print(f"model: {self.model} (n = {self.n})")
        print("-" * 70)

        print("{:10} {:10} {:10} {:10} {:20}".format(
            "Parameter", "Coeff", "Std.Error", "t-Stats", f"CI (Z alpha = 0.01)")
        )
        print("-" * 70)

        for idx, (coeff, std_error, t_stat) in enumerate(zip(self.coeffs, self.standard_errors, self.t_stats)):
            par: str =  f"B{idx}" if self.const else f"B{idx + 1}"
            cff: str = str(round(coeff, 5))
            stderr: str = str(round(std_error, 5))
            tstat: str = str(round(t_stat, 5))
            ci: str = f"{round(coeff - 2.576 * std_error, 3)} < {par} < {round(coeff + 2.576 * std_error, 3)}"

            print(
                  "{:10.10} {:10.10} {:10.10} {:10.10} {:20.20}".format(
                                                               par, cff, stderr, tstat, ci
                  )
            )

        print("-" * 70)
        print(f"r-squarred: {self.r2:5f}, adj.r-squarred: {self.adj_r2:5f}, mse: {self.mse:5f}")
        print(f"aic: {self.aic: 5f},      bic: {self.bic: 5f},          d.f.: {self.dof}")
        print(f"dw: {self.dw: 5f}")
        print("-" * 70)



class LSModeller:

    """Least Square Modeller Class"""

    @staticmethod
    def _convert_to_df(series: FrameLike) -> pd.DataFrame:

        """Converts compatible types intp pandas DataFrame

        Args:
            series (FrameLike): Data provided.

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

    def __init__(self, data: Optional[FrameLike] = None):

        self.data: FrameLike = data

    def _extract_y(self, series: pd.DataFrame, test: Union[str, int]) -> pd.DataFrame:

        """Extracts a series as dependent variable vector by given series name or column index

        Args:
            - series (pd.DataFrame): DataFrame mades up of dependent and independent variables
            - test (Union[str, int]): series to be extracted.
                - Column name of the dependent variable in DataFrame
                - Column index (starting from 0) of dependent variable in DataFrame

        Raises:
            - KeyError: If given column name for dependent variable is not in DataFrame
            - IndexError: If given column index for dependent variable is out of bounds
            - TypeError: If wrong type is given for deternmining dependent variable

        Returns:
            - pd.DataFrame: _description_
        """

        if isinstance(test, str):
            try:
                y: pd.DataFrame = series.loc[:, series.columns == test]
            except KeyError:
                raise KeyError(f"Given column ({test}) is not in DataFrame!") from None
        elif isinstance(test, int):
            try:
                y = series.iloc[:, test].to_frame()
            except IndexError:
                raise IndexError(f"Given column index ({test}) is out of bounds!") from None
        else:
            raise TypeError(
                "test variable must be given by either the name of the column or column index"
            )

        return y

    def _get_data(self, dataset: FrameLike) -> pd.DataFrame:

        """Creates data sets from given source

        Args:
            - dataset (FrameLike): A FrameLike object

        Raises:
            - ValueError: IF a bad data source is provided

        Returns:
            - pd.DataFrame: dataset
        """

        if dataset is None:
            if self.data is not None:
                series: pd.DataFrame = LSModeller._convert_to_df(self.data)
            else:
                raise ValueError("LSEstimator needs a data source to give results")
        else:
            series = LSModeller._convert_to_df(dataset)

        return series

    def model(
              self,
              dependent: Union[str, int] = 0,
              const: bool = True,
              trend: bool = False,
              show_results: bool = False,
              dataset: Optional[FrameLike] = None
    ) -> LSEModelResults:

        """Models a Least Square Estimation Equation and calculates related stats and series

        Args:
            - dependent (Union[str, int], optional): Dependent variable. Defaults to 0.
                - Column name of the dependent variable in DataFrame
                - Column index (starting from 0) of dependent variable in DataFrame
            - const (bool, optional): Model includes constant term. Defaults to True.
            - trend (bool, optional): Model includes deterministic trend. Defaults to False.
            - show_results (bool, optional): Gives model output. Defaults to False.
            - dataset (Optional[FrameLike], optional): An external data source. Defaults to None.

        Raises:
            - ValueError: If no data is provided for modelling
            - ValueError: If provided data is insufficient

        Returns:
            - LSEModelResults: Result of the model
        """

        series: pd.DataFrame = self._get_data(dataset)

        if len(series) < 2:
            raise ValueError("LSEstimator needs a data set made up of at leats 2 variables!")

        series = series.iloc[::].dropna(how='any')

        y, x = LSELinalg._variable_matrixes(series=series, y=dependent)
        x: np.ndarray = LSELinalg._id_variable_matrix(x=x, const=const, trend=trend)

        n: int = len(y)
        k: int = x.shape[1]
        dof: int = len(y) - x.shape[1]

        # for ADF test returns
        if dof <= 0:
            if dataset is not None:
                return None

        coeffs: np.ndarray = LSELinalg._lse_coeffs(y=y, x=x)
        forecast: np.ndarray = LSELinalg._forecast(y=y, x=x, coeffs=coeffs)
        resids: np.ndarray = LSELinalg._resids(y=y, forecast=forecast)
        beta_var_cov: np.ndarray = LSELinalg._beta_varcov_matrix(x=x, resids=resids)
        standard_errors: np.ndarray = LSELinalg._beta_standard_errors(var_cov_matrix=beta_var_cov)

        rss: np.floating = LSELinalg._rss(resids=resids)
        ess: np.floating = LSELinalg._ess(y=y, forecast=forecast)
        tss: np.floating = LSELinalg._tss(y=y)
        t_stats: np.ndarray = LSELinalg._t_stats(coeffs=coeffs, standard_errors=standard_errors)

        r2: np.floating = LSELinalg._r2(y=y, resids=resids)
        adj_r2: np.floating = LSELinalg._adj_r2(y=y, x=x, resids=resids)
        dw: np.floating = LSELinalg._dw(resids=resids)
        mse: np.floating = LSELinalg._mse(resids=resids)
        aic: np.floating = LSELinalg._aic(resids=resids, k=k)
        bic: np.floating = LSELinalg._bic(resids=resids, k=k)

        model_repr: str = LSELinalg._model_repr(
            series=series, y=dependent, const=const, trend=trend
        )

        ls_result: LSEModelResults = LSEModelResults(
                                                     model=model_repr,
                                                     y=y,
                                                     x=x,
                                                     coeffs=coeffs,
                                                     standard_errors=standard_errors,
                                                     t_stats=t_stats,
                                                     forecast=forecast,
                                                     resids=resids,
                                                     r2=r2,
                                                     adj_r2=adj_r2,
                                                     aic=aic,
                                                     bic=bic,
                                                     mse=mse,
                                                     rss=rss,
                                                     ess=ess,
                                                     tss=tss,
                                                     dw=dw,
                                                     n=n,
                                                     k=k,
                                                     dof=dof,
                                                     const=const,
                                                     trend=trend
        )

        if show_results:
            ls_result.show_model()

        return ls_result

    def adf_test(
                 self,
                 test: Union[str, int] = 0,
                 const: bool = True,
                 trend: bool = False,
                 lag_criterion: str = "bic",
                 max_lag: int = 2,
                 alpha: float = "0.05",
                 show_results: bool = True,
                 dataset: Optional[FrameLike] = None
    ) -> TestResult:

        """Returns Augmented Dickey-Fuller Test Result

        Dickey, D. A., & Fuller, W. A. (1979). "Distribution of the estimators for autoregressive
        time series with a unit root.", Journal of the American Statistical Association, 74(366a),
        427-431.

        Args:
            - test (Union[str, int], optional): Series to be tested. Defaults to 0.
                - Column name of the dependent variable in DataFrame
                - Column index (starting from 0) of dependent variable in DataFrame
            - const (bool, optional): Model includes constant term. Defaults to True.
            - trend (bool, optional): Model includes deterministic trend. Defaults to False.
            - lag_criterion (str, optional): Lag determination criterion for A-DF process.
            Defaults to "bic". Can be given as one of below;
                - "aic": Akaike Information Criterion
                - "bic": Schwars Bayesian Information Criterion
            - max_lag (int, optional): Maximum lag for A-DF process. Defaults to 2.
            - alpha (float, optional): Significance level for hypothesis test. Defaults to "0.05".
            - show_results (bool, optional): Shows test result. Defaults to True.
            - dataset (Optional[FrameLike], optional): An external data source. Defaults to None.

        Raises:
            - ValueError: If given lag criterion is not defined

        Returns:
            - TestResult: Test result
        """

        defined_criteria: List[str] = ["aic", "bic"]

        series: pd.DataFrame = self._get_data(dataset)

        if str(lag_criterion).lower() not in defined_criteria:
            raise ValueError(
                f"{lag_criterion} is not a defined lag criterion. Select one of {defined_criteria}"
            )

        y: pd.DataFrame = self._extract_y(series=series, test=test)

        series_name: str = y.columns[0]
        dy: pd.DataFrame = y - y.shift(1)
        dy.columns = [f"D({series_name})"]
        yt1: pd.DataFrame = y.shift(1)

        base: pd.DataFrame = pd.concat([dy, yt1], axis=1)
        base.columns = [f"D({series_name})", f"{series_name}(t-1)"]

        results: List[LSEModelResults] = []

        # test for base (DF) model
        results.append(self.model(dataset=base, dependent=0, const=const, trend=trend))

        # ADF
        for i in range(1, max_lag + 1):

            lag_set: pd.DataFrame = pd.DataFrame()

            for k in range(1, i + 1):
                lag_set[f"D({series_name}(t-{k}))"] = dy.shift(k)

            test_set: pd.DataFrame = pd.concat([base, lag_set], axis=1)

            results.append(self.model(dataset=test_set, dependent=0, const=const, trend=trend))

        results: List[LSEModelResults] = list(filter(None, results))

        if lag_criterion == "aic":
            sorted_models: List[LSEModelResults] = sorted(results, key=lambda result: result.aic)
            best_model: LSEModelResults = sorted_models[0]
            if show_results:
                best_model.show_model()
        elif lag_criterion == "bic":
            sorted_models: List[LSEModelResults] = sorted(results, key=lambda result: result.bic)
            best_model: LSEModelResults = sorted_models[0]
            if show_results:
                best_model.show_model()

        n: int = best_model.n

        # B1
        tau: np.floating = best_model.t_stats[1] if const else best_model.t_stats[0]

        evaluator: Evaluator = Evaluator()

        test_result: TestResult = evaluator.evaluate(
            test_type=TestType.ADF, stats=tau, alpha=alpha, n=n, const=const, trend=trend
        )

        if show_results:
            print(f"tau = {round(test_result.stats, 5)}, critical value = {test_result.critical}")
            if test_result.result:
                print(f"{series_name} is STATIONARY")
            else:
                print(f"{series_name} is NON-STATIONARY")

        return test_result

    def coint_test(
                   self,
                   dependent: Union[str, int] = 0,
                   ensure_integration = False,
                   const: bool = True,
                   trend: bool = False,
                   lag_criterion: str = "bic",
                   max_lag: int = 2,
                   alpha: float = "0.05",
                   show_results: bool = True,
                   dataset: Optional[FrameLike] = None
    ) -> TestResult:
        """Engle-Granger Cointegration Test for given model

        Engle, R. and Granger, C. (1987) "Cointegration and Error Correction: Representation,
        Estimation and Testing.", Econometrica, 55, 251-276.

        Args:
            - dependent (Union[str, int], optional): Dependent variable. Defaults to 0.
                - Column name of the dependent variable in DataFrame
                - Column index (starting from 0) of dependent variable in DataFrame
            ensure_integration (bool, optional): Check for individual integration levels.
            Defaults to False.
            - const (bool, optional): Model includes constant term. Defaults to True.
            - trend (bool, optional): Model includes deterministic trend. Defaults to False.
            - lag_criterion (str, optional): Lag determination criterion for A-DF process.
            Defaults to "bic". Can be given as one of below;
                - "aic": Akaike Information Criterion
                - "bic": Schwars Bayesian Information Criterion
            - max_lag (int, optional): Maximum lag for A-DF process. Defaults to 2.
            - alpha (float, optional): Significance level for hypothesis test. Defaults to "0.05".
            - show_results (bool, optional): Shows test result. Defaults to True.
            - dataset (Optional[FrameLike], optional): An external data source. Defaults to None.

        Raises:
            - ValueError: If given lag criterion is not defined

        Returns:
            - TestResult: Cointegration test result
        """

        defined_criteria: List[str] = ["aic", "bic"]

        series: pd.DataFrame = self._get_data(dataset)

        if str(lag_criterion).lower() not in defined_criteria:
            raise ValueError(
                f"{lag_criterion} is not a defined lag criterion. Select one of {defined_criteria}"
            )

        if ensure_integration:
            integration_results: List[TestResult] = []

            for i in range(len(series.columns)):
                integration_results.append(
                    self.adf_test(
                        test=i, const=const, trend=trend, lag_criterion=lag_criterion,
                        max_lag=max_lag, alpha=alpha, show_results=False
                    )
                )

            check_unit_roots: bool = any(test.result for test in integration_results)
            check_levels: bool = all(test.result for test in integration_results)

            if check_unit_roots or check_levels:
                if check_unit_roots:
                    print("One of given series is already stationary. Check the results below.")
                if check_levels:
                    print("All given series are already stationary. Check the results below.")

                for idx, col_name in enumerate(series.columns):
                    print(f"{col_name}: {integration_results[idx]}")

                return

        series_names = ", ".join(name for name in series.columns)

        coint_eq: LSEModelResults = self.model(
            dependent=dependent, const=const, trend=trend, show_results=False
        )

        resids: np.ndarray = coint_eq.resids
        resid_series: pd.DataFrame = pd.DataFrame(resids)
        resid_series.columns = ["CI_ERRORS"]

        test_result: TestResult = self.adf_test(
            dataset=resid_series, test=0, const=True, trend=False, lag_criterion=lag_criterion,
            max_lag=max_lag, alpha=alpha, show_results=show_results
        )

        if show_results:
            if test_result.result:
                print(f"{series_names} series are CO-INTEGRATED as per given model")
            else:
                print(f"{series_names} series are NOT CO-INTEGRATED as per given model")

        return test_result

