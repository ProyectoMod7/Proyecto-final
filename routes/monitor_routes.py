from flask import Blueprint, render_template
from models.models import Machine, Sector

monitor_bp = Blueprint('monitor', __name__)

@monitor_bp.route('/')
def dashboard():
    machines = Machine.query.all()
    return render_template('monitor/dashboard.html', machines=machines)

@monitor_bp.route('/machine/<int:machine_id>')
def machine_detail(machine_id):
    machine = Machine.query.get_or_404(machine_id)
    return render_template('monitor/machine_detail.html', machine=machine)

@monitor_bp.route('/sectors')
def sectors():
    sectors = Sector.query.all()
    return render_template('monitor/sectors.html', sectors=sectors)

@monitor_bp.route('/sector/<int:sector_id>')
def sector_detail(sector_id):
    sector = Sector.query.get_or_404(sector_id)
    return render_template('monitor/sector_detail.html', sector=sector)

@monitor_bp.route('/alerts')
def alerts():
    alerts = []  # Reemplaza con lógica real
    return render_template('monitor/alerts.html', alerts=alerts)

@monitor_bp.route('/reports')
def reports():
    reports = []  # Reemplaza con lógica real
    return render_template('monitor/reports.html', reports=reports)

@monitor_bp.route('/settings')
def settings():
    return render_template('monitor/settings.html')

@monitor_bp.route('/about')
def about():
    return render_template('monitor/about.html')

@monitor_bp.route('/help')
def help():
    return render_template('monitor/help.html')

@monitor_bp.route('/contact')
def contact():
    return render_template('monitor/contact.html')

@monitor_bp.route('/faq')
def faq():
    return render_template('monitor/faq.html')

@monitor_bp.route('/terms')
def terms():
    return render_template('monitor/terms.html')

@monitor_bp.route('/privacy')
def privacy():
    return render_template('monitor/privacy.html')

@monitor_bp.route('/dashboard')
def main_dashboard():
    return render_template('monitor/main_dashboard.html')

@monitor_bp.route('/performance')
def performance():
    return render_template('monitor/performance.html')

@monitor_bp.route('/maintenance')
def maintenance():
    return render_template('monitor/maintenance.html')

@monitor_bp.route('/usage')
def usage():
    return render_template('monitor/usage.html')

@monitor_bp.route('/history')
def history():
    return render_template('monitor/history.html')

@monitor_bp.route('/analytics')
def analytics():
    return render_template('monitor/analytics.html')

@monitor_bp.route('/notifications')
def notifications():
    return render_template('monitor/notifications.html')

@monitor_bp.route('/logs')
def logs():
    return render_template('monitor/logs.html')

@monitor_bp.route('/users')
def users():
    return render_template('monitor/users.html')

@monitor_bp.route('/profile')
def profile():
    return render_template('monitor/profile.html')

@monitor_bp.route('/settings/general')
def general_settings():
    return render_template('monitor/settings_general.html')

@monitor_bp.route('/settings/security')
def security_settings():
    return render_template('monitor/settings_security.html')

@monitor_bp.route('/settings/notifications')
def notification_settings():
    return render_template('monitor/settings_notifications.html')

@monitor_bp.route('/settings/integrations')
def integration_settings():
    return render_template('monitor/settings_integrations.html')

@monitor_bp.route('/settings/billing')
def billing_settings():
    return render_template('monitor/settings_billing.html')

@monitor_bp.route('/settings/api')
def api_settings():
    return render_template('monitor/settings_api.html')

@monitor_bp.route('/settings/about')
def about_settings():
    return render_template('monitor/settings_about.html')

@monitor_bp.route('/settings/help')
def help_settings():
    return render_template('monitor/settings_help.html')

@monitor_bp.route('/settings/contact')
def contact_settings():
    return render_template('monitor/settings_contact.html')