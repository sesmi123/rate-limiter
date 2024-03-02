import unittest
from unittest.mock import Mock, patch
from rate_limiter.token_bucket_algo.token_bucket import TokenBucket
from rate_limiter.token_bucket_algo.singleton import Singleton
from rate_limiter.token_bucket_algo.token_bucket_factory import TokenBucketFactory

class TestTokenBucketFactory(unittest.TestCase):

    def setUp(self):
        self.database_client = Mock()
        self.config = {
            "capacity": 100,
            "refill_amount": 10,
            "refill_time_in_seconds": 60
        }
        self.factory = TokenBucketFactory(self.database_client, self.config)

    def test_factory_returns_existing_token_bucket_if_present_in_db(self):
        ip = "127.0.0.1"
        serialized_token_bucket = b"serialized_bucket"
        self.database_client.get.return_value = serialized_token_bucket

        with patch("pickle.dumps") as mock_dumps, \
            patch("pickle.loads") as mock_loads:
            mock_loads.return_value = TokenBucket(100, 10, 60)
            token_bucket = self.factory(ip)

        self.database_client.get.assert_called_once_with(ip)
        mock_loads.assert_called_once_with(serialized_token_bucket)
        mock_dumps.assert_not_called()
        self.assertIsInstance(token_bucket, TokenBucket)

    def test_factory_creates_new_token_bucket_if_not_present_in_db(self):
        ip = "127.0.0.1"
        self.database_client.get.return_value = None

        with patch("pickle.dumps") as mock_dumps, \
             patch("pickle.loads") as mock_loads:
            mock_dumps.return_value = b"serialized_bucket"
            mock_loads.return_value = TokenBucket(100, 10, 60)
            token_bucket = self.factory(ip)

        self.database_client.get.assert_called_once_with(ip)
        mock_dumps.assert_called_once()
        mock_loads.assert_not_called()
        self.assertIsInstance(token_bucket, TokenBucket)

    def test_save_token_bucket(self):
        ip = "127.0.0.1"
        token_bucket = TokenBucket(100, 10, 60)
        
        with patch("pickle.dumps") as mock_dumps:
            mock_dumps.return_value = b"serialized_bucket"
            self.factory.save_token_bucket(ip, token_bucket)

        self.database_client.set.assert_called_once_with(ip, b"serialized_bucket")
