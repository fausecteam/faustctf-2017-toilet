from util import *
from test import BasicTest

class AdmireWorkTest(BasicTest):
    def __init__(self, s):
        self._name = "Admire Work Test"
        self._socket = s

    def run_all_tests(self):
        self.admire_before_login()
        self.admire_before_drop()
        self.admire_after_drop()
        self.admire_after_flush()
        
    def admire_before_login(self):
        print_info("{}: admire_before_login".format(self._name))
        ret = admire_work(self._socket)
        if ret == 1:
            print_success("{}: show_before_login".format(self._name))
        else:
            print_error("{}: show_before_login".format(self._name))

    def admire_before_drop(self):
        print_info("{}: admire_before_drop".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = admire_work(self._socket)
        if not ret and ret2 == 1:
            print_success("{}: admire_before_drop".format(self._name))
        else:
            print_error("{}: admire_before_drop".format(self._name))
        logout(self._socket)

    def admire_after_drop(self):
        print_info("{}: admire_after_drop".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = drop_load(self._socket, 20, "CONS", "LOAD")
        ret3 = admire_work(self._socket)
        if not ret and not ret2 and ret3 != 1:
            print_success("{}: admire_after_drop".format(self._name))
        else:
            print_error("{}: admire_after_drop".format(self._name))
        flush(self._socket)
        logout(self._socket)

    def admire_after_flush(self):
        print_info("{}: admire_after_flush".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = drop_load(self._socket, 20, "CONS", "LOAD")
        ret3 = flush(self._socket)
        ret4 = admire_work(self._socket)
        if not ret and not ret2 and not ret3 and ret4 == 1:
            print_success("{}: admire_after_flush".format(self._name))
        else:
            print_error("{}: admire_after_flush".format(self._name))
        logout(self._socket)
