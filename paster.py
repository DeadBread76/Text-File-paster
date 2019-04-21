import os
import json
import requests
import string
import random
from tkinter import *
from tkinter.filedialog import *
from itertools import cycle
from threading import Thread
from queue import Queue
from proxyscrape import create_collector

Tk().withdraw()
class Worker(Thread):
    """
    Pooling
    """

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as ex:
                pass
            finally:
                self.tasks.task_done()

class ThreadPool:
    """
    Pooling
    """

    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """
        Add a task to be completed by the thread pool
        """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """
        Map an array to the thread pool
        """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """
        Await completions
        """
        self.tasks.join()

pool = ThreadPool(800)
collector = create_collector('my-collector', 'https')

def asciigen(length):
    asc = ''
    for x in range(int(length)):
        num = random.randrange(13000)
        asc = asc + chr(num)
    return asc

def get_proxies(proxyammount):
    proxies = set()
    for x in range(int(proxyammount)):
        proxy = collector.get_proxy()
        port = proxy[1]
        proxy = proxy[0]
        proxy = proxy + ":" + port
        proxies.add(proxy)
    return proxies

def main():
    print("Multi paster.")
    file = askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
    print(file)
    with open(file, 'r') as handle:
        x = handle.read()
    proxyammount = input("Ammount of proxies: ")
    proxies = get_proxies(proxyammount)
    proxy_pool = cycle(proxies)
    for proxy in proxies:
        proxy = next(proxy_pool)
        pool.add_task(throwbin,x,proxy)
        pool.add_task(pastr,x,proxy)
        pool.add_task(hastebin,x,proxy)
    pool.wait_completion()
    print("Completed.")
    input()
    main()

def throwbin(x, proxy):
    headers = { 'Content-Type': 'application/json;charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    payload = {'id': 'null', 'paste': x, 'title': asciigen(10)}
    response = requests.put("https://api.throwbin.io/v1/store", headers=headers,json=payload,proxies={"http": proxy, "https": proxy},timeout=20)
    jsoncont = json.loads(response.content)
    print("https://throwbin.io/{}".format(jsoncont["id"]))
    with open ("pasted.txt","a+") as handle:
        handle.write("https://throwbin.io/{}".format(jsoncont["id"])+"\n")

def pastr(x, proxy):
    headers = { 'Content-Type': 'application/json;charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    payload = {'destruct': "none", 'paste': x, 'syntax': "nohighlight", 'title': asciigen(10)}
    response = requests.post("https://pastr.io/api/create", headers=headers,json=payload,proxies={"http": proxy, "https": proxy},timeout=20)
    jsoncont = json.loads(response.content)
    print("https://pastr.io/{}".format(jsoncont["data"]["url"]))
    with open ("pasted.txt","a+") as handle:
        handle.write("https://pastr.io/{}".format(jsoncont["data"]["url"])+"\n")

def hastebin(x, proxy):
    headers = { 'Content-Type': 'application/json;charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    payload = str(x)
    response = requests.post("https://hastebin.com/documents", headers=headers,json=payload,proxies={"http": proxy, "https": proxy},timeout=20)
    jsoncont = json.loads(response.content)
    print("https://hastebin.com/{}".format(jsoncont["key"]))
    with open ("pasted.txt","a+") as handle:
        handle.write("https://hastebin.com/{}".format(jsoncont["key"])+"\n")

main()
