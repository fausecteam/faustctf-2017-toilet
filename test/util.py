from pwn import *

def connect_remote(ip, port, timeout):
    s = remote(ip, port, timeout=timeout, level='CRITICAL')
    read_menu(s)
    return s

def read_menu(s):
    return s.recvuntil('Your choice:')

def menu_choice(s, num):
    s.sendline('{}'.format(num))

def login(s, name):
    s.sendline('1')
    s.recvline()
    ret = s.recv(10)
    if 'Please' in ret:
        s.sendline('{}'.format(name))
        read_menu(s)
        return 0
    else:
        read_menu(s)
        return 1

def change_seat_temp(s, temp):
    s.sendline('2')
    s.recvline()
    ret = s.recv(10)
    if 'You have' in ret:
        read_menu(s)
        return 1
    s.sendline('{}'.format(temp))
    ret = s.recvlines(3)
    read_menu(s)
    if 'Something went wrong, please try again!' in ret:
        return 1
    else:
        return 0

def show_settings(s):
    s.sendline('3')
    ret = s.recvlines(6)
    read_menu(s)
    if 'Something went wrong, please try again!' in ret:
        return 1
    return ret

def drop_load(s, size, consistency, load):
    s.sendline('4')
    ret = s.recvlines(2)
    if "Alright here we go!" not in ret:
        read_menu(s)
        return 1
    s.sendline('{}'.format(size))
    s.recvline()
    ret = s.recv(10)
    if "Please" not in ret:
        read_menu(s)
        return 1
    s.sendline('{}'.format(consistency))
    s.recvline()
    ret = s.recv(10)
    if "Now we" not in ret:
        read_menu(s)
        return 1
    s.sendline('{}'.format(load))
    ret = read_menu(s)
    if "You've landed the jumbo! Nice work!" in ret:
        return 0
    else:
        return 1

def admire_work(s):
    s.sendline('5')
    ret = s.recvlines(2)
    if 'Oh look, what a beauty: ' not in ret:
        read_menu(s)
        return 1
    ret = s.recvuntil('1. Login')
    read_menu(s)
    return ret

def flush(s):
    s.sendline('6')
    ret = s.recvlines(2)
    read_menu(s)
    if 'Going to flush now' not in ret:
        return 1
    return 0

def show_highscores(s):
    s.sendline('7')
    ret = s.recvuntil('1. Login')
    read_menu(s)
    return ret

def logout(s):
    s.sendline('8')
    ret = s.recvuntil('1. Login')
    read_menu(s)
    if 'Something went wrong, please try again!' in ret:
        return 1
    else:
        return 0

def exit(s):
    s.sendline('9')

def print_info(msg):
    log.info("{}".format(msg))

def print_success(msg):
    log.success("{}".format(msg))

def print_error(msg):
    log.error("{}".format(msg))
