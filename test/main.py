#!/usr/bin/env python2

from pwn import *
from sys import argv, exit
from menu_test import MenuTest
from login_test import LoginTest
from temp_test import TempTest
from drop_load_test import DropLoadTest
from admire_work_test import AdmireWorkTest
from flush_test import FlushTest
from settings_test import SettingsTest
from highscores_test import HighscoresTest
from storage_test import StorageTest
from scaling_test import ScalingTest
from util import read_menu
import argparse

PATH = "../src/toilet"
IP = "127.0.0.1"
PORT = 4242
LOCAL = True

def run_basic_tests(sock):
    # read menu once
    read_menu(sock)
    run_menu_tests(sock)
    run_login_tests(sock)
    run_temp_tests(sock)
    run_drop_load_tests(sock)
    run_admire_work_tests(sock)
    run_flush_tests(sock)
    run_settings_tests(sock)
    run_highscores_tests(sock)
    run_storage_tests(sock)

def run_menu_tests(sock):
    test = MenuTest(sock)
    test.run_all_tests()

def run_login_tests(sock):
    test = LoginTest(sock)
    test.run_all_tests()

def run_temp_tests(sock):
    test = TempTest(sock)
    test.run_all_tests()

def run_drop_load_tests(sock):
    test = DropLoadTest(sock)
    test.run_all_tests()

def run_admire_work_tests(sock):
    test = AdmireWorkTest(sock)
    test.run_all_tests()

def run_flush_tests(sock):
    test = FlushTest(sock)
    test.run_all_tests()

def run_settings_tests(sock):
    test = SettingsTest(sock)
    test.run_all_tests()

def run_highscores_tests(sock):
    test = HighscoresTest(sock)
    test.run_all_tests()

def run_storage_tests(sock):
    global LOCAL, IP, PORT, PATH
    test = StorageTest(LOCAL, IP, PORT, PATH)
    test.run_all_tests()

def run_scaling_tests(num_threads, num_actions, timeout):
    global IP, PORT
    test = ScalingTest(IP, PORT, num_threads, num_actions, timeout)
    test.run_all_tests()

def main(argv):
    global LOCAL, IP, PORT, PATH
    parser = argparse.ArgumentParser(description='Test environment for FAUSTCTF\'s toilet-service.')
    parser.add_argument('-r', nargs=2, metavar='<ip> <port>',  help='Specify a remote target')
    parser.add_argument('-p', default='../src/toilet', help='Give the path to the local binary')
    parser.add_argument('--scaling', help='Run the scaling test', action='store_true')
    parser.add_argument('--num-threads', type=int, default=10, help='Number of threads for scaling test')
    parser.add_argument('--num-actions', type=int, default=1000, help='Number of actions per thread for scaling test')
    parser.add_argument('--timeout', type=int, default=2, help='Number of actions per thread for scaling test')
    args = parser.parse_args()

    if args.p:
        PATH = args.p
    if args.r:
        LOCAL = False
        IP = args.r[0]
        try:
            PORT = int(args.r[1])
        except ValueError:
            print("Invalid port: {}".format(args.r[1]))
            sys.exit(1)

    if args.scaling:
        if LOCAL:
            print("Can't run scaling test locally")
            sys.exit(1)
        run_scaling_tests(args.num_threads, args.num_actions, args.timeout)
        return

    if LOCAL:
        sock = process(PATH, level='error')
    else:
        sock = remote(IP, PORT, level='error')

    run_basic_tests(sock)
    sock.close()
    print "All basic tests were successfull!"

if __name__ == "__main__":
    main(argv[1:])
