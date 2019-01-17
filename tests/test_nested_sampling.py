import unittest

import numpy as np

from nsampling import NestedSampling, CUniform
from functools import partial


def lighthouse(vals, data):
        x = vals[0]
        y = vals[1]
        N = len(data)
        logL = 0
        for k in range(0, N):
            logL += np.log((y / np.pi) /
                           ((data[k] - x) * (data[k] - x) + y * y))
        return logL


class NestedSamplingTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_nested_sampling(self):
        x = CUniform('x', -2., 2.)
        y = CUniform('y', 0., 2.)
        D = [4.73, 0.45, -1.73, 1.09, 2.19, 0.12,
             1.31, 1.00, 1.32, 1.07, 0.86, -0.49, -2.59, 1.73, 2.11,
             1.61, 4.98, 1.71, 2.23, -57.20, 0.96, 1.25, -1.56, 2.45,
             1.19, 2.17, -10.66, 1.91, -4.16, 1.92, 0.10, 1.98, -2.51,
             5.55, -0.47, 1.91, 0.95, -0.78, -0.84, 1.72, -0.01, 1.48,
             2.70, 1.21, 4.41, -4.79, 1.33, 0.81, 0.20, 1.58, 1.29,
             16.19, 2.75, -2.38, -1.79, 6.50, -18.53, 0.72, 0.94, 3.64,
             1.94, -0.11, 1.57, 0.57]

        ns = NestedSampling()
        lh = partial(lighthouse, data=D)
        rs = ns.explore([x, y], 100, 1000, lh, 20, 0.1)
        ep = rs.getexpt()
        ev = rs.getZ()
        h = rs.getH()
        var = rs.getvar()
        m = rs.getmax()
        self.assertAlmostEqual(ep[0], 1.247664, 6)
        self.assertAlmostEqual(ep[1], 0.990766, 6)
        self.assertAlmostEqual(np.sqrt(var[0]), 0.169442, 6)
        self.assertAlmostEqual(np.sqrt(var[1]), 0.188281, 6)
        self.assertAlmostEqual(m[0], 1.262122, 6)
        self.assertAlmostEqual(m[1], 0.938676, 6)
        self.assertAlmostEqual(m[2], -156.4098, 4)
        self.assertAlmostEqual(ev[0], -160.2666, 4)
        self.assertAlmostEqual(ev[1], 0.167092, 6)
        self.assertAlmostEqual(h, 2.791979, 6)

    def test_exception(self):

        def callback_raising_exception(vals):
            raise Exception("Something went wrong")

        x = CUniform('x', -2., 2.)
        y = CUniform('y', 0., 2.)
        ns = NestedSampling()
        with self.assertRaises(Exception):
            ns.explore([x, y], 100, 1000,
                       callback_raising_exception,
                       20, 0.1)



def suite():
    return unittest.makeSuite(NestedSamplingTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
