'''
pydb
'''

import json


class User:
    def __init__(self, room_user="", role_bitmap=0, user_status=0):
        self.room_user = room_user
        self.role_bitmap = role_bitmap
        self.user_status = user_status
        self.sessions = {}

    def __repr__(self):
        return '{"room_user": "' + str(self.room_user) + '"' \
               + ', "role_bitmap": ' + str(self.role_bitmap) \
               + ', "user_status": ' + str(self.user_status) \
               + ', "sessions": ' + json.dumps(self.sessions) \
               + '}'


class Account:
    def __init__(self, room_account="", role_bitmap=0, account_status=0):
        self.room_account = room_account
        self.role_bitmpa = role_bitmap
        self.account_status = account_status
        self.users = {}
        self.anon_ids = []

    def __repr__(self):
        return '{"room_account": "' + str(self.room_account) + '"' \
               + ', "role_bitmap": ' + str(self.role_bitmpa) \
               + ', "account_status": ' + str(self.account_status) \
               + ', "users": ' + self.users.__repr__() \
               + ', "anon_ids": ' + json.dumps(self.anon_ids) \
               + '}'


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
        return '{"room_id": "' + str(self.room_id) + '"' \
               + ', "room_title": "' + str(self.room_title) + '"' \
               + ', "room_description": "' + str(self.room_description) + '"' \
               + ', "room_type": ' + str(self.room_type) \
               + ', "members_limit": ' + str(self.members_limit) \
               + ', "accounts": ' + json.dumps(self.accounts) \
               + ', "appproperties": ' + json.dumps(self.appproperties) \
               + '}'
