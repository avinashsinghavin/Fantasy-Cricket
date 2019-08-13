import sqlite3
from collections import defaultdict


class DBConnect:
    # Constructor for creating table if it doesn't exist
    def __init__(self):
        self.conn = sqlite3.connect('E:\\Project\\Fantasy_Cricket\\db.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS teams(team_name VARCHAR(30), player1 VARCHAR(30), "
                            "player2 VARCHAR(30), player3 VARCHAR(30), player4 VARCHAR(30), player5 VARCHAR(30), "
                            "player6 VARCHAR(30), player7 VARCHAR(30), player8 VARCHAR(30), player9 VARCHAR(30), "
                            "player10 VARCHAR(30), player11 VARCHAR(30))")
        self.conn.commit()

    # Function to search for a team by name
    def search(self, name):
        row = self.cursor.execute("SELECT * FROM teams WHERE team_name='%s' ;" % name)
        if not row:
            return False
        else:
            return True

    # Function to insert teams created in database
    def add(self, name, players):
        players = (list(players))
        players.insert(0, name)
        players = tuple(players)
        if self.search(name):
            self.cursor.execute("DELETE FROM teams WHERE team_name='%s';" % name)
        self.cursor.execute("INSERT INTO teams VALUES %s;" % (players,))
        self.conn.commit()

    def open(self):
        row = self.cursor.execute("SELECT * FROM teams;")
        return [i[0] for i in row]

    def player_details(self):
        l = []
        self.cursor.execute("SELECT * FROM match1;")
        rows = self.cursor.fetchall()
        for row in rows:
            l.append(row)
        return l

    # Function to get all batsmen and their value
    def bat_player(self):
        dic = defaultdict(int)
        self.cursor.execute("SELECT player, value FROM match1 WHERE ctg = 'BAT';")
        rows = self.cursor.fetchall()
        for i in rows:
            dic[i[0]] = i[1]
        return dic

    # Function to get all bowlers and their value
    def bwl_player(self):
        dic = defaultdict(int)
        self.cursor.execute("SELECT player,value FROM match1 WHERE ctg = 'BWL';")
        rows = self.cursor.fetchall()
        for i in rows:
            dic[i[0]] = i[1]
        return dic

    # Function to get all all-rounder and their value
    def ar_player(self):
        dic = defaultdict(int)
        self.cursor.execute("SELECT player,value FROM match1 WHERE ctg = 'AR';")
        rows = self.cursor.fetchall()
        for i in rows:
            dic[i[0]] = i[1]
        return dic

    # Function to get all wicket-keeper and their value
    def wk_player(self):
        dic = defaultdict(int)
        self.cursor.execute("SELECT player,value FROM match1 WHERE ctg = 'WK';")
        rows = self.cursor.fetchall()
        for i in rows:
            dic[i[0]] = i[1]
        return dic

    # Function to fetch batsmen of already saved team and their value
    def _bat_player(self, teamname):
        dic = defaultdict(int)
        self.cursor.execute(f"SELECT * FROM teams WHERE team_name = '{teamname}' ;")
        rows = self.cursor.fetchall()
        rows = [rows[0][i] for i in range(1, 12)]
        self.cursor.execute("SELECT player, value FROM match1 WHERE ctg = 'BAT';")
        row1 = self.cursor.fetchall()
        for i in row1:
            if i[0] in rows:
                dic[i[0]] = i[1]
        return dic

    # Function to fetch bowlers of already saved team and their value
    def _bwl_player(self, teamname):
        dic = defaultdict(int)
        self.cursor.execute(f"SELECT * FROM teams WHERE team_name = '{teamname}' ;")
        rows = self.cursor.fetchall()
        rows = [rows[0][i] for i in range(1, 12)]
        self.cursor.execute("SELECT player, value FROM match1 WHERE ctg = 'BWL';")
        row1 = self.cursor.fetchall()
        for i in row1:
            if i[0] in rows:
                dic[i[0]] = i[1]
        return dic

    # Function to fetch all-rounder of already saved team and their value
    def _ar_player(self, teamname):
        dic = defaultdict(int)
        self.cursor.execute(f"SELECT * FROM teams WHERE team_name = '{teamname}' ;")
        rows = self.cursor.fetchall()
        rows = [rows[0][i] for i in range(1, 12)]
        self.cursor.execute("SELECT player, value FROM match1 WHERE ctg = 'AR';")
        row1 = self.cursor.fetchall()
        for i in row1:
            if i[0] in rows:
                dic[i[0]] = i[1]
        return dic

    # Function to fetch wicket-keeper of already saved team and their value
    def _wk_player(self, teamname):
        dic = defaultdict(int)
        self.cursor.execute(f"SELECT * FROM teams WHERE team_name = '{teamname}' ;")
        rows = self.cursor.fetchall()
        rows = [rows[0][i] for i in range(1, 12)]
        self.cursor.execute("SELECT player, value FROM match1 WHERE ctg = 'WK';")
        row1 = self.cursor.fetchall()
        for i in row1:
            if i[0] in rows:
                dic[i[0]] = i[1]
        return dic

    # Function to calculate the score of individual player and return the list
    def _evaluate_(self, team, match_name):
        self.cursor.execute(f"SELECT * FROM teams WHERE team_name = '{team}';")
        rows = self.cursor.fetchall()
        l = [rows[0][i] for i in range(1, 12)]
        totl_point = 0
        self.cursor.execute(f"SELECT * FROM {match_name};")
        list_player_point = []
        rows = self.cursor.fetchall()
        for i in l:
            temp_list = []
            temp_player_score = 0
            for row in rows:
                if i == row[0]:
                    temp_player_score += int(row[1] / 2)  # 1  point for 2 run
                    if row[1] >= 50:  # Adding 5 point for half century
                        temp_player_score += 5
                    if row[2] != 0:
                        strick = row[1] / row[2] * 100  # Strike rate
                        if 80 <= strick <= 100:
                            temp_player_score += 2
                        if strick > 100:
                            temp_player_score += 4
                    temp_player_score += row[3]  # Fours
                    temp_player_score += row[4] * 2  # Six
                    temp_player_score += row[8] * 10  # Wickets
                    if 3 <= row[8] < 5:
                        temp_player_score += 5
                    if row[8] >= 5:
                        temp_player_score += 10
                    over = float(row[5] / 6)
                    economy = 0.00
                    if over != 0:
                        economy = float(row[7] / over)
                    if 3.5 >= economy >= 2:
                        temp_player_score += 7
                    if economy < 2:
                        temp_player_score += 10
                    temp_player_score += row[9] * 10  # Catches
                    temp_player_score += row[10] * 10  # Stumps
                    temp_player_score += row[11] * 10  # Runouts
                    temp_list.append(temp_player_score)
                    list_player_point.append(temp_player_score)
        return list_player_point

    # Function for returning the names of players to be evaluated
    def _teamname_(self, team):
        self.cursor.execute(f"SELECT * FROM teams WHERE team_name = '{team}';")
        rows = self.cursor.fetchall()
        l = [rows[0][i] for i in range(1, 12)]
        return l
