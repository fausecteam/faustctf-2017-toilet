from util import *
from test import BasicTest

class HighscoresTest(BasicTest):
    def __init__(self, s):
        self._name = "Highscores Test"
        self._socket = s

    def run_all_tests(self):
        self.highscores_before_login()
        self.highscores_after_login()
        self.score_highscore()

    def highscores_before_login(self):
        print_info("{}: highscores_before_login".format(self._name))
        ret = show_highscores(self._socket)
        if ret:
            print_success("{}: highscores_before_login".format(self._name))
        else:
            print_error("{}: highscores_before_login".format(self._name))

    def highscores_after_login(self):
        print_info("{}: highscores_after_login".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = show_highscores(self._socket)
        if not ret and ret2:
            print_success("{}: highscores_after_login".format(self._name))
        else:
            print_error("{}: highscores_after_login".format(self._name))
        logout(self._socket)

    def score_highscore(self):
        print_info("{}: score_highscore".format(self._name))
        ret = login(self._socket, "foobar")
        ret2 = show_highscores(self._socket)
        ret3 = drop_load(self._socket, 2**16-1, "CONS", "LOAD")
        ret4 = flush(self._socket)
        ret5 = show_highscores(self._socket)
        if not ret and not ret3 and not ret4 and ret2 != ret5:
            print_success("{}: score_highscore".format(self._name))
        else:
            print_error("{}: score_highscore".format(self._name))
        logout(self._socket)

