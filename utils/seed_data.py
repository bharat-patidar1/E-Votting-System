from werkzeug.security import generate_password_hash
from models import db, Voter

def seed_voters(app):
    """
    Seeds initial voter data directly into the database using SQLAlchemy.
    This replaces the previous Excel dependency (pandas/numpy).
    """
    with app.app_context():
        # Check if voters already exist so we don't duplicate them
        if Voter.query.first():
            print("Voter data already initialized. Skipping seeding.")
            return

        print("Seeding initial voter data...")
        
        # Sample voters data
        sample_voters = [
            {"voter_id": "VOTER001", "name": "Test Voter 1", "password": "pass123"},
            {"voter_id": "VOTER002", "name": "Test Voter 2", "password": "pass123"},
            {"voter_id": "VOTER003", "name": "Test Voter 3", "password": "pass123"},
            {"voter_id": "VOTER004", "name": "Test Voter 4", "password": "pass123"},
            {"voter_id": "VOTER005", "name": "Test Voter 5", "password": "pass123"},
        ]

        for v_data in sample_voters:
            hashed_pwd = generate_password_hash(v_data["password"])
            try:
                voter = Voter(
                    voter_id=v_data["voter_id"], 
                    name=v_data["name"], 
                    password=hashed_pwd
                )
                db.session.add(voter)
            except Exception as e:
                print(f"Failed to process voter {v_data['voter_id']}: {e}")
        
        db.session.commit()
        print("Initial voters seeded successfully.")
