
from rate_limiter.token_bucket import TokenBucket
import unittest


class TestTokenBucket(unittest.TestCase):

    def test_token_bucket_should_have_capacity_and_refill_amountand_refill_time_in_seconds(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 60
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)

        self.assertIsNotNone(sut)
        self.assertIsInstance(sut, TokenBucket)
        self.assertEqual(sut.capacity, capacity)
        self.assertEqual(sut.refill_amount, refill_amount)
        self.assertEqual(sut.refill_time_in_seconds, refill_time_in_seconds)

    def test_token_bucket_should_be_initialized_with_full_capacity(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 60
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)

        self.assertEqual(sut.fill_level, capacity)

    def test_token_bucket_cannot_be_created_with_negative_capacity(self):
        capacity = -10
        refill_amount = 1
        refill_time_in_seconds = 60
        with self.assertRaises(ValueError):
            TokenBucket(capacity, refill_amount, refill_time_in_seconds)

    def test_token_bucket_cannot_be_created_with_negative_refill_amount(self):
        capacity = 10
        refill_amount = -1
        refill_time_in_seconds = 60
        with self.assertRaises(ValueError):
            TokenBucket(capacity, refill_amount, refill_time_in_seconds)

    def test_token_bucket_cannot_be_created_with_negative_refill_time_in_seconds(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = -60
        with self.assertRaises(ValueError):
            TokenBucket(capacity, refill_amount, refill_time_in_seconds)

    def test_token_bucket_cannot_be_created_with_zero_capacity(self):
        capacity = 0
        refill_amount = 1
        refill_time_in_seconds = 60
        with self.assertRaises(ValueError):
            TokenBucket(capacity, refill_amount, refill_time_in_seconds)

    def test_token_bucket_cannot_be_created_with_zero_refill_amount(self):
        capacity = 10
        refill_amount = 0
        refill_time_in_seconds = 60
        with self.assertRaises(ValueError):
            TokenBucket(capacity, refill_amount, refill_time_in_seconds)

    def test_token_bucket_cannot_be_created_with_zero_refill_time_in_seconds(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 0
        with self.assertRaises(ValueError):
            TokenBucket(capacity, refill_amount, refill_time_in_seconds)

    def test_token_bucket_cannot_be_created_with_fractional_capacity(self):
        capacity = 1.5
        refill_amount = 1
        refill_time_in_seconds = 60
        with self.assertRaises(ValueError):
            TokenBucket(capacity, refill_amount, refill_time_in_seconds)

    def test_token_bucket_cannot_be_created_with_fractional_refill_amount(self):
        capacity = 10
        refill_amount = 2.3
        refill_time_in_seconds = 60
        with self.assertRaises(ValueError):
            TokenBucket(capacity, refill_amount, refill_time_in_seconds)

    def test_token_bucket_cannot_be_created_with_fractional_refill_time_in_seconds(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 4.6
        with self.assertRaises(ValueError):
            TokenBucket(capacity, refill_amount, refill_time_in_seconds)