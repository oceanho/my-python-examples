# -*- coding: utf-8 -*-
"""
    Content repairer interfaces
"""

from uuid import uuid4
from queue import Empty
from common.psub import OneProducerMultipleConsumer


class ContentRepairer(OneProducerMultipleConsumer):
    def __init__(self):
        super().__init__(consumer_nums=100)

    # Override __producer__()
    # impl the Content repairer produce logic at here.
    def __producer__(self):
        n = 0
        while n <= 1000:
            n += 1
            self.queues.put("{}".format(uuid4()))
        self.producer_done()

    # Override __consumer__()
    # impl the Content repairer consume logic at here.
    def __consumer__(self, worker_id):
        while not self.has_done():
            try:
                url = self.queues.get(timeout=1)
                self.reporter.report('INFO', "work id:{}, data:{}".format(worker_id, url))
            except Empty:
                pass
