from util import *
from test import BasicTest

class FlushTest(BasicTest):
    def __init__(self, s):
        self._name = "Flush Test"
        self._socket = s

    def run_all_tests(self):
        self.flush_before_login()
        self.flush_before_drop()
        self.flush_after_drop()
        self.flush_twice()

    def flush_before_login(self):
        print_info("{}: flush_before_login".format(self._name))
        ret = flush(self._socket)
        if ret:
            print_success("{}: show_before_login".format(self._name))
        else:
            print_error("{}: show_before_login".format(self._name))

    def flush_before_drop(self):
        print_info("{}: flush_before_drop".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = flush(self._socket)
        if not ret and ret2:
            print_success("{}: flush_before_drop".format(self._name))
        else:
            print_error("{}: flush_before_drop".format(self._name))
        logout(self._socket)

    def flush_after_drop(self):
        print_info("{}: flush_after_drop".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = drop_load(self._socket, 20, "CONS", "LOAD")
        ret3 = flush(self._socket)
        if not ret and not ret2 and not ret3:
            print_success("{}: flush_after_drop".format(self._name))
        else:
            print_error("{}: flush_after_drop".format(self._name))
        logout(self._socket)

    def flush_twice(self):
        print_info("{}: flush_twice".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = drop_load(self._socket, 20, "CONS", "LOAD")
        ret3 = flush(self._socket)
        ret4 = flush(self._socket)
        if not ret and not ret2 and not ret3 and ret4:
            print_success("{}: flush_twice".format(self._name))
        else:
            print_error("{}: flush_twice".format(self._name))
        logout(self._socket)
