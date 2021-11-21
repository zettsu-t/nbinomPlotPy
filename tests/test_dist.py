"""
Testing states of negative binomial distribution
"""

import unittest
from nb_plot_streamlit.dist import get_pdf


class TestCppDist(unittest.TestCase):
    """Testing public interfaces of C++ code"""

    def test_density_set(self):
        """Test a density set"""

        expected = [0.177978516, 0.266967773, 0.233596802, 0.155731201,
                    0.087598801, 0.043799400, 0.020074725, 0.008603454,
                    0.003495153, 0.001359226]

        actual = get_pdf(6.0, 0.75, 0.999, 1.0)
        self.assertEqual(len(actual), len(expected))

        for index, value in enumerate(expected):
            print(value)
            self.assertTrue(abs(value - actual[index]) < 1e-6)


if __name__ == "__main__":
    unittest.main()
