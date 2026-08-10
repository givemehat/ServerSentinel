# ServerSentinel 📡

<div align="center">
  <img src="https://img.shields.io/github/repo-size/givemehat/ServerSentinel?style=for-the-badge&color=blue" alt="Repository Size" />
  <img src="https://img.shields.io/github/license/givemehat/ServerSentinel?style=for-the-badge&color=green" alt="License" />
  <img src="https://img.shields.io/github/commit-activity/m/givemehat/ServerSentinel?style=for-the-badge&color=orange" alt="Commit Activity" />
  <img src="https://img.shields.io/github/last-commit/givemehat/ServerSentinel?style=for-the-badge&color=red" alt="Last Commit" />
</div>

<br/>

**ServerSentinel** is a lightweight, cloud-native server monitoring and telemetry agent. It gathers critical system metrics (CPU, Memory, Disk, Network) across a distributed fleet of servers and streams them to a centralized FastAPI ingestion server, visualized via a beautiful Streamlit dashboard.

## 🚀 Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

## ✨ Features
* **Cross-Platform Agent:** A lightweight `psutil` based agent capable of running on Linux, macOS, or Windows.
* **High-Performance Ingestion:** Built with FastAPI and SQLAlchemy for rapid metric persistence.
* **Real-time Analytics Dashboard:** A Streamlit dashboard utilizing Plotly for historical trend analysis.
* **Docker Native:** Deploy the entire stack effortlessly using `docker-compose`.

## 📦 Quickstart (Docker)

Spin up the entire stack (API, Agent, Dashboard) using Docker:

```bash
git clone https://github.com/givemehat/ServerSentinel.git
cd ServerSentinel
docker-compose up --build
```

Access the services:
* **Dashboard:** http://localhost:8501
* **API Swagger Docs:** http://localhost:8000/docs

## 🛠️ Manual Setup

If you prefer to run it manually without Docker:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the FastAPI Ingestion Server
uvicorn server.main:app --host 0.0.0.0 --port 8000

# 3. Start the Monitoring Agent
python agent/agent.py

# 4. Start the Streamlit Dashboard
streamlit run dashboard/app.py
```

## 🤝 Contributing
Contributions are always welcome! Feel free to open issues or submit Pull Requests.
