#!/usr/bin/make -f
.PHONY: clean

build: toilet

toilet: toilet.o profile.o profile_extra.o util.o connection.o
	gcc -o toilet $^ -lcrypto
	strip toilet

toilet-debug: toilet.o profile.o profile_extra.o util.o connection.o
	gcc -o toilet $^ -lcrypto
%.o: %.c
	gcc -c -Wall -Werror -O1 -o $@ $<

toilet.o: toilet.c

profile.o: profile.c profile.h
profile_extra.o: profile_extra.c profile.h

util.o: util.c util.h

connection.o: connection.c connection.h

clean:
	rm *.o

distclean:
	rm toilet *.o
