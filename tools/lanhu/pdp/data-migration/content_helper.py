# -*- coding: utf-8 -*-
"""
    Content Helper
"""

from uuid import uuid4
from sys import stdout
from threading import Thread
from queue import Queue, Empty


class Reporter(object):
    def __init__(self):
        self.printer = stdout
        self.messages = Queue(4096)
        self.worker = Thread(target=self.__do_report)

    def start(self):
        self.worker.start()

    def report(self, level, msg):
        self.messages.put("[{}] - {}".format(level, msg))

    def __do_report(self):
        while True:
            msg = self.messages.get()
            self.messages.task_done()
            self.printer.write(msg + "\n")
            self.printer.flush()


class ContentRepair(object):
    def __init__(self):
        self.reporter = Reporter()
        self.queues = Queue(8192)
        self.producerWorker = Thread(target=self.__producer__)
        self.consumerWorkers = []
        for n in range(1, 5):
            self.consumerWorkers.append({
                "id": n,
                "thread": Thread(target=self.__consumer__, args=(n,))
            })

    def start(self):
        self.reporter.start()
        self.producerWorker.start()
        for cw in self.consumerWorkers:
            t = cw["thread"]
            t.start()

    def __producer__(self):
        while True:
            self.queues.put("https://baidu.com/{}".format(uuid4()))

    def __consumer__(self, worker):
        while True:
            url = self.queues.get()
            if not url:
                return
            self.reporter.report('INFO', "work id:{}, url:{}".format(worker, url))


if __name__ == '__main__':
    repair = ContentRepair()
    repair.start()
