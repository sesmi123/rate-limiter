from flask import Flask
from redis_connection import RedisConnection
from decorators import LeakyBucketRateLimiter, TokenBucketRateLimiter
from token_bucket_algo.token_bucket_factory import TokenBucketFactory
from leaky_bucket_algo.leaky_bucket_factory import LeakyBucketFactory
import settings

app = Flask(__name__)
token_bucket_db = RedisConnection(settings.redis["host"],settings.redis["port"],settings.redis["token_bucket_db"])
token_bucket_db.connect()
token_bucket_factory = TokenBucketFactory(token_bucket_db, settings.token_bucket)
token_bucket_rate_limiter = TokenBucketRateLimiter(token_bucket_factory)

leaky_bucket_db = RedisConnection(settings.redis["host"],settings.redis["port"],settings.redis["leaky_bucket_db"])
leaky_bucket_db.connect()
leaky_bucket_factory = LeakyBucketFactory(leaky_bucket_db, settings.leaky_bucket)
leaky_bucket_rate_limiter = LeakyBucketRateLimiter(leaky_bucket_factory)

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/token-bucket-rate-limited', methods=['GET'])
@token_bucket_rate_limiter
def token_bucket_rate_limited():
    return "Limited by token bucket, don't over use me!"

@app.route('/leaky-bucket-rate-limited', methods=['GET'])
@leaky_bucket_rate_limiter
def leaky_bucket_rate_limited():
    return "Limited by leaky bucket, don't over use me!"

@app.route('/unlimited', methods=['GET'])
def unlimited():
    return "Unlimited! Let's Go!"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
