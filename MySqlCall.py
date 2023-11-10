import io

from mysql.connector import MySQLConnection, Error
from mysql.connector.plugins import mysql_native_password, caching_sha2_password
import configparser
import logging
import pathlib
from pathlib import Path
from datetime import date, time
from MyDBLogger import MyDBLogger
from PIL import Image

class MySqlCall:
    def __init__(self):
        # logging
        self.my_logger = MyDBLogger("MySqlCall", logging.ERROR).logger
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d, %(name)s, %(levelname)s: %(message)s',
                                      '%Y-%m-%d %H:%M:%S')

        path_config = Path(pathlib.Path.cwd(), "logs", "MySqlCall.log")
        file_log = logging.FileHandler(filename=path_config, mode="w")
        file_log.setFormatter(formatter)
        self.my_logger.addHandler(file_log)
        # ---------------------------------------------------------

        console_out = logging.StreamHandler()
        console_out.setFormatter(formatter)
        self.my_logger.addHandler(console_out)


        config = configparser.ConfigParser()
        path_config = Path(pathlib.Path.cwd(), "Config.ini")
        config.read(path_config)

        # mysql
        user = config.get("mysql", "user")
        password = config.get("mysql", "password")
        host = config.get("mysql", "host")
        database = config.get("mysql", "database")

        self.param = {
          'user': user,
          'password': password,
          'host': host,
          'database': database,
          'raise_on_warnings': False,
          'auth_plugin': 'mysql_native_password'
        }

        self.conn = None
        self.cursor = None

    def start_conn(self):
        try:
            self.conn = MySQLConnection(**self.param, autocommit=True)
            self.cursor = self.conn.cursor()
        except Error as e:
            self.my_logger.error(f"e start_conn: {e}")
        except Exception as ex:
            self.my_logger.error(f"ex start_conn: {ex}")

    def stop_conn(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Error as e:
            self.my_logger.error(f"stop_conn: {e}")

    def get_me_prices(self):
        dict = {}

        # try:
        sql = "SELECT * FROM quik_prices_view"
        self.cursor.execute(sql)

        result = self.cursor.fetchall()
        # self.my_logger.info(f"mysql get_me_prices: {result}")

        for row in result:
            dict[row[0]] = {'bid': row[1], 'bid_datetime': row[3], 'ask': row[4], 'ask_datetime': row[6]}

        # except Error as e:
        #     print(e)
        #     self.my_logger.error(f"get_me_prices: {e}")

        return dict

    def save_image(self, brief, img_byte_arr):
        sql = "update image set image = %s where brief = %s"
        self.cursor.execute(sql, (img_byte_arr, brief))

    def save_status(self, xml, datetime):
        sql = "insert into status(xml, datetime) values(%s, %s)"
        self.cursor.execute(sql, (xml, datetime))

    def load_image(self, brief):
        sql = "select image from image where brief ='" + brief + "'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()

        pil_image = Image.open(io.BytesIO(row[0]))

        pil_image.save("222.png")




if __name__ == "__main__":
    db = MySqlCall()
    db.start_conn()

    path = Path(pathlib.Path.cwd(), "images", "canvas.png")
    img_byte_arr = open(path, "rb").read()

    db.save_image("canvas", img_byte_arr)
    db.load_image("canvas")

    db.stop_conn()
