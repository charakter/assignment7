
from interval import *
import unittest

class IntervalTest(unittest.TestCase):
    '''
    Run the test in the project root directory from console by:
    $ python -m unittest discover
    '''
    def test_default_ctor(self):
        i = interval(5, 9)  # should succeed
        j = interval(4, 4)  # should succeed
        with self.assertRaises(ValueError):
            i = interval(5, 1)

    def test_fromString(self):
        # Normal cases
        i = interval.fromString('[500,0950]')
        self.assertEqual(i._left, 500)
        self.assertEqual(i._right, 950)
        i = interval.fromString('[-700,-300]')
        self.assertEqual(i._left, -700)
        self.assertEqual(i._right, -300)
        self.assertEqual(interval.fromString('(500,950]')._left, 501)
        self.assertEqual(interval.fromString('[-700,-300)')._right, -301)
        # Whitespacces
        self.assertEqual(
                interval.fromString('   [ \t 500 ,  950  ]   ')._left,
                500
                )
        self.assertEqual(
                interval.fromString('   [ \t 500 ,  950  ]   ')._right,
                950
                )
        # Errors
        def assertValueError(s):
            with self.assertRaises(ValueError):
                interval.fromString(s)
        assertValueError('')
        assertValueError('   (  8  9  ,  100 ]')
        assertValueError('(8,9)')
        assertValueError('[5]')
        assertValueError('[6,7,8]')
        assertValueError('6,8')
        assertValueError('[6,8')
        assertValueError('9,10)')
        assertValueError('[9,9)')
        assertValueError('(9,9]')
        assertValueError('[a,c]')

    def test_eq(self):
        '''
        Check if == operator and != operator works, so that we can directly
        use assertEqual() to check interval equivalence.
        '''
        self.assertTrue(interval(3, 8) == interval(3, 8))
        self.assertEqual(interval(3, 8), interval(3, 8))
        self.assertFalse(interval(3, 8) != interval(3, 8))
        self.assertNotEqual(interval(2, 9), interval(3, 8))

    def test_mergeIntervals(self):
        a = interval(3, 8)
        b = interval(4, 9)
        c = interval(3, 9)
        d = interval(2, 10)
        e = interval(-4, 2)
        f = interval(-4, 1)
        g = interval(-4, 8)
        self.assertEqual(mergeIntervals(a, b), c)
        self.assertEqual(mergeIntervals(a, c), c)
        self.assertEqual(mergeIntervals(d, a), d)
        self.assertEqual(mergeIntervals(a, e), g)
        with self.assertRaises(ValueError):
            mergeIntervals(a, f)

    def test_mergeOverlapping(self):
        self.assertEqual(len(mergeOverlapping([])), 0)
        
        # A real example:
        raw = [
                interval(1, 5),
                interval(2, 5),
                interval(9, 10),
                interval(8, 18),
                ]
        target = [interval(1, 5), interval(8, 18)]
        merged = mergeOverlapping(raw)
        for answer, result in zip(target, merged):
            self.assertEqual(result, answer)

    def test_insert(self):
        intervals = [
                interval(1, 2),
                interval(4, 4),
                interval(6, 6),
                interval(9, 10),
                interval(12, 16),
                ]
        newint = interval(4, 9)
        target = [interval(1, 2), interval(4, 10), interval(12, 16)]
        inserted = insert(intervals, newint)
        for answer, result in zip(target, inserted):
            self.assertEqual(result, answer)
