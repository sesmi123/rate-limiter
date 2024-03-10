
from rate_limiter.token_bucket.bucket import Bucket
import unittest


class TestBucket(unittest.TestCase):

    def test_bucket_should_have_capacity(self):
        capacity = 10
        sut = Bucket(capacity)

        self.assertIsNotNone(sut)
        self.assertIsInstance(sut, Bucket)

    def test_bucket_cannot_be_created_with_negative_capacity(self):
        capacity = -10
        with self.assertRaises(ValueError):
            Bucket(capacity)

    def test_bucket_cannot_be_created_with_zero_capacity(self):
        capacity = 0
        with self.assertRaises(ValueError):
            Bucket(capacity)

    def test_bucket_cannot_be_created_with_fractional_capacity(self):
        capacity = 1.5
        with self.assertRaises(ValueError):
            Bucket(capacity)

    def test_bucket_cannot_be_overfilled(self):
        capacity = 10
        sut = Bucket(capacity)

        sut.fill([i for i in range(100)])

        self.assertEqual(capacity, sut.fill_level())