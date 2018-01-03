import pymysql

class Database:
    def __init__(self):
        with open('password.txt') as f:
            password = f.readline().strip('\n')
        self.db = pymysql.connect("localhost", "root", password, "news_bot_data")

    def insert(self, chat_id, username):
        self._exec("INSERT INTO user_data(chat_id, username) VALUES('%s', '%s')" % (chat_id, username))

    def create(self):
        command =   """ CREATE TABLE user_data (
                        chat_id VARCHAR(30) UNIQUE,
                        username VARCHAR(30) NOT NULL,
                        politics INT DEFAULT'0',
                        finance INT DEFAULT'0',
                        entertainment INT DEFAULT'0',
                        sports INT DEFAULT'0',
                        society INT DEFAULT'0',
                        local INT DEFAULT'0',
                        world INT DEFAULT'0',
                        lifestyle INT DEFAULT'0',
                        health INT DEFAULT'0',
                        technology INT DEFAULT'0',
                        travel INT DEFAULT'0',
                        odd INT DEFAULT'0'
                        ) """
        self.db.cursor().execute(command)

    def select(self, select):
        cursor = self.db.cursor()
        results=(())
        try:
            cursor.execute('SELECT %s FROM user_data' % (select))
            results = cursor.fetchall()
        except:
            print('Error: unable to fetch data')
        print(results)
        return results

    def update(self, chat_id, kind, inc=1):
        command = "UPDATE user_data set %s = %s + %d WHERE %s = '%s'" % (kind, kind, inc, chat_id, chat_id)
        print(command)
        self._exec(command)

    def exist(self, chat_id):
        chat_ids = self.select('chat_id')
        for x in chat_ids:
            if x[0] == chat_id:
                return True
        return False

    def _exec(self, command):
        try:
            self.db.cursor().execute(command)
            self.db.commit()
        except:
            self.db.rollback()
        self.close()

    def close(self):
        self.db.close()

'''
db = Database()
db.create()
db.insert('12341234', 'lalala')
print(db.select('*'))
db.update('lalala', "finance", 4)
db.insert('43214321', 'qqqq')
print(db.exist('lalala'))
print(db.exist('lala'))
# init(db)
# insert(db, 'lalala')
update('lalala', 'finance', 2)
print(select(db, '*'))
print(select(db, 'username'))

'''
