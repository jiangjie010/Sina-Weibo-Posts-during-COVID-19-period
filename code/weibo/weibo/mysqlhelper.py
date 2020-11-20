import pymysql


class MysqlHelper(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', database='spider',
                                    charset='utf8mb4')
        self.cursor = self.conn.cursor()

    def execute_insert_sql(self, insert_sql, data):
        self.cursor.execute(insert_sql, data)
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    m = MysqlHelper()
    insert_sql = 'INSERT INTO weibo_chenglong(create_at,content) VALUES(%s,%s)'
    data = ('10-1', 'ddddd')
    m.execute_insert_sql(insert_sql, data)
