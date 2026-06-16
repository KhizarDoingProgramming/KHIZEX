# KHIZEX

> The Future of Intelligent Ecosystems 🚀
> Preview here : ([khizex.pythonanywhere.com](https://khizex.pythonanywhere.com/))
> **Author:** MUSTAFA ([@KhizarDoingProgramming](https://github.com/KhizarDoingProgramming))

[![Python](https://img.shields.io/badge/python-3.11+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/django-5.2+-green?style=for-the-badge&logo=django)](https://djangoproject.com)
[![PythonAnywhere](https://img.shields.io/badge/host-pythonanywhere-323232?style=for-the-badge)](https://pythonanywhere.com)
[![License](https://img.shields.io/badge/license-MIT-purple?style=for-the-badge)]()

---

## What's the Tea? ☕

KHIZEX is a next-gen web platform that brings all your dev tools into one sleek, cyberpunk-inspired dashboard. Think Discord meets Jira meets personal portfolio, but make it drip.

Built with Django + modern JS, this isn't your grandma's CRUD app. It's got AI assistance, real-time chat, project tracking, and a community feed to flex your code.

---

## Features That Slap ✨

- 🔐 **Authentication** - Register, login, profile customization with avatar uploads
- 📊 **Dashboard** - Your command center with stats and quick access
- 📁 **Projects & Tasks** - Full project management with task boards (todo → in_progress → done)
- 👥 **Teams** - Create teams, add members, manage collaboration
- 💬 **Chat** - Real-time messaging between users
- 🔔 **Notifications** - Real-time alerts for mentions, assignments, likes
- 🌐 **Community** - Post, comment, and like like it's Twitter but for devs
- 📈 **Analytics** - Track your team's velocity and project health
- 🤖 **AI Assistant** - Your personal coding sidekick
- 🛍️ **Marketplace** - Built-in marketplace (ready for integration)
- 📂 **File Manager** - Upload and manage your files
- ⚙️ **Admin Panel** - Full admin dashboard with audit logs

---

## Tech Stack 💻

```
Backend:   Python 3.11 + Django 5.2
Frontend:  HTML5, CSS3, JavaScript, Three.js, GSAP
Icons:     Font Awesome
Fonts:     Space Grotesk, Outfit
Database:  SQLite / Supabase PostgreSQL
```

---

## Quick Start (No Cap) 🚀

```bash
# Clone the repo
git clone https://github.com/KhizarDoingProgramming/KHIZEX.git
cd KHIZEX

# Create venv (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install deps (all included)
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

Visit `http://localhost:8000` and yeet yourself into the future.

---

## Project Structure 🗂️

```
KHIZEX/
├── core/                    # Main app (all the magic happens here)
│   ├── models.py           # User, Profile, Team, Project, Task, Message, etc.
│   ├── views.py            # All view logic
│   ├── urls.py             # URL routing
│   └── templates/core/     # HTML templates
├── khizex/                 # Project settings
│   ├── settings.py         # Config + SQLite setup
│   └── urls.py             # Root URLconf
├── static/                 # Static files (CSS, JS)
├── media/                  # User uploads (avatars, files)
└── db.sqlite3              # Database (pre-migrated)
```

---

## Models Breakdown 📊

| Model | What's Good |
|-------|-------------|
| **Profile** | User bio, avatar, badge collection |
| **Team** | Team creation with member management |
| **Project** | Projects with owner + optional team |
| **Task** | Kanban-style tasks (todo/in_progress/done) |
| **Message** | User-to-user chat system |
| **Notification** | Real-time alerts |
| **Post/Comment** | Community feed with likes |
| **Badge** | Achievement system for users |

---


---

## Pages Rundown 📖

| URL | Page | What For |
|-----|------|----------|
| `/` | Landing | Marketing page with features |
| `/register` | Register | Create account |
| `/login` | Login | Access your stuff |
| `/dashboard` | Dashboard | Your main hub |
| `/projects` | Projects | All your projects |
| `/teams` | Teams | Team management |
| `/chat` | Chat | Messaging users |
| `/community` | Community | Posts + comments |
| `/analytics` | Analytics | Stats dashboard |
| `/ai-assistant` | AI | AI helper page |
| `/marketplace` | Marketplace | Shop integration |
| `/file-manager` | Files | File uploads |
| `/admin` | Admin | Django admin |

---

## Screenshots (Coming Soon) 📸

The landing page features:
- Animated Three.js particle background
- Glass-morphism cards
- Responsive design
- Cyberpunk color palette (blue/purple/green/pink)

---

## Contributing 🤝

Wanna contribute? Hell yeah!

1. Fork it
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open a PR

---

## License

MIT License - do what you want, just don't sue me.

---

Made with 💜 by MUSTAFA | [GitHub](https://github.com/KhizarDoingProgramming) | [Discord](https://discord.gg/khizarwantsmangoes)
