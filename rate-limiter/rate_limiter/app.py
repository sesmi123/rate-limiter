from flask import Flask
from redis_connection import RedisConnection
from decorators import TokenBucketRateLimiter
from token_bucket_algo.token_bucket_factory import TokenBucketFactory
import settings

app = Flask(__name__)
db_connection = RedisConnection(**settings.redis)
db_connection.connect()
token_bucket_factory = TokenBucketFactory(db_connection, settings.token_bucket)
token_bucket_rate_limiter = TokenBucketRateLimiter(token_bucket_factory)

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/token-bucket-rate-limited', methods=['GET'])
@token_bucket_rate_limiter
def token_bucket_rate_limited():
    return "Limited by token bucket, don't over use me!"

@app.route('/unlimited', methods=['GET'])
def unlimited():
    return "Unlimited! Let's Go!"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
