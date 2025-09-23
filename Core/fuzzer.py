# Core/fuzzer.py
"""
Simple fuzzer payload generator. Keep payloads short and defensive — this is for testing only.
You can extend this list with more payloads as needed.
"""
DEFAULT_PAYLOADS = [
    "' OR '1'='1",                  # basic SQLi-ish payload (test only)
    "<script>alert(1)</script>",    # XSS-ish payload
    "../../../../etc/passwd",       # path traversal-ish
    "'; DROP TABLE users; --",      # SQL-like
    "' OR 'x'='x",
    "' or 1=1 --",
    "admin' --",
    "test@example.com",
    "1234567890",
    "A" * 300,                      # long string
]

def parameter_fuzz_values(param_name, param_schema=None):
    # can be extended to map param types -> payloads
    return DEFAULT_PAYLOADS
