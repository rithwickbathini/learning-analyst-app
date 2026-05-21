# 🎓 Learning Platform

A web-based learning platform with quizzes, video lessons, progress tracking,
and role-based access for students and admins. Built with Python and Streamlit,
backed by a PostgreSQL database.

**Live app:** https://learning-analyst-app-e8cu5erzok4vt7fpc9shp3.streamlit.app/

## Features

- 🔐 **Authentication** — secure signup/login with hashed passwords (bcrypt)
- 👥 **Roles** — separate experiences for students and admins
- 📝 **Quizzes** — 30+ days of Python & Data Structures questions with instant scoring
- 📈 **Score tracking** — students see their quiz history and progress over time
- 🎥 **Video lessons** — embedded Python tutorial videos
- 📊 **Dashboard** — KPIs and charts on course data
- 🛠️ **Admin panel** — manage users and monitor all student scores
- 🗄️ **Persistent storage** — accounts and scores saved in a PostgreSQL database (Supabase)

## Tech Stack

- **Frontend & App:** Streamlit
- **Data & Charts:** Pandas, Plotly
- **Database:** PostgreSQL (Supabase)
- **Auth:** bcrypt password hashing
- **Hosting:** Streamlit Community Cloud

## Getting Started (Local Setup)

1. Clone the repository:
```bash
   git clone https://github.com/rithwickbathini/learning-analyst-app.git
   cd learning-analyst-app
```

2. Create and activate a virtual environment:
```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Create a `.env` file with your Supabase keys:
