# -*- coding: utf-8 -*-

from sys import stdout
from time import sleep
from threading import Thread
from queue import Queue, Empty


class Reporter(object):
    """
    Reporter 表示执行状态/结果等的反馈对象
    """
    def __init__(self):
        self.printer = stdout
        self.messages = Queue(4096)
        self.__worker_has_stop = False
        self.worker = Thread(target=self.__do_report)

    def start(self):
        """
        启动 reporter 汇报任务
        """
        self.worker.start()

    def stop(self):
        """
        停止 reporter 汇报任务，并且汇报所有 queues 中的消息
        """
        self.__worker_has_stop = True
        self.worker.join()
        self.__report()

    def report(self, level, msg):
        """
        发送一条汇报信息给 Reporter 的队列
        :param level: 级别(INFO/WARN/ERROR)
        :param msg: 消息内容
        """
        self.messages.put("[{}] - {}".format(level, msg))

    def __report(self):
        while not self.messages.empty():
            try:
                msg = self.messages.get(timeout=1)
                self.printer.write(msg + "\n")
                self.printer.flush()
            except Empty:
                pass

    def __do_report(self):
        while not self.__worker_has_stop:
            self.__report()


class OneProducerMultipleConsumer(object):
    """
    定义一个通用的单生产者,多消费者对象,抽象了对本地(单机)生产者/消费者模型的通用基础操作封装
    """
    def __init__(self, consumer_nums=1):
        self.errs = []
        self.queues = Queue(8192)
        self.reporter = Reporter()
        self.__exit_code = 0
        self.__producer_has_done = False
        self.__consumer_has_done = False
        self.consumer_workers = []
        self.producer_worker = Thread(target=self.__producer__)
        self.has_done_checker = Thread(target=self.__done_check__)
        for n in range(0, consumer_nums):
            self.consumer_workers.append({
                "id": n,
                "thread": Thread(target=self.__consumer__, args=(n,))
            })

    def __done_check__(self):
        # producer done and queues are empty.
        while not self.__producer_has_done or not self.queues.empty():
            sleep(1)
        self.__consumer_has_done = True

    def __report_errors(self):
        for err in self.errs:
            stdout.write(err + "\n")
        stdout.flush()
        self.__exit_code = 127 if len(self.errs) > 0 else 0
        self.errs.clear()

    def start(self):
        """
        启动生产/消费服务
        :return: 错误数,如果没有错误返回零(表示任务执行正常完成)
        """
        self.reporter.start()
        self.producer_worker.start()
        self.has_done_checker.start()
        for cw in self.consumer_workers:
            t = cw["thread"]
            t.start()
        self.producer_worker.join()
        self.has_done_checker.join()
        for cw in self.consumer_workers:
            t = cw["thread"]
            t.join()
        self.reporter.stop()
        self.__report_errors()
        return self.__exit_code

    """
    设置 producer 状态为已完成
    """
    def producer_done(self):
        self.__producer_has_done = True

    """
    获取 queues 是否被已经被消费完了（前提条件: producer 已经完成,并且 queues 为空）
    """
    def has_done(self):
        return self.__consumer_has_done

    """
    自定义 class 的 producer 应该重写这个 API.
    """
    def __producer__(self):
        pass

    """
    自定义 class 的 consumer 应该重写这个 API.
    """
    def __consumer__(self, worker_id):
        pass
