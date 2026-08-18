from .base_db import BaseDb
from ...model.coin_model import CoinModel
from ...model.alert_model import AlertModel
import sqlite3
import json


class SqlLiteDb(BaseDb):
    def __init__(self, db: str) -> None:
        super().__init__(db)
        self.connection()

    def connection(self) -> None:
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread = False)
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")

        try:
            cur = self.conn.cursor()
            cur.execute("create table if not exists alert(id INTEGER PRIMARY KEY AUTOINCREMENT, alert_type TEXT, coin TEXT, source TEXT, params TEXT)")
            cur.execute("create table if not exists crypto(id INTEGER PRIMARY KEY AUTOINCREMENT, name Text, time DATETIME, price FLOAT, source TEXT)")
        except Exception as e:
                print(f"Ошибка создания таблицы: {e}")

    def get_history_price(self, coin: str, limit: int=10000) -> list[CoinModel] | None:
        res =[]
        try:
            cur = self.conn.cursor()
            output = cur.execute('select * from crypto where name = ? limit ?', (coin, limit)).fetchall()
            if output is not None:
                for coins in output:
                    res.append(CoinModel(coins[1], coins[2], coins[3], coins[4]))
            else:
                print('Нет таких записей')
                return None
        except Exception as e:
            print(f'Ошибка получения данных: {e}')
        return res

    def get_coin_price(self, coin: str, source: str) -> CoinModel | None:
        try:
            cur = self.conn.cursor()
            output = cur.execute('select * from crypto where name = ? and source = ? order by time desc limit 1', (coin, source)).fetchone()
            if output is not None:
                return CoinModel(output[1], output[2], output[3], output[4])
            else:
                print('Нет таких записей')
                return None
        except Exception as e:
            print(f'Ошибка получения данных: {e}')
            return None

    def save_cache(self, coin: CoinModel) -> None:
        cur = self.conn.cursor()
        cur.execute('insert into crypto(name, time, price, source) values (?, ?, ?, ?)', (coin.name, coin.time, coin.price, coin.source))
        self.conn.commit()

    def get_all_alert(self) -> list[AlertModel] | None:
        res = []
        try:
            cur = self.conn.cursor()
            output = cur.execute('select * from alert')
            if output is not None:
                for alerts in output:
                    res.append(AlertModel(alert_type=alerts[1], coin=alerts[2], source=alerts[3], id=alerts[0], **json.loads(alerts[4])))
            else:
                print('Нет таких записей')
                return None
        except Exception as e:
            print(f'Ошибка получения данных: {e}')
            return None
        return res

    def add_alert(self, alert: AlertModel) -> int | None:
        try:
            cur = self.conn.cursor()
            cur.execute('insert into alert(alert_type, coin, source, params) values (?, ?, ?, ?)',
                             (alert.alert_type, alert.coin, alert.source, json.dumps(alert.alert_params)))
            self.conn.commit()
            return cur.lastrowid
        except Exception as e:
            print(f'Ошибка при вставке{e}')
            return None

    def delete_alert(self, id: int) -> bool:
        try:
            cur = self.conn.cursor()
            cur.execute('delete from alert where id = ?', (id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f'Ошибка при удалении{e}')
            return False