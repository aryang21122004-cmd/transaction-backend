# Transaction Tracking System

Built as part of an internship assignment. A Flask backend with 3 APIs — submit transactions, view user stats, and see a live leaderboard ranked by a composite score.

## Live Links
- Frontend: https://velvety-kheer-6cca4f.netlify.app
- Backend API: https://transaction-backend-0oit.onrender.com
- GitHub: https://github.com/aryang21122004-cmd/transaction-backend

> Note: Render free tier sleeps after inactivity — first request may take 30-50 seconds to wake up.

## Tech Stack
- Python, Flask, SQLAlchemy, SQLite
- Flask-CORS for cross-origin requests
- Deployed on Render (backend) + Netlify (frontend)

## Run Locally
```bash
git clone https://github.com/aryang21122004-cmd/transaction-backend
cd transaction-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
Server runs on http://127.0.0.1:5000

## APIs

### POST /transaction
Submits a transaction. Validates input, checks for duplicates, then updates user balance safely.

```json
{
  "userId": "user1",
  "amount": 500,
  "transactionId": "txn-001"
}
```

Returns:
- `201` — recorded successfully
- `400` — validation failed (missing fields, negative amount, blank userId)
- `409` — duplicate transactionId, not processed again

### GET /summary/:userId
Returns that user's total amount, transaction count, and current rank.

### GET /ranking
Returns all users sorted by score, highest first.

## Ranking Formula

Didn't want to rank purely by amount — too easy to game with one large transaction. Used a composite score instead:
- Amount is weighted highest (65%) since it's the primary signal
- Transaction count rewards consistent activity over one-time dumps
- Consistency bonus is capped at 10 — prevents spam gaming

## Duplicate Prevention
Every transaction requires a unique `transactionId`. System checks if it exists before processing — if yes, returns 409 immediately without touching the database.

## Concurrency
Used `threading.Lock()` before any DB write. Without it, two simultaneous requests for the same user can both read a stale balance and overwrite each other. Lock forces sequential execution.

Limitation: works for single instance only. For horizontal scaling, would need a Redis distributed lock.

## Assumptions
- No auth system — userId is just a string identifier
- SQLite is fine for this scale; would use Postgres in production
- Mock data cleared before final demo