import os
from dotenv import load_dotenv
load_dotenv()
pwd = os.getenv("SMTP_PASSWORD", "")
print("=== PASSWORD CHECK ===")
print("Length:", len(pwd))
print("Actual:", repr(pwd))
print("First 4:", pwd[:4] if pwd else "EMPTY")
