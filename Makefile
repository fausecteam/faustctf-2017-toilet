#!/usr/bin/make -f

USER    ?= toilet
HOME    ?= /srv/toilet

build:
	$(MAKE) -C src build

install: build
	install -m 700 -o $(USER) -d $(HOME)/data
	install -m 755 -o root src/toilet $(HOME)
	install -m 644 -o root src/toilet@.service /etc/systemd/system
	install -m 644 -o root src/toilet.socket /etc/systemd/system
	install -m 644 -o root src/system-toilet.slice /etc/systemd/system
	systemctl enable toilet.socket

test-all: test-basic test-scaling

test-basic: build
	test/main.py -p src/toilet

test-scaling: build run-socat run-scaling

run-socat:
	socat tcp-l:7777,reuseaddr,fork, EXEC:"src/toilet" &

run-scaling:
	test/main.py -r localhost 7777 --scaling
