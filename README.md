# e-Voting System Prototype

This is a complete, production-quality prototype for the e-Voting System of the Election Commission of Madhya Pradesh.

## Features Added

1. **Flask-SQLAlchemy**: Robust Object-Relational Mapping for safe database queries.
2. **Dynamic Campaign Status**: Campaigns automatically calculate their status (Upcoming, Active, Completed, Published) based on current datetime.
3. **Chart.js Visualization**: Beautiful pie charts and bar charts on the results page.
4. **Activity Logs**: Tracks admin actions securely in the database and displays them on the dashboard.
5. **Vote Percentage**: Calculates exact vote percentages and shows them in Bootstrap progress bars.

## Project Structure

- `app.py`: Main application factory and initialization script.
- `config.py`: Application configurations including `SQLALCHEMY_DATABASE_URI`.
- `models.py`: Database models for Admin, Voter, Campaign, Candidate, Vote, Result, and ActivityLog.
- `routes/`: Contains blueprints for `auth`, `admin`, and `voter`.
- `utils/excel_loader.py`: Pandas loader that feeds Excel data into the SQLAlchemy `Voter` model securely.
- `templates/`: Jinja2 HTML templates enhanced with Chart.js and conditional status badging.
- `static/`: Custom CSS and assets.

## Installation & Setup

1. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python3 app.py
   ```
   *The database and sample voters will be initialized automatically on the first run.*

## Screenshots

*(In a real production environment, place images in `static/images/` and reference them here)*
- `dashboard.png`: Shows the admin panel with activity logs and colored status badges.
- `voting.png`: The EVM-style radio button interface.
- `results.png`: Chart.js visualizations of the winner and vote distribution.

## Default Credentials

### Admin
- **Username**: `admin`
- **Password**: `admin123`

### Voters (From `voter_data.xlsx`)
- **Voter ID**: `VOTER001`, `VOTER002`, `VOTER003`, `VOTER004`, `VOTER005`
- **Password**: `pass123`
