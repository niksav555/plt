import datetime
import unittest

from plt import parseLatencyList, readFile

class TestPltRender(unittest.TestCase):
    def test_readFile(self):
        test_filename = "sample_test.log"
        expected_latency_list = [['0.002s/0.790s/0.322s'], ['0.002s/0.986s/0.165s'], ['0.002s/0.496s/0.186s'], ['0.002s/0.474s/0.194s']]
        expected_time_list = [datetime.datetime(1900, 1, 7, 11, 15, 55), datetime.datetime(1900, 1, 7, 11, 15, 56), 
        datetime.datetime(1900, 1, 7, 11, 15, 57), datetime.datetime(1900, 1, 7, 11, 15, 58)]
        latency_list, time_list = readFile(test_filename, 0)
        self.assertEqual(latency_list, expected_latency_list)
        self.assertEqual(time_list, expected_time_list)
    def test_parseLatencyList(self):
        expected_min_latency_list = [0.002, 0.002, 0.002, 0.002]
        expected_max_latency_list = [0.79, 0.986, 0.496, 0.474]
        expected_med_latency_list = [0.322, 0.165, 0.186, 0.194]
        test_latency_list = [['0.002s/0.790s/0.322s'], ['0.002s/0.986s/0.165s'], ['0.002s/0.496s/0.186s'], ['0.002s/0.474s/0.194s']]
        result_parse_latency_list = parseLatencyList(test_latency_list)
        self.assertEqual(result_parse_latency_list, [expected_min_latency_list, expected_max_latency_list,expected_med_latency_list])

if __name__ == "__main__":
  unittest.main()