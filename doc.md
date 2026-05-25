# Wallet System API Documentation

**Project Overview**: A high-performance Django-based digital wallet system with strong concurrency control, atomic transactions, and duplicate prevention mechanisms.

**Database**: MySQL  
**Framework**: Django + Django REST Framework

---

## 1. Database Configuration

- **Type**: MySQL
- **Reason for choosing MySQL**:
  - Excellent support for **Row-level Locking**
  - Superior concurrency handling under high load
  - Better performance compared to SQLite in production environments
- Connection settings are loaded from `.env` file in the project root.
- If database connection fails, the application will stop immediately.

---

## 2. Models

### Wallet Model
- `wallet_id`: UUID (Primary Key) – Non-guessable and unique
- Foreign Keys:
  - `user` → User model
  - `symbol` → Symbol model (e.g., BTC, USDT, ETH)
- `balance`: `DecimalField(max_digits=32, decimal_places=16)`
- `created_at`, `updated_at`
- **Unique Constraint**: `(user, symbol)` – One wallet per user per asset type

### TransactionLog Model
- `transaction_id`: UUID (Primary Key)
- Foreign Key: `wallet` (with `on_delete=PROTECT`)
- `transaction_type`: Enum (`DEPOSIT`, `WITHDRAW`)
- `amount`: `DecimalField` (same precision as balance)
- `reference_key`: Unique string from client (anti-duplication mechanism)
- `created_at`

### User Model (Simplified)
- `user_id`: UUID
- `name`: CharField
- `created_at`

### Symbol Model
- `symbol_id`: UUID
- `name`: CharField (e.g., "BTC", "USDT")
- `created_at`

---

## 3. Key Features & Mechanisms

### Duplicate Transaction Prevention (Idempotency)
- Every transaction must include a unique `reference_key`
- System checks if `reference_key` already exists in `TransactionLog`
- If exists → Returns the **previous result** with status 200
- If not → Processes the transaction normally

### Concurrency Control
- Uses `select_for_update()` for pessimistic locking on Wallet records
- All critical operations (deposit/withdraw) are wrapped in `transaction.atomic()`
- Prevents race conditions and double-spending

### Error Handling
Custom exceptions return consistent format:

```json
{
  "success": false,
  "message": "Descriptive error message"
}

Method,Endpoint,Description,Request Parameters

GET,/api/wallets/,Get all wallets,-

POST,/api/wallet/,Create new wallet,"symbol_name, user_id"

POST,/api/wallet/deposit/,Deposit into wallet,"wallet_id, user_id, amount, refrence_key"

POST,/api/wallet/withdraw/,Withdraw from wallet,"wallet_id, user_id, amount, refrence_key"

GET,/api/wallet/balance/,Get wallet balance,"wallet_id, user_id (query)"

GET,/api/transactions/,Get transaction history,wallet_id or user_id (optional)


Method,Endpoint,Description

POST,/api/user/,Create new user

GET,/api/users/,List all users

POST,/api/symbol/,Create new symbol

GET,/api/symbols/,List all symbols