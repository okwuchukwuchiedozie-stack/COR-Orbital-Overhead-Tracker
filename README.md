# 🛰️ Overhead ISS Tracker & Email Notifier Engine

An automated tracking script built in Python that monitors the real-time position of the International Space Station (ISS). When the engine determines that the space station is directly above your coordinate grid during dark night hours, it automatically uses secure SMTP layers to drop a target notification email straight to your device.

---

## 🏗️ Key Architectural Layout & Fixes

- **Timezone Alignment Guarantee:** Replaces manual string splitting text methods with native timezone-aware `datetime.now(dt.UTC)` evaluations, aligning local clocks smoothly with the sunrise/sunset API target outputs.
- **Robust Exception Firewalls:** Wraps API requests inside descriptive network exception tracking blocks (`timeout=10`) to prevent infinite freezes if connection states fail.
- **Explicit Functional Returns:** Cleans up implicit return logic conditions by applying explicit type hint tags (`-> bool` and `-> None`), ensuring predictable variable behavior.
- **Isolated Environmental Security:** Leverages the `python-dotenv` driver suite to isolate sensitive credential attributes and custom latitude/longitude parameters out of public sight.

---

## 📦 System Dependencies

- **requests:** Manages API endpoint calls to the telemetry databases.
- **python-dotenv:** Sources variable bindings directly from the hidden system layer environment.

Ensure you install these tools via your terminal prompt space before firing up the script:
```bash
pip install requests python-dotenv
```

---

## 🚀 Step-by-Step Initial Setup Guide

### 1. Initialize Configuration Secrets
Create a file named `.env` inside your project root and drop your variables directly inside:
```text
EMAIL=your_sending_email@gmail.com
EMAIL_PASSWORD=your_app_generated_password
MY_LAT=6.342450
MY_LNG=5.633840
```
*(Note: If you use Gmail, the `EMAIL_PASSWORD` variable must be a custom 16-character **App Password** generated inside your Google Account Security Dashboard, not your basic standard login password).*

### 2. Security Guard Rails (.gitignore)
Create a `.gitignore` text configuration container file to ensure your secret parameter metrics never get uploaded to GitHub:
```text
.env
__pycache__/
*.pyc
```

### 3. Execution Integration Action
Launch the continuous background processing thread loop directly inside your workspace terminal window:
```bash
python main.py
```

---

## ⚖️ License
Distributed cleanly under the custom **COR_CARES** Development Framework. Copyright &copy; 2026. All rights reserved.
