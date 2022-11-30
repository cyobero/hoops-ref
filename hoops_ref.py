"""
A Python client to retrieve NBA team and individual stats
"""
import pandas as pd
import numpy as np
from urllib.error import HTTPError


class HoopsRefClient:
    ENDPOINT = "https://www.basketball-reference.com"

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            self.k = v

    def games(self, team: str, season: int, playoffs=False) -> pd.DataFrame:
        """
        Returns a pandas DataFrame for game results for a given `team` and `season`. The
        `playoffs` flag indicates whether to retrieve regular season or playoffs data. By
        default, this retrieves regular season statistics.

        Example:
          ```
          hoops = HoopsRefClient()
          # retrieve 2022 results for Chicago Bulls
          res = hoops.results('CHI', 2022)
          res.head()
          ```
        """
        def _load_df(team=team, season=season, playoffs=playoffs) -> pd.DataFrame:
            """
            Returns a pandas DataFrame of game results for a given `team` and `year`.

            Credit: Data is retrieved from http://www.basketball-reference.com/

            Parameters
            -----------------
            team (str) - The 3-letter NBA team abbreviation (e.g. Chicago Bulls is 'CHI') 
            year (int) - The year of season. Because a season starts and ends in different years,
                         the year provided is assumed to be the year the season ends. Thus,
                         passing in `2022` retrieves the game results for the 2021-2022 season
            """
            url = f'{self.ENDPOINT}/teams/{team}/{season}_games.html'
            if playoffs:
                url += '#games_playoffs'
                try:
                    df = pd.read_html(url)[1]
                    return df
                except IndexError:
                    print("""
                          Them clowns didn't make the playoffs! LMAO. Here are their
                          regular season stats instead.
                        """)

            df = pd.read_html(url)[0]
            return df

        def _clean_df(df: pd.DataFrame) -> pd.DataFrame:
            """
            Cleans a pandas DataFrame retrieved from the `load_df` function.
            """
            df = pd.DataFrame(
                df[['Date', 'Opponent', 'Tm', 'Opp', 'Unnamed: 5']])
            # The HTML table is arranged so the column headers are shown every 20 rows.
            # This removes them.
            df.drop(df[df['Date'] == 'Date'].index, inplace=True)
            df.reset_index(inplace=True)

            df.rename(columns={'Unnamed: 5': 'Venue'}, inplace=True)
            # Convert columns to their appropriate types
            df[['Tm', 'Opp']] = df[['Tm', 'Opp']].astype('int')
            # Make `Date` column the index
            df.index = pd.Index(df['Date'])
            # Make `Venue` either 'H' for NaN or 'A' for '@'
            df['Venue'] = df['Venue'].apply(
                lambda x: 'H' if x is np.nan else 'A')
            return df[['Opponent', 'Tm', 'Opp', 'Venue']]

        return _clean_df(_load_df(team, season))

    def per_game_team(self, season: int, opponent=False) -> pd.DataFrame:
        """
        Returns a pandas DataFrame of per game statistics (e.g. PTS, AST, etc) for all
        teams in a given `season`

        Original table: https://www.basketball-reference.com/leagues/NBA_2022.html#per_game-team
        """
        url = f'{self.ENDPOINT}/leagues/NBA_{season}.html#per_game-'
        if opponent:
            url += 'opponent'
            df = pd.read_html(url)
            return df[5]

        # removes the asterisk (*) from some of the team names
        df = pd.read_html(url)[4]
        df['Team'] = df['Team'].apply(lambda x: x.strip('*'))
        return df[1:-2]

    def per_game_player(self, season: int) -> pd.DataFrame:
        """
        Return a pandas DataFrame containing individual players' per-game stats for a
        given `season`.
        """
        url = f'{self.ENDPOINT}/leagues/NBA_{season}_per_game.html#per_game_stats'
        try:
            df = pd.read_html(url)[0]
            df = df.drop(df[df['Player'] == 'Player'].index).reset_index()
            df['Age'] = df['Age'].astype('int')
            df['Pos'] = df['Pos'].astype('category')
            df.iloc[:,6:] = df.iloc[:, 6:].astype('float')
            return df.iloc[:, 2:]
        except HTTPError:
            pass

        return pd.DataFrame()
