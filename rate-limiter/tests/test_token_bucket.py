
import time
from unittest.mock import MagicMock
from rate_limiter.token_bucket_algo.token_bucket import TokenBucket
from rate_limiter.token_bucket_algo.bucket import Bucket
import unittest


class TestTokenBucket(unittest.TestCase):

    def test_token_bucket_should_have_capacity_and_refill_amountand_refill_time_in_seconds(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 60
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)

        self.assertIsNotNone(sut)
        self.assertIsInstance(sut, TokenBucket)
        self.assertIsInstance(sut._my_bucket, Bucket)
        self.assertEqual(sut.refill_amount, refill_amount)
        self.assertEqual(sut.refill_time_in_seconds, refill_time_in_seconds)

    def test_token_bucket_should_be_initialized_with_full_capacity(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 60
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)

        self.assertEqual(sut._available_tokens(), capacity)

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

    def test_token_bucket_is_not_refilled_if_time_elapsed_from_last_refill_is_less_than_refill_time(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 4
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)
        # empty the tokens in bucket
        for _ in range(capacity):
            sut._pop_token()

        # immediately try refill after creation of token bucket and verify no tokens got added
        sut._refill_tokens()

        self.assertEqual(0, sut._available_tokens())

    def test_token_bucket_is_refilled_with_refill_amount_if_time_elapsed_from_last_refill_is_equal_to_refill_time(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 4
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)
        # empty the tokens in bucket
        for _ in range(capacity):
            sut._pop_token()
        # set last refill time to refill_time seconds ago
        current_time = int(time.time())
        sut.last_refill_time = current_time - refill_time_in_seconds

        sut._refill_tokens()

        self.assertEqual(refill_amount, sut._available_tokens())

    def test_token_bucket_is_refilled_with_twice_refill_amount_if_time_elapsed_from_last_refill_is_equal_to_two_times_refill_time(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 4
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)
        for _ in range(capacity):
            sut._pop_token()
        current_time = int(time.time())
        sut.last_refill_time = current_time - refill_time_in_seconds * 2

        sut._refill_tokens()

        self.assertEqual(refill_amount * 2, sut._available_tokens())

    def test_token_bucket_is_not_overfilled_by_refill(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 4
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)
        for _ in range(capacity):
            sut._pop_token()
        current_time = int(time.time())
        sut.last_refill_time = current_time - 100

        sut._refill_tokens()

        self.assertEqual(capacity, sut._available_tokens())

    def test_token_bucket_returns_available_number_of_tokens_at_given_instant(self):
        capacity = 10
        refill_amount = 1
        refill_time_in_seconds = 4
        sut = TokenBucket(capacity, refill_amount, refill_time_in_seconds)
        for _ in range(capacity):
            sut._pop_token()
        current_time = int(time.time())
        sut.last_refill_time = current_time - refill_time_in_seconds

        result = sut._available_tokens()

        self.assertEqual(refill_amount, result)
    
    def test_consume_token_returns_true_and_pop_a_token_when_token_is_available(self):
        sut = TokenBucket(10, 1, 4)
        sut._available_tokens = MagicMock(return_value=3)
        sut._pop_token = MagicMock()

        self.assertTrue(sut.consume_token())

        sut._available_tokens.assert_called_once()
        sut._pop_token.assert_called_once()

    def test_consume_token_returns_false_when_token_is_not_available(self):
        sut = TokenBucket(10, 1, 4)
        sut._available_tokens = MagicMock(return_value=0)
        sut._pop_token = MagicMock()

        self.assertFalse(sut.consume_token())

        sut._available_tokens.assert_called_once()
        sut._pop_token.assert_not_called()