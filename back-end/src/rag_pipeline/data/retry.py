import time
import random

def retry_with_backoff(fn, retries=5, base_delay=5, max_delay=60):
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            if "rate limit" in str(e).lower() or "429" in str(e):
                wait = min(max_delay, base_delay * 2 ** attempt + random.uniform(0, 1))
                print(f"Rate limit excedido. Retentando em {wait:.1f}s... ({attempt+1})")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Máximo de tentativas atingido.")