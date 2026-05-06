# 🚀 Lab Control System - Multi-Machine Deployment Guide

## आपका Lab Control System अब Multiple PCs को Monitor कर सकता है!

### 📋 Step-by-Step Guide

#### Step 1: Server Setup (एक बार करें)
1. अपने main PC पर Lab Control System install करें
2. Database में systems add करें (जितने PCs monitor करना है)
3. Server को run करें: `python run.py`
4. Server का IP address note करें (e.g., 192.168.1.100)

#### Step 2: Client Setup (हर PC पर करें)

##### Windows PC के लिए:
1. `client_setup.bat` और `monitoring_agent.py` को client PC पर copy करें
2. `client_setup.bat` को Administrator के रूप में run करें
3. Lab Control System से System ID check करें
4. Agent को run करें:

```batch
python monitoring_agent.py --system-id YOUR_ID --server http://YOUR_SERVER_IP:5000
```

##### Linux/Mac PC के लिए:
1. `client_setup.py` और `monitoring_agent.py` को client PC पर copy करें
2. Setup run करें:

```bash
python client_setup.py
```

3. Agent को run करें:

```bash
python monitoring_agent.py --system-id YOUR_ID --server http://YOUR_SERVER_IP:5000
```

#### Step 3: System ID कैसे पता करें?

1. Lab Control System में login करें
2. Systems page पर जाएं
3. Table में ID column देखें
4. उस ID को agent में use करें

#### Step 4: Testing

Agent run करने के बाद:
- Server पर Systems page check करें
- Status "Online" होना चाहिए
- CPU, Memory, Disk usage show होना चाहिए
- हर 30 seconds में update होना चाहिए

### 📁 Files Required for Client PCs:

**Windows:**
- `client_setup.bat`
- `monitoring_agent.py`

**Linux/macOS:**
- `client_setup.py`
- `monitoring_agent.py`

### 🔧 Troubleshooting

**Problem:** "psutil not found"
**Solution:** `pip install psutil requests` run करें

**Problem:** "Connection refused"
**Solution:** Server IP और port check करें, firewall check करें

**Problem:** Agent start नहीं होता
**Solution:** Python install है कि नहीं check करें

### 💡 Pro Tips

1. **Auto-Start:** Windows Task Scheduler या Linux crontab से agent को boot पर automatically start कराएं
2. **Network:** सभी PCs same network में होने चाहिए
3. **Firewall:** Port 5000 को allow करें
4. **Monitoring:** Server पर real-time status देख सकते हैं

### 📊 What Gets Monitored

हर PC से ये information मिलती है:
- ✅ CPU Usage (%)
- ✅ Memory Usage (%)
- ✅ Disk Usage (%)
- ✅ Online/Offline Status
- ✅ Health Status (Healthy/Warning/Critical)
- ✅ Last Check Time

### 🎯 Example Setup

**Server:** 192.168.1.100 (Main Lab PC)
**Clients:**
- Lab-PC-01: `python monitoring_agent.py --system-id 1 --server http://192.168.1.100:5000`
- Lab-PC-02: `python monitoring_agent.py --system-id 2 --server http://192.168.1.100:5000`
- Teacher-PC: `python monitoring_agent.py --system-id 3 --server http://192.168.1.100:5000`

अब आपका Lab Control System multiple machines को monitor कर सकता है! 🚀