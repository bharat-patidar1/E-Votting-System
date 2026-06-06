from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Campaign, Candidate, Vote, Result
from functools import wraps
from datetime import datetime

voter_bp = Blueprint('voter', __name__)

def voter_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'voter':
            flash('Voter access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@voter_bp.route('/dashboard')
@voter_required
def dashboard():
    all_campaigns = Campaign.query.all()
    
    active_campaigns = []
    published_campaigns = []
    
    for c in all_campaigns:
        if c.status == 'Active':
            active_campaigns.append(c)
        elif c.status == 'Published':
            published_campaigns.append(c)

    return render_template('voter/dashboard.html', campaigns=active_campaigns, published_campaigns=published_campaigns)

@voter_bp.route('/campaign/<campaign_id>/vote', methods=('GET', 'POST'))
@voter_required
def vote(campaign_id):
    voter_id = session['user_id']
    campaign = Campaign.query.get_or_404(campaign_id)
    
    if campaign.status != 'Active':
        flash('This campaign is not currently active.', 'danger')
        return redirect(url_for('voter.dashboard'))

    # Check if voter already voted
    existing_vote = Vote.query.filter_by(campaign_id=campaign_id, voter_id=voter_id).first()
    
    if existing_vote:
        flash('You have already cast your vote for this campaign.', 'warning')
        return redirect(url_for('voter.dashboard'))

    candidates = Candidate.query.filter_by(campaign_id=campaign_id).all()

    if request.method == 'POST':
        candidate_id = request.form.get('candidate_id')
        if not candidate_id:
            flash('Please select a candidate to vote for.', 'danger')
        else:
            new_vote = Vote(campaign_id=campaign_id, voter_id=voter_id, candidate_id=candidate_id)
            db.session.add(new_vote)
            db.session.commit()
            flash('Your vote has been cast successfully!', 'success')
            return redirect(url_for('voter.dashboard'))

    return render_template('voter/vote.html', campaign=campaign, candidates=candidates)

@voter_bp.route('/campaign/<campaign_id>/results')
@voter_required
def results(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    
    if campaign.status != 'Published':
        flash('Results for this campaign are not published yet.', 'info')
        return redirect(url_for('voter.dashboard'))

    # Get results with candidate details
    results_data = db.session.query(Result, Candidate).join(Candidate, Result.candidate_id == Candidate.candidate_id).filter(Result.campaign_id == campaign_id).order_by(Result.total_votes.desc()).all()

    total_votes = sum(r.Result.total_votes for r in results_data)
    
    # Format data for chart
    chart_labels = [r.Candidate.candidate_name for r in results_data]
    chart_data = [r.Result.total_votes for r in results_data]

    winner = results_data[0] if results_data and len(results_data) > 0 else None

    return render_template('voter/results.html', campaign=campaign, results=results_data, total_votes=total_votes, winner=winner, chart_labels=chart_labels, chart_data=chart_data)
