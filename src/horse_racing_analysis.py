import numpy as np
import pandas as pd
from scipy.fft import fft
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import random

class HorseRacingAnalysis:
    def __init__(self):
        self.a1 = [1, 0.5, 2] + [random.random() / 5.0 / hn for hn in range(4, 20)]
        self.a2 = [1, 0.5, 0.2, 2] + [random.random() / 5.0 / hn for hn in range(5, 20)]
        self.nr_values = []
        self.y_values = []
        self.z_values = []
        self.w_values = []
        self.observation = []

    def generate_data(self, race_data, place_latlon):
        """
        レースデータから NR、Y、Z、W の値を計算する。
        
        :param race_data: レースデータのDataFrame
        :param place_latlon: 競馬場の緯度経度情報を含むDataFrame
        """
        for index, row in race_data.iterrows():
            race_datetime = pd.to_datetime(row['日付'], format='%Y年%m月%d日')
            birth_date = pd.to_datetime(row['騎手生年月日'])
            race_time = row['発走時刻']
            placement = row['着順']
            place_name = row['場名']

            # 緯度経度の取得
            lat, lon = place_latlon[place_latlon['場名'] == place_name][['緯度', '経度']].iloc[0]

            # BRとNRの計算
            br, nr = self.calculate_br_nr(race_datetime, birth_date, lat, lon, race_time)

            # Y軸の計算
            y = self.calculate_y(nr - br)

            # Z軸の計算（ここでは仮の計算とする）
            z = np.log1p(y * random.random())

            # W軸の得点計算
            w = self.calculate_w_score(placement)

            # 値の保存
            self.nr_values.append(nr)
            self.y_values.append(y)
            self.z_values.append(z)
            self.w_values.append(w)
            self.observation.append(row)

    def calculate_y(self, theta):
        y = sum([a * np.sin(i * (theta + 0)) for i, a in enumerate(self.a1)]) / sum(self.a1)
        return y

    def moving_average(self, values, window_size):
        return pd.Series(values).rolling(window=window_size).mean().tolist()

    def apply_fft(self, data):
        # FFTを適用してデータを分析
        fft_result = fft(data)
        return fft_result

    def interpolate_data(self, data):
        # データの補間処理
        interpolated_data = pd.Series(data).interpolate()
        return interpolated_data

    def plot_data(self, data):
        plt.plot(data)
        plt.show()

    def train_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model = RandomForestRegressor()
        model.fit(X_train, y_train)
        return model

    def calculate_br_nr(self, race_datetime, birth_date, lat, lon, race_time):
        # BRとNRの計算
        br = 6  # 固定値
        nr = random.random()  # 乱数生成
        return br, nr

    def calculate_w_score(self, placement):
        # 着順に基づいて得点を計算
        return 1 if placement <= 5 else 0
