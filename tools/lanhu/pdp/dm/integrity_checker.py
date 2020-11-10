# -*- coding: utf-8 -*-
"""
    Content Sign Checker interfaces
"""

from requests import head, HTTPError
from queue import Empty
from subprocess import check_output
from common.psub import OneProducerMultipleConsumer


class DataIntegrityChecker(OneProducerMultipleConsumer):
    def __init__(self):
        super().__init__(consumer_nums=100)
        self.__totalUrls = 0

    def __initial(self):
        pass

    def __producer__(self):
        self.__initial()
        for url in self.versions_urls():
            self.queues.put(url)
        self.producer_done()

    def __consumer__(self, worker_id):
        while not self.has_done():
            try:
                url = self.queues.get(timeout=1)
                code = self.__check_url_exists(url)
                if not code == 200:
                    msg = "url: {}, code: {}".format(url, code)
                    self.reporter.report("ERROR", msg)
                    self.errs.append(msg)
            except Empty:
                pass

    @staticmethod
    def __check_url_exists(url):
        try:
            resp = head(url, timeout=0.5)
            return resp.status_code
        except:
            return -1

    @staticmethod
    def versions_urls():
        page_size = 1000
        offset = 0
        cmd = [
            "docker exec",
            "docker_magic_postgres_1",
            "psql -U postgres -d magic -t",
            "-c \"select url from versions where url like 'http%' limit " + str(page_size) + " offset {}\""]
        while True:
            cmd_str = " ".join(cmd).format(offset)
            results = check_output(cmd_str, shell=True).split(b'\n')
            if len(results) == 0 or results[0] == b'':
                break
            for item in results:
                url = item.decode().replace('\t', "").replace('\n', "").replace(" ", "")
                if url:
                    yield url
            offset += page_size
