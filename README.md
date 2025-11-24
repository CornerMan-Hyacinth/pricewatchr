# PriceWatchr

A full-stack price monitoring application with automated web scraping, price tracking, and alert notifications.
Backend: FastAPI + PostgreSQL
Frontend: Next.js

## Overview

PriceGuardian is a full-stack application that monitors product prices across e-commerce websites.
Users can:

- Add product URLs they want to track
- Automatically scrape product prices at intervals
- Store price history
- Receive alerts when prices drop
- View analytics through a modern frontend

## Tech Stack

### Backend

- FastAPI
- PostgreSQL
- SQLAlchemy ORM (2.0-style)
- pgcrypto extension (UUID generation)
- Alembic (database migrations)
- httpx / Requests (for scraping)
- BeautifulSoup / Selectolax (HTML parsing)
- APScheduler (background jobs)

### Frontend

- Next.js (App Router)
- Tailwind CSS
- React Query (API data fetching)
- Custom Auth

## Setup (Backend)

1. ### Create Virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

2. ### Install dependencies

```bash
pip install -r requirements.txt
```

3. ### Enable PostgreSQL extension
   Log into Postgres:

```bash
psql -U postgres -d pricewatchr
```

Enable pgcrypto:

```bash
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

4. ### Run database migrations

```bash
alembic upgrade head
```

5. ### Start FastAPI

```bash
uvicorn app.main:app --reload
```

## Setup (Frontend)

```bash
cd frontend
npm install
npm run dev
```

## Background Scheduler

```bash
python app/scheduler.py
```

## Features

✔ Track multiple products
✔ Automatic price scraping
✔ API-based architecture
✔ UUID-based models
✔ Postgres-backed price history
✔ Price-drop alerts
✔ Modern Next.js frontend
✔ Clean project structure
✔ Professional & scalable design

## Screenshots (Coming Soon)

## Future Improvements

- Browser-based scraping (Playwright)
- Email/Telegram notifications
- AI-based price forecasting

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss.

## License

MIT License.
