# routes/monitor_routes.py
from flask import Blueprint, render_template
from models.models import Machine, Sector

bp = Blueprint('monitor', __name__)

@bp.route('/')
def dashboard():
    machines = Machine.query.all()
    return render_template('monitor/dashboard.html', machines=machines)

@bp.route('/machine/<int:machine_id>')
def machine_detail(machine_id):
    machine = Machine.query.get_or_404(machine_id)
    return render_template('monitor/machine_detail.html', machine=machine)  

@bp.route('/sectors')
def sectors():
    sectors = Sector.query.all()
    return render_template('monitor/sectors.html', sectors=sectors) 
@bp.route('/sector/<int:sector_id>')
def sector_detail(sector_id):
    sector = Sector.query.get_or_404(sector_id)
    return render_template('monitor/sector_detail.html', sector=sector)     
@bp.route('/alerts')
def alerts():
    # Placeholder for alerts logic
    alerts = []  # This would be replaced with actual alert fetching logic
    return render_template('monitor/alerts.html', alerts=alerts)    
@bp.route('/reports')
def reports():
    # Placeholder for reports logic
    reports = []  # This would be replaced with actual report fetching logic
    return render_template('monitor/reports.html', reports=reports) 
@bp.route('/settings')
def settings():
    return render_template('monitor/settings.html')
@bp.route('/about')
def about():
    return render_template('monitor/about.html')    
@bp.route('/help')
def help():
    return render_template('monitor/help.html')
    return render_template('monitor/help.html') 
@bp.route('/contact')
def contact():
    return render_template('monitor/contact.html')
@bp.route('/faq')
def faq():
    return render_template('monitor/faq.html')
@bp.route('/terms')
def terms():
    return render_template('monitor/terms.html')

@bp.route('/privacy')
def privacy():
    return render_template('monitor/privacy.html')  
@bp.route('/dashboard')
def main_dashboard():
    return render_template('monitor/main_dashboard.html')   
@bp.route('/performance')
def performance():
    return render_template('monitor/performance.html')
@bp.route('/maintenance')
def maintenance():
    return render_template('monitor/maintenance.html')
@bp.route('/usage')
def usage():
    return render_template('monitor/usage.html')    
@bp.route('/history')
def history():
    return render_template('monitor/history.html')
@bp.route('/analytics')
def analytics():
    return render_template('monitor/analytics.html')    
@bp.route('/notifications')
def notifications():
    return render_template('monitor/notifications.html')    
@bp.route('/logs')
def logs():
    return render_template('monitor/logs.html') 
@bp.route('/users')
def users():
    return render_template('monitor/users.html')
@bp.route('/profile')
def profile():
    return render_template('monitor/profile.html')  
@bp.route('/settings/general')
def general_settings():
    return render_template('monitor/settings_general.html')
@bp.route('/settings/security')
def security_settings():
    return render_template('monitor/settings_security.html')    
@bp.route('/settings/notifications')
def notification_settings():
    return render_template('monitor/settings_notifications.html')
@bp.route('/settings/integrations')
def integration_settings():
    return render_template('monitor/settings_integrations.html')
@bp.route('/settings/billing')
def billing_settings():
    return render_template('monitor/settings_billing.html')
@bp.route('/settings/api')
def api_settings():
    return render_template('monitor/settings_api.html') 
@bp.route('/settings/about')
def about_settings():
    return render_template('monitor/settings_about.html')   
@bp.route('/settings/help')
def help_settings():
    return render_template('monitor/settings_help.html')    
@bp.route('/settings/contact')
def contact_settings():
    return render_template('monitor/settings_contact.html') 