from util import *
from test import BasicTest

class LoginTest(BasicTest):
    def __init__(self, s):
        self._name = "Login Test"
        self._socket = s

    def run_all_tests(self):
        self.login_regular()
        self.login_overflow()
        self.login_twice_same_user()
        self.login_twice_different_user()
        self.logout_regular()
        self.logout_twice()
        self.logout_before_login()
        self.logout_after_drop()
        self.logout_after_flush()

    def login_regular(self):
        print_info("{}: login_regular".format(self._name))
        ret = login(self._socket, "foobar")
        if not ret:
            print_success("{}: login_regular".format(self._name))
        else:
            print_error("{}: login_regular".format(self._name))
        logout(self._socket)

    def login_overflow(self):
        print_info("{}: login_overflow".format(self._name))
        ret = login(self._socket, "A"*200)
        read_menu(self._socket)
        if not ret:
            print_success("{}: login_overflow".format(self._name))
        else:
            print_error("{}: login_overflow".format(self._name))
        logout(self._socket)

    def login_twice_same_user(self):
        print_info("{}: login_twice_same_user".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = login(self._socket, "foobar")
        if not ret and ret2:
            print_success("{}: login_twice_same_user".format(self._name))
        else:
            print_error("{}: login_twice_same_user".format(self._name))
        logout(self._socket)

    def login_twice_different_user(self):
        print_info("{}: login_twice_different_user".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = login(self._socket, "barfoo")
        if not ret and ret2:
            print_success("{}: login_twice_different_user".format(self._name))
        else:
            print_error("{}: login_twice_different_user".format(self._name))
        logout(self._socket)

    def logout_regular(self):
        print_info("{}: logout_regular".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = logout(self._socket)
        if not ret and not ret2:
            print_success("{}: logout_regular".format(self._name))
        else:
            print_error("{}: logout_regular".format(self._name))

    def logout_twice(self):
        print_info("{}: logout_twice".format(self._name))
        ret = login(self._socket, "foobar")
        ret2= logout(self._socket)
        ret3 = logout(self._socket)
        if not ret and not ret2 and ret3:
            print_success("{}: logout_twice".format(self._name))
        else:
            print_error("{}: logout_twice".format(self._name))

    def logout_before_login(self):
        print_info("{}: logout_before_login".format(self._name))
        ret = logout(self._socket)
        if ret:
            print_success("{}: logout_before_login".format(self._name))
        else:
            print_error("{}: logout_before_login".format(self._name))

    def logout_after_drop(self):
        print_info("{}: logout_after_drop".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = drop_load(self._socket, 30, "CONS", "LOAD")
        ret3 = logout(self._socket)
        if not ret and not ret2 and ret3:
            print_success("{}: logout_after_drop".format(self._name))
        else:
            print_error("{}: logout_after_drop".format(self._name))
        flush(self._socket)
        logout(self._socket)

    def logout_after_flush(self):
        print_info("{}: logout_after_flush".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = drop_load(self._socket, 30, "CONS", "LOAD")
        ret3 = flush(self._socket)
        ret4 = logout(self._socket)
        if not ret and not ret2 and not ret3 and not ret4:
            print_success("{}: logout_after_flush".format(self._name))
        else:
            print_error("{}: logout_after_flush".format(self._name))

