from .base_db import BaseDb
from ...model.сoin_model import CoinModel
from ...model.alert_model import AlertModel
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
            self.cur.execute("create table if not exists alert(id INTEGER PRIMARY KEY AUTOINCREMENT, alert_price FLOAT, coin TEXT, source TEXT, opr TEXT)")
            self.cur.execute("create table if not exists crypto(id INTEGER PRIMARY KEY AUTOINCREMENT, name Text, time DATETIME, price FLOAT, source TEXT)")
        except Exception as e:
                print(f"Ошибка создания таблицы: {e}")

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

    def get_all_alert(self):
        res = []
        try:
            output = self.cur.execute('select * from alert')
            if output is not None:
                for alerts in output:
                    res.append(AlertModel(alerts[1], alerts[2], alerts[3], alerts[4], alerts[0]))
            else:
                print('Нет таких записей')
                return None
        except Exception as e:
            print(f'Ошибка получения данных: {e}')
        return res

    def add_alert(self, alert: AlertModel):
        try:
            self.cur.execute('insert into alert(alert_price, coin, source, opr) values (?, ?, ?, ?)',
                             (alert.alert_price, alert.coin, alert.source, alert.opr))
            self.conn.commit()
            return self.cur.lastrowid
        except Exception as e:
            print(f'Ошибка при вставке{e}')

    def delete_alert(self, id):
        try:
            self.cur.execute('delete from alert where id = ?', (id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f'Ошибка при удалении{e}')