from util import *
from test import BasicTest
from threading import Thread, Lock, Semaphore
from random import choice
from socket import timeout
from pwn import *

error_count = 0
timeout_count = 0

class Barrier:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0)

    def wait(self):
        self.mutex.acquire()
        self.count = self.count + 1
        self.mutex.release()
        if self.count == self.n: self.barrier.release()
        self.barrier.acquire()
        self.barrier.release()

class Runner(Thread):
    def __init__(self, name, ip, port, timeout, lock, barrier, num):
        Thread.__init__(self)
        self.name = name
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.lock = lock
        self.barrier = barrier
        self.num = num
        self.timeout_count = 0
        self.error_count = 0

    def run(self):
        global error_count, timeout_count
        self.barrier.wait()
        self.register_users()
        self.barrier.wait()
        self.dump_shits()
        self.barrier.wait()
        self.open_connections()
        self.lock.acquire()
        error_count += self.error_count
        timeout_count += self.timeout_count
        self.lock.release()

    def register_users(self):
        try:
            s = connect_remote(self.ip, self.port, self.timeout)
        except:
            #self.lock.acquire()
            #print_info("{}: CONNECT-ERROR".format(self.name))
            #self.lock.release()
            self.error_count += 1
            return
        for i in range(0, self.num):
            try:
                ret = login(s, ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(20)))
            except timeout:
                #self.lock.acquire()
                #print_info("{}: TIMEOUT".format(self.name))
                #self.lock.release()
                self.timeout_count += 1
                continue
            except EOFError:
                self.error_count += 1
                continue
            if ret:
                #self.lock.acquire()
                #print_info("{}: LOGIN-ERROR".format(self.name))
                #self.lock.release()
                self.error_count += 1
                continue
            try:
                ret = logout(s)
            except timeout:
                #self.lock.acquire()
                #print_info("{}: TIMEOUT".format(self.name))
                #self.lock.release()
                self.timeout_count += 1
                continue
            except EOFError:
                self.error_count += 1
                continue
            if ret:
                #self.lock.acquire()
                #print_info("{}: LOGOUT-ERROR".format(self.name))
                #self.lock.release()
                self.error_count += 1
        try:
            exit(s)
        except timeout:
            #self.lock.acquire()
            #print_info("{}: TIMEOUT".format(self.name))
            #self.lock.release()
            self.timeout_count += 1
        except EOFError:
            self.error_count += 1
        s.close()
        return

    def dump_shits(self):
        try:
            s = connect_remote(self.ip, self.port, self.timeout)
        except:
            #self.lock.acquire()
            #print_info("{}: CONNECT-ERROR".format(self.name))
            #self.lock.release()
            self.error_count += 1
            return
        try:
            ret = login(s, ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        except timeout:
            #self.lock.acquire()
            #print_info("{}: TIMEOUT".format(self.name))
            #self.lock.release()
            self.timeout_count += 1
            s.close()
            return
        except EOFError:
            self.error_count += 1
            s.close()
            return
        if ret:
            #self.lock.acquire()
            #print_info("{}: LOGIN-ERROR".format(self.name))
            #self.lock.release()
            self.error_count += 1
            s.close()
            return
        for i in range(0, self.num):
            try:
                ret = drop_load(s, 20, "DUMP", "SHIT")
            except timeout:
                #self.lock.acquire()
                #print_info("{}: TIMEOUT".format(self.name))
                #self.lock.release()
                self.timeout_count += 1
            except EOFError:
                self.error_count += 1
                continue
            if ret:
                #self.lock.acquire()
                #print_info("{}: DUMP-ERROR".format(self.name))
                #self.lock.release()
                self.error_count += 1
                continue
            try:
                ret = flush(s)
            except timeout:
                #self.lock.acquire()
                #print_info("{}: TIMEOUT".format(self.name))
                #self.lock.release()
                self.timeout_count += 1
            except EOFError:
                self.error_count += 1
                continue
            if ret:
                self.lock.acquire()
                print_info("{}: FLUSH-ERROR".format(self.name))
                self.lock.release()
                self.error_count += 1
                s.close()
                return
        try:
            exit(s)
        except timeout:
            #self.lock.acquire()
            #print_info("{}: TIMEOUT".format(self.name))
            #self.lock.release()
            self.timeout_count += 1
        except EOFError:
            self.error_count += 1
        s.close()

    def open_connections(self):
        for i in range(0, self.num):
            try:
                s = connect_remote(self.ip, self.port, self.timeout)
            except:
                #self.lock.acquire()
                #print_info("{}: CONNECT-ERROR".format(self.name))
                #self.lock.release()
                self.error_count += 1
                continue
            try:
                ret = exit(s)
            except timeout:
                #self.lock.acquire()
                #print_info("{}: TIMEOUT".format(self.name))
                #self.lock.release()
                self.timeout_count += 1
                s.close()
                continue
            except EOFError:
                self.error_count += 1
                s.close()
                continue
            if ret:
                #self.lock.acquire()
                #print_info("{}: EXIT-ERROR".format(self.name))
                #self.lock.release()
                self.error_count += 1
                s.close()
                continue
            s.close()
        return

class ScalingTest(BasicTest):
    def __init__(self, ip, port, num_threads, num_actions, timeout):
        self._name = "Scaling Test"
        self._ip = ip
        self._port = port
        self._num_threads = num_threads
        self._num_actions = num_actions
        self._lock = Lock()
        self._barrier = Barrier(num_threads)
        self._threads = []
        self._timeout = timeout
        #context.log_level = "INFO"

    def run_all_tests(self):
        global error_count, timeout_count
        self.createThreads()
        self._barrier.wait()
        self._lock.acquire()
        p = log.progress("{} [{}-Threads]".format(self._name, self._num_threads))
        p.status("Started register_users test")
        #print_info("Started register_users test")
        self._lock.release()
        # Registers users
        self._barrier.wait()
        self._lock.acquire()
        p.status("Started dump_shits test")
        #print_info("Started dump_shits test")
        self._lock.release()
        # Dump shits
        self._barrier.wait()
        self._lock.acquire()
        p.status("Started open_connections test")
        #print_info("Started open_connections test")
        self._lock.release()
        # Open connections
        self.joinThreads()
        p.success("{} threads executed {} tests in total\n{} timeouts occurred\n{} errors occurred".format(self._num_threads, 3 * self._num_actions * self._num_threads, timeout_count, error_count))
        #print_info("{} timeouts occurred".format(timeout_count))
        #print_info("{} errors occurred".format(error_count))

    def createThreads(self):
        for i in range(0,self._num_threads):
            thread = Runner("Thread {}".format(i), self._ip,
                self._port, self._timeout, self._lock, self._barrier, self._num_actions)
            self._threads.append(thread)
            thread.start()
            
            print_info("Started Thread {}".format(i))

    def joinThreads(self):
        for thread in self._threads:
            thread.join()
