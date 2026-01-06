#!/usr/bin/env python3
"""
Simple vulnerable Flask app for testing NET_SCAN
Created for testing purposes only
"""

from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    cursor.execute('''INSERT INTO users (username, password) VALUES ('admin', 'password123')''')
    cursor.execute('''INSERT INTO users (username, password) VALUES ('user', 'test123')''')
    conn.commit()
    return conn

db = init_db()

@app.route('/')
def index():
    """Home page"""
    return '''
    <html>
        <head><title>Vulnerable Test App</title></head>
        <body>
            <h1>Test Application</h1>
            <h2>Search Users</h2>
            <form method="GET" action="/search">
                <input type="text" name="username" placeholder="Enter username">
                <input type="submit" value="Search">
            </form>
            <h2>Contact Form</h2>
            <form method="POST" action="/contact">
                <input type="text" name="email" placeholder="Email">
                <textarea name="message" placeholder="Message"></textarea>
                <input type="submit" value="Send">
            </form>
        </body>
    </html>
    '''

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Vulnerable SQL injection endpoint"""
    username = request.args.get('username', '')
    
    # VULNERABLE: Direct string interpolation
    query = f"SELECT * FROM users WHERE username LIKE '%{username}%'"
    
    try:
        cursor = db.cursor()
        cursor.execute(query)  # VULNERABLE!
        results = cursor.fetchall()
        
        if results:
            return f"<p>Found: {results}</p>"
        return "<p>No users found</p>"
    except Exception as e:
        # VULNERABLE: Error shown to user
        return f"<p>Database error: {str(e)}</p>", 500

@app.route('/contact', methods=['POST'])
def contact():
    """Vulnerable XSS endpoint"""
    email = request.form.get('email', '')
    message = request.form.get('message', '')
    
    # VULNERABLE: No sanitization - reflected XSS
    return f'''
    <h1>Thank you!</h1>
    <p>Email: {email}</p>
    <p>Message: {message}</p>
    '''

@app.route('/api/users')
def api_users():
    """API endpoint for testing"""
    search = request.args.get('q', '')
    
    # VULNERABLE: Command injection
    import os
    result = os.popen(f"grep {search} /dev/null").read()
    
    return {'result': result}

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
