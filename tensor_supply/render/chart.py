import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


class Chart:

    def __init__(self):
        # Legends Base
        self.legends = ['Stock']

        # Create new figure
        self.figure = plt.figure()

        self.figure.suptitle("Simulation of system inventory")

        self.history = plt.subplot2grid((6,1), (0,0), rowspan=4, colspan=1)

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
        plt.grid(which='both')

        self.orders = plt.subplot2grid((6, 1), (4, 0), rowspan=2, colspan=1, sharex=self.history)

        self.orders.xaxis_date()
        #self.orders.xaxis.set_major_locator(years)
        #self.orders.xaxis.set_major_formatter(years_fmt)

        #self.orders.xaxis.set_minor_locator(months)

        self.orders.set_title("Orders")
        self.orders.set_xlabel("Date")
        self.orders.set_ylabel("Quantity")

        plt.tight_layout()

        # Show the graph without blocking the rest of the program
        plt.grid(which='both')
        plt.show(block=False)


    def render(self, df, iterator):

        if iterator > 0:
            serie = df.iloc[:iterator]

            self.history.plot(serie.index.values, serie['stock'].values, 'g--')
            #self.history.legend(['ROP', 'Stock'])
            #self.history.step(df.index.values, df['transito'].values, 'r')

            #self.orders.plot(df.index.values, df['pedido'].values, 'b+')
            self.orders.bar(serie.index.values, serie['pedido'].values, width=5, color='b')

            plt.pause(0.001)

    def close(self):
        plt.close()
