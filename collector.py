import sqlite_db_maker as sql


COLUMN_FORMAT = """ SR INTEGER PRIMARY KEY AUTOINCREMENT,
                    TIMESTAMP VARCHAR(255),
                    SYMBOL VARCHAR(225),
                    OPEN REAL,
                    HIGH REAL,
                    LOW REAL,
                    PREVIOUS_CLOSE REAL,
                    DAY_END_CLOSE REAL,
                    LAST_TRADED_PRICE REAL,
                    CHANGE REAL,
                    PERCENTAGE_CHANGE REAL,
                    VOLUME REAL,
                    TURNOVER REAL,
                    YEAR_HIGH REAL,
                    YEAR_LOW REAL,
                    YEAR_PERCENTAGE_CHANGE REAL,
                    MONTH_PERCENTAGE_CHANGE REAL"""


keys = {
"symbol": "SYMBOL",
"open": "OPEN",
"high": "HIGH",
"low": "LOW",
"ltP": "LAST_TRADED_PRICE",
"ptsC": "CHANGE",
"per": "PERCENTAGE_CHANGE",
"trdVol": "TURNOVER",
"wkhi": "YEAR_HIGH",
"wklo": "YEAR_LOW",
"previousClose": "PREVIOUS_CLOSE",
"dayEndClose": "DAY_END_CLOSE",
"yPC": "YEAR_PERCENTAGE_CHANGE",
"mPC": "MONTH_PERCENTAGE_CHANGE",
"lastUpdateTime": "LAST_UPDATE_TIME"
}
