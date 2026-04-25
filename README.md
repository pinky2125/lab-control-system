# 🧪 Lab Control System

A professional Flask-based Lab Control System for managing and monitoring multiple PCs in a lab environment. Track system status, health metrics, user activities, and manage lab resources efficiently.

---

## ✨ Features

### Core Features
- ✅ **System Management** - Add, edit, delete, and monitor PCs
- ✅ **Real-time Monitoring** - Track CPU, Memory, Disk usage
- ✅ **Health Status** - Monitor system health (Healthy/Warning/Critical)
- ✅ **User Management** - Manage users with different roles (Admin/Manager/User)
- ✅ **Audit Logging** - Track all user actions and changes
- ✅ **Dashboard** - Real-time overview of lab status
- ✅ **Monitoring Agent** - Client-side agent to report system metrics

### Advanced Features
- 🔐 Session-based authentication
- 📊 System health history tracking
- 📱 Responsive Admin Dashboard (AdminLTE)
- 🔔 Status alerts and notifications
- 💾 SQLite database with relational schema
- 🌐 RESTful API for system monitoring
- 🛡️ CSRF protection (prepared)

---

## 🛠️ Tech Stack

- **Backend**: Python 3.8+ with Flask 2.3.3
- **Database**: SQLite3 with audit logging
- **Frontend**: HTML5, Bootstrap 4, AdminLTE 3.2, Font Awesome 6
- **Monitoring**: psutil for system metrics
- **API**: RESTful JSON endpoints

---

## 📋 Requirements

```
Flask==2.3.3
Werkzeug==2.3.7
psutil==5.9.0  (for monitoring agent)
requests==2.31.0  (for monitoring agent)
```

---

## 🚀 Quick Start

### 1. Setup Project

```bash
# Clone or navigate to project directory
cd lab_control_system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
# Create tables
python create_db.py

# Seed with default users and systems (optional)
python seed_db.py
```

**Default Credentials** (after seeding):
- Username: `admin` | Password: `admin123`
- Username: `manager` | Password: `manager123`
- Username: `user1` | Password: `user123`

### 3. Run Application

```bash
python run.py
```

Access at: `http://localhost:5000`

---

## 📡 System Architecture

### Database Schema

#### `systems` table
- `id` - System ID (Primary Key)
- `name` - System name (Unique)
- `ip_address` - IPv4 address
- `mac_address` - MAC address
- `status` - Online/Offline/Unknown
- `health_status` - Healthy/Warning/Critical
- `cpu_usage` - CPU percentage
- `memory_usage` - Memory percentage
- `disk_usage` - Disk percentage
- `last_check_time` - Last monitoring timestamp
- `created_at`, `updated_at` - Timestamps

#### `users` table
- `id` - User ID (Primary Key)
- `name` - Username (Unique)
- `password` - Password (plaintext - use hashing in production!)
- `role` - Admin/Manager/User
- `is_active` - Account status
- `created_at`, `last_login` - Timestamps

#### `audit_logs` table
- Tracks all user actions (Add, Update, Delete)
- Records what was changed and by whom

#### `system_health` table
- Historical tracking of system metrics
- Useful for trend analysis and reporting

---

## 🎮 Usage Guide

### 1. Dashboard
- View total systems, online/offline count
- Check healthy systems
- Quick access to management pages

### 2. Systems Management
**Add System:**
- Enter System Name (e.g., PC-LAB-01)
- Optionally add IP and MAC address
- Select initial status

**Edit System:**
- Click edit button to modify system details
- Update name, IP, or status

**Monitor Status:**
- View real-time status (Online/Offline)
- Check health status
- See CPU, Memory, Disk usage
- Check last check timestamp

**Toggle Status:**
- Click sync button to toggle Online/Offline

**Delete System:**
- Remove system from monitoring

### 3. User Management
**Add User:**
- Enter username
- Select role (Admin/Manager/User)
- System assigns default password (change in production!)

**Manage Users:**
- View all users and their roles
- Delete inactive users

---

## 📡 Monitoring Agent Setup

The monitoring agent runs on client PCs and reports system health to the server.

### Installation on Client PC

