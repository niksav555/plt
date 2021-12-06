import matplotlib.pyplot as plt
import logging as log
from sys import argv
import re
import sys
import datetime
import numpy as np


def readFile(log_file_name, sample_rate):
    log.info("start file reading...")
    latency_list = []
    time_list = []
    try:
        with open(log_file_name, 'r') as logFile:
            i = 0
            for line in logFile:
                check_sample = re.search(r'Done', line)
                if not check_sample:
                    continue
                if sample_rate == 0 or i % sample_rate == 0:
                    immediate_slice = line.split()
                    #обрезаем строку до только значений latency и собираем в один список
                    latency_list.append(immediate_slice[-1:])
                    time_stamp_slice = immediate_slice[2:][0].split('.')
                    day_stamp = immediate_slice[1]
                    month_stamp = immediate_slice[0].split('[')
                    result_date_time_string = "{0} {2}".format(day_stamp, month_stamp[3], time_stamp_slice[0])
                    result_date_time_date = datetime.datetime.strptime(result_date_time_string, '%d %H:%M:%S')
                    time_list.append(result_date_time_date)
                i+=1
    except FileNotFoundError:
        log.error("File {0} not found".format(log_file_name))
        sys.exit(1)

    log.info("finish file reading...")
    return latency_list, time_list

def parseLatencyList(latency_list):
    min_latency_list = []
    max_latency_list = []
    med_latency_list = []

    log.info("start data preparing")
    #разбиваем список с latency на три разных списка
    for latencies in latency_list:
        immediate_latencies = latencies[0].split('/')
        # обрезаем лишнюю букву s, чтобы преобразовать значение
        min_latency_list.append(np.double(immediate_latencies[0][:-1]))
        max_latency_list.append(np.double(immediate_latencies[1][:-1]))
        med_latency_list.append(np.double(immediate_latencies[2][:-1]))

    log.info("finish data preparing")
    return [min_latency_list, max_latency_list, med_latency_list]


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    log_file_name = argv[1]
    sample_rate = int(argv[2])
    latency_list, time_list = readFile(log_file_name, sample_rate)
    if not latency_list or not time_list:
        log.error("reading of log file returned emply list. Please, check file name")
        sys.exit(1)
    result_parse_latency_list =  parseLatencyList(latency_list)
    plt.title(log_file_name)
    plt.plot(time_list, result_parse_latency_list[0], label='min latency')
    plt.plot(time_list, result_parse_latency_list[1], label='max latency')
    plt.plot(time_list, result_parse_latency_list[2], label='median latency')
    plt.xlabel('time')
    plt.ylabel('latency, second')
    plt.grid()
    plt.legend(loc='best')
    plt.show()