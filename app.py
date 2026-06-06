from flask import Flask, redirect, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash
from config import Config
from models import db, Admin
from utils.seed_data import seed_voters

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize session
    Session(app)

    # Initialize SQLAlchemy
    db.init_app(app)

    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Initialize default admin if not exists
        admin = Admin.query.filter_by(username="bharat").first()

        if not admin:
            hashed_pwd = generate_password_hash("bharat123")
            new_admin = Admin(
                username="bharat",
                password=hashed_pwd
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Admin account created.")
            
        # Load voters
        seed_voters(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.voter import voter_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(voter_bp, url_prefix='/voter')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
