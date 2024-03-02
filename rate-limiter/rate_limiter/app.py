from functools import wraps
import threading
from flask import Flask, jsonify, request
from token_bucket_algo.token_bucket import TokenBucket

app = Flask(__name__)

token_bucket_lock = threading.Lock()
token_buckets = {} 

def get_token_bucket(ip):
    if ip not in token_buckets:
        token_buckets[ip] = TokenBucket(capacity=3, refill_amount=3, refill_time_in_seconds=10) 
    return token_buckets[ip]

def rate_limit_using_token_bucket(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ip = request.remote_addr
        token_bucket = get_token_bucket(ip)
        with token_bucket_lock:
            if token_bucket.consume_token():
                return func(*args, **kwargs)
            else:
                return jsonify({"error": "Rate limit exceeded"}), 429 
    return wrapper

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/token-bucket-rate-limited', methods=['GET'])
@rate_limit_using_token_bucket
def token_bucket_rate_limited():
    return "Limited by token bucket, don't over use me!"

@app.route('/unlimited', methods=['GET'])
def unlimited():
    return "Unlimited! Let's Go!"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
