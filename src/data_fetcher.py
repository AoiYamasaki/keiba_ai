import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, date
from concurrent.futures import ThreadPoolExecutor, as_completed
from jockey_info import get_jockey_info
from config import base_url, place_names
from utils import make_request_with_retry
# from .jockey_info import get_jockey_info # testモード時
# from .config import base_url, place_names # testモード時
# from .utils import make_request_with_retry # testモード時
from tqdm import tqdm
from cache_manager import load_from_cache, save_to_cache

# セッションの初期化
session = requests.Session()

def fetch_race_data(year, test_mode=False):
    """
    指定された年の全レースデータを取得し、CSVファイルに保存する。
    """
    print(f"Processing year: {year}")
    today = date.today()
    race_data_all = []
    # CSVファイルのヘッダー
    race_data_all.append(['race_id', '馬', '騎手ID', '騎手名', '騎手生年月日', '馬番', '走破時間', 'オッズ', '通過順', '着順', '体重', '体重変化', '性', '齢', '斤量', '上がり', '人気', 'レース名', '日付', '開催', 'クラス', '芝・ダート', '距離', '回り', '馬場', '天気', '発走時刻', '場id', '場名'])

    # レースIDのリストを作成
    # race_ids = [f"{year}{place_code}{meeting:02d}{day:02d}{race_number:02d}" for place_code in place_names for meeting in range(1, 7) for day in range(1, 13) for race_number in range(1, 13)]
    race_ids = []
    for place_code in place_names:
        for meeting in range(1, 7):
            for day in range(1, 13):
                for race_number in range(1, 13):
                    race_date = datetime(year, int(place_code), day).date()
                    if race_date <= today:  # 未来日のレースは除外
                        race_id = f"{year}{place_code}{meeting:02d}{day:02d}{race_number:02d}"
                        race_ids.append(race_id)

    if test_mode:
        race_ids = race_ids[:5]  # テストモードの場合は最初の5レースのみ
        print(race_ids)

    for race_id in race_ids:
        cached_data = load_from_cache(race_id)
        if cached_data:
            print(f"Loaded from cache: {race_id}")
            race_data_all.extend(cached_data)
        else:
            place_code = race_id[4:6]
            place_name = place_names.get(place_code, "不明")
            data = process_race(race_id, place_code, place_name)
            if data:
                race_data_all.extend(data)
                print(f"Saving to cache: {race_id}")
                save_to_cache(race_id, data)
    
    # 未取得のレースIDを特定
    to_fetch_race_ids = []
    for race_id in race_ids:
        if not load_from_cache(race_id):
            to_fetch_race_ids.append(race_id)
    print(f"Race IDs to fetch: {to_fetch_race_ids}")

    # 並列処理の設定
    with ThreadPoolExecutor(max_workers=10) as executor:
        # future_to_race = {
        #     executor.submit(process_race, f"{year}{place_code}{meeting:02d}{day:02d}{race_number:02d}", place_code, place_names[place_code])
        #     for place_code in place_names
        #     for meeting in range(1, 7)
        #     for day in range(1, 13)
        #     for race_number in range(1, 13)
        # }

        # future_to_race = {
        #     executor.submit(process_race, race_id, race_id[4:6], place_names[race_id[4:6]]): race_id for race_id in race_ids
        # }

        future_to_race = {executor.submit(process_race, race_id, race_id[4:6], place_names[race_id[4:6]]): race_id for race_id in to_fetch_race_ids}

        # プログレスバーを使用
        with tqdm(total=len(to_fetch_race_ids), desc=f"Processing races for {year}") as progress:
            for future in as_completed(future_to_race):
                race_id = future_to_race[future]
                race_data = future.result()
                if race_data:
                    race_data_all.extend(race_data)
                    save_to_cache(race_id, race_data)
                progress.update(1)

    for future in as_completed(future_to_race):
        race_data = future.result()
        if race_data:
            race_data_all.extend(race_data)

    print(f"Completed processing for year: {year}")

   # ファイル名の決定
    if test_mode:
        filename = f'./data/{today}_keiba_racedata_{year}_test.csv'
    else:
        filename = f'./data/{today}_keiba_racedata_{year}.csv'

    # CSVファイルにデータを書き込み
    with open(filename, 'w', newline='', encoding="utf-8") as f:
        csv.writer(f).writerows(race_data_all)

