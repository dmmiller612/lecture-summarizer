import sqlite3


class ConnectionHandler(object):

    __instance = None

    def __init__(self, conn):
        self.conn = conn
        ConnectionHandler.__instance = self

    @staticmethod
    def get_conn():
        if ConnectionHandler.__instance is None:
            ConnectionHandler(sqlite3.connect('data.db'))
        return ConnectionHandler.__instance.conn
