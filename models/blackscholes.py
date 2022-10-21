"""
Black-Scholes-Merton pricing class
"""

import numpy as np
from scipy.stats import norm
import pandas as pd

class BSOpt:
    def __init__(self, CP, S, K, T, r, v, q = 0):

        """BSM Class option

        Args:
            CP: Call or Put
            S : Underlyings Price
            K : Strike Price
            r : risk-free interest rate
            T : time-to-maturity (years)
            v : implied volatility, IV
            q : dividend yield
        """
        self.CP = BSOpt.valid_option(CP)
        self.S  = BSOpt.valid_underlying(S)
        self.K  = BSOpt.valid_strike(K)
        self.T  = BSOpt.valid_maturity(T)
        self.r  = BSOpt.valid_intrate(r)
        self.v  = BSOpt.valid_volatility(v)
        self.q  = BSOpt.valid_yield(q)

    @staticmethod
    def valid_option(CP):
        if CP in ["C", "P"]:
            return CP
        else:
            raise ValueError("First class argument 'CP' must be either 'C' or 'P'")

    @staticmethod
    def valid_underlying(K):
        if K > 0:
            return K
        else:
            raise ValueError("Third argument 'K' (strike price) must be greater than 0")

    @staticmethod
    def valid_maturity(T):
        if T >= 0:
            return T
        else:
            raise ValueError("Fourth argument 'T' (maturity) cant be negative")

    @staticmethod
    def valid_intrate(r):
        if r >= 0:
            return r
        else:
            raise ValueError("Fifth argument 'r' (interest rate) cannot be negative")

    @staticmethod
    def valid_maturity(v):
        if v>= 0:
            return v
        else:
            raise ValueError("Sixth argument 'v' (IV, volatility) cant be negative")

    @staticmethod
    def valid_intrate(q):
        if q >= 0:
            return q
        else:
            raise ValueError("Seventh argument 'q' (divvie yield) cannot be negative")

    @property
    def params(self):
        """
        Returns all input option params
        """
        return {
            "type": self.CP,
            "S"   : self.S,
            "K"   : self.K,
            "T"   : self.T,
            "r"   : self.r,
            "v"   : self.v,
            "q"   : self.q}

    @staticmethod
    def N(x, cum = 1):
        """
        Standard Normal CDF (or PDF) evaluated at the input point x.
        """
        if cum:
            # returns standard normal CDF
            return norm.cdf(x, loc = 0, scale = 1)
        else:
            # returns standard normal PDF
            return norm.pdf(x, loc = 0, scale = 1)

    def d1(self):
        return (np.log(self.S/self.K) + (self.r - self.q + 0.5 * self.v**2)*self.T) / (self.v * np.sqrt(self.T))

    def d2(self):
        return self.d1() - self.v * np.sqrt(self.T)

    def price(self):
        if self.CP == 'CP':
            # Call option
            if self.T > 0:
                return + self.S * np.exp(-self.q * self.T) * self.N(self.d1())  \
                       - self.K * np.exp(-self.r * self.T) * self.N(self.d2())

            else:
                # The call has expired
                return max(self.S - self.K, 0)
        else:
            # the put option
            if self.T > 0:
                return - self.S * np.exp(-self.q * self.T) * self.N(-self.d1())  \
                       + self.K * np.exp(-self.r * self.T) * self.N(-self.d2())
            else:
                return max(self.K - self.S, 0)


    def delta(self):
        """
        BSM delta
        """
        if self.CP == 'C':
            if self.T > 0:
                return np.exp(-self.q*self.T) * self.N(self.d1())
            else:
                if self.price() > 0:
                    return +1
                else:
                    return 0
        else:
            if self.T > 0:
                return np.exp(-self.q*self.T) * self.N(self.d1()) - 1
            else:
                if self.price() > 0:
                    return -1
                else:
                    return 0

    def Lambda(self):
        """
        BSM Lambda
        """
        if self.CP == "C":
            # Call opt
            if self.delta() < 1e-10 or self.price() < 1e-10:
                return +np.inf
            else:
                return self.delta() * self.S / self.price()
        else:
            # Put opt
            if self.delta() > -1e-10 or self.price() < 1e-10:
                return -np.inf
            else:
                return self.delta() * self.S / self.price()

    def gamma(self):
        """
        BSM Gamma
        Gamma is the same for both calls and puts
        """
        if self.T > 0:
            # opt hasnt expired yet
            return +np.exp(-self.q*self.T) * self.N(self.d1(), cum = 0) / (self.S * self.v * np.sqrt(self.T))
        else:
            # opt has expired
            return 0

    def theta(self):
        if self.CP == "C":
            # call opt
            if self.T > 0:
                # call hasnt exired yet
                return - np.exp(-self.q*self.T) * self.S * self.v * self.N(self.d1(), cum = 0) / (2*np.sqrt(self.T)) \
                       + self.q * np.exp(-self.q*self.T) * self.S * self.N(self.d1())  \
                       - self.r * np.exp(-self.r*self.T) * self.K * self.N(self.d2())

            else:
                # call expired
                return 0
        else:
            # put opt
            if self.T > 0:
                # put hasnt expired yet
                return - np.exp(-self.q * self.T) * self.S * self.v * self.N(self.d1(), cum = 0) / (2*np.sqrt(self.T)) \
                    - self.q*np.exp(-self.q*self.T) * self.S * (1 - self.N(self.d1())) \
                    + self.r*np.exp(-self.r*self.T) * self.K * (1 - self.N(self.d2()))
            else:
                # put expired
                return 0

    def vega(self):
        if self.T > 0:
            return + np.exp(-self.q*self.T) * self.S * np.sqrt(self.T) * self.N(self.d1(), cum = 0)
        else:
            return 0
