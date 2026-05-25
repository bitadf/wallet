import os
import time
import uuid
import requests
import django
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from transaction.models import Wallet, TransactionLog
from django.db import connection

# ================== CONFIG ==================
WALLET_ID = "6a5a68a6-1e08-49cf-8179-766b883ed582"
USER_ID = "23212e96-e6d3-4a03-8b7a-47f2e5fde0ac"
API_URL = "http://127.0.0.1:8000/api/wallet/withdraw/"
TOTAL_REQUESTS = 10000
MAX_WORKERS = 20
# ===========================================

def main():
    print(f"Using database: {connection.settings_dict['NAME']}")
    print(f"Running {TOTAL_REQUESTS} deposit requests with {MAX_WORKERS} workers...\n")

    try:
        wallet = Wallet.objects.get(wallet_id=WALLET_ID)
        start_balance = wallet.balance
        print(f"Wallet found | Starting Balance: {start_balance}")
    except Wallet.DoesNotExist:
        print(f"Wallet {WALLET_ID} not found in real database!")
        return

    def make_request():
        ref_key = str(uuid.uuid4())
        try:
            resp = requests.post(
                API_URL,
                json={
                    "wallet_id": WALLET_ID,
                    "user_id": USER_ID,
                    "amount": "10",
                    "refrence_key": ref_key,    
                },
                timeout=15
            )
            return resp.status_code == 200
        except:
            return False

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(executor.map(lambda _: make_request(), range(TOTAL_REQUESTS)))

    duration = time.time() - start_time
    successful = sum(results)
    failed = TOTAL_REQUESTS - successful

    # Refresh wallet
    wallet.refresh_from_db()

    print("\n" + "="*65)
    print("THROUGHPUT TEST RESULTS (REAL DATABASE)")
    print("="*65)
    print(f"Total Requests     : {TOTAL_REQUESTS}")
    print(f"Successful      : {successful}")
    print(f"Failed          : {failed}")
    print(f"Duration           : {duration:.2f} seconds")
    print(f"Throughput         : {TOTAL_REQUESTS / duration:.2f} req/sec")
    print(f"Success Rate       : {(successful / TOTAL_REQUESTS)*100:.1f}%")
    print(f"Balance Increase   : {wallet.balance - start_balance}")
    # print(f"Total Logs         : {TransactionLog.objects.count()}")
    print("="*65)

if __name__ == "__main__":
    main()