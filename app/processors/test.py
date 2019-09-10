import time
from concurrent.futures import ThreadPoolExecutor  # 线程池模块

def get(url):
    # time.sleep(3)  # 模拟网络延时
    print(url)
    return url  # 页面地址和页面内容

def parse(res):
    res = res.result()  # !取到res结果 【回调函数】带参数需要这样
    print(res)

pool = ThreadPoolExecutor(4)

pool.submit(get, 'i').add_done_callback(parse)  # 【回调函数】执行完线程后，跟一个函数 