"""
python3 -m cProfile bin/app1.py
https://time.geekbang.org/column/article/108350
"""
def main():
    n = 1
    while True:
        n = add(n)
        if n > 1000000:
            break


def add(n):
    return n + 1


if __name__ == '__main__':
    main()
