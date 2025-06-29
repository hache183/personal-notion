"""
Personal Notion - A minimal self-hosted note-taking app
Main Flask application with routes and database initialization
"""

import os
from datetime import datetime
import click
import markdown
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Page

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration
DATABASE_URL = 'sqlite:///notes.db'
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Markdown processor
md = markdown.Markdown(extensions=['extra'])


def get_db_session():
    """Get database session"""
    return SessionLocal()


@app.route('/')
def index():
    """Homepage - list all pages ordered by last updated"""
    session = get_db_session()
    try:
        pages = session.query(Page).order_by(Page.updated_at.desc()).all()
        return render_template('index.html', pages=pages)
    finally:
        session.close()


@app.route('/page/<int:page_id>')
def view_page(page_id):
    """View a single page with rendered Markdown"""
    session = get_db_session()
    try:
        page = session.query(Page).filter(Page.id == page_id).first()
        if not page:
            flash('Page not found', 'error')
            return redirect(url_for('index'))
        
        # Render Markdown to HTML
        content_html = md.convert(page.content)
        return render_template('page.html', page=page, content_html=content_html)
    finally:
        session.close()


@app.route('/new')
def new_page():
    """Show form to create new page"""
    return render_template('edit.html', page=None, is_new=True)


@app.route('/create', methods=['POST'])
def create_page():
    """Create a new page"""
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    
    if not title:
        flash('Title is required', 'error')
        return redirect(url_for('new_page'))
    
    session = get_db_session()
    try:
        page = Page(title=title, content=content)
        session.add(page)
        session.commit()
        flash('Page created successfully', 'success')
        return redirect(url_for('view_page', page_id=page.id))
    except Exception as e:
        session.rollback()
        flash(f'Error creating page: {str(e)}', 'error')
        return redirect(url_for('new_page'))
    finally:
        session.close()


@app.route('/edit/<int:page_id>')
def edit_page(page_id):
    """Show form to edit existing page"""
    session = get_db_session()
    try:
        page = session.query(Page).filter(Page.id == page_id).first()
        if not page:
            flash('Page not found', 'error')
            return redirect(url_for('index'))
        
        return render_template('edit.html', page=page, is_new=False)
    finally:
        session.close()


@app.route('/update/<int:page_id>', methods=['POST'])
def update_page(page_id):
    """Update an existing page"""
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    
    if not title:
        flash('Title is required', 'error')
        return redirect(url_for('edit_page', page_id=page_id))
    
    session = get_db_session()
    try:
        page = session.query(Page).filter(Page.id == page_id).first()
        if not page:
            flash('Page not found', 'error')
            return redirect(url_for('index'))
        
        page.title = title
        page.content = content
        page.updated_at = datetime.utcnow()
        session.commit()
        flash('Page updated successfully', 'success')
        return redirect(url_for('view_page', page_id=page.id))
    except Exception as e:
        session.rollback()
        flash(f'Error updating page: {str(e)}', 'error')
        return redirect(url_for('edit_page', page_id=page_id))
    finally:
        session.close()


@app.route('/delete/<int:page_id>', methods=['POST'])
def delete_page(page_id):
    """Delete a page"""
    session = get_db_session()
    try:
        page = session.query(Page).filter(Page.id == page_id).first()
        if not page:
            flash('Page not found', 'error')
            return redirect(url_for('index'))
        
        session.delete(page)
        session.commit()
        flash('Page deleted successfully', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        session.rollback()
        flash(f'Error deleting page: {str(e)}', 'error')
        return redirect(url_for('view_page', page_id=page_id))
    finally:
        session.close()


@app.route('/search')
def search():
    """Search pages by title and content"""
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('index'))
    
    session = get_db_session()
    try:
        # Simple LIKE search on title and content
        search_term = f'%{query}%'
        pages = session.query(Page).filter(
            Page.title.like(search_term) | Page.content.like(search_term)
        ).order_by(Page.updated_at.desc()).all()
        
        return render_template('search.html', pages=pages, query=query)
    finally:
        session.close()


@app.cli.command('init-db')
def init_db_command():
    """Initialize the database with tables"""
    try:
        Base.metadata.create_all(bind=engine)
        click.echo('Database initialized successfully.')
    except Exception as e:
        click.echo(f'Error initializing database: {str(e)}')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)