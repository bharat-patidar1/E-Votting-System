from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from models import db, Admin, Voter, ActivityLog
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_type = request.form.get('login_type')
        username_or_id = request.form.get('username')
        password = request.form.get('password')
        
        if login_type == 'admin':
            admin = Admin.query.filter_by(username=username_or_id).first()
            
            if admin is None:
                flash('Incorrect admin username.', 'danger')
            elif admin.locked == 1:
                flash('Admin account is locked due to too many failed attempts.', 'danger')
            elif not check_password_hash(admin.password, password):
                admin.failed_attempts += 1
                if admin.failed_attempts >= 3:
                    admin.locked = 1
                db.session.commit()
                
                if admin.locked:
                    flash('Admin account locked. Too many failed attempts.', 'danger')
                else:
                    flash('Incorrect password.', 'danger')
            else:
                admin.failed_attempts = 0
                db.session.commit()
                session.clear()
                session['user_id'] = admin.id
                session['role'] = 'admin'
                
                # Log admin login
                log = ActivityLog(admin_id=admin.id, action="Logged in successfully.")
                db.session.add(log)
                db.session.commit()
                
                return redirect(url_for('admin.dashboard'))
                
        elif login_type == 'voter':
            voter = Voter.query.filter_by(voter_id=username_or_id).first()
            
            if voter is None:
                flash('Incorrect Voter ID.', 'danger')
            elif voter.locked == 1:
                flash('Voter account is locked.', 'danger')
            elif not check_password_hash(voter.password, password):
                voter.failed_attempts += 1
                if voter.failed_attempts >= 3:
                    voter.locked = 1
                db.session.commit()
                
                if voter.locked:
                    flash('Voter account locked. Too many failed attempts.', 'danger')
                else:
                    flash('Incorrect password.', 'danger')
            else:
                voter.failed_attempts = 0
                db.session.commit()
                session.clear()
                session['user_id'] = voter.voter_id
                session['role'] = 'voter'
                return redirect(url_for('voter.dashboard'))
                
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    if session.get('role') == 'admin':
        log = ActivityLog(admin_id=session.get('user_id'), action="Logged out.")
        db.session.add(log)
        db.session.commit()
        
    session.clear()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('auth.login'))
