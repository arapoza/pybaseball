import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_soup_fg(playerid):
    url = "https://www.fangraphs.com/statss.aspx?playerid={}".format(playerid)
    s = requests.get(url).content
    return BeautifulSoup(s, "html.parser")


def get_table(soup):
    tables = soup.find_all('table')
    # want the 10th table on the page, which is for standard stats
    table = tables[9]
    data = []
    headings = [th.get_text() for th in table.find("tr").find_all("th")][:]
    data.append(headings)
    table_body = table.find('tbody')
    rows = table_body.find_all('tr', class_=['rgAltRow', 'rgRow'])
    rows = [row for row in rows if not any(tag.startswith('grid') for tag in row['class'])]
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols])
    data = pd.DataFrame(data)
    data = data.rename(columns=data.iloc[0])
    data = data.reindex(data.index.drop(0))
    return data


def is_major_season(css_class):
    return css_class == "rgAltRow" and not "grid" in css_class

def batting_stats_player(playerid):
    """
    Get all batting stats for a player's career. Supply fangraphs playerid obtained from
    playerid_lookup function.
    """
    # retrieve html from fangraphs
    soup = get_soup_fg(playerid)
    table = get_table(soup)
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


print(batting_stats_player(14162))
