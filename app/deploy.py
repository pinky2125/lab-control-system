from flask import Blueprint, render_template, request, send_file, jsonify
import os
import zipfile
import tempfile

deploy = Blueprint('deploy', __name__)

@deploy.route('/')
def deployment_page():
    """Web-based deployment page for clients"""
    try:
        import sqlite3
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()
        systems = cursor.execute(
            """
            SELECT id, name,
                   CASE
                     WHEN last_check_time IS NOT NULL
                       AND (julianday('now') - julianday(last_check_time)) * 86400 > 120
                     THEN 'Offline'
                     ELSE status
                   END AS status,
                   last_check_time
            FROM systems
            ORDER BY id
            """
        ).fetchall()
        conn.close()
    except:
        systems = []
    return render_template('deploy.html', systems=systems)

@deploy.route('/download-agent')
def download_agent():
    """Download monitoring agent as ZIP"""
    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, 'lab_monitor_agent.zip')

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add monitoring agent
                agent_path = os.path.join(os.getcwd(), 'monitoring_agent.py')
                if os.path.exists(agent_path):
                    zipf.write(agent_path, 'monitoring_agent.py')

                # Add client setup files
                setup_files = ['client_setup.py', 'client_setup.bat', 'auto_installer.bat']
                for setup_file in setup_files:
                    file_path = os.path.join(os.getcwd(), setup_file)
                    if os.path.exists(file_path):
                        zipf.write(file_path, setup_file)

                # Create a README for clients
                readme_content = """Lab Control System - Client Setup

1. Extract this ZIP file
2. Run auto_installer.bat (Windows) or client_setup.py (Linux/Mac)
3. Enter your System ID and Server IP when prompted
4. The agent will start monitoring automatically

For manual setup:
python monitoring_agent.py --system-id YOUR_ID --server http://SERVER_IP:5000

Contact your administrator for System ID and Server IP.
"""
                zipf.writestr('README.txt', readme_content)

            return send_file(zip_path, as_attachment=True, download_name='lab_monitor_agent.zip')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@deploy.route('/get-installer/<platform>')
def get_installer(platform):
    """Download platform-specific installer"""
    try:
        if platform == 'windows':
            installer_path = os.path.join(os.getcwd(), 'auto_installer.bat')
            if os.path.exists(installer_path):
                return send_file(installer_path, as_attachment=True, download_name='lab_monitor_installer.bat')
        elif platform == 'linux':
            installer_path = os.path.join(os.getcwd(), 'client_setup.py')
            if os.path.exists(installer_path):
                return send_file(installer_path, as_attachment=True, download_name='lab_monitor_setup.py')

        return jsonify({'error': 'Installer not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500