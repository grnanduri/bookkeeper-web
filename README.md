# Bookkeeper Web App

A simple bookkeeping web application built with Flask and SQLite.

**Live Demo**: [https://bookkeeper-web.onrender.com](https://bookkeeper-web.onrender.com)

## Features

- Add income and expense transactions
- View all transactions in a table
- Export data to CSV and Excel
- Mobile-friendly UI using Bootstrap
- Deployable via GitHub + Render

## Screenshots

_Add your screenshots here for a better README presentation._

## Tech Stack

- Python 3
- Flask
- SQLite
- Bootstrap 5
- HTML/Jinja2

## Getting Started (Local Setup)

1. Clone this repository:

    ```bash
    git clone https://github.com/grnanduri/bookkeeper-flask.git
    cd bookkeeper-flask
    ```

2. Create a virtual environment and activate it (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\\Scripts\\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the app:

    ```bash
    python app.py
    ```

5. Open your browser and go to [http://localhost:5000](http://localhost:5000)

## Deploying to Render

1. Push this code to a GitHub repo
2. Go to [https://render.com](https://render.com)
3. Click "New Web Service" → "Connect GitHub Repo"
4. Use the following settings:

    - **Build Command:** `pip install -r requirements.txt`
    - **Start Command:** `python app.py`
    - **Runtime:** Python
    - **Port Binding:** `$PORT` environment variable (Render handles this automatically)

Render will give you a public URL to access your app.

## File Structure

bookkeeper-flask/
├── app.py # Flask application
├── templates/
│ └── index.html # HTML page with transaction form + table
├── requirements.txt # Python dependencies
├── Procfile # Required by Render


## Exported Formats

- **transactions.csv** – can be opened in Excel/Google Sheets
- **transactions.xlsx** – Excel file (via openpyxl)

## Notes

- SQLite database is ephemeral when deployed on Render free tier.
- Export your data regularly.
- You can upgrade to PostgreSQL or other persistent storage in the future.