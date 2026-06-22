# Transaction Tracking System

A backend service with a live frontend that handles transactions, user summaries, and fair leaderboard ranking.

## Live Links
- Frontend: https://velvety-kheer-6cca4f.netlify.app
- Backend API: https://transaction-backend-0oit.onrender.com

## Tech Stack
- Backend: Python, Flask, SQLAlchemy, SQLite
- Frontend: HTML, CSS, Vanilla JS
- Deployment: Render (backend), Netlify (frontend)

## How to Run Locally
```bash
git clone https://github.com/aryang21122004-cmd/transaction-backend
cd transaction-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## API Reference

### POST /transaction
Records a new transaction.

**Request:**
```json
{
  "userId": "user1",
  "amount": 500,
  "transactionId": "txn-001"
}
```

**Responses:**
- `201` — Transaction recorded
- `400` — Validation error (missing fields, negative amount)
- `409` — Duplicate transaction ID

### GET /summary/:userId
Returns a user's total amount, transaction count, and current rank.

**Response:**
```json
{
  "userId": "user1",
  "totalAmount": 800.0,
  "transactionCount": 2,
  "rank": 2
}
```

### GET /ranking
Returns all users sorted by composite score.

## How Ranking Works
Score is calculated using a composite formula:
- **totalAmount × 0.6** — Primary factor, rewards higher spend
- **transactionCount × 0.3** — Rewards frequent activity
- **consistencyBonus** — `min(transactionCount, 10) × 1.0`, capped to prevent spam

This prevents manipulation by a single large transaction.

## How Duplicate Requests Are Prevented
Every transaction has a unique `transactionId`. Before processing, the system checks if that ID already exists in the database. If it does, it returns `409 Conflict` without processing again.

## How Concurrency Is Handled
A `threading.Lock()` is used before any database write. This ensures only one request modifies user data at a time, preventing race conditions and data corruption.

## Assumptions & Trade-offs
- SQLite used instead of PostgreSQL — sufficient for this scale, easy to deploy
- In-memory threading lock works for single-instance deployment; would use Redis lock in production
- userId is a string — no auth system, users are identified by ID only