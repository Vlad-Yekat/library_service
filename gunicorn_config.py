import multiprocessing
import os

bind = os.getenv("GUNICORN_BIND") or "0.0.0.0:5000"
workers = int(os.getenv("GUNICORN_WORKERS") or min(multiprocessing.cpu_count(), 5))
worker_class = os.getenv("GUNICORN_WORKER_CLASS") or "gthread"
threads = int(os.getenv("GUNICORN_THREADS") or 5)
reload = bool(eval(os.getenv("GUNICORN_RELOAD", "True").title()))
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS") or 25000)
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER") or 2500)
