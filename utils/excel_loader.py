import pandas as pd
import os
from werkzeug.security import generate_password_hash
from models import db, Voter

def load_voters_from_excel(app):
    """
    Loads voters from the specified Excel file and inserts them into the database using SQLAlchemy.
    Passwords are hashed before insertion.
    """
    excel_path = app.config['VOTER_DATA_FILE']
    if not os.path.exists(excel_path):
        print(f"Warning: {excel_path} not found. Skipping voter initialization.")
        return

    try:
        df = pd.read_excel(excel_path)
        required_cols = {'VoterID', 'Name', 'Password'}
        
        if not required_cols.issubset(df.columns):
            print(f"Error: {excel_path} is missing required columns. Must contain {required_cols}.")
            return

        with app.app_context():
            # Check if voters already exist
            if Voter.query.first():
                print("Voter data already initialized. Skipping Excel load.")
                return

            print("Loading voter data from Excel...")
            for _, row in df.iterrows():
                voter_id = str(row['VoterID']).strip()
                name = str(row['Name']).strip()
                password = str(row['Password']).strip()
                
                # Basic validation
                if not voter_id or not name or not password:
                    continue

                hashed_pwd = generate_password_hash(password)
                try:
                    voter = Voter(voter_id=voter_id, name=name, password=hashed_pwd)
                    db.session.add(voter)
                except Exception as e:
                    print(f"Failed to process voter {voter_id}: {e}")
            
            db.session.commit()
            print("Voter data loaded successfully.")
            
    except Exception as e:
        print(f"Error reading Excel file: {e}")
