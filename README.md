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

### 🌐 Web-Based Deployment (Recommended - No File Copying!)

**Easiest Method - Clients just need a web browser!**

1. Login to Lab Control System
2. Go to "Deploy Clients" page from sidebar
3. Choose download option:
   - **One-Click Installer**: Download single BAT file for Windows
   - **Agent ZIP**: Download all files as ZIP
4. Run downloaded file on client PC
5. Enter System ID and Server IP when prompted

**Web Interface**: `http://your-server:5000/deploy`

### Quick Client Setup

#### For Windows Clients:
```batch
# Download and run one-click installer from web interface
# Or manually:
pip install psutil requests
python monitoring_agent.py --system-id 1 --server http://server-ip:5000
```

#### For Linux/macOS Clients:
```bash
pip install psutil requests
python monitoring_agent.py --system-id 1 --server http://server-ip:5000
```

### Network Deployment (Advanced)

For IT administrators with network access:

```powershell
# Run on server with admin credentials
.\network_deploy.ps1 -ServerIP "192.168.1.100" -ClientIPs "192.168.1.101", "192.168.1.102"
```

**Requirements:**
- PowerShell remoting enabled
- Admin access to client machines
- Same network/domain

### Manual Installation

```bash
# Install dependencies
pip install psutil requests

# Run agent
python monitoring_agent.py --system-id 1 --server http://lab-server:5000 --interval 30
```

**Parameters:**
- `--system-id` - The system ID from database (required)
- `--server` - Lab Control Server URL (required)
- `--interval` - Report interval in seconds (default: 30)

### Getting System ID

1. Login to Lab Control System
2. Go to Systems page
3. Note the ID column for your system
4. Use that ID when running the agent

### Auto-Start on Boot (Windows)

1. Create a batch file `start_monitoring.bat`:
```batch
@echo off
python "C:\path\to\monitoring_agent.py" --system-id 1 --server http://192.168.1.100:5000
```

2. Add to Windows Task Scheduler:
   - Create new task
   - Set trigger: "At log on"
   - Set action: Start program -> select your batch file
   - Set to run whether user is logged on or not

### Auto-Start on Linux

Add to crontab:
```bash
@reboot /usr/bin/python3 /path/to/monitoring_agent.py --system-id 1 --server http://192.168.1.100:5000
```
3. Note the ID column for your system
4. Use that ID when running the agent

### Example Deployment

**Server IP:** `192.168.1.100`
**System IDs:**
- PC-LAB-01: ID 1
- PC-LAB-02: ID 2
- SERVER-01: ID 3

**On PC-LAB-01:**
```bash
python monitoring_agent.py --system-id 1 --server http://192.168.1.100:5000
```

**On PC-LAB-02:**
```bash
python monitoring_agent.py --system-id 2 --server http://192.168.1.100:5000
```

### Auto-Start on Boot (Windows)

1. Create a batch file `start_monitoring.bat`:
```batch
@echo off
python "C:\path\to\monitoring_agent.py" --system-id 1 --server http://192.168.1.100:5000
```

2. Add to Windows Task Scheduler:
   - Create new task
   - Set trigger: "At log on"
   - Set action: Start program -> select your batch file
   - Set to run whether user is logged on or not

### Auto-Start on Linux

Add to crontab:
```bash
@reboot /usr/bin/python3 /path/to/monitoring_agent.py --system-id 1 --server http://192.168.1.100:5000
```

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

