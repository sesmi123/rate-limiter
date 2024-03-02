import os

redis = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", 6379),
    "db": os.environ.get("DB_NAME", 0),
}

token_bucket = {
    "capacity": int(os.environ.get("TOKEN_BUCKET_CAPACITY", 10)),
    "refill_amount": int(os.environ.get("TOKEN_BUCKET_REFILL_AMOUNT", 2)),
    "refill_time_in_seconds": int(os.environ.get("TOKEN_BUCKET_REFILL_TIME_IN_SECONDS", 10))
}

leaky_bucket = {}