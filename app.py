from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def form():
    return render_template('form.html', active_page='home')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()

    return f"Thanks, {name}! Your data has been saved."
    
@app.route('/api/submit', methods=['POST'])
def api_submit():
    data = request.get_json()

    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Missing name or email'}), 400

    name = data['name']
    email = data['email']

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User added successfully', 'name': name, 'email': email}), 201

@app.route('/api/users', methods=['GET'])
def api_users_page():
    # Optional: if you have a page to show API usage
    return render_template('api.html', active_page='api')
    
def list_users():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT id, name, email FROM users')
    users = [{'id': row[0], 'name': row[1], 'email': row[2]} for row in c.fetchall()]
    conn.close()

    return jsonify(users)
    
@app.route('/users')
def users_page():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT id, name, email FROM users')
    users = c.fetchall()
    conn.close()
    return render_template('users.html', users=users, active_page='users')

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    deleted_rows = c.rowcount
    conn.close()

    if deleted_rows == 0:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'message': f'User {user_id} deleted successfully'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)