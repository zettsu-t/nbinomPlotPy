"""
Testing states of negative binomial distribution
"""

import unittest
from nb_plot_streamlit.dist import get_pdf


class TestCppDist(unittest.TestCase):
    """Testing public interfaces of C++ code"""

    def check_density_set(self, expected, actual):
        """Check a density set"""

        self.assertEqual(len(actual), len(expected))
        for index, value in enumerate(expected):
            self.assertTrue(abs(value - actual[index]) < 1e-6)

    def test_density_set(self):
        """Test a density set"""

        expected = [0.177978516, 0.266967773, 0.233596802, 0.155731201,
                    0.087598801, 0.043799400, 0.020074725, 0.008603454,
                    0.003495153, 0.001359226]
        actual = get_pdf(6.0, 0.75, 9.0, 1.0)
        self.check_density_set(expected, actual)

        expected = [0.0625, 0.0811899, 0.09375, 0.101487, 0.105469, 0.106562]
        actual = get_pdf(2.0, 0.25, 2.6, 0.5)
        self.check_density_set(expected, actual)

    def test_bad_parameters(self):
        """Test a density set"""
        self.assertTrue(len(get_pdf(-1.0, 0.75, 9.0, 1.0)) == 0)
        self.assertTrue(len(get_pdf(0.0, 0.75, 9.0, 1.0)) == 0)
        self.assertTrue(len(get_pdf(6.0, 1.5, 9.0, 1.0)) == 0)
        self.assertTrue(len(get_pdf(6.0, -0.75, 9.0, 1.0)) == 0)
        self.assertTrue(len(get_pdf(6.0, 0.75, -1.0, 1.0)) == 0)
        self.assertTrue(len(get_pdf(6.0, 0.75, 9.0, 0.0)) == 0)
        self.assertTrue(len(get_pdf(6.0, 0.75, 9.0, -1.0)) == 0)


if __name__ == "__main__":
    unittest.main()
