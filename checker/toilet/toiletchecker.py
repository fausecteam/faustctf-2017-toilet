#!/usr/bin/env python3

from ctf_gameserver.checker import BaseChecker, OK, NOTWORKING, TIMEOUT, NOTFOUND
from telnetlib import Telnet
from re import findall
from socket import timeout
from random import choice, randint
from string import digits, ascii_uppercase
from hashlib import sha256

class Remote(Telnet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def recvline(self):
        try:
            return self.read_until(b'\n')
        except EOFError:
            return None
        except timeout:
            return None

    def recvlines(self, num):
        lines = []
        if num <= 0:
            return lines
        for i in range(0,num):
            line = self.recvline()
            if line is None:
                return None
            lines.append(line)
        return lines

    def recvuntil(self, text):
        try:
            return self.read_until(text.encode('utf-8'))
        except EOFError:
            return None
        except timeout:
            return None

    def sendline(self, text):
        try:
            self.write(("{}\n".format(text)).encode('utf-8'))
            return 1
        except EOFError:
            return None


class ToiletChecker(BaseChecker):

    def __init__(self, tick, team, service, ip):
        BaseChecker.__init__(self, tick, team, service, ip)
        self._tick = tick
        self._team = team
        self._service = service
        self._ip = ip
        self._port = 5743
        self._sock = None


    def close_sock(self):
        self._sock.close()
        self._sock = None

    def check_service(self):
        name = self.genRandString(10)
        self._sock = self.connect()
        if self._sock is None:
            return TIMEOUT
        if self.login(self._sock, name) is None:
            self.close_sock()
            return NOTWORKING
        temp = randint(-10, 100)
        if temp < 10 or temp > 60:
            if self.change_seat_temp(self._sock, temp) is not None:
                self.close_sock()
                return NOTWORKING
        else:
            if self.change_seat_temp(self._sock, temp) is None:
                self.close_sock()
                return NOTWORKING
            stored_temp = self.get_temp(self.get_settings(self._sock))
            if stored_temp is None or stored_temp != str(temp):
                self.close_sock()
                return NOTWORKING
        if self.change_flush_func(self._sock, 1) is None:
            self.close_sock()
            return NOTWORKING
        if self.drop_load(self._sock, self.genRandString(29), self.genRandString(30)) is None:
            self.close_sock()
            return NOTWORKING
        if self.show_latest_notes(self._sock) is None:
            self.close_sock()
            return NOTWORKING
        if self.logout(self._sock, False) is None:
            self.close_sock()
            return NOTWORKING
        self.close_sock()
        return OK

    def place_flag(self):
        name = self.get_flag(self._tick)
        self._sock = self.connect()
        if self._sock is None:
            return TIMEOUT
        if self.login(self._sock, name) is None:
            self.close_sock()
            return NOTWORKING
        if self.drop_load(self._sock, self.genRandString(10), self.genRandString(30)) is None:
            self.close_sock()
            return NOTWORKING
        if self.flush(self._sock) is None:
            self.close_sock()
            return NOTWORKING
        if self.logout(self._sock, True) is None:
            self.close_sock()
            return NOTWORKING
        self.close_sock()
        return OK

    def check_flag(self, tick):
        name = self.get_flag(tick)
        if self._sock is None:
            self._sock = self.connect()
            if self._sock is None:
                return TIMEOUT
        if self.login(self._sock, name) is None:
            self.close_sock()
            return NOTWORKING
        profile_name = self.get_name(self.get_settings(self._sock))
        if profile_name is None:
            self.close_sock()
            return NOTWORKING
        if name != profile_name:
            self.close_sock()
            return NOTFOUND
        name_hash = sha256()
        name_hash.update(name.encode('utf-8'))
        log = self.get_log(self._sock)
        if log is None:
            self.close_sock()
            return NOTWORKING
        if self.find_log_entry(self._sock, log, name_hash.hexdigest()) is False:
            self.close_sock()
            return NOTFOUND
        if self.logout(self._sock, False) is None:
            self.close_sock()
            return NOTWORKING
        self.close_sock()
        return OK

    def genRandString(self, N):
        return ''.join(choice(ascii_uppercase + digits) for _ in range(N))

    def connect(self):
        try:
            s = Remote(self._ip, self._port)
        except:
            return None
        if self.read_menu(s) is None:
            return None
        return s

    def read_menu(self, s):
        return s.recvuntil("Your choice: ")

    def login(self, s, name):
        if s.sendline('1') is None:
            return None
        if s.recvuntil('Please give me your name: ') is None:
            return None
        if s.sendline(name) is None:
            return None
        if self.read_menu(s) is None:
            return None
        return 1

    def change_seat_temp(self, s, temp):
        if s.sendline('2') is None:
            return None
        if s.recvuntil('Please give me the new temperature: ') is None:
            return None
        if s.sendline(str(temp)) is None:
            return None
        resp = s.recvlines(2)[1]
        if self.read_menu(s) is None:
            return None
        if "Alright, let me arrange that for you." not in resp.decode('utf-8'):
            return None
        return 1

    def change_flush_func(self, s, choice):
        if s.sendline('3') is None:
            return None
        if s.recvuntil('Your choice: ') is None:
            return None
        if s.sendline(str(choice)) is None:
            return None
        resp = s.recvlines(2)[1]
        if self.read_menu(s) is None:
            return None
        if "Something went wrong, please try again!" in resp.decode('utf-8'):
            return None
        return 1

    def get_settings(self, s):
        if (s.sendline('4') is None):
            return None
        ret = s.recvuntil('1. Login')
        if self.read_menu(s) is None:
            return None
        return ret

    def get_id(self, text):
        if text is None:
            return None
        hits = findall(r'ID: (\d*)', text.decode('utf-8'))
        if not hits:
            return None
        return hits[0]

    def get_name(self, text):
        if text is None:
            return None
        hits = findall(r'Name: ([\w+_/]*)', text.decode('utf-8'))
        if not hits:
            return None
        return hits[0]

    def get_temp(self, text):
        if text is None:
            return None
        hits = findall(r'Seat temperature: (\d*)', text.decode('utf-8'))
        if not hits:
            return None
        return hits[0]

    def drop_load(self, s, cons, content):
        if (s.sendline('5') is None):
            return None
        ret = s.recvuntil('the consistency:')
        if not ret:
            return None
        if (s.sendline(cons) is None):
            return None
        ret = s.recvline()
        if not ret:
            return None
        if (s.sendline(content) is None):
            return None
        if self.read_menu(s) is None:
            return None
        return 1

    def show_latest_notes(self, s):
        if (s.sendline('6') is None):
            return None
        ret = s.recvlines(2)[1]
        if "Here are your notes:" not in ret.decode('utf-8'):
            self.read_menu(s)
            return None
        notes = s.recvline()
        if not notes:
            return None
        if self.read_menu(s) is None:
            return None
        return notes

    def flush(self, s):
        if (s.sendline('7') is None):
            return None
        ret = s.recvuntil('1. Login')
        if ret is not None and b'Going to flush now' not in ret:
            return None
        self.read_menu(s)
        return 1

    def get_log(self, s):
        if s.sendline('8') is None:
            return None
        ret = s.recvuntil('1. Login')
        if self.read_menu(s) is None:
            return None
        return ret

    def find_log_entry(self, s, hs, profile_id):
        try:
            lines = hs.decode('utf-8').split('\n')
        except:
            return False
        for line in lines:
            hits = findall(r'#==== ([\da-f]{64}) ==== | ==== [\d:]* ====#', line)
            if not hits:
                continue
            curr_id = hits[0]
            if profile_id == curr_id:
                return True
        return False

    def logout(self, s, store):
        if (s.sendline('9') is None):
            return None
        s.recvline()
        if store:
            s.sendline('y')
            ret = s.recvuntil('1. Login')
            if ret is None or b'Hope you feel relieved now! Come back soon!' not in ret:
                return None
        else:
            s.sendline('n')
        self.read_menu(s)
        return 1

    def exit(self, s):
        if (s.sendline('10') is None):
            return None
        return 1

