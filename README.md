# rate-limiter
An API rate limiter plays a crucial role in constructing an API or a large-scale distributed system, aiding in traffic throttling based on user activity. They enable you to maintain control, ensuring that the service isn't overwhelmed by one or more users, whether intentionally or unintentionally, preventing potential disruptions.


## Local setup

```sh
python -m venv venv
venv\Scripts\activate.bat
pip install poetry
cd rate_limiter
poetry install
```

## Results

Token bucket rate limiting with capacity of 10 tokens with new tokens added at a rate of 1 token per second.

![token_bucket_performance_testing](./screenshots/token_bucket.PNG)