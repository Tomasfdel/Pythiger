#!/usr/bin/env bash
gcc -c putting_it_all_together/runtime.c

python3 main.py "$1"
gcc -no-pie -g output.s runtime.o

rm "output.s"
rm "runtime.o"
