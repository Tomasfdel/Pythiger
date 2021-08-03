#!/usr/bin/env bash
gcc -c runtime.c

python3 main.py "$1"
gcc -no-pie -g output.s runtime.o
./a.out

rm "output.s"
rm "runtime.o"
