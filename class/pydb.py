'''
pydb
'''

import json
from json import JSONEncoder


class MyJSONEnc(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Session:
    def __init__(self, session_id, is_legacy):
        self.session_id = session_id
        self.is_legacy = is_legacy

    def __repr__(self):
        return json.dumps(self.__dict__)


class User:
    def __init__(self, room_user="", role_bitmap=0, user_status=0):
        self.room_user = room_user
        self.role_bitmap = role_bitmap
        self.user_status = user_status
        self.sessions = {}

    def __repr__(self):
        return json.dumps(self, cls=MyJSONEnc)
        # return '{"room_user": "' + str(self.room_user) + '"' \
        #        + ', "role_bitmap": ' + str(self.role_bitmap) \
        #        + ', "user_status": ' + str(self.user_status) \
        #        + ', "sessions": ' + json.dumps(self.sessions, cls=MyJSONEnc) \
        #        + '}'

    def get_sessions(self, room_id, account_id):
        sql = "SELECT * FROM roomsession WHERE room_id='" + room_id + "'" \
              + " AND room_account='" + account_id + "'" \
              + " AND room_use'" + self.room_user + "'"

        session_id = self.room_user + ":xxxx"
        session = Session(session_id, True)
        self.sessions[session_id] = session

        session_id = self.room_user + ":yyyy"
        session = Session(session_id, False)
        self.sessions[session_id] = session

    def dump(self):
        print self


class Account:
    def __init__(self, room_account="", role_bitmap=0, account_status=0):
        self.room_account = room_account
        self.role_bitmpa = role_bitmap
        self.account_status = account_status
        self.users = {}
        self.anon_ids = []

    def __repr__(self):
        return json.dumps(self, cls=MyJSONEnc)
        # return '{"room_account": "' + str(self.room_account) + '"' \
        #        + ', "role_bitmap": ' + str(self.role_bitmpa) \
        #        + ', "account_status": ' + str(self.account_status) \
        #        + ', "users": ' + self.users.__repr__() \
        #        + ', "anon_ids": ' + json.dumps(self.anon_ids) \
        #        + '}'

    def get_user(self, room_id):
        sql = "SELECT * FROM roomusers WHERE room_id='" + room_id \
              + "' AND room_account='" + self.room_account + "'"

        user_id = self.room_account + ":0001"
        user = User(user_id)
        user.get_sessions(room_id, self.room_account)
        self.users[user_id] = user


class Room:
    def __init__(self, room_id="", room_title="", room_description="", members_limit=0, room_type=0):
        self.room_id = room_id
        self.room_title = room_title
        self.room_description = room_description
        self.room_type = room_type
        self.members_limit = members_limit
        self.accounts = {}
        self.appproperties = {}

    def __repr__(self):
        return json.dumps(self, cls=MyJSONEnc)
        # return '{"room_id": "' + str(self.room_id) + '"' \
        #        + ', "room_title": "' + str(self.room_title) + '"' \
        #        + ', "room_description": "' + str(self.room_description) + '"' \
        #        + ', "room_type": ' + str(self.room_type) \
        #        + ', "members_limit": ' + str(self.members_limit) \
        #        + ', "accounts": ' + json.dumps(self.accounts) \
        #        + ', "appproperties": ' + json.dumps(self.appproperties) \
        #        + '}'

    def get_accounts(self):
        sql = "SELECT * FROM roomusers WHERE room_id='" + self.room_id + "'"

        account_id = self.room_id + ":11111"
        account = Account(account_id)
        account.get_user(self.room_id)
        self.accounts[account_id] = account

        account_id = self.room_id + ":22222"
        account = Account(account_id, 1, 1)
        account.get_user(self.room_id)
        self.accounts[account_id] = account

        account_id = self.room_id + ":33333"
        account = Account(account_id, 7, 6)
        account.get_user(self.room_id)
        self.accounts[account_id] = account

    def dump(self):
        print self
