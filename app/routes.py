from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
import sqlite3
from datetime import datetime

main = Blueprint('main', __name__)

# ============ HELPER FUNCTIONS ============
def log_audit(user_id, action, target_type, target_id, details=""):
    """Log user actions for audit trail"""
    try:
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO audit_logs (user_id, action, target_type, target_id, details) 
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, action, target_type, target_id, details)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Audit logging error: {e}")

def get_current_user_id():
    """Get current logged-in user's ID"""
    if 'user' not in session:
        return None
    try:
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()
        user = cursor.execute("SELECT id FROM users WHERE name=?", (session['user'],)).fetchone()
        conn.close()
        return user[0] if user else None
    except:
        return None

def update_last_login(username):
    """Update user's last login time"""
    try:
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_login=? WHERE name=?", (datetime.now().isoformat(), username))
        conn.commit()
        conn.close()
    except:
        pass

# ================== SYSTEMS PAGE ==================
@main.route('/systems')
def systems():
    if 'user' not in session:
        return redirect('/')

    try:
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()
        data = cursor.execute("SELECT * FROM systems").fetchall()
        conn.close()
        return render_template('systems.html', systems=data, page_title="Systems")
    except Exception as e:
        flash(f"Error loading systems: {e}", "danger")
        return render_template('systems.html', systems=[], page_title="Systems")

# ================== LOGIN ==================
@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash("Username and password required ❌", "danger")
            return render_template('login.html')

        try:
            conn = sqlite3.connect('lab.db')
            cursor = conn.cursor()
            user = cursor.execute("SELECT id, password, is_active FROM users WHERE name=?", (username,)).fetchone()
            conn.close()

            if user and user[2]:  # user exists and is active
                # For now, simple password check. In production, use werkzeug.security.check_password_hash()
                if user[1] == password:
                    session['user'] = username
                    session['user_id'] = user[0]
                    update_last_login(username)
                    return redirect('/dashboard')
            
            flash("Invalid Credentials ❌", "danger")
        except Exception as e:
            flash(f"Login error: {e}", "danger")

    return render_template('login.html')

# ================== DASHBOARD ==================
@main.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    try:
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()

        # System statistics
        total = cursor.execute("SELECT COUNT(*) FROM systems").fetchone()[0]
        online = cursor.execute("SELECT COUNT(*) FROM systems WHERE status='Online'").fetchone()[0]
        offline = cursor.execute("SELECT COUNT(*) FROM systems WHERE status='Offline'").fetchone()[0]
        healthy = cursor.execute("SELECT COUNT(*) FROM systems WHERE health_status='Healthy'").fetchone()[0]

        conn.close()

        return render_template(
            'dashboard.html',
            total=total,
            online=online,
            offline=offline,
            healthy=healthy,
            page_title="Dashboard"
        )
    except Exception as e:
        flash(f"Dashboard error: {e}", "danger")
        return render_template('dashboard.html', total=0, online=0, offline=0, healthy=0, page_title="Dashboard")

