# Personal Notion

A minimal, self-hosted note-taking application inspired by Notion. Run it locally on your laptop with no sign-in required.

## Features

- 📝 Create, edit, and delete pages with Markdown support
- 🔍 Full-text search across all pages
- 👀 Live Markdown preview while editing
- 📱 Responsive design that works on all devices
- 💾 SQLite database for reliable local storage
- ⚡ Fast and lightweight - no external dependencies

## Tech Stack

- **Backend**: Python 3.12, Flask 3.x, SQLAlchemy 2.x
- **Database**: SQLite
- **Frontend**: HTML, Tailwind CSS, Alpine.js
- **Markdown**: Python-Markdown + Marked.js for live preview

## Quick Start

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd personal-notion
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt