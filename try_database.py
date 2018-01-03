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
                        politics INT DEFAULT'2',
                        finance INT DEFAULT'2',
                        entertainment INT DEFAULT'2',
                        sports INT DEFAULT'2',
                        society INT DEFAULT'2',
                        local INT DEFAULT'2',
                        world INT DEFAULT'2',
                        lifestyle INT DEFAULT'2',
                        health INT DEFAULT'2',
                        technology INT DEFAULT'2',
                        travel INT DEFAULT'2',
                        odd INT DEFAULT'2'
                        ) """
        self.db.cursor().execute(command)

    def select(self, chat_id, select):
        cursor = self.db.cursor()
        results=(())
        try:
            cursor.execute("SELECT %s FROM user_data WHERE chat_id = '%s'" % (select, chat_id))
            results = cursor.fetchall()
        except:
            print('Error: unable to fetch data')
        return results

    def select_all(self, select):
        cursor = self.db.cursor()
        results=(())
        try:
            cursor.execute('SELECT %s FROM user_data' % (select))
            results = cursor.fetchall()
        except:
            print('Error: unable to fetch data')
        return results

    def update(self, chat_id, kind, inc=1):
        command = "UPDATE user_data set %s = %s + %d WHERE chat_id = '%s'" % (kind, kind, inc, chat_id)
        print(command)
        self._exec(command)

    def exist(self, chat_id):
        chat_ids = self.select_all('chat_id')
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

    def close(self):
        self.db.close()

'''
db = Database()
db.update('316205244', 'politics', 3)
all_kinds = ['politics', 'finance', 'entertainment', 'sports', 'society', 'local', 'world', 'lifestyle', 'health', 'technology', 'travel', 'odd']
for x in all_kinds:
    print(db.select('316205244', x))
db.close()
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
