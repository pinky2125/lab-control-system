-- Lab Control System - SQL Reference Guide
-- Useful queries for debugging and analysis

-- ============================================
-- SYSTEMS TABLE QUERIES
-- ============================================

-- Get all systems with their current status
SELECT id, name, ip_address, status, health_status, cpu_usage, memory_usage, disk_usage, last_check_time
FROM systems
ORDER BY id;

-- Get all online systems
SELECT id, name, ip_address, health_status
FROM systems
WHERE status = 'Online'
ORDER BY name;

-- Get all offline systems
SELECT id, name, ip_address
FROM systems
WHERE status = 'Offline'
ORDER BY name;

-- Get systems with high CPU usage (> 80%)
SELECT id, name, cpu_usage, memory_usage
FROM systems
WHERE cpu_usage > 80
ORDER BY cpu_usage DESC;

-- Get systems with high memory usage (> 85%)
SELECT id, name, memory_usage, cpu_usage
FROM systems
WHERE memory_usage > 85
ORDER BY memory_usage DESC;

-- Get systems with low disk space (> 90% used)
SELECT id, name, disk_usage
FROM systems
WHERE disk_usage > 90
ORDER BY disk_usage DESC;

-- Get systems that haven't been checked in the last hour
SELECT id, name, last_check_time, status
FROM systems
WHERE last_check_time < datetime('now', '-1 hour');

-- Get system status distribution
SELECT status, COUNT(*) as count
FROM systems
GROUP BY status;

-- Get average metrics across all systems
SELECT 
    AVG(cpu_usage) as avg_cpu,
    AVG(memory_usage) as avg_memory,
    AVG(disk_usage) as avg_disk,
    MIN(cpu_usage) as min_cpu,
    MAX(cpu_usage) as max_cpu,
    MIN(memory_usage) as min_memory,
    MAX(memory_usage) as max_memory
FROM systems;

-- Get system information with formatted last check time
SELECT 
    id, 
    name, 
    ip_address, 
    mac_address, 
    status,
    health_status,
    datetime(last_check_time) as last_check,
    datetime(created_at) as created
FROM systems
ORDER BY last_check_time DESC;

-- ============================================
-- USERS TABLE QUERIES
-- ============================================

-- Get all users
SELECT id, name, role, is_active, 
       datetime(last_login) as last_login,
       datetime(created_at) as created
FROM users
ORDER BY name;

-- Get active users only
SELECT id, name, role
FROM users
WHERE is_active = 1
ORDER BY name;

-- Get users by role
SELECT name, role
FROM users
WHERE role = 'Admin'
ORDER BY name;

-- Get users by role count
SELECT role, COUNT(*) as count
FROM users
GROUP BY role;

-- Get users who have never logged in
SELECT id, name, role
FROM users
WHERE last_login IS NULL;

-- Get users sorted by last login
SELECT id, name, role,
       datetime(last_login) as last_login
FROM users
WHERE is_active = 1
ORDER BY last_login DESC;

-- ============================================
-- AUDIT LOG QUERIES
-- ============================================

-- Get all audit logs
SELECT 
    id,
    user_id,
    action,
    target_type,
    target_id,
    details,
    datetime(created_at) as created
FROM audit_logs
ORDER BY created_at DESC
LIMIT 100;

-- Get recent actions (last 24 hours)
SELECT 
    audit_logs.id,
    users.name as user_name,
    audit_logs.action,
    audit_logs.target_type,
    audit_logs.target_id,
    datetime(audit_logs.created_at) as created
FROM audit_logs
LEFT JOIN users ON audit_logs.user_id = users.id
WHERE audit_logs.created_at > datetime('now', '-1 day')
ORDER BY audit_logs.created_at DESC;

-- Get actions by user
SELECT 
    users.name,
    COUNT(*) as action_count,
    audit_logs.action
FROM audit_logs
LEFT JOIN users ON audit_logs.user_id = users.id
GROUP BY users.name, audit_logs.action
ORDER BY action_count DESC;

-- Get actions on specific system
SELECT 
    users.name as user_name,
    audit_logs.action,
    datetime(audit_logs.created_at) as created
FROM audit_logs
LEFT JOIN users ON audit_logs.user_id = users.id
WHERE audit_logs.target_type = 'system' 
  AND audit_logs.target_id = 1
ORDER BY created_at DESC;

-- Get all delete actions (for safety audit)
SELECT 
    users.name as user_name,
    audit_logs.target_type,
    audit_logs.target_id,
    datetime(audit_logs.created_at) as deleted_at
FROM audit_logs
LEFT JOIN users ON audit_logs.user_id = users.id
WHERE audit_logs.action LIKE '%DELETE%'
ORDER BY created_at DESC;

-- ============================================
-- SYSTEM HEALTH HISTORY QUERIES
-- ============================================

-- Get health history for specific system (last 24 hours)
SELECT 
    id,
    system_id,
    status,
    health_status,
    cpu_usage,
    memory_usage,
    disk_usage,
    datetime(timestamp) as checked
FROM system_health
WHERE system_id = 1
  AND timestamp > datetime('now', '-1 day')
ORDER BY timestamp DESC;

-- Get average metrics per system (last 24 hours)
SELECT 
    system_id,
    AVG(cpu_usage) as avg_cpu,
    AVG(memory_usage) as avg_memory,
    AVG(disk_usage) as avg_disk,
    MAX(cpu_usage) as peak_cpu
