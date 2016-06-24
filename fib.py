#!/usr/bin/env python
import sys
import time

class fib(object):
    def calc(self, n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        else:
            return self.calc(n-1) + self.calc(n-2)
    
    def calc2(self, n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        else:
            fib_1 = 1
            fib_2 = 0
            for i in range(1, n):
                fib_0 = fib_1 + fib_2
                fib_2 = fib_1
                fib_1 = fib_0
            return fib_1

    def test(self, n):
        for i in range(0, n):
            print " fib1(%d)=%d, fib2(%d)=%d" % (i, self.calc(i), i, self.calc2(i))

def test(n):
    f = fib()
    f.test(n)

def main(n):
    start = time.time()
    f = fib()
    x = f.calc(n)
    end = time.time()

    print " fibonacci(%d)=%d, time=%d micro seconds" % (n, x, (end-start)*1000000)

if __name__ == '__main__':
    test(int(sys.argv[1]))
