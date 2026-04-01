from flask import Blueprint, render_template, request, redirect, session, flash
import sqlite3

main = Blueprint('main', __name__)

# -------------------- SYSTEMS PAGE --------------------
@main.route('/systems')
def systems():
    if 'user' not in session:
        return redirect('/')

    conn = sqlite3.connect('lab.db')
    cursor = conn.cursor()

    data = cursor.execute("SELECT * FROM systems").fetchall()

    conn.close()

    return render_template('systems.html', systems=data, page_title="Systems")


# -------------------- LOGIN --------------------
@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "123":
            session['user'] = username
            return redirect('/dashboard')
        else:
            flash("Invalid Credentials ❌", "danger")

    return render_template('login.html')


# -------------------- DASHBOARD --------------------
@main.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    conn = sqlite3.connect('lab.db')
    cursor = conn.cursor()

    total = cursor.execute("SELECT COUNT(*) FROM systems").fetchone()[0]
    available = cursor.execute("SELECT COUNT(*) FROM systems WHERE status='Available'").fetchone()[0]
    occupied = cursor.execute("SELECT COUNT(*) FROM systems WHERE status='Occupied'").fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        total=total,
        available=available,
        occupied=occupied,
        page_title="Dashboard"
    )


# -------------------- ADD SYSTEM --------------------
@main.route('/add-system', methods=['POST'])
def add_system():
    name = request.form['name']
    status = request.form['status']

    conn = sqlite3.connect('lab.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO systems (name, status) VALUES (?, ?)",
        (name, status)
    )

    conn.commit()
    conn.close()

    flash("System Added Successfully ✅", "success")

    return redirect('/systems')


# -------------------- TOGGLE STATUS --------------------
@main.route('/toggle/<int:id>')
def toggle(id):
    conn = sqlite3.connect('lab.db')
    cursor = conn.cursor()

    current = cursor.execute(
        "SELECT status FROM systems WHERE id=?",
        (id,)
    ).fetchone()[0]

    new_status = "Occupied" if current == "Available" else "Available"

    cursor.execute(
        "UPDATE systems SET status=? WHERE id=?",
        (new_status, id)
    )

    conn.commit()
    conn.close()

    flash("Status Updated 🔄", "info")

    return redirect('/systems')


# -------------------- DELETE --------------------
@main.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('lab.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM systems WHERE id=?", (id,))

    conn.commit()
    conn.close()

    flash("System Deleted ❌", "danger")

    return redirect('/systems')


# -------------------- LOGOUT --------------------
@main.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# -------------------- UPDATE SYSTEM --------------------
@main.route('/update-system', methods=['POST'])
def update_system():
    id = request.form['id']
    name = request.form['name']
    status = request.form['status']

    conn = sqlite3.connect('lab.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE systems SET name=?, status=? WHERE id=?",
        (name, status, id)
    )

    conn.commit()
    conn.close()

    flash("System Updated ✏️", "info")

    return redirect('/systems')