FROM system_health
WHERE timestamp > datetime('now', '-1 day')
GROUP BY system_id
ORDER BY system_id;

-- Get systems with most health records
SELECT 
    system_id,
    COUNT(*) as record_count
FROM system_health
GROUP BY system_id
ORDER BY record_count DESC;

-- Get uptime percentage for system
SELECT 
    system_id,
    COUNT(CASE WHEN status = 'Online' THEN 1 END) * 100.0 / COUNT(*) as uptime_percent
FROM system_health
WHERE timestamp > datetime('now', '-7 days')
GROUP BY system_id
ORDER BY uptime_percent DESC;

-- ============================================
-- MAINTENANCE QUERIES
-- ============================================

-- Count total records per table
SELECT 
    'systems' as table_name, COUNT(*) as count FROM systems
UNION ALL
SELECT 'users', COUNT(*) FROM users
UNION ALL
SELECT 'audit_logs', COUNT(*) FROM audit_logs
UNION ALL
SELECT 'system_health', COUNT(*) FROM system_health;

-- Get database size information
SELECT 
    'lab.db' as database,
    (SELECT COUNT(*) FROM systems) as systems_count,
    (SELECT COUNT(*) FROM users) as users_count,
    (SELECT COUNT(*) FROM audit_logs) as audit_logs_count,
    (SELECT COUNT(*) FROM system_health) as health_records_count;

-- Delete old health records (older than 30 days)
-- WARNING: This deletes data, backup first!
-- DELETE FROM system_health
-- WHERE timestamp < datetime('now', '-30 days');

-- Delete old audit logs (older than 90 days)
-- WARNING: This deletes data, backup first!
-- DELETE FROM audit_logs
-- WHERE created_at < datetime('now', '-90 days');

-- Export systems to CSV format (view in tool, copy to file)
SELECT 
    id || ',' ||
    quote(name) || ',' ||
    quote(ip_address) || ',' ||
    quote(mac_address) || ',' ||
    status || ',' ||
    health_status
FROM systems;

-- ============================================
-- TROUBLESHOOTING QUERIES
-- ============================================

-- Find duplicate system names (should not exist)
SELECT name, COUNT(*) as count
FROM systems
GROUP BY name
HAVING count > 1;

-- Find duplicate usernames (should not exist)
SELECT name, COUNT(*) as count
FROM users
GROUP BY name
HAVING count > 1;

-- Get systems without IP addresses
SELECT id, name
FROM systems
WHERE ip_address IS NULL OR ip_address = '';

-- Get systems without recent health checks (no data in 1 hour)
SELECT 
    id,
    name,
    status,
    datetime(last_check_time) as last_checked,
    datetime('now') as current_time
FROM systems
WHERE last_check_time < datetime('now', '-1 hour')
   OR last_check_time IS NULL;

-- Get users with inactive accounts
SELECT id, name, role, is_active
FROM users
WHERE is_active = 0;

-- ============================================
-- REPORTING QUERIES
-- ============================================

-- Daily summary
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_actions,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(CASE WHEN action LIKE 'ADD%' THEN 1 END) as adds,
    COUNT(CASE WHEN action LIKE 'DELETE%' THEN 1 END) as deletes,
    COUNT(CASE WHEN action LIKE 'UPDATE%' THEN 1 END) as updates
FROM audit_logs
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- System uptime report (last 7 days)
SELECT 
    system_id,
    (SELECT name FROM systems WHERE id = system_health.system_id) as system_name,
    COUNT(CASE WHEN status = 'Online' THEN 1 END) * 100.0 / COUNT(*) as uptime_percent,
    COUNT(CASE WHEN status = 'Offline' THEN 1 END) as offline_events,
    MIN(cpu_usage) as min_cpu,
    AVG(cpu_usage) as avg_cpu,
    MAX(cpu_usage) as max_cpu
FROM system_health
WHERE timestamp > datetime('now', '-7 days')
GROUP BY system_id
ORDER BY uptime_percent DESC;

-- Peak usage times
SELECT 
    strftime('%H:00', timestamp) as hour,
    COUNT(*) as sample_count,
    AVG(cpu_usage) as avg_cpu,
    AVG(memory_usage) as avg_memory,
    MAX(cpu_usage) as peak_cpu
FROM system_health
WHERE timestamp > datetime('now', '-7 days')
GROUP BY hour
ORDER BY hour;

-- ============================================
-- BACKUP VERIFICATION
-- ============================================

-- Verify data integrity (no gaps)
SELECT 
    id,
    name,
    CASE 
        WHEN ip_address IS NULL THEN 'Missing IP'
        WHEN status IS NULL THEN 'Missing Status'
        WHEN created_at IS NULL THEN 'Missing Created Date'
        ELSE 'OK'
    END as status
FROM systems;

-- Quick health check
SELECT 
    (SELECT COUNT(*) FROM systems) as total_systems,
    (SELECT COUNT(*) FROM systems WHERE status = 'Online') as online_systems,
    (SELECT COUNT(*) FROM systems WHERE status = 'Offline') as offline_systems,
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM users WHERE is_active = 1) as active_users,
    (SELECT COUNT(*) FROM audit_logs) as total_audit_records;

-- ============================================
-- NOTES
-- ============================================
-- Remember: Always backup before running DELETE queries!
-- These are SELECT-only safe queries unless explicitly noted.
-- For complex analysis, consider exporting to CSV and using Excel/Python.
-- For production systems, implement proper backup procedures.