```bash
# Install psutil
pip install psutil requests

# Run agent (Linux/macOS)
python monitoring_agent.py --system-id 1 --server http://lab-server:5000

# Or with custom interval (every 60 seconds)
python monitoring_agent.py --system-id 1 --server http://lab-server:5000 --interval 60
```

**Parameters:**
- `--system-id` - The system ID in database (required)
- `--server` - Lab Control Server URL (required)
- `--interval` - Report interval in seconds (default: 30)

### Example: Windows Startup Script

Create `monitoring_agent.bat`:
```batch
@echo off
python monitoring_agent.py --system-id 1 --server http://192.168.1.100:5000
pause
```

Add to Windows Task Scheduler for automatic startup.

---

## 🔌 API Endpoints

### Get All Systems
```
GET /api/systems
```
Response: JSON array of all systems with current status and metrics

### Report System Health
```
POST /api/systems/{id}/health
```
Body:
```json
{
  "status": "Online",
  "health_status": "Healthy",
  "cpu_usage": 45.2,
  "memory_usage": 62.5,
  "disk_usage": 78.3
}
```

---

## 🔐 Security Features

### Current Implementation
- ✅ Session-based authentication
- ✅ Database query parameterization (SQL injection protection)
- ✅ Audit logging of all actions
- ✅ User role tracking

### Recommended for Production
- 🔒 Implement password hashing (werkzeug.security)
- 🔒 Enable CSRF protection
- 🔒 Use HTTPS/SSL
- 🔒 Implement role-based access control (RBAC)
- 🔒 Rate limiting on API endpoints
- 🔒 Environment variables for secrets
- 🔒 Database backup strategy

---

## 📊 Workflow Example

1. **Administrator** logs in with admin credentials
2. **Adds new lab PCs** via Systems page with IP addresses
3. **Creates user accounts** for lab managers and students
4. **Installs monitoring agent** on each lab PC
5. **Agent reports** CPU, Memory, Disk usage every 30 seconds
6. **Dashboard updates** in real-time
7. **Admin reviews** system health and audit logs
8. **Manages access** by enabling/disabling users

---

## 📁 Project Structure

```
lab_control_system/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── database.py              # Database schema & initialization
│   ├── routes.py                # All application routes & APIs
│   └── templates/
│       ├── base.html            # Base template with navigation
│       ├── login.html           # Login page
│       ├── dashboard.html       # Dashboard/overview
│       ├── systems.html         # System management
│       └── users.html           # User management
├── static/                      # CSS, JS, Images (currently empty)
├── venv/                        # Virtual environment
├── config.py                    # Configuration settings
├── create_db.py                 # Database initialization
├── seed_db.py                   # Database seeding
├── monitoring_agent.py          # Client monitoring script
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🚀 Deployment Checklist

- [ ] Change `SECRET_KEY` in config.py
- [ ] Switch to ProductionConfig
- [ ] Enable password hashing for user passwords
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure database backups
- [ ] Set up monitoring/logging
- [ ] Test with multiple client agents
- [ ] Configure firewall rules
- [ ] Set up reverse proxy (nginx/Apache)
- [ ] Plan disaster recovery strategy

---

## 🐛 Troubleshooting

### Agent cannot connect to server
- Check server URL and port
- Verify firewall allows outbound connections
- Ensure Lab Control System is running

### Systems showing as "Unknown"
- Wait 30-60 seconds for first report
- Check if monitoring agent is running on client PC
- Review browser console for errors

### Database locked error
- Close all open instances of the application
- Delete `lab.db-wal` and `lab.db-shm` files if present
- Restart application

---

## 📝 Future Enhancements

- [ ] Real PC discovery/scanning
- [ ] Web-based monitoring agent deployment
- [ ] Alert notifications (email/Slack)
- [ ] Performance trend graphs
- [ ] System grouping/labs
- [ ] Automated remediation scripts
- [ ] Mobile app
- [ ] Multi-server support
- [ ] LDAP/Active Directory integration
- [ ] SSO (Single Sign-On)

---

## 📄 License

This project is open source.

---

## 👥 Contributors

- Reshma (Initial Development)
- Enhanced by: AI Assistant

---

## 📞 Support

For issues, questions, or improvements, please review the code comments and documentation above.

Last Updated: 2024

