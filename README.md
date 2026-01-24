# Medical Research Sample Product

Simple full-stack product for a medical research workflow:
- Frontend: Vue 3 + Vite
- Backend: Django + DRF
- Database: PostgreSQL (local or Heroku)
- Deployment: Heroku

## Structure
```
frontend/   # Vue 3 app
backend/    # Django app
```

## Backend setup (local)
```
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Frontend setup (local)
```
cd frontend
npm install
npm run dev
```

## Environment variables
Backend uses these variables (examples):
```
SECRET_KEY=replace-me
DEBUG=true
DATABASE_URL=postgres://user:pass@localhost:5432/medresearch
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Heroku
```
heroku create
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python backend/manage.py migrate
```

