from util import *
from test import BasicTest
from pwn import *

class MenuTest(BasicTest):
    def __init__(self, s):
        self._name = "Menu Test"
        self._socket = s

    def run_all_tests(self):
        self.negativ_index()
        self.invalid_index()
        self.overflow_index()

    def negativ_index(self):
        print_info("{}: negative_index".format(self._name))
        menu_choice(self._socket, -1)
        ret = read_menu(self._socket)
        if ret:
            print_success("{}: negative_index".format(self._name))
        else:
            print_error("{}: negative_index".format(self._name))

    def invalid_index(self):
        print_info("{}: invalid_index".format(self._name))
        menu_choice(self._socket, 100)
        ret = read_menu(self._socket)
        if ret:
            print_success("{}: invalid_index".format(self._name))
        else:
            print_error("{}: invalid_index".format(self._name))

    def overflow_index(self):
        print_info("{}: overflow_index".format(self._name))
        menu_choice(self._socket, 2**31-1)
        ret = read_menu(self._socket)
        if ret:
            print_success("{}: overflow_index".format(self._name))
        else:
            print_error("{}: overflow_index".format(self._name))

