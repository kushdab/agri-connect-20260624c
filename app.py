from flask import Flask, render_template_string, request, redirect, url_for, session
import uuid

app = Flask(__name__)
app.secret_key = 'agri-connect-2026-secret'

# Mock Database
listings = [
    {'id': '1', 'farmer': 'Kamau', 'produce': 'Grade A Potatoes', 'quantity': '500kg', 'price': '3500 KES/bag', 'location': 'Nyandarua'},
    {'id': '2', 'farmer': 'Muthoni', 'produce': 'Hass Avocados', 'quantity': '2000 units', 'price': '15 KES/pc', 'location': 'Murang\'a'}
]
users = {}  # {username: {'password': p, 'role': r}}

BASE_TEMPLATE = """
<!DOCTYPE html>
<html><head><title>AgriConnect Kenya</title>
<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'>
</head><body class='bg-light'>
<nav class='navbar navbar-expand-lg navbar-dark bg-success shadow-sm mb-4'>
    <div class='container'><a class='navbar-brand font-weight-bold' href='/'>AgriConnect Kenya</a>
    <div class='navbar-nav ms-auto'>
        {% if session.get('user') %}
            <span class='nav-link text-white'>Welcome, {{ session['user'] }} ({{ session['role'] }})</span>
            <a class='nav-item nav-link border rounded px-2 ms-2' href='/logout'>Logout</a>
        {% else %}
            <a class='nav-item nav-link' href='/login'>Login</a>
        {% endif %}
    </div></div>
</nav>
<div class='container'>{% block content %}{% endblock %}</div>
<footer class='text-center mt-5 text-muted'><small>&copy; 2026 AgriConnect Kenya - Connecting Nakuru, Eldoret & Nairobi</small></footer>
</body></html>
"""

@app.route('/')
def index():
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class='jumbotron bg-white p-5 shadow-sm rounded'>
        <h1>Nairobi Wholesaler? Meet Your Farmers.</h1>
        <p class='lead'>The digital bridge between rural Kenyan farms and city markets.</p>
        <hr>
        <div class='d-flex gap-2'>
            <a href='/listings' class='btn btn-success btn-lg'>Browse Produce</a>
            {% if session.get('role') == 'Farmer' %}
            <a href='/add' class='btn btn-outline-success btn-lg'>List Your Harvest</a>
            {% endif %}
            {% if not session.get('user') %}
            <a href='/register' class='btn btn-primary btn-lg'>Create Account</a>
            {% endif %}
        </div>
    </div>
    """)
    return render_template_string(html)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users[request.form['user']] = {'password': request.form['pass'], 'role': request.form['role']}
        return redirect(url_for('login'))
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class='col-md-4 mx-auto'><div class='card p-4 shadow-sm'><h3>Farmer/Wholesaler Signup</h3>
    <form method='POST'><input name='user' placeholder='Username' class='form-control mb-2' required>
    <input name='pass' type='password' placeholder='Password' class='form-control mb-2' required>
    <select name='role' class='form-control mb-3'><option>Farmer</option><option>Wholesaler</option></select>
    <button class='btn btn-success w-100'>Register</button></form></div></div>"""))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['user']
        if u in users and users[u]['password'] == request.form['pass']:
            session['user'], session['role'] = u, users[u]['role']
            return redirect(url_for('index'))
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class='col-md-4 mx-auto'><div class='card p-4 shadow-sm'><h3>Market Login</h3>
    <form method='POST'><input name='user' placeholder='Username' class='form-control mb-2' required>
    <input name='pass' type='password' placeholder='Password' class='form-control mb-2' required>
    <button class='btn btn-success w-100'>Login</button></form></div></div>"""))

@app.route('/listings')
def view_listings():
    rows = "".join([f"<tr><td>{l['produce']}</td><td>{l['quantity']}</td><td>{l['price']}</td><td>{l['location']}</td><td>{l['farmer']}</td></tr>" for l in listings])
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', f"""
    <h3>Available Produce for Nairobi Delivery</h3>
    <table class='table bg-white shadow-sm mt-3'><thead><tr><th>Produce</th><th>Qty</th><th>Price</th><th>Location</th><th>Farmer</th></tr></thead>
    <tbody>{rows}</tbody></table>"""))

@app.route('/add', methods=['GET', 'POST'])
def add_listing():
    if session.get('role') != 'Farmer': return redirect(url_for('index'))
    if request.method == 'POST':
        listings.append({'id': str(uuid.uuid4()), 'farmer': session['user'], 'produce': request.form['p'], 
                         'quantity': request.form['q'], 'price': request.form['pr'], 'location': request.form['l']})
        return redirect(url_for('view_listings'))
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class='col-md-6 mx-auto card p-4 shadow-sm'><h3>List New Produce</h3>
    <form method='POST'><input name='p' placeholder='Produce Type (e.g. Maize)' class='form-control mb-2' required>
    <input name='q' placeholder='Quantity (e.g. 10 Tons)' class='form-control mb-2' required>
    <input name='pr' placeholder='Price (e.g. 4000 KES/bag)' class='form-control mb-2' required>
    <input name='l' placeholder='Origin (e.g. Eldoret)' class='form-control mb-2' required>
    <button class='btn btn-success w-100'>Post Marketplace Listing</button></form></div>"""))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)