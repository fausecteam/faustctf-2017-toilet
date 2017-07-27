from util import *
from test import BasicTest

class DropLoadTest(BasicTest):
    def __init__(self, s):
        self._name = "Drop Load Test"
        self._socket = s

    def run_all_tests(self):
        self.drop_before_login()
        self.drop_after_login()
        self.negative_weight()
        self.zero_weight()
        self.overflow_weight()
        self.overflow_consistency()
        self.overflow_load()

    def drop_before_login(self):
        print_info("{}: drop_before_login".format(self._name))
        ret = drop_load(self._socket, 50, "CONS", "LOAD")
        if ret:
            print_success("{}: drop_before_login".format(self._name))
        else:
            print_error("{}: drop_before_login".format(self._name))

    def drop_after_login(self):
        print_info("{}: drop_after_login".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = drop_load(self._socket, 50, "CONS", "LOAD")
        if not ret and not ret2:
            print_success("{}: drop_after_login".format(self._name))
        else:
            print_error("{}: drop_after_login".format(self._name))
        flush(self._socket)
        logout(self._socket)

    def negative_weight(self):
        print_info("{}: negative_weight".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = drop_load(self._socket, -50, "CONS", "LOAD")
        if not ret and not ret2:
            print_success("{}: negative_weight".format(self._name))
        else:
            print_error("{}: negative_weight".format(self._name))
        flush(self._socket)
        logout(self._socket)

    def zero_weight(self):
        print_info("{}: zero_weight".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = drop_load(self._socket, 0, "CONS", "LOAD")
        if not ret and ret2:
            print_success("{}: zero_weight".format(self._name))
        else:
            print_error("{}: zero_weight".format(self._name))
        logout(self._socket)


    def overflow_weight(self):
        print_info("{}: overflow_weight".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = drop_load(self._socket, 2**16+10, "CONS", "LOAD")
        if not ret and not ret2:
            print_success("{}: overflow_weight".format(self._name))
        else:
            print_error("{}: overflow_weight".format(self._name))
        flush(self._socket)
        logout(self._socket)

    def overflow_consistency(self):
        print_info("{}: overflow_consistency".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = drop_load(self._socket, 50, "A"*40, "LOAD")
        read_menu(self._socket)
        ret3 = admire_work(self._socket)
        if not ret and not ret2 and "A"*10 in ret3:
            print_success("{}: overflow_consistency".format(self._name))
        else:
            print_error("{}: overflow_consistency".format(self._name))
        flush(self._socket)
        logout(self._socket)

    def overflow_load(self):
        print_info("{}: overflow_load".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = drop_load(self._socket, 1, "C", "A"*20)
        read_menu(self._socket)
        if not ret and not ret2:
            print_success("{}: overflow_load".format(self._name))
        else:
            print_error("{}: overflow_load".format(self._name))
        flush(self._socket)
        logout(self._socket)
