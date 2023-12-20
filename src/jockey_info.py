import requests
from bs4 import BeautifulSoup
import re  # 正規表現モジュールをインポート
from utils import make_request_with_retry

def get_jockey_info(jockey_id):
    url = f"https://db.netkeiba.com/jockey/{jockey_id}"
    # r = requests.get(url)
    r = make_request_with_retry(url)

    if r is None:
        print(f"Failed to retrieve data for jockey ID: {jockey_id}")
        return "不明", "不明"

    soup = BeautifulSoup(r.content.decode("euc-jp", "ignore"), "html.parser")

    # 騎手の名前を取得
    jockey_name = "不明"
    h1_elements = soup.find_all("h1")
    for element in h1_elements:
        if element.get_text(strip=True):
            jockey_name = element.get_text(strip=True)
            break

    # 不要なテキスト（カナ読みや余分な空白）を除去
    jockey_name = re.sub(r'\s*\([^)]*\)', '', jockey_name).strip()


    # 生年月日を取得
    birth_date_element = soup.find("p", class_="txt_01")
    birth_date = birth_date_element.get_text(strip=True).split(" ")[0] if birth_date_element else "不明"
    birth_date = birth_date.strip()

    return jockey_name, birth_date