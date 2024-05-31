import sqlite3
import sys
import unittest

from aggregator import db

class TestFormatter(unittest.TestCase):
    def test_format_summary(self):
        # formatter = db.RowFormatter()
        # foo = sqlite3.Row(a=1, b=2)
        foo = {'a': 1, 'b': 2}
        print(f"foo: {foo}, {foo['a']}")
        
if __name__ == '__main__':
    unittest.main()