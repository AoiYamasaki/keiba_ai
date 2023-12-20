from data_fetcher import fetch_race_data
from config import year_start, year_end

def main():
    for year in range(year_start, year_end):
        fetch_race_data(year)

if __name__ == "__main__":
    main()
