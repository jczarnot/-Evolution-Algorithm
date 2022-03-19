from pop import reflection, resampling, wrapping, our_method, before_projection
import unittest


class LimitationsTests(unittest.TestCase):
    def test_reflection_1D(self):
        population = [[1], [3], [2], [2.3], [1.8], [2.9], [2.4], [2.1]]
        limitations = [[-5, 2.5]]
        new_population = reflection(population, limitations)
        expected_population = [[1], [2], [2],
                               [2.3], [1.8], [2.1], [2.4], [2.1]]
        self.assertEqual(new_population, expected_population)

    def test_reflection_2D(self):
        population = [[1., 3.], [3., 5.], [2., 6.], [2.3, 5.4],
                      [1.8, 23.9], [2.9, 3.9], [2.4, 4.5], [2.1, 4.]]
        limitations = [[-5., 2.5], [4., 5.5]]
        new_population = reflection(population, limitations)
        expected_population = [[1., 5.], [2., 5.], [2., 5.],
                               [2.3, 5.4], [1.8, -12.899999999999999], [2.1, 4.1], [2.4, 4.5], [2.1, 4.]]
        self.assertEqual(new_population, expected_population)

    def test_wrapping_1D(self):
        population = [[1], [3], [2], [2.3], [1.8], [2.9], [2.4], [2.1]]
        limitations = [[-5, 2.5]]
        new_population = wrapping(population, limitations, k=0.5)
        expected_population = [[1], [-0.75], [2],
                               [2.3], [1.8], [-0.8500000000000001], [2.4], [2.1]]
        self.assertEqual(new_population, expected_population)

    def test_wrapping_2D(self):
        population = [[1., 3.], [3., 5.], [2., 6.], [
            2.3, 5.4], [2.9, 3.9], [2.4, 4.5], [2.1, 4.]]
        limitations = [[-5., 2.5], [4., 5.5]]
        new_population = wrapping(population, limitations, k=0.5)
        expected_population = [[1., 3.75], [-0.75, 5.], [2., 5.25],
                               [2.3, 5.4], [-0.8500000000000001, 4.65], [2.4, 4.5], [2.1, 4.]]
        self.assertEqual(new_population, expected_population)

    def test_our_method_1D(self):
        population = [[1], [3], [2], [2.3], [1.8], [2.9], [2.4], [2.1]]
        limitations = [[-5, 2.5]]
        new_population = our_method(population, limitations)
        expected_population = [[1], [-0.5681818181818182], [2],
                               [2.3], [1.8], [-0.5555555555555556], [2.4], [2.1]]
        self.assertEqual(new_population, expected_population)

    def test_our_method_2D(self):
        population = [[1., 3.], [3., 5.], [2., 6.], [2.3, 5.4],
                      [2.9, 3.9], [2.4, 4.5], [2.1, 4.]]
        limitations = [[-5., 2.5], [4., 5.5]]
        new_population = our_method(population, limitations)
        expected_population = [[1., 4.857142857142857], [-0.5681818181818182, 5.], [2., 4.815217391304348],
                               [2.3, 5.4], [-0.5555555555555556, 4.844936708860759], [2.4, 4.5], [2.1, 4.]]
        self.assertEqual(new_population, expected_population)

    def test_resampling_1D(self):
        population = [[-1], [3], [-2], [2.3], [-1.8], [2.9], [-2.4], [2.1]]
        limitations = [[0.25, 2.5]]
        new_population = resampling(population, [], limitations, 0.5)
        self.assertGreater(new_population[0], limitations[0])
        self.assertGreater(new_population[1], limitations[0])

    def test_projection1(self):
        population = [[1], [2], [2], [2.3], [1.8], [2.1], [2.4], [2.1]]
        limitations = [[-5, 2.5]]
        new_population = before_projection(population, limitations)
        expected_population = [[1], [2], [2],
                               [2.3], [1.8], [2.1], [2.4], [2.1]]
        self.assertEqual(new_population, expected_population)

    def test_projection2(self):
        population = [[10], [-20], [2], [2.3], [1.8], [2.1], [2.6], [2.1]]
        limitations = [[-5, 2.5]]
        new_population = before_projection(population, limitations)
        expected_population = [[2.5], [-5], [2],
                               [2.3], [1.8], [2.1], [2.5], [2.1]]
        self.assertEqual(new_population, expected_population)


unittest.main()
