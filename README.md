# Gothenburg Tram System

A full-stack Django web application for modeling, analyzing, and visualizing the Gothenburg tram network.

This project was developed in three progressive layers:
data processing → graph modeling → web application.

---

## Features

- Parse and structure tram network data
- Model tram stops and routes as graph structures
- Compute and visualize routes
- Interactive web interface for exploring the tram system
- Django-based backend with modular architecture

---

## Project Structure

gothenburg-tram-system/

- lab1-tram-data/        → Data extraction and preprocessing
- lab2-tram-graph/       → Graph modeling and route computation
- lab3-tram-webapp/      → Full-stack Django web application

---

## Tech Stack

- Python
- Django
- SQLite (development)
- NetworkX (graph modeling)
- HTML / Django templates

---

## How to Run (Web Application)

Navigate to the web application directory:

    cd lab3-tram-webapp

Create a virtual environment:

    python -m venv venv
    source venv/bin/activate   (macOS / Linux)

Install dependencies:

    pip install -r requirements.txt

Apply migrations:

    python manage.py migrate

Run the development server:

    python manage.py runserver

Open in browser:

    http://127.0.0.1:8000/

---

## Learning Focus

This project demonstrates:

- Data processing pipelines
- Graph-based modeling of transport networks
- Separation of concerns across project layers
- Full-stack web application development with Django
- Modular and maintainable Python architecture

---

## Notes

This repository contains a cleaned and production-style version of the project structure.

Local development artifacts (virtual environments, databases, cache files) are excluded.
