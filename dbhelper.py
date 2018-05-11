import sqlite3

database_directory = 'data/database.db'

print("[ LOG ] : Importing lickorce's dbhelper...")
db = sqlite3.connect(database_directory)
print("[ LOG ] : Database successfully connected at", database_directory)


class DBHelper():
    def init(self):
        # this function initializes the database
        c = db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS pending_list(
                        id INTEGER PRIMARY KEY,
                        userID TEXT,
                        serverID TEXT,
                        pending BOOLEAN
        )''')
        db.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS dm_list(
                        id INTEGER PRIMARY KEY,
                        userID TEXT unique,
                        privatechannelID TEXT unique
        )''')
        db.commit()

    def insertPending(self, userID, serverID, pending):
        # inserts a row to the pending list
        c = db.cursor()
        c.execute('''INSERT INTO pending_list(userID, serverID, pending)
                    VALUES(?, ?, ?)''', (userID, serverID, pending,))
        print('[ DB- ] : {} inserted into pending database'.format(userID))
        db.commit()

    def insertDMList(self, userID, channelID):
        # inserts a row to the DM Channels list
        c = db.cursor()
        c.execute('''INSERT INTO dm_list(userID, privatechannelID)
                    VALUES(?, ?)''', (userID, channelID))
        print('[ DB- ] : {} inserted into dm channels database'.format(userID))
        db.commit()

    def fetchDMChannelID(self, userID):
        # returns a DM channel ID when given a user ID
        c = db.cursor()
        c.execute('''SELECT privatechannelID FROM dm_list WHERE userID =?''',
                  (userID,))
        channelID = c.fetchone()
        return channelID

    def fetchPendingServerID(self, userID):
        # returns a server ID when given a user ID where the user is pending.
        c = db.cursor()
        c.execute('''SELECT serverID FROM pending_list WHERE userID =?
                    AND pending == TRUE''',
                  (userID,))
        serverID = c.fetchone()
        return serverID

    def updatePending(self, userID, serverID, pending):
        c = db.cursor()
        c.execute('''UPDATE pending_list SET pending = FALSE,
                WHERE userID = ? AND serverID = ?''',
                  (userID, serverID,))
        db.commit()
