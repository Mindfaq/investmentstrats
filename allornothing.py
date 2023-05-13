import pandas as pd
import numpy as np
import yfinance as yf

class InvestmentStrategies:
    """
    Class for comparing different investment strategies.
    
    Parameters
    ----------
    amount : float
        The amount to be invested.
    years : list of int
        The list of years for which the strategies should be tested.
    """

    def __init__(self, amount, years):
        self.amount = amount
        self.years = years

    def invest_dca(self, amount, prices):
        """
        Perform Dollar-Cost Averaging investment.

        Parameters
        ----------
        amount : float
            The amount to be invested.
        prices : np.array
            The historical prices of the asset.

        Returns
        -------
        tuple
            The ending value of the investment and the annualized return.
        """
        shares_bought_each_period = amount / prices
        total_shares_bought = np.sum(shares_bought_each_period)
        avg_cost_per_share = amount * len(prices) / total_shares_bought
        final_value_per_share = prices[-1]
        ending_value = total_shares_bought * final_value_per_share
        total_return = (final_value_per_share - avg_cost_per_share) / avg_cost_per_share
        years = len(prices) / 12
        annualized_return = (1 + total_return) ** (1 / years) - 1
        return ending_value, annualized_return

    def invest_lumpsum(self, amount, prices):
        """
        Perform Lump Sum investment.

        Parameters
        ----------
        amount : float
            The amount to be invested.
        prices : np.array
            The historical prices of the asset.

        Returns
        -------
        tuple
            The ending value of the investment and the annualized return.
        """
        shares_bought = amount / prices[0]
        ending_value = shares_bought * prices[-1]
        return ending_value, (ending_value / amount) ** (1 / (len(prices) / 12)) - 1

    def test_strategies(self):
        """
        Test and compare the performance of lump sum and dollar-cost averaging (DCA) investment strategies.

        For each year in the `self.years` attribute, the method simulates both investment strategies 
        over every possible `year`-long period in the historical data. 

        It calculates the number of wins and the average annualized return for each strategy.

        The method returns a DataFrame that contains these results for each year.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the results of the comparison. The DataFrame has the following columns:
            - 'Year': The number of years over which the strategies were compared.
            - 'Lump Sum Wins': The number of periods in which the lump sum strategy resulted in a greater ending value.
            - 'Dollar-Cost Averaging Wins': The number of periods in which the DCA strategy resulted in a greater ending value.
            - 'Average Annualized Lump Sum Return': The average annualized return of the lump sum strategy over all periods.
            - 'Average Annualized DCA Return': The average annualized return of the DCA strategy over all periods.
            - 'Lump Sum Win Ratio': The percentage of periods in which the lump sum strategy resulted in a greater ending value.
        """
        results = []

        # Download all the available data at once
        data = yf.download('^IXIC', period="max", interval='1mo')
        data.dropna(inplace=True)  # drop rows with missing data
        data = data['Adj Close']  # we're only interested in the adjusted close prices

        for year in self.years:
            lumpsum_wins = 0
            dca_wins = 0
            lumpsum_returns = []
            dca_returns = []

            for start in range(len(data) - year * 12):
                prices = data.iloc[start:start + year * 12]
                lumpsum_ending_value, lumpsum_return = self.invest_lumpsum(self.amount, prices)
                dca_ending_value, dca_return = self.invest_dca(self.amount / (year * 12), prices)
                lumpsum_returns.append(lumpsum_return)
                dca_returns.append(dca_return)

                if lumpsum_ending_value > dca_ending_value:
                    lumpsum_wins += 1
                else:
                    dca_wins += 1

            results.append({
                'Year': year,
                'Lump Sum Wins': lumpsum_wins,
                'Dollar-Cost Averaging Wins': dca_wins,
                'Average Annualized Lump Sum Return': np.mean(lumpsum_returns) * 100,
                'Average Annualized DCA Return': np.mean(dca_returns) * 100,
                'Lump Sum Win Ratio': lumpsum_wins / (lumpsum_wins + dca_wins) * 100
            })

        return pd.DataFrame(results)


if __name__ == "__main__":
    strategies = InvestmentStrategies(10000000, [5, 10, 15])
    results = strategies.test_strategies()
    print(results)
