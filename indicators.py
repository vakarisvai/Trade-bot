import pandas as pd


class Indicators:
    short_term_window = 10
    long_term_window = 50
    rsi_window = 14

    def __init__(self, data: pd.DataFrame, day: str) -> None:
        self._day: str = day
        self.data = data
        self._rsi: float = self.count_rsi()
        self._short_term_ma: float = self.count_ma(Indicators.short_term_window)
        self._long_term_ma: float = self.count_ma(Indicators.long_term_window)

    @property
    def rsi(self):
        return self._rsi

    @property
    def short_term_ma(self):
        return self._short_term_ma

    @property
    def long_term_ma(self):
        return self._long_term_ma

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: pd.DataFrame) -> pd.DataFrame:
        if self._day == "YESTERDAY":
            self._data = data
        else:
            data = data.drop(data.index[-1])
            self._data = data

    def count_rsi(self) -> float:
        """
        Calculates RSI value for yesterday.
        :param data: data of the stock.
        :return: RSI value of yesterday.
        """
        data = self.data[-Indicators.rsi_window:]
        diff: pd.Series = data["Price"].diff()
        avg_gain = (
            (diff.where(diff > 0, 0)).rolling(window=Indicators.rsi_window).mean()
        )
        avg_loss = (
            (-diff.where(diff < 0, 0)).rolling(window=Indicators.rsi_window).mean()
        )

        rs: float = avg_gain.iloc[-1] / avg_loss.iloc[-1]
        rsi: float = 100 - (100 / (1 + rs))
        return rsi

    def count_ma(self, window: int) -> float:
        """
        Calculates the moving average depending on the selected period of time.
        :param window: size of the window.
        :return: moving average value of the given period of time.
        """
        moving_average: float = self.data["Price"].rolling(window=window).mean()
        return moving_average.iloc[-1]
