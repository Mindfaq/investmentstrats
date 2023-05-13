# Investment Strategies Comparison

This Python project is a tool for comparing two investment strategies over a given period of time:

- **Lump Sum Investing (LSI)**: Investing all of your money at once.
- **Dollar-Cost Averaging (DCA)**: Investing your money in equal portions, at regular intervals regardless of the share price. 

The two strategies are tested on historical data of NASDAQ Composite Index (`^IXIC`), which is downloaded using the `yfinance` package.

## Requirements
- Python 3.6+
- yfinance
- pandas
- numpy


You can install the required packages using:

```
pip install -r requirements.txt
```

## How to Run
To run the code, simply execute the main Python file:

```sh
python main.py
```

## Output
The program will output a DataFrame showing the comparison between the two strategies over different time periods. The DataFrame includes:

- The number of wins for each strategy.
- The average annualized returns for each strategy.
- The win ratio of Lump Sum Investing.

## Disclaimer
This tool is for educational purposes only. Past performance is not indicative of future results. Always do your own research and consider your financial decisions carefully.

## Contribution
Feel free to fork the project and make your own changes, or propose changes by creating a new issue.
