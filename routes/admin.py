from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Campaign, Candidate, Vote, Result, ActivityLog
from functools import wraps
from datetime import datetime
import uuid
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def log_activity(action):
    log = ActivityLog(admin_id=session['user_id'], action=action)
    db.session.add(log)

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    campaigns = Campaign.query.all()
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(10).all()
    return render_template('admin/dashboard.html', campaigns=campaigns, logs=logs)

@admin_bp.route('/campaign/create', methods=('GET', 'POST'))
@admin_required
def create_campaign():
    if request.method == 'POST':
        campaign_name = request.form['campaign_name']
        constituency = request.form['constituency']
        start_datetime = datetime.strptime(request.form['start_datetime'], '%Y-%m-%dT%H:%M')
        end_datetime = datetime.strptime(request.form['end_datetime'], '%Y-%m-%dT%H:%M')
        
        new_campaign = Campaign(
            campaign_id=str(uuid.uuid4()),
            campaign_name=campaign_name,
            constituency=constituency,
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )
        db.session.add(new_campaign)
        log_activity(f"Created new campaign: {campaign_name}")
        db.session.commit()
        
        flash('Campaign created successfully.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/create_campaign.html')

@admin_bp.route('/campaign/<campaign_id>/edit', methods=('GET', 'POST'))
@admin_required
def edit_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    if request.method == 'POST':
        campaign.campaign_name = request.form['campaign_name']
        campaign.constituency = request.form['constituency']
        campaign.start_datetime = datetime.strptime(request.form['start_datetime'], '%Y-%m-%dT%H:%M')
        campaign.end_datetime = datetime.strptime(request.form['end_datetime'], '%Y-%m-%dT%H:%M')

        log_activity(f"Edited campaign: {campaign.campaign_name}")
        db.session.commit()
        
        flash('Campaign updated successfully.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_campaign.html', campaign=campaign)

@admin_bp.route('/campaign/<campaign_id>/delete', methods=('POST',))
@admin_required
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign_name = campaign.campaign_name
    db.session.delete(campaign)
    log_activity(f"Deleted campaign: {campaign_name}")
    db.session.commit()
    flash('Campaign deleted.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/campaign/<campaign_id>/candidates', methods=('GET', 'POST'))
@admin_required
def manage_candidates(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    
    if request.method == 'POST':
        candidate_name = request.form['candidate_name']
        party_symbol = request.form['party_symbol']
        party_name = request.form['party_name']
        additional_info = request.form['additional_info']
        
        new_candidate = Candidate(
            candidate_id=str(uuid.uuid4()),
            campaign_id=campaign_id,
            candidate_name=candidate_name,
            party_symbol=party_symbol,
            party_name=party_name,
            additional_info=additional_info
        )
        db.session.add(new_candidate)
        log_activity(f"Added candidate {candidate_name} to campaign {campaign.campaign_name}")
        db.session.commit()
        
        flash('Candidate added successfully.', 'success')

    candidates = Candidate.query.filter_by(campaign_id=campaign_id).all()
    return render_template('admin/candidates.html', candidates=candidates, campaign=campaign)

@admin_bp.route('/campaign/<campaign_id>/publish_results', methods=('POST',))
@admin_required
def publish_results(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.is_published = True
    
    # Calculate results
    vote_counts = db.session.query(
        Vote.candidate_id, func.count(Vote.id).label('total')
    ).filter_by(campaign_id=campaign_id).group_by(Vote.candidate_id).all()
    
    for row in vote_counts:
        # Check if result already exists
        existing_result = Result.query.filter_by(campaign_id=campaign_id, candidate_id=row.candidate_id).first()
        if existing_result:
            existing_result.total_votes = row.total
        else:
            result = Result(campaign_id=campaign_id, candidate_id=row.candidate_id, total_votes=row.total)
            db.session.add(result)
    
    log_activity(f"Published results for campaign {campaign.campaign_name}")
    db.session.commit()
    
    flash('Results published successfully.', 'success')
    return redirect(url_for('admin.dashboard'))
