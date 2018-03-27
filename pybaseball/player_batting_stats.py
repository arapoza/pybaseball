import requests
import pandas as pd
import io
from bs4 import BeautifulSoup


def get_soup_fg(playerid):
    url = "https://www.fangraphs.com/statss.aspx?playerid={}".format(playerid)
    s = requests.get(url).content
    return BeautifulSoup(s, "html.parser")


def get_table(soup, site):
    tables = soup.find_all('table')
    table = tables[9]
    data = []
    headings = [th.get_text() for th in table.find("tr").find_all("th")][:]
    data.append(headings)
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols])
    data = pd.DataFrame(data)
    data = data.rename(columns=data.iloc[0])
    data = data.reindex(data.index.drop(0))
    return data


def batting_stats_player(playerid):
    """
    Get all batting stats for a set time range. This can be the past week, the
    month of August, anything. Just supply the start and end date in YYYY-MM-DD
    format.
    """
    # retrieve html from baseball reference
    soup = get_soup_fg(playerid)
    table = get_table(soup, -1)
    table = table.dropna(how='all')  # drop if all columns are NA
    # scraped data is initially in string format.
    # convert the necessary columns to numeric.
    for column in ['G', 'AB', 'PA', 'H', '1B', '2B', '3B',
                   'HR', 'R', 'RBI', 'BB', 'IBB', 'SO', 'HBP', 'SF', 'SH', 'GDP',
                   'SB', 'CS', 'AVG']:
        # table[column] = table[column].astype('float')
        table[column] = pd.to_numeric(table[column])
        # table['column'] = table['column'].convert_objects(convert_numeric=True)
    return table
