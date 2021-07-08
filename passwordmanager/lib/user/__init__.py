import sqlite3
import uuid
import hashlib


class User(object):

    def __init__(self, username=None, password=None):
        self.name = username.strip().upper()
        self.password = password
        self.conn = sqlite3.connect('userdata\\database.db')
        self.cursor = self.conn.cursor()
        self.exist = self.checkUser()
        self.authenticated = False

    def checkUser(self):
        name = self.hashCred(self.name)
        self.cursor.execute(f'SELECT * FROM user;')
        cont = 0
        for row in self.cursor:
            equal = self.decryptCred(self.name, row[0])
            if equal:
                cont += 1
        if cont == 1:
            return True
        else:
            return False

    def createDataBase(self):
        self.cursor.execute(f'CREATE TABLE {self.name}passwords(account text,login text,password text);')
        self.conn.commit()

    def insertUserCred(self):
        name = self.hashCred(self.name)
        password = self.hashCred(self.password)
        self.cursor.execute(f"INSERT INTO user(username,userpass) VALUES (?,?);", [name, password])
        self.conn.commit()

    def authenticate(self):
        name = self.hashCred(self.name)
        psw = self.hashCred(self.password)
        self.cursor.execute(f'SELECT * FROM user;')
        for row in self.cursor:
            nameEqual = self.decryptCred(self.name, row[0])
            pswEqual = self.decryptCred(self.password, row[1])
            if nameEqual:
                if pswEqual:
                    self.authenticated = True
                else:
                    self.authenticated = False

    def writeData(self, account, login, password):
        self.cursor.execute(f"INSERT INTO {self.name}passwords(account,login,password) VALUES (?,?,?);",
                            (account.encode('utf-32'), login.encode('utf-32'), password.encode('utf-32')))
        self.conn.commit()

    def readData(self):
        self.cursor.execute(f'SELECT * FROM {self.name}passwords;')
        rows = list()
        for row in self.cursor:
            rows.append([string.decode('utf-32') for string in row])
        return rows

    def editData(self, account, login, password):
        self.cursor.execute(f'UPDATE {self.name}passwords set account=?, login=?, password=? WHERE account=?;',
                            (account.encode('utf-32'), login.encode('utf-32'),
                             password.encode('utf-32'), account.encode('utf-32')))
        self.conn.commit()

    def deleteData(self, account):
        self.cursor.execute(f'DELETE FROM {self.name}passwords WHERE account=?;', [account.encode('utf-32')])
        self.conn.commit()

    def disconnect(self):
        self.conn.close()

    def hashCred(self, cred):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + cred.encode()).hexdigest() + ':' + salt

    def decryptCred(self, clear, hashed):
        decPsw, salt = hashed.split(':')
        return decPsw == hashlib.sha256(salt.encode() + clear.encode()).hexdigest()

