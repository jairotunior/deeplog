import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



class Chart:

    def __init__(self):

        # Create new figure
        self.figure = plt.figure()

        self.history = plt.subplot2grid((6,1), (0,0), rowspan=3, colspan=1)

        self.history.set_title('Inventory Levels')
        self.history.set_xlabel('Date')
        self.history.set_ylabel('Quantity')

        years = mdates.YearLocator()  # every year
        months = mdates.MonthLocator()  # every month

        years_fmt = mdates.DateFormatter('%Y')
        months_fmt = mdates.DateFormatter('%m')

        self.history.xaxis.set_major_locator(years)
        self.history.xaxis.set_major_formatter(years_fmt)

        self.history.xaxis.set_minor_locator(months)

        self.orders = plt.subplot2grid((6, 1), (3, 0), rowspan=2, colspan=1, sharex=self.history)

        self.orders.set_title("Orders")
        self.orders.set_xlabel("Date")
        self.orders.set_ylabel("Quantity")

        plt.tight_layout()

        # Show the graph without blocking the rest of the program
        plt.show(block=False)


    def render(self, df):

        self.history.plot(df.index.values, df['stock'].values, 'g')

        self.history.step(df.index.values, df['transito'].values, 'r')

        self.history.step(df.index.values, df['rop'].values, 'b')


        self.history.plot(df.index.values, df['pedido'].values, 'b+')

        plt.pause(0.001)

    def close(self):
        plt.close()
