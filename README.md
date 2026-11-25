# SYNTRA

### Network Intrusion Detection & Real-Time Traffic Analysis System

SYNTRA is a cybersecurity project designed to monitor
network traffic, detect suspicious activity, and visualize
security events through a centralized web dashboard.

## Objectives

- Network traffic monitoring
- Signature-based intrusion detection
- Security event collection and analysis
- Centralized alert visualization
- Custom intrusion detection rules

## Technology Stack

- Python
- Flask
- Suricata IDS
- SQLite
- HTML, CSS and JavaScript
- Kali Linux

## Project Structure

    SYNTRA/
    ├── app/
    │   ├── collector.py
    │   ├── database.py
    │   ├── parser.py
    │   ├── routes.py
    │   ├── static/
    │   └── templates/
    ├── rules/
    │   └── syntra.rules
    ├── requirements.txt
    └── README.md

## Architecture

    Network Traffic
          |
          v
    Suricata IDS
          |
          v
    Event Collection and Parsing
          |
          v
    SQLite Database
          |
          v
    Flask Web Dashboard

## Purpose

Developed as an academic Network Security project
to demonstrate practical intrusion detection,
network monitoring and security event analysis.

## Disclaimer

This project is intended for educational purposes
and authorized network monitoring only.

## Author

Recon-404-afk
Cyber Security Student
