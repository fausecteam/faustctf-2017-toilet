from util import *
from test import BasicTest
from re import findall
from random import choice
from time import sleep

class SettingsTest(BasicTest):
    def __init__(self, s):
        self._name = "Settings Test"
        self._socket = s

    def run_all_tests(self):
        self.show_before_login()
        self.show_after_login()
        self.change_seat_temp()
        self.change_max_weight()
        self.change_last_visit()
        self.persistant_settings()

    def show_before_login(self):
        print_info("{}: settings_before_login".format(self._name))
        ret = show_settings(self._socket)
        if ret:
            print_success("{}: show_before_login".format(self._name))
        else:
            print_error("{}: show_before_login".format(self._name))

    def show_after_login(self):
        print_info("{}: show_after_login".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = show_settings(self._socket)
        if not ret and ret2 != 1:
            print_success("{}: show_after_login".format(self._name))
        else:
            print_error("{}: show_after_login".format(self._name))
        logout(self._socket)

    def change_seat_temp(self):
        print_info("{}: change_seat_temp".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = show_settings(self._socket)
        ret3 = change_seat_temp(self._socket, 36)
        ret4 = show_settings(self._socket)
        if not ret and not ret3 and ret2 != 1 and ret4 != 1 and ret2 != ret4:
            print_success("{}: change_seat_temp".format(self._name))
        else:
            print_error("{}: change_seat_temp".format(self._name))
        logout(self._socket)

    def change_max_weight(self):
        print_info("{}: change_max_weight".format(self._name))
        # need a random name here!
        ret = login(self._socket, ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(6)))
        ret2 = show_settings(self._socket)
        ret3 = drop_load(self._socket, 50, "CONS", "LOAD")
        ret4 = show_settings(self._socket)
        ret5 = flush(self._socket)
        if not ret and not ret3 and not ret5 and ret2 != 1 and ret4 != 1 and ret2 != ret4:
            print_success("{}: change_max_weight".format(self._name))
        else:
            print_error("{}: change_max_weight".format(self._name))
        logout(self._socket)

    def change_last_visit(self):
        print_info("{}: change_last_visit".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = show_settings(self._socket)
        ret3 = logout(self._socket)
        sleep(1)
        ret4 = login(self._socket, "foobar")
        ret5 = show_settings(self._socket)
        if not ret and not ret3  and not ret4 and ret2 != 1 and ret5 != 1 and ret2 != ret5:
            print_success("{}: change_last_visit".format(self._name))
        else:
            print_error("{}: change_last_visit".format(self._name))
        logout(self._socket)

    def persistant_settings(self):
        print_info("{}: persistent_settings".format(self._name))
        ret = login(self._socket, "foobar")
        ret3 = change_seat_temp(self._socket, 42)
        ret2 = show_settings(self._socket)
        ret3 = change_seat_temp(self._socket, 36)
        ret4 = show_settings(self._socket)
        ret5 = logout(self._socket)
        ret6 = login(self._socket, "foobar")
        ret7 = show_settings(self._socket)
        if not ret and not ret3  and not ret5 and not ret6 and ret2 != 1 and ret4 != 1 and ret7 != 1:
            val = findall(r"Seat temperature: ([\d]*)", ret2[3])[0]
            val1 = re.findall(r"Seat temperature: ([\d]*)", ret4[3])[0]
            val2 = re.findall(r"Seat temperature: ([\d]*)", ret7[3])[0]
            if val != val1 and val1 == val2:
                print_success("{}: persistent_settings".format(self._name))
            else:
                print_error("{}: persistent_settings".format(self._name))
        else:
            print_error("{}: persistent_settings".format(self._name))
        logout(self._socket)

