from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    failed_attempts = db.Column(db.Integer, default=0)
    locked = db.Column(db.Integer, default=0)

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    campaign_id = db.Column(db.String(50), primary_key=True)
    campaign_name = db.Column(db.String(150), nullable=False)
    constituency = db.Column(db.String(100), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    
    candidates = db.relationship('Candidate', backref='campaign', lazy=True, cascade="all, delete-orphan")
    votes = db.relationship('Vote', backref='campaign', lazy=True, cascade="all, delete-orphan")
    results = db.relationship('Result', backref='campaign', lazy=True, cascade="all, delete-orphan")

    @property
    def status(self):
        if self.is_published:
            return 'Published'
        now = datetime.now()
        if now < self.start_datetime:
            return 'Upcoming'
        elif self.start_datetime <= now <= self.end_datetime:
            return 'Active'
        else:
            return 'Completed'

class Candidate(db.Model):
    __tablename__ = 'candidates'
    candidate_id = db.Column(db.String(50), primary_key=True)
    campaign_id = db.Column(db.String(50), db.ForeignKey('campaigns.campaign_id'), nullable=False)
    candidate_name = db.Column(db.String(100), nullable=False)
    party_symbol = db.Column(db.String(50))
    party_name = db.Column(db.String(100), nullable=False)
    additional_info = db.Column(db.Text)
    
    votes = db.relationship('Vote', backref='candidate', lazy=True, cascade="all, delete-orphan")
    results = db.relationship('Result', backref='candidate', lazy=True, cascade="all, delete-orphan")

class Voter(db.Model):
    __tablename__ = 'voters'
    voter_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    failed_attempts = db.Column(db.Integer, default=0)
    locked = db.Column(db.Integer, default=0)
    
    votes = db.relationship('Vote', backref='voter', lazy=True)

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.String(50), db.ForeignKey('campaigns.campaign_id'), nullable=False)
    voter_id = db.Column(db.String(50), db.ForeignKey('voters.voter_id'), nullable=False)
    candidate_id = db.Column(db.String(50), db.ForeignKey('candidates.candidate_id'), nullable=False)
    vote_time = db.Column(db.DateTime, default=datetime.utcnow)

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.String(50), db.ForeignKey('campaigns.campaign_id'), nullable=False)
    candidate_id = db.Column(db.String(50), db.ForeignKey('candidates.candidate_id'), nullable=False)
    total_votes = db.Column(db.Integer, default=0)

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
