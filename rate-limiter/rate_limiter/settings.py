import os

token_bucket = {
    "capacity": int(os.environ.get("TOKEN_BUCKET_CAPACITY", 10)),
    "refill_amount": int(os.environ.get("TOKEN_BUCKET_REFILL_AMOUNT", 2)),
    "refill_time_in_seconds": int(os.environ.get("TOKEN_BUCKET_REFILL_TIME_IN_SECONDS", 10))
}

leaky_bucket = {}