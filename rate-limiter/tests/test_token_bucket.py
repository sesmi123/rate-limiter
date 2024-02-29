
import time
from rate_limiter.token_bucket_algo.token_bucket import TokenBucket
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

        self.assertEqual(sut.fill_level(), capacity)

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

    def test_token_bucket_cannot_be_overfilled(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 4
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)

        sut.fill([i for i in range(100)])

        self.assertEqual(capacity, sut.fill_level())

    def test_token_bucket_is_not_refilled_if_time_elapsed_from_last_refill_is_less_than_refill_time(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 4
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)
        # empty the tokens in bucket
        for _ in range(capacity):
            sut.pop_token()

        # immediately try refill after creation of token bucket and verify no tokens got added
        sut.refill_tokens()

        self.assertEqual(0, sut.fill_level())

    def test_token_bucket_is_refilled_with_refill_amount_if_time_elapsed_from_last_refill_is_equal_to_refill_time(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 4
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)
        # empty the tokens in bucket
        for _ in range(capacity):
            sut.pop_token()
        # set last refill time to refill_time seconds ago
        current_time = int(time.time())
        sut.last_refill_time = current_time - refill_time_in_seconds

        sut.refill_tokens()

        self.assertEqual(refill_amount, sut.fill_level())

    def test_token_bucket_is_refilled_with_twice_refill_amount_if_time_elapsed_from_last_refill_is_equal_to_two_times_refill_time(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 4
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)
        for _ in range(capacity):
            sut.pop_token()
        current_time = int(time.time())
        sut.last_refill_time = current_time - refill_time_in_seconds * 2

        sut.refill_tokens()

        self.assertEqual(refill_amount * 2, sut.fill_level())

    def test_token_bucket_is_not_overfilled_by_refill(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 4
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)
        for _ in range(capacity):
            sut.pop_token()
        current_time = int(time.time())
        sut.last_refill_time = current_time - 100

        sut.refill_tokens()

        self.assertEqual(capacity, sut.fill_level())