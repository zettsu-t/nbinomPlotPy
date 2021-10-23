import re
import numpy as np
import unittest
from nb_plot_streamlit.nbinom import NbinomDist


class TestNbinomDist(unittest.TestCase):
    def check_data_frame(self, x: str, n_row: int):
        pattern = re.compile("x,density\\n(\\d+\\.0,0\\.\\d+\\n){" +
                             str(int(n_row)) + "}")
        self.assertTrue(pattern.match(x) is not None)

        pattern = re.compile("x,density\\n(\\d+\\.0,0\\.\\d+\\n){" +
                             str(int(n_row + 1)) + "}")
        self.assertTrue(pattern.match(x) is None)

    def test_init(self):
        """Test init"""
        params = {"initial_size": 1.0, "initial_prob": 0.5}
        nb = NbinomDist(initial_values=params)
        self.assertAlmostEqual(nb.get_size(), 1.0)
        self.assertAlmostEqual(nb.get_prob(), 0.5)
        self.assertAlmostEqual(nb.get_mu(), 1.0)

    def test_init_another(self):
        """Test init with another parameter set"""
        params = {"initial_size": 4.0, "initial_prob": 0.25}
        nb = NbinomDist(initial_values=params)
        self.assertAlmostEqual(nb.get_size(), 4.0)
        self.assertAlmostEqual(nb.get_prob(), 0.25)
        self.assertAlmostEqual(nb.get_mu(), 12.0)

    def test_reset(self):
        """Test rest"""
        params = {"initial_size": 6.0, "initial_prob": 0.75}
        nb = NbinomDist(initial_values=params)
        self.assertAlmostEqual(nb.get_size(), 6.0)
        self.assertAlmostEqual(nb.get_prob(), 0.75)
        self.assertAlmostEqual(nb.get_mu(), 2.0)

        nb.update_size_prob(size=4.0, prob=0.25)
        self.assertAlmostEqual(nb.get_size(), 4.0)

        nb.reset()
        self.assertAlmostEqual(nb.get_size(), 6.0)
        self.assertAlmostEqual(nb.get_prob(), 0.75)
        self.assertAlmostEqual(nb.get_mu(), 2.0)

    def test_update_size_prob(self):
        """Test update_size_prob"""
        params = {"initial_size": 1.0, "initial_prob": 0.5}
        nb = NbinomDist(initial_values=params)
        self.assertAlmostEqual(nb.get_size(), 1.0)

        nb.update_size_prob(size=4.0, prob=0.25)
        self.assertAlmostEqual(nb.get_size(), 4.0)
        self.assertAlmostEqual(nb.get_prob(), 0.25)
        self.assertAlmostEqual(nb.get_mu(), 12.0)

    def test_update_mu_prob(self):
        """Test update_mu_prob"""
        params = {"initial_size": 1.0, "initial_prob": 0.5}
        nb = NbinomDist(initial_values=params)
        self.assertAlmostEqual(nb.get_size(), 1.0)

        nb.update_mu_prob(mu=2.0, prob=0.75)
        self.assertAlmostEqual(nb.get_size(), 6.0)
        self.assertAlmostEqual(nb.get_prob(), 0.75)
        self.assertAlmostEqual(nb.get_mu(), 2.0)

    def test_set_quantile(self):
        """Test set_quantile and get_data"""
        params = {"initial_size": 4.0, "initial_prob": 0.25}
        nb = NbinomDist(initial_values=params)

        nb.set_quantile(quantile="0.99")
        expected_n_rows = 34
        self.assertAlmostEqual(nb.get_max_x_plus_one(), expected_n_rows)
        xs, ys = nb.get_data()
        self.assertTrue(np.allclose(xs, np.arange(0, expected_n_rows, 1)))
        self.assertEqual(ys.shape[0], expected_n_rows)
        self.check_data_frame(x=nb.get_df().decode('utf-8'),
                              n_row=expected_n_rows)

        nb.set_quantile(quantile="0.999")
        expected_n_rows = 44
        self.assertAlmostEqual(nb.get_max_x_plus_one(), expected_n_rows)
        xs, ys = nb.get_data()
        self.assertTrue(np.allclose(xs, np.arange(0, expected_n_rows, 1)))
        self.assertEqual(ys.shape[0], expected_n_rows)
        self.check_data_frame(x=nb.get_df().decode('utf-8'),
                              n_row=expected_n_rows)

    def test_set_quantile_another(self):
        """Test set_quantile and get_data with another parameter set"""
        params = {"initial_size": 6.0, "initial_prob": 0.75}
        nb = NbinomDist(initial_values=params)

        nb.set_quantile(quantile="0.99")
        expected_n_rows = 8
        self.assertAlmostEqual(nb.get_max_x_plus_one(), expected_n_rows)
        xs, ys = nb.get_data()
        self.assertTrue(np.allclose(xs, np.arange(0, expected_n_rows, 1)))
        self.assertEqual(ys.shape[0], expected_n_rows)
        self.check_data_frame(x=nb.get_df().decode('utf-8'),
                              n_row=expected_n_rows)

        nb.set_quantile(quantile="0.9999")
        expected_n_rows = 12
        self.assertAlmostEqual(nb.get_max_x_plus_one(), expected_n_rows)
        xs, ys = nb.get_data()
        self.assertTrue(np.allclose(xs, np.arange(0, expected_n_rows, 1)))
        self.assertEqual(ys.shape[0], expected_n_rows)
        self.check_data_frame(x=nb.get_df().decode('utf-8'),
                              n_row=expected_n_rows)

    def test_wrong_quantile(self):
        """Test wrong quantiles"""
        params = {"initial_size": 4.0, "initial_prob": 0.25}
        nb = NbinomDist(initial_values=params)

        expected_quantile = "0.99"
        nb.set_quantile(quantile=expected_quantile)
        self.assertEqual(nb.get_quantile(), expected_quantile)

        for quantile in ["-0.1", "0", "1.0", "1.01", "X"]:
            nb.set_quantile(quantile=quantile)
            self.assertEqual(nb.get_quantile(), expected_quantile)


if __name__ == "__main__":
    unittest.main()
