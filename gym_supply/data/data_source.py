# Copyright 2019 The TensorTrade Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

import pandas as pd
import numpy as np
from datetime import datetime
from abc import ABC, abstractmethod

import random


class DataSource(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def next(self):
        raise NotImplemented


class SinteticDataSource(DataSource):
    def __init__(self, start_date: str, end_date: str, dist_fn, freq='D'):
        #assert isinstance(dist_fn, int) or isinstance(dist_fn, float) or callable(dist_fn)

        self.start_date = datetime.strptime(start_date, "%Y/%m/%d")
        self.end_date = datetime.strptime(end_date, "%Y/%m/%d")
        self.dist_fn = dist_fn

        self.range_date = pd.date_range(start=start_date, end=end_date, freq=freq)

        self.df = pd.DataFrame({'index': self.range_date,
                                'value': np.zeros((len(self.range_date),)),
                                })
        self.df = self.df.set_index('index')

        self.iterator = 0
        self.current_date = self.range_date[self.iterator]

    def _generate(self):
        if callable(self.dist_fn):
            return self.dist_fn()
        return self.dist_fn

    def next(self):
        # Get the consumo
        self.df.at[self.current_date, 'value'] = self._generate()

        obs = self.df.loc[self.current_date]

        self.iterator += 1
        self.current_date = self.range_date[self.iterator]

        return obs


if __name__ == "__main__":
    start = "2018/01/01"
    end = "2018/12/31"

    def fn_demand(mean, sigma):
        def fnc():
            return np.ceil(np.random.normal(mean, sigma, 1))
        return fnc

    ds_demand = SinteticDataSource(start, end, fn_demand(100, 10))

    for i in range(10):
        print(ds_demand.next())

