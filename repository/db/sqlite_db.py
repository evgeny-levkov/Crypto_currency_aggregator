from .base_db import BaseDb
from ...model.сoin_model import CoinModel
import sqlite3

class SqlLiteDb(BaseDb):
    def __init__(self, db):
        super().__init__(db)
        self.connetion()

    def connetion(self):
        try:
            self.conn = sqlite3.connect(self.db)
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")

        try:
            self.cur.execute(f"select * from crypto")
        except Exception as e:
            print(f"Таблицы не существует: {e}")
            self.cur.execute("create table crypto(id INTEGER PRIMARY KEY AUTOINCREMENT, name Text, time DATETIME, price FLOAT, source TEXT)")

    def get_history_price(self, coin, limit=10000):
        res =[]
        try:
            output = self.cur.execute('select * from crypto where name = ? limit ?', (coin, limit)).fetchall()
            if output is not None:
                for coins in output:
                    res.append(CoinModel(coins[1], coins[2], coins[3], coins[4]))
            else:
                print('Нет таких записей')
                return None
        except Exception as e:
            print(f'Ошибка получения данных: {e}')
        return res

    def get_coin_price(self, coin, source):
        try:
            output = self.cur.execute('select * from crypto where name = ? and source = ? order by time desc limit 1', (coin, source)).fetchone()
            if output is not None:
                return CoinModel(output[1], output[2], output[3], output[4])
            else:
                print('Нет таких записей')
                return None
        except Exception as e:
            print(f'Ошибка получения данных: {e}')

    def save_cache(self, coin: CoinModel):
        self.cur.execute('insert into crypto(name, time, price, source) values (?, ?, ?, ?)', (coin.name, coin.time, coin.price, coin.source))
        self.conn.commit()