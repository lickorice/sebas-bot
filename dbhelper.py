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
        c.execute('''CREATE TABLE IF NOT EXISTS admin_list(
                        id INTEGER PRIMARY KEY,
                        userID TEXT,
                        serverID TEXT,
                        UNIQUE(userID, serverID)
        )''')
        db.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS mod_list(
                        id INTEGER PRIMARY KEY,
                        userID TEXT,
                        serverID TEXT,
                        UNIQUE(userID, serverID)
        )''')
        db.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS v_channels_list(
                        id INTEGER PRIMARY KEY,
                        serverID TEXT UNIQUE,
                        channelID TEXT UNIQUE
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

    def insertAdmin(self, userID, serverID):
        # inserts a row to the DM Channels list
        c = db.cursor()
        c.execute('''INSERT INTO admin_list(userID, serverID)
                    VALUES(?, ?)''', (userID, serverID))
        print('[ DB- ] : {} inserted into admins database'.format(userID))
        db.commit()

    def insertMod(self, userID, serverID):
        # inserts a row to the DM Channels list
        c = db.cursor()
        c.execute('''INSERT INTO mod_list(userID, serverID)
                    VALUES(?, ?)''', (userID, serverID))
        print('[ DB- ] : {} inserted into admins database'.format(userID))
        db.commit()

    def insertVerifChannel(self, serverID, channelID):
        # inserts a row to the DM Channels list
        c = db.cursor()
        c.execute('''INSERT INTO v_channels_list(serverID, channelID)
                    VALUES(?, ?)''', (serverID, channelID))
        db.commit()

    def fetchDMChannelID(self, userID):
        # returns a DM channel ID when given a user ID
        c = db.cursor()
        c.execute('''SELECT privatechannelID FROM dm_list WHERE userID =?''',
                  (userID,))
        channelID = c.fetchone()
        return channelID[0]

    def fetchPendingServerID(self, userID):
        # returns a server ID when given a user ID where the user is pending.
        c = db.cursor()
        c.execute('''SELECT serverID FROM pending_list WHERE userID = ?''',
                  (userID,))
        serverID = c.fetchone()
        return serverID[0]

    def fetchVerifyChannel(self, serverID):
        c = db.cursor()
        c.execute('''SELECT channelID FROM v_channels_list
                    WHERE serverID = ?''',
                  (serverID,))
        channelID = c.fetchone()
        return channelID[0]

    def fetchallAdmins(self):
        c = db.cursor()
        c.execute('''SELECT userID, serverID FROM admin_list''')
        adminList = c.fetchall()
        return adminList

    def fetchallMods(self):
        c = db.cursor()
        c.execute('''SELECT userID, serverID FROM mod_list''')
        modList = c.fetchall()
        return modList

    def fetchallVChannels(self):
        c = db.cursor()
        c.execute('''SELECT serverID, channelID FROM v_channels_list''')
        VChannelList = c.fetchall()
        return VChannelList

    def dropPending(self, userID):
        c = db.cursor()
        c.execute('''DELETE FROM pending_list WHERE userID = ?''',
                  (userID,))
        db.commit()

    def dropAdmin(self, userID, serverID):
        c = db.cursor()
        c.execute('''DELETE FROM mod_list WHERE(userID = ?
                    AND serverID = ?)''', (userID, serverID))
        db.commit()

    def dropMod(self, userID, serverID):
        c = db.cursor()
        c.execute('''DELETE FROM admin_list WHERE(userID = ?
                    AND serverID = ?)''', (userID, serverID))
        db.commit()

    def dropVerifyChannel(self, serverID, channelID):
        c = db.cursor()
        c.execute('''DELETE FROM v_channels_list WHERE(serverID = ?
                    AND channelID = ?)''', (serverID, channelID))
        db.commit()
