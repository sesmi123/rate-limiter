from flask import Flask
from redis_connection import RedisConnection
from decorators import LeakyBucketRateLimiter, TokenBucketRateLimiter, \
                        FixedWindowCounterRateLimiter, SlidingWindowLogRateLimiter, \
                        SlidingWindowCounterRateLimiter
from token_bucket.token_bucket_factory import TokenBucketFactory
from leaky_bucket.leaky_bucket_factory import LeakyBucketFactory
from fixed_window_counter.fixed_window_counter_factory import FixedWindowCounterFactory
from sliding_window_log.sliding_window_log_factory import SlidingWindowLogFactory
from sliding_window_counter.sliding_window_counter_factory import SlidingWindowCounterFactory
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

fwc_db = RedisConnection(settings.redis["host"],settings.redis["port"],settings.redis["fwc_db"])
fwc_db.connect()
fwc_factory = FixedWindowCounterFactory(fwc_db, settings.fixed_window_counter)
fwc_rate_limiter = FixedWindowCounterRateLimiter(fwc_factory)

swl_db = RedisConnection(settings.redis["host"],settings.redis["port"],settings.redis["swl_db"])
swl_db.connect()
swl_factory = SlidingWindowLogFactory(swl_db, settings.sliding_window_log)
swl_rate_limiter = SlidingWindowLogRateLimiter(swl_factory)

swc_db = RedisConnection(settings.redis["host"],settings.redis["port"],settings.redis["swc_db"])
swc_db.connect()
swc_factory = SlidingWindowCounterFactory(swc_db, settings.sliding_window_counter)
swc_rate_limiter = SlidingWindowCounterRateLimiter(swc_factory)

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

@app.route('/fixed-window-counter-rate-limited', methods=['GET'])
@fwc_rate_limiter
def fwc_rate_limited():
    return "Limited by fixed window counter, don't over use me!"

@app.route('/sliding-window-log-rate-limited', methods=['GET'])
@swl_rate_limiter
def swl_rate_limited():
    return "Limited by sliding window log, don't over use me!"

@app.route('/sliding-window-counter-rate-limited', methods=['GET'])
@swc_rate_limiter
def swc_rate_limited():
    return "Limited by sliding window counter, don't over use me!"

@app.route('/unlimited', methods=['GET'])
def unlimited():
    return "Unlimited! Let's Go!"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
