from util import *
from test import BasicTest
from pwn import *
from re import findall
from time import sleep

class StorageTest(BasicTest):
    def __init__(self, local, ip, port, path):
        self._name = "Storage Test"
        self._local = local
        self._ip = ip
        self._port = port
        self._path = path

    def __connect(self):
        if self._local:
            r = process(self._path)
            read_menu(r)
            return r
        else:
            r = remote(self._ip,self._port)
            read_menu(r)
            return r

    def __login(self):
        s = self.__connect()
        ret = login(s, "foobar")
        if ret:
            return None
        else:
            return s

    def __logout(self, s):
        ret2 = logout(s)
        exit(s)
        return ret2

    def __get_set_info(self, s, field, index):
        out = show_settings(s)
        val = findall(r"{} ([\w:]*)".format(field), out[index])[0]
        return val

    def run_all_tests(self):
        self.seat_temp_storage()
        self.max_weight_storage()
        self.name_storage()
        self.last_visit_storage()
        self.highscore_storage()

    def seat_temp_storage(self):
        print_info("{}: seat_temp_storage".format(self._name))
        s = self.__login()
        if not s:
            print_error("{}: seat_temp_storage".format(self._name))
            return
        change_seat_temp(s, 45)
        temp_before = self.__get_set_info(s, "Seat temperature:", 3)
        ret = self.__logout(s)
        if ret:
            print_error("{}: seat_temp_storage".format(self._name))
            return

        s.close()
        s = self.__login()
        if not s:
            print_error("{}: seat_temp_storage".format(self._name))
            return
        temp_after = self.__get_set_info(s, "Seat temperature:", 3)
        ret = self.__logout(s)
        if ret:
            print_error("{}: seat_temp_storage".format(self._name))
            return

        if temp_before == temp_after:
            print_success("{}: seat_temp_storage".format(self._name))
        else:
            print_error("{}: seat_temp_storage".format(self._name))
        s.close()

    def max_weight_storage(self):
        print_info("{}: max_weight_storage".format(self._name))
        s = self.__login()
        if not s:
            print_error("{}: max_weight_storage".format(self._name))
            return
        ret = drop_load(s, 40, "CONS", "LOAD")
        if ret:
            print_error("{}: max_weight_storage".format(self._name))
            return
        ret = flush(s)
        if ret:
            print_error("{}: max_weight_storage".format(self._name))
            return
        max_before = self.__get_set_info(s, "Max. weight:", 4)
        ret = self.__logout(s)
        if ret:
            print_error("{}: max_weight_storage".format(self._name))
            return

        s.close()
        s = self.__login()
        if not s:
            print_error("{}: max_weight_storage".format(self._name))
            return
        max_after = self.__get_set_info(s, "Max. weight:", 4)
        ret = self.__logout(s)
        if ret:
            print_error("{}: max_weight_storage".format(self._name))
            return

        if max_before == max_after:
            print_success("{}: max_weight_storage".format(self._name))
        else:
            print_error("{}: max_weight_storage".format(self._name))
        s.close()

    def name_storage(self):
        print_info("{}: name_storage".format(self._name))
        s = self.__login()
        if not s:
            print_error("{}: name_storage".format(self._name))
            return
        name_before = self.__get_set_info( s, "Name:", 2)
        id_before = self.__get_set_info(s, "ID:", 1)
        ret = self.__logout(s)
        if ret:
            print_error("{}: name_storage".format(self._name))
            return

        s.close()
        s = self.__login()
        if not s:
            print_error("{}: name_storage".format(self._name))
            return
        name_after = self.__get_set_info(s, "Name:", 2)
        id_after = self.__get_set_info(s, "ID:", 1)
        ret = self.__logout(s)
        if ret:
            print_error("{}: name_storage".format(self._name))
            return

        if name_before == name_after and id_before == id_after:
            print_success("{}: name_storage".format(self._name))
        else:
            print_error("{}: name_storage".format(self._name))
        s.close()

    def last_visit_storage(self):
        print_info("{}: last_visit_storage".format(self._name))
        s = self.__login()
        if not s:
            print_error("{}: last_visit_storage".format(self._name))
            return
        visit_before = self.__get_set_info(s, "Last visit:", 5)
        ret = self.__logout(s)
        if ret:
            print_error("{}: last_visit_storage".format(self._name))
            return

        s.close()
        sleep(1)
        s = self.__login()
        if not s:
            print_error("{}: last_visit_storage".format(self._name))
            return
        visit_after = self.__get_set_info(s, "Last visit:", 5)
        ret = self.__logout(s)
        if ret:
            print_error("{}: last_visit_storage".format(self._name))
            return

        if visit_before != visit_after:
            print_success("{}: last_visit_storage".format(self._name))
        else:
            print_error("{}: last_visit_storage".format(self._name))
        s.close()

    def highscore_storage(self):
        print_info("{}: highscore_storage".format(self._name))
        s = self.__login()
        if not s:
            print_error("{}: highscore_storage".format(self._name))
            return
        ret3 = drop_load(s, 2**16-1, "CONS", "HIGHSCORE")
        if ret3:
            print_error("{}: highscore_storage".format(self._name))
            return
        highscore_before = show_highscores(s)
        ret = flush(s)
        ret2 = self.__logout(s)
        if ret or ret2:
            print_error("{}: highscore_storage".format(self._name))
            return

        s.close()
        s = self.__login()
        if not s:
            print_error("{}: highscore_storage".format(self._name))
            return
        highscore_after = show_highscores(s)
        ret = self.__logout(s)
        if ret:
            print_error("{}: highscore_storage".format(self._name))
            return

        if highscore_before == highscore_after:
            print_success("{}: highscore_storage".format(self._name))
        else:
            print_error("{}: highscore_storage".format(self._name))
        s.close()
