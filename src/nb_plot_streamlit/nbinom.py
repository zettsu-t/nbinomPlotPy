"""
A statefull negative binomial distribution
"""

from typing import Tuple
import numpy as np
import pandas as pd
from scipy.stats import nbinom


class NbinomDist:
    """A negative binomial distribution"""

    initial_size: float = 1.0  # overwritten in initialization
    initial_prob: float = 0.5  # overwritten in initialization
    size: float = 1.0  # the size parameter
    prob: float = 0.5  # the prob parameter
    mu: float = 1.0    # derived from the size and prob parameter
    quantile: str = "0.99"  # passed by the UI
    max_x_plus_one: float = 1  # n for a range [0, n) as Xs

    def __init__(self, initial_values: dict):
        """
        Initialize

        :type initial_values: dict
        :param initial_values: an initial value set to reset
        """

        self.initial_size = initial_values["initial_size"]
        self.initial_prob = initial_values["initial_prob"]
        self.reset()

    def _update(self):
        """Update private variables consistent"""

        self.mu = self.size * (1 - self.prob) / self.prob
        x_value: int = 0
        accum: float = 0.0
        quantile: float = float(self.quantile)

        while accum < quantile:
            accum = accum + nbinom.pmf(x_value, self.size, self.prob)
            x_value = x_value + 1
        self.max_x_plus_one = x_value

    def _set_quantile(self, quantile: str):
        """
        Update the quantile if the argument is acceptable

        :type quantile: str
        :param quantile: a quantile value in (0.0, 1.0)
        """

        try:
            value = float(quantile)
            if 0.0 < value < 1.0:
                self.quantile = quantile
                self._update()
        except ValueError:
            pass

    def reset(self):
        """Reinitialize private variables"""

        self.size = self.initial_size
        self.prob = self.initial_prob
        self._update()

    def update_size_prob(self, size: float, prob: float):
        """
        Update the size and prob parameters and calculate the mu parameter

        :type size: float
        :param size: the size parameter of a negative binomial distribution

        :type prob: float
        :param prob: the prob parameter of a negative binomial distribution
        """

        self.size = size
        self.prob = prob
        self._update()

    def update_mu_prob(self, mu: float, prob: float):
        """
        Update the mu and prob parameters and calculate the size parameter

        :type mu: float
        :param mu: the size parameter of a negative binomial distribution

        :type prob: float
        :param prob: the prob parameter of a negative binomial distribution
        """

        self.mu = mu
        self.prob = prob
        self.size = self.mu * self.prob / (1 - self.prob)
        self._update()

    def set_quantile(self, quantile: str):
        """
        Set the upper bound quantile parameter

        :type quantile: str
        :param quantile: a quantile value in (0.0, 1.0)
        """

        self._set_quantile(quantile=quantile)

    def get_max_x_plus_one(self) -> float:
        """
        Get the upper bound x for the quantile parameter.

        :rtype: float
        :return: Returns the upper bound plus one to make a range [0, bound).
        """

        return self.max_x_plus_one

    def get_size(self) -> float:
        """
        Get the size parameter

        :rtype: float
        :return: Returns the size parameter
        """

        return self.size

    def get_prob(self) -> float:
        """
        Get the prob parameter

        :rtype: float
        :return: Returns the prob parameter
        """

        return self.prob

    def get_mu(self) -> float:
        """
        Get the mu parameter

        :rtype: float
        :return: Returns the mu parameter
        """

        return self.mu

    def get_quantile(self) -> str:
        """
        Get the quantile parameter

        :rtype: str
        :return: Returns the quantile parameter
        """

        return self.quantile

    def _get_raw_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate [0, bound) and their probability

        :rtype: Tuple[np.ndarray, np.ndarray]
        :return: Returns a pair of xs and their probability
        """

        xs: np.ndarray = np.arange(0, int(np.ceil(self.max_x_plus_one)), 1)
        ys: np.ndarray = nbinom.pmf(xs, self.size, self.prob)
        return xs, ys

    def get_df(self) -> bytes:
        """
        Make a CSV table [0, bound) and their probability to write a file

        :rtype: bytes
        :return: Returns a CSV table as a file-writable byte sequence
        """

        xs, ys = self._get_raw_data()
        mat: np.ndarray = np.array([xs, ys]).T
        df: pd.DataFrame = pd.DataFrame(data=mat, columns=["x", "density"])
        return df.to_csv(index=False).encode("utf-8")

    def get_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make a CSV table [0, bound) and their probability to write a file

        :rtype: Tuple[np.ndarray, np.ndarray]
        :return: Returns a pair of xs and their probability
        """

        return self._get_raw_data()