def process_race(race_id, place_code, place_name):
    """
    特定のレースIDに基づいてレースデータを処理する。
    """
    print(f"Starting process_race for {race_id}")
    url = f"{base_url}{race_id}"
    try:
        # response = session.get(url)
        response = make_request_with_retry(url, session=session)

        if response is None or response.status_code == 404:
            print(f"Failed to retrieve data for race ID: {race_id}")
            return None

        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching race data for {race_id}: {e}")
        return None

    soup = BeautifulSoup(response.content.decode("euc-jp", "ignore"), "html.parser")

    # レースデータの処理
    race_data = []
    soup_span = soup.find_all("span")
    # 馬の数
    allnum = (len(soup_span) - 6) / 3
    allnum = int(allnum)
    # urlにデータがあるか判定
    if allnum < 1:
        print('continue: ' + url)
        return None

    for num in range(allnum):
        # 各馬のデータを取得
        soup_txt_l = soup.find_all(class_="txt_l")
        soup_txt_r = soup.find_all(class_="txt_r")

        jockey_id = soup_txt_l[4*num+1].contents[1]['href'].split("/")[-2]
        jockey_name, birth_date = get_jockey_info(jockey_id)

        runtime = ''
        try:
            runtime = soup_txt_r[2+5*num].contents[0]
        except IndexError:
            runtime = ''

        soup_nowrap = soup.find_all("td", nowrap="nowrap", class_=None)
        pas = ''
        try:
            pas = str(soup_nowrap[3*num].contents[0])
        except:
            pas = ''

        weight = 0
        weight_dif = 0
        var = soup_nowrap[3*num+1].contents[0]
        try:
            weight = int(var.split("(")[0])
            weight_dif = int(var.split("(")[1][0:-1])
        except ValueError:
            weight = 0
            weight_dif = 0

        soup_tet_c = soup.find_all("td", nowrap="nowrap", class_="txt_c")
        last = ''
        try:
            last = soup_tet_c[6*num+3].contents[0].contents[0]
        except IndexError:
            last = ''

        pop = ''
        try:
            pop = soup_span[3*num+10].contents[0]
        except IndexError:
            pop = ''

        # その他のレース情報の処理
        try:
            var = soup_span[8]
            sur = str(var).split("/")[0].split(">")[1][0]
            rou = str(var).split("/")[0].split(">")[1][1]
            dis = str(var).split("/")[0].split(">")[1].split("m")[0][-4:]
            con = str(var).split("/")[2].split(":")[1][1]
            wed = str(var).split("/")[1].split(":")[1][1]
            start_time = str(var).split("/")[3].split("発走 : ")[1].split("<")[0].strip()
        except IndexError:
            try:
                var = soup_span[7]
                sur = str(var).split("/")[0].split(">")[1][0]
                rou = str(var).split("/")[0].split(">")[1][1]
                dis = str(var).split("/")[0].split(">")[1].split("m")[0][-4:]
                con = str(var).split("/")[2].split(":")[1][1]
                wed = str(var).split("/")[1].split(":")[1][1]
                start_time = str(var).split("/")[3].split("発走 : ")[1].split("<")[0].strip()
            except IndexError:
                var = soup_span[6]
                sur = str(var).split("/")[0].split(">")[1][0]
                rou = str(var).split("/")[0].split(">")[1][1]
                dis = str(var).split("/")[0].split(">")[1].split("m")[0][-4:]
                con = str(var).split("/")[2].split(":")[1][1]
                wed = str(var).split("/")[1].split(":")[1][1]
                start_time = str(var).split("/")[3].split("発走 : ")[1].split("<")[0].strip()

        soup_smalltxt = soup.find_all("p", class_="smalltxt")
        detail = str(soup_smalltxt).split(">")[1].split(" ")[1]
        date = str(soup_smalltxt).split(">")[1].split(" ")[0]
        clas = str(soup_smalltxt).split(">")[1].split(" ")[2].replace(u'\xa0', u' ').split(" ")[0]
        title = str(soup.find_all("h1")[1]).split(">")[1].split("<")[0]

        race_data.append([
            race_id, 
            soup_txt_l[4*num].contents[1].contents[0],  # 馬の名前
            jockey_id, 
            jockey_name, 
            birth_date, 
            soup_txt_r[1+5*num].contents[0],  # 馬番
            runtime, 
            soup_txt_r[3+5*num].contents[0],  # オッズ
            pas, 
            num+1,  # 着順
            weight, 
            weight_dif, 
            soup_tet_c[6*num].contents[0][0],  # 性
            soup_tet_c[6*num].contents[0][1],  # 齢
            soup_tet_c[6*num+1].contents[0],  # 斤量
            last, 
            pop, 
            title,  # レース名
            date,  # 日付
            detail,  # 開催
            clas,  # クラス
            sur,  # 芝・ダート
            dis,  # 距離
            rou,  # 回り
            con,  # 馬場状態
            wed,  # 天気
            start_time,  # 発走時刻
            place_code,  # 場id
            place_name  # 場名
        ])

    print(f"Completed process_race for {race_id}")
    return race_data