# ================== ADD SYSTEM ==================
@main.route('/add-system', methods=['POST'])
def add_system():
    if 'user' not in session:
        return redirect('/')
    
    try:
        name = request.form.get('name', '').strip()
        ip_address = request.form.get('ip_address', '').strip()
        mac_address = request.form.get('mac_address', '').strip()
        status = request.form.get('status', 'Unknown')

        if not name:
            flash("System name is required ❌", "danger")
            return redirect('/systems')

        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO systems (name, ip_address, mac_address, status, last_check_time) 
               VALUES (?, ?, ?, ?, ?)""",
            (name, ip_address, mac_address, status, datetime.now().isoformat())
        )

        conn.commit()
        system_id = cursor.lastrowid
        conn.close()

        # Log the action
        log_audit(get_current_user_id(), 'ADD_SYSTEM', 'system', system_id, f"Added system: {name}")
        flash("System Added Successfully ✅", "success")
        
    except sqlite3.IntegrityError:
        flash("System name already exists ❌", "danger")
    except Exception as e:
        flash(f"Error adding system: {e}", "danger")

    return redirect('/systems')

# ================== TOGGLE STATUS ==================
@main.route('/toggle/<int:id>')
def toggle(id):
    if 'user' not in session:
        return redirect('/')
    
    try:
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()

        current = cursor.execute("SELECT status FROM systems WHERE id=?", (id,)).fetchone()
        
        if not current:
            flash("System not found ❌", "danger")
            return redirect('/systems')

        new_status = "Offline" if current[0] == "Online" else "Online"

        cursor.execute(
            "UPDATE systems SET status=?, updated_at=? WHERE id=?",
            (new_status, datetime.now().isoformat(), id)
        )

        conn.commit()
        conn.close()

        log_audit(get_current_user_id(), 'TOGGLE_STATUS', 'system', id, f"Changed to: {new_status}")
        flash("Status Updated 🔄", "info")
        
    except Exception as e:
        flash(f"Error toggling status: {e}", "danger")

    return redirect('/systems')

# ================== DELETE SYSTEM ==================
@main.route('/delete/<int:id>')
def delete(id):
    if 'user' not in session:
        return redirect('/')
    
    try:
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM systems WHERE id=?", (id,))
        cursor.execute("DELETE FROM system_health WHERE system_id=?", (id,))

        conn.commit()
        conn.close()

        log_audit(get_current_user_id(), 'DELETE_SYSTEM', 'system', id)
        flash("System Deleted ❌", "danger")
        
    except Exception as e:
        flash(f"Error deleting system: {e}", "danger")

    return redirect('/systems')

# ================== LOGOUT ==================
@main.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect('/')

# ================== UPDATE SYSTEM ==================
@main.route('/update-system', methods=['POST'])
def update_system():
    if 'user' not in session:
        return redirect('/')
    
    try:
        id = request.form.get('id')
        name = request.form.get('name', '').strip()
        ip_address = request.form.get('ip_address', '').strip()
        status = request.form.get('status', 'Unknown')

        if not id or not name:
            flash("Invalid data ❌", "danger")
            return redirect('/systems')

        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()

        cursor.execute(
            """UPDATE systems SET name=?, ip_address=?, status=?, updated_at=? WHERE id=?""",
            (name, ip_address, status, datetime.now().isoformat(), id)
        )

        conn.commit()
        conn.close()

        log_audit(get_current_user_id(), 'UPDATE_SYSTEM', 'system', int(id))
        flash("System Updated ✏️", "info")
        
    except Exception as e:
        flash(f"Error updating system: {e}", "danger")

    return redirect('/systems')

# ================== USERS PAGE ==================
@main.route('/users')
def users():
    if 'user' not in session:
        return redirect('/')

    try:
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()
        data = cursor.execute("SELECT id, name, role FROM users").fetchall()
        conn.close()
        return render_template('users.html', users=data)
    except Exception as e:
        flash(f"Error loading users: {e}", "danger")
        return render_template('users.html', users=[])

# ================== ADD USER ==================
@main.route('/add-user', methods=['POST'])
def add_user():
    if 'user' not in session:
        return redirect('/')
    
    try:
        name = request.form.get('name', '').strip()
        role = request.form.get('role', 'User')
        password = request.form.get('password', 'defaultpass123')  # Should come from form in real app

        if not name:
            flash("User name is required ❌", "danger")
            return redirect('/users')

        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, password, role) VALUES (?, ?, ?)",
            (name, password, role)
        )

        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        log_audit(get_current_user_id(), 'ADD_USER', 'user', user_id, f"Added user: {name}")
        flash("User Added ✅", "success")
        
    except sqlite3.IntegrityError:
        flash("User already exists ❌", "danger")
    except Exception as e:
        flash(f"Error adding user: {e}", "danger")

    return redirect('/users')

# ================== DELETE USER ==================
@main.route('/delete-user/<int:id>')
def delete_user(id):
    if 'user' not in session:
        return redirect('/')
    
    try:
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (id,))
        conn.commit()
        conn.close()

        log_audit(get_current_user_id(), 'DELETE_USER', 'user', id)
        flash("User Deleted ❌", "danger")
        
    except Exception as e:
        flash(f"Error deleting user: {e}", "danger")

    return redirect('/users')

# ================== API: System Health Check ==================
@main.route('/api/systems/<int:id>/health', methods=['POST'])
def update_system_health(id):
    """API endpoint for monitoring agents to report system health"""
    try:
        data = request.get_json()
        
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()

        # Update main systems table
        cursor.execute(
            """UPDATE systems SET 
               status=?, health_status=?, cpu_usage=?, memory_usage=?, 
               disk_usage=?, last_check_time=? WHERE id=?""",
            (
                data.get('status', 'Unknown'),
                data.get('health_status', 'Unknown'),
                data.get('cpu_usage'),
                data.get('memory_usage'),
                data.get('disk_usage'),
                datetime.now().isoformat(),
                id
            )
        )

        # Record in history table
        cursor.execute(
            """INSERT INTO system_health 
               (system_id, status, health_status, cpu_usage, memory_usage, disk_usage) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                id,
                data.get('status', 'Unknown'),
                data.get('health_status', 'Unknown'),
                data.get('cpu_usage'),
                data.get('memory_usage'),
                data.get('disk_usage')
            )
        )

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Health updated'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ================== API: Get Systems Status ==================
@main.route('/api/systems')
def api_systems():
    """API endpoint to get all systems status"""
    try:
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()
        
        systems = cursor.execute(
            """SELECT id, name, ip_address, status, health_status, cpu_usage, 
                      memory_usage, disk_usage, last_check_time FROM systems"""
        ).fetchall()
        
        conn.close()

        systems_data = []
        for s in systems:
            systems_data.append({
                'id': s[0],
                'name': s[1],
                'ip_address': s[2],
                'status': s[3],
                'health_status': s[4],
                'cpu_usage': s[5],
                'memory_usage': s[6],
                'disk_usage': s[7],
                'last_check_time': s[8]
            })

        return jsonify({'success': True, 'systems': systems_data})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400