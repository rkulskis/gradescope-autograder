import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    with open('../results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible', stream=f).run(suite)
