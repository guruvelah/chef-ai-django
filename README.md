# ChefAI Django 🍳

> **Live Demo:** https://chef-ai-django.onrender.com
> **GitHub:** https://github.com/guruvelah/chef-ai-django

An AI-powered recipe assistant rebuilt in **Django 5** with a full **SQLite relational database**, Django Admin panel, REST API endpoints, and an integrated AI chat assistant.

## 🧱 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 5.2 |
| Database | SQLite (via Django ORM) |
| Server | Gunicorn |
| Static Files | WhiteNoise |
| Frontend | Vanilla HTML/CSS/JS |
| Deployment | Render (Free Tier) |

## 🗄 Database Models

| Model | Fields |
|-------|--------|
| `Recipe` | title, category, cuisine, time_minutes, difficulty, calories, protein, carbs, fat, image_url, description |
| `Ingredient` | recipe (FK), name, order |
| `CookingStep` | recipe (FK), step_number, instruction |
| `ChatLog` | session_key, user_message, ai_reply, response_type, timestamp |
| `Bookmark` | session_key, recipe (FK), saved_at |

## 🌟 Features

- **Django Admin** at `/admin/` — full CRUD for all models
- **AI Chat API** at `/api/chat/` — saves every conversation to `ChatLog` table
- **Pantry Matcher** at `/api/pantry/` — ingredient-based recipe search
- **Recipe JSON API** at `/api/recipes/` — full recipe list as JSON
- **7 curated recipes** seeded automatically on deployment

## 🚀 Local Setup

```bash
git clone https://github.com/guruvelah/chef-ai-django.git
cd chef-ai-django
pip install -r requirements.txt
python manage.py migrate
python recipes/seed.py
python manage.py createsuperuser
python manage.py runserver
```

Open http://localhost:8000 — Admin at http://localhost:8000/admin/

## 👨‍💻 Author

**Guruvelah A S** — [GitHub @guruvelah](https://github.com/guruvelah)
