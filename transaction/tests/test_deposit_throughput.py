# import time
# import uuid
# from decimal import Decimal
# import requests
# from concurrent.futures import ThreadPoolExecutor

# from rest_framework.test import (APITestCase, APIClient)
# from django.test import TransactionTestCase
# from rest_framework import status

# from transaction.models import(User , Wallet , TransactionLog  , Symbol)
# from transaction.models import TransactionLog


# class DepositThroughputTest(APITestCase):

#     def setUp(self):
     
#         self.user = User.objects.create(
#             name="Bita"
#         )

#         self.symbol = Symbol.objects.create(
#             name="BTC"
#         )

#         self.wallet = Wallet.objects.create(
#             user=self.user,
#             symbol=self.symbol,
         
#         )
#         self.wallet_id = str(self.wallet.wallet_id)
#         self.user_id = str(self.user.user_id)
#         self.wallet.refresh_from_db()

#     def make_request(self):
#         res =  requests.post(
#             "http://127.0.0.1:8000/api/wallet/deposit/",
#             json={
#                 "wallet_id": self.wallet_id,
#                 "user_id": self.user_id,
#                 "amount": "10",
#                 "refrence_key": str(uuid.uuid4())
#             }
#         ).status_code
#         print(res.dat)
#         return res
    

#     def test_deposit_throughput(self):

#         total_requests = 100
#         max_workers = 20

#         start_time = time.time()

#         with ThreadPoolExecutor(max_workers=max_workers) as executor:
          

#             results = list(
#                 executor.map(
#                     lambda _: self.make_request(),
#                     range(total_requests)
#                 )
#             )

#         end_time = time.time()

#         duration = end_time - start_time

#         success_count = results.count(status.HTTP_200_OK)

#         self.wallet.refresh_from_db()

#         print(f"Total Requests : {total_requests}")
#         print(f"Successful Requests : {success_count}")
#         print(f"Duration : {duration:.2f} sec")
#         print(f"Requests/sec : {total_requests / duration:.2f}")
#         print(f"Final Balance : {self.wallet.balance}")

#         self.assertEqual(
#             success_count,
#             total_requests
#         )

#         self.assertEqual(
#             self.wallet.balance,
#             Decimal("1000")
#         )

#         self.assertEqual(
#             TransactionLog.objects.count(),
#             total_requests
#         )