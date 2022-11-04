import pandas as pd
import numpy as np
from scipy.stats import norm

class BSOpt:
    """BSOpt."""


    def __init__(self, CP, S, K, T, r, v, q = 0):
        """__init__.

        :param CP:
        :param S:
        :param K:
        :param T:
        :param r:
        :param v:
        :param q:
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
        """
        CP: Validate input option type

        Returns:
            string: Call or Put
        """
        if CP in ["C", "P"]:
            return CP
        else:
            raise ValueError("First class argument 'CP' must be either 'C' or 'P'")

    @staticmethod
    def valid_underlying(S):
        """
        Validate input underlying price
        """
        if S > 0:
            return S
        else:
            raise ValueError("Second class argument 'S' (strike price) must be greater than 0")

    @staticmethod
    def valid_strike(K):
        """
        Validate input strike price
        """
        if K > 0:
            return K
        else:
            raise ValueError("Third argument 'K' (strike price) must be greater than 0")

    @staticmethod
    def valid_maturity(T):
        """
        Validate input maturity
        """
        if T >= 0:
            return T
        else:
            raise ValueError("Fourth argument 'T' (maturity) cant be negative")

    @staticmethod
    def valid_intrate(r):
        """
        Validate input interest rate
        """
        if r >= 0:
            return r
        else:
            raise ValueError("Fifth argument 'r' (interest rate) cannot be negative")

    @staticmethod
    def valid_volatility(v):
        """
        Validate input implied volatility
        """
        if v >= 0:
            return v
        else:
            raise ValueError("Sixth argument 'v' (IV, volatility) cant be negative")

    @staticmethod
    def valid_yield(q):
        """
        Validate input divvie yield
        """
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
            "S": self.S,
            "K": self.K,
            "T": self.T,
            "r": self.r,
            "v": self.v,
            "q": self.q,
        }

    @staticmethod
    def N(x, cum=1):
        """
        Standard Normal CDF (or PDF) evaluated at the input point x.
        """
        if cum:
            # returns standard normal CDF
            return norm.cdf(x, loc=0, scale=1)
        else:
            # returns standard normal PDF
            return norm.pdf(x, loc=0, scale=1)

    def d1(self, S):
        """
        Compute the quantity d1 of BSM options pricing
        """
        return (
            np.log(self.S / self.K) + (self.r - self.q + 0.5 * self.v**2) * self.T
        ) / (self.v * np.sqrt(self.T))

    def d2(self, S):
        """
        Compute the quantity d2 of BSM options pricing
        """
        return self.d1(S) - self.v * np.sqrt(self.T)

    def price(self, argv):
        """price.

        :param argv:
        """
        try:
            S = argv[0]
        except:
            S = self.S

        if self.CP == "C":
            if self.T > 0:
                return + S * np.exp(-self.q*self.T) * self.N(self.d1(S)) \
                    - self.K * np.exp(-self.r*self.T) * self.N(self.d2(S))
            else:
                return max(S - self.K, 0)
        else:
            if self.T > 0:
                return  - S * np.exp(-self.q*self.T) * self.N(-self.d1(S)) \
                    + self.K * np.exp(-self.r*self.T) * self.N(-self.d2(S))
            else:
                return max(self.K - S, 0)

    def Delta(self):
        """
        BSM delta
        """
        if self.CP == "C":
            if self.T > 0:
                return np.exp(-self.q * self.T) * self.N(self.d1())
            else:
                if self.price() > 0:
                    return +1
                else:
                    return 0
        else:
            if self.T > 0:
                return np.exp(-self.q * self.T) * self.N(self.d1()) - 1
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

    def Gamma(self):
        """
        BSM Gamma
        Gamma is the same for both calls and puts
        """
        if self.T > 0:
            # opt hasnt expired yet
            return (
                +np.exp(-self.q * self.T)
                * self.N(self.d1(), cum=0)
                / (self.S * self.v * np.sqrt(self.T))
            )
        else:
            # opt has expired
            return 0

    def Theta(self):
        """Theta."""
        if self.CP == "C":
            # call opt
            if self.T > 0:
                # call hasnt exired yet
                return (
                    -np.exp(-self.q * self.T)
                    * self.S
                    * self.v
                    * self.N(self.d1(), cum=0)
                    / (2 * np.sqrt(self.T))
                    + self.q * np.exp(-self.q * self.T) * self.S * self.N(self.d1())
                    - self.r * np.exp(-self.r * self.T) * self.K * self.N(self.d2())
                )

            else:
                # call expired
                return 0
        else:
            # put opt
            if self.T > 0:
                # put hasnt expired yet
                return (
                    -np.exp(-self.q * self.T)
                    * self.S
                    * self.v
                    * self.N(self.d1(), cum=0)
                    / (2 * np.sqrt(self.T))
                    - self.q
                    * np.exp(-self.q * self.T)
                    * self.S
                    * (1 - self.N(self.d1()))
                    + self.r
                    * np.exp(-self.r * self.T)
                    * self.K
                    * (1 - self.N(self.d2()))
                )
            else:
                # put expired
                return 0

    def Vega(self):
        """
        BSM Vega
        """
        if self.T > 0:
            return (
                +np.exp(-self.q * self.T)
                * self.S
                * np.sqrt(self.T)
                * self.N(self.d1(), cum=0)
            )
        else:
            return 0

    def greeks(self):
        """greeks."""
        return {
            "Lambda": np.round(BSOpt.Lambda(self), 2),
            "Delta": np.round(BSOpt.Delta(self), 2),
            "Gamma": np.round(BSOpt.Gamma(self), 2),
            "Theta": np.round(BSOpt.Theta(self), 2),
            "Vega": np.round(BSOpt.Vega(self), 2),
        }

    def underlying_set(self, *argv):
        try:
            S = argv[0]
        except:
            S = self.S
        Smin = S * (1 - 0.4)
        Smax = S * (1 + 0.4)
        return list(np.linspace(Smin, S, 100)[:-1]) + list(np.linspace(S, Smax, 100))

    def setprices(self):
        """setprices."""
        oprices = [self.price(p) for p in self.underlying_set()]
        oprices = pd.Series(oprices, index = self.underlying_set())
        return oprices


class BSOptStrat:
    """BSOptStrat."""

    def __init__(self, S = 100, r = 0.03, q = 0):
        self.S = S
        self.r = r
        self.q = q
        self.instruments = []
        self.payoffs = BSOptStrat.init_payoffs(S)
        self.payoffs_exp = BSOptStrat.init_payoffs(S)
        self.payoffs_exp_df = pd.DataFrame()

    def init_payoffs(S):
        ss = pd.Series([0] * len(BSOpt.underlying_set(0, S)), index = BSOpt.underlying_set(0, S))
        return ss

    def call(self, NP=+1, K = 100, T = 0.25, v = 0.3, M = 100, optprice = None):
        option = BSOpt("C", self.S, K, T, self.r, v, q = self.q)

        # call payoff before exp
        if option is not None:
            call_price = optprice
        else:
            call_price = option.price()

        """
        Notes:
        Generating the set of payoff for at different underlying prices
        Here: option.setprices() are the prices of the call, i.e., as if it were long)
        - if NP > 0, price must be paid (debit), then:
          payoffs = option.setprices() * NP * M - Call price * NP * M
        - If NP < 0, the price is to be received, then:
          payoffs = Call price * abs(NP) * M - option.setprices() * abs(NP) * M
                  = option.setprices() * NP * M  - Call price * NP * M

        Summary: ( option.setprices() - call_price ) * NP * M
        """
        payoffs = (option.setprices() - call_price) * NP * M

        # update strategy instruments with current instrument data
        self.update_strategy("C", call_price, NP, K, T, v, M, payoffs)

        # update strategy with current instrument data at maturity
        self.option_at_exp("C", call_price, NP, K, v, M)

    def put(self, NP=+1, K = 100, T = 0.25, v = 0.3, M = 100, optprice = None):
        option = BSOpt("P", self.S, K, T, self.r, v, q=self.q)

        if optprice is not None:
            put_price = optprice
        else:
            put_price = option.price()

        # generate the set of payoff for at diff underlying prices
        payoffs = (option.setprices() - put_price) * NP * M

        self.update_strategy("P", put_price, NP, K, T, v, M, payoffs)

        self.option_at_exp("P", put_price, NP, K, v, M)

    def update_strategy(self, CP, price, NP, K, T, v, M, payoffs):
        self.update_payoffs(payoffs, T=T)

        # create dict w/ the data of the given option
        inst = {"CP": CP,
                "NP": NP,
                "K": K,
                "T": T,
                "v": v,
                "M": M,
                "Pr": round(price, 2)}

        # concat new instrument to total strategy instrument list
        self.instruments.append(inst)

    def update_payoffs(self, payoffs, T = 0):
        if T > 0:
            self.payoffs = payoffs + self.payoffs
        else:
            self.payoffs_exp = payoffs + self.payoffs_exp


    def option_at_exp(self, CP, price, NP, K, v, M):
        """
        calculates the payoff of the option at maturity T=0
        """
        option = BSOpt(CP, self.S, K, 0, self.r, v, q=self.q)

        # opt payoff at maturity:
        # - Call: (max(S - K; 0) - C) * NP * M
        # - Put:  (P - max(S - K; 0)) * NP * M
        payoffs_exp = (option.setprices() - price) * NP * M

        # Update the dataframe of payoff at maturity of single options with the new current inserted option
        self.update_payoffs_exp_df(payoffs_exp)

        # Update the strategy payoff at maturity with the one of the new current inserted option
        self.update_payoffs(payoffs_exp, T = 0)


    def update_payoffs_exp_df(self, payoffs_exp):
        # concat new option payoff with current df
        self.payoffs_exp_df = pd.concat([self.payoffs_exp_df, pd.DataFrame(payoffs_exp)], axis = 1)

        # update cols
        self.payoffs_exp_df.columns = [n for n in range(1, self.payoffs_exp_df.shape[1] + 1)]

    def describe_strat(self):  # , stratname=None):
        '''
        This method can be called once the option has been set.
        Here, all option data saved so far in the list of instrument are now saved
        in a dictionary and the cost of entering the strategy is also computed
        '''
        # create dict of options inserted in the strategy
        StratData = dict()

        strat_cost = 0
        for n, o in enumerate(self.instruments):
            # key of the dictionary (option number)
            StratData["Option_{}".format(n + 1)] = 0

            # compute total strat cost: sum of Net Liquidation Value of option
            # NLV = price * net position * multiplier
            strat_cost = strat_cost + o["Pr"] * o["NP"] * o["M"]

        # Save the cost
        StratData["Cost"] = strat_cost
        return StratData

    def get_payoffs_exp_df(self):
        # returns df w/ the payoff at maturity of the strat's option
        return self.payoffs_exp_df

    def get_payoffs(self):
        # returns current strat payoff
        return self.payoffs

    def get_payoffs_exp(self):
        # returns strat payoff at maturity
        return self.payoffs_exp
