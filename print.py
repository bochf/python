#!/usr/bin/env python
import sys

def printMsg(msg):
    print msg

def main():
    msg = ''.join(sys.argv[1]) or 'hello'
    for x in sys.argv[2:]:
        msg = msg + ' ' + x

    printMsg(msg)

if __name__ == '__main__':
    main()
