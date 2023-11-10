import logging
import configparser
import pathlib
from pathlib import Path
from mysql.connector import MySQLConnection, Error
from mysql.connector.plugins import mysql_native_password, caching_sha2_password

class MyDBLogger:
    def __init__(self, name_logger, level):
        self.logger = logging.getLogger(name_logger)
        self.logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d, %(name)s, %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')

        handler = LogDBHandler()
        self.logger.addHandler(handler)


class LogDBHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

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


    def emit(self, record):
        log_msg = record.msg
        log_msg = log_msg.strip()
        log_msg = log_msg.replace('\'', '\'\'')

        try:
            conn = MySQLConnection(**self.param, autocommit=True)
            cursor = conn.cursor()

            sql = 'INSERT INTO log (log_level, log_levelname, log, created_by) ' + \
                'VALUES (' + \
                ''   + str(record.levelno) + ', ' + \
                '\'' + str(record.levelname) + '\', ' + \
                '\'' + str(log_msg) + '\', ' + \
                '\'' + str(record.name) + '\')'

            cursor.execute(sql)
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    log = MyDBLogger('db', logging.DEBUG)

    log.logger.info("Test 3")
