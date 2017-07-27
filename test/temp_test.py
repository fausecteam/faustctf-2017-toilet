from util import *
from test import BasicTest

class TempTest(BasicTest):
    def __init__(self, s):
        self._name = "Temp Test"
        self._socket = s

    def run_all_tests(self):
        self.temp_before_login()
        self.temp_after_login()
        self.temp_low_value()
        self.temp_high_value()
        self.temp_negative_value()
        self.temp_overflow_value()
        self.temp_overflow2_value()
        self.temp_valid_value()

    def temp_before_login(self):
        print_info("{}: temp_before_login".format(self._name))
        ret = change_seat_temp(self._socket, 20)
        if ret:
            print_success("{}: temp_before_login".format(self._name))
        else:
            print_error("{}: temp_before_login".format(self._name))

    def temp_after_login(self):
        print_info("{}: temp_after_login".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = change_seat_temp(self._socket, 20)
        if not ret and not ret2:
            print_success("{}: temp_after_login".format(self._name))
        else:
            print_error("{}: temp_after_login".format(self._name))
        logout(self._socket)

    def temp_low_value(self):
        print_info("{}: temp_low_value".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = change_seat_temp(self._socket, 5)
        if not ret and ret2:
            print_success("{}: temp_low_value".format(self._name))
        else:
            print_error("{}: temp_low_value".format(self._name))
        logout(self._socket)

    def temp_high_value(self):
        print_info("{}: temp_high_value".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = change_seat_temp(self._socket, 100)
        if not ret and ret2:
            print_success("{}: temp_high_value".format(self._name))
        else:
            print_error("{}: temp_high_value".format(self._name))
        logout(self._socket)

    def temp_negative_value(self):
        print_info("{}: temp_negative_value".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = change_seat_temp(self._socket, -10)
        if not ret and ret2:
            print_success("{}: temp_negative_value".format(self._name))
        else:
            print_error("{}: temp_negative_value".format(self._name))
        logout(self._socket)

    def temp_overflow_value(self):
        print_info("{}: temp_overflow_value".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = change_seat_temp(self._socket, 2**16)
        if not ret and ret2:
            print_success("{}: temp_overflow_value".format(self._name))
        else:
            print_error("{}: temp_overflow_value".format(self._name))
        logout(self._socket)

    def temp_overflow2_value(self):
        print_info("{}: temp_overflow2_value".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = change_seat_temp(self._socket, 2**16+10)
        if not ret and not ret2:
            print_success("{}: temp_overflow2_value".format(self._name))
        else:
            print_error("{}: temp_overflow2_value".format(self._name))
        logout(self._socket)

    def temp_valid_value(self):
        print_info("{}: temp_valid_value".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = change_seat_temp(self._socket, 30)
        if not ret and not ret2:
            print_success("{}: temp_valid_value".format(self._name))
        else:
            print_error("{}: temp_valid_value".format(self._name))
        logout(self._socket)
