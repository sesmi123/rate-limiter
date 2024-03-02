import os

redis = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", 6379),
    "token_bucket_db": os.environ.get("TOKEN_BUCKET_DB", 0),
    "leaky_bucket_db": os.environ.get("LEAKY_BUCKET_DB", 1),
}

token_bucket = {
    "capacity": int(os.environ.get("TOKEN_BUCKET_CAPACITY", 10)),
    "refill_amount": int(os.environ.get("TOKEN_BUCKET_REFILL_AMOUNT", 1)),
    "refill_time_in_seconds": int(os.environ.get("TOKEN_BUCKET_REFILL_TIME_IN_SECONDS", 1))
}

leaky_bucket = {
    "capacity": int(os.environ.get("LEAKY_BUCKET_CAPACITY", 10)),
    "leak_rate": float(os.environ.get("LEAKY_BUCKET_LEAK_RATE", 1.0))
}