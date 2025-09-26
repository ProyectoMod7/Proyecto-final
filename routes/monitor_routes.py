from flask import Blueprint, render_template, request, redirect, url_for

monitor_bp = Blueprint('monitor', __name__)

# Lista global de máquinas para pruebas
machines = [
    {"id": 1, "name": "Máquina A", "status": "Activo"},
    {"id": 2, "name": "Máquina B", "status": "Inactivo"},
]

@monitor_bp.route('/')
def dashboard():
    return render_template('monitor/dashboard.html', machines=machines)

@monitor_bp.route('/machine/<int:machine_id>/edit', methods=['GET', 'POST'])
def edit_machine(machine_id):
    machine = next((m for m in machines if m["id"] == machine_id), None)
    if not machine:
        return "Máquina no encontrada", 404
    if request.method == 'POST':
        machine["name"] = request.form['name']
        machine["status"] = request.form['status']
        return redirect(url_for('monitor.dashboard'))
    return render_template('monitor/machine_form.html', machine=machine)

@monitor_bp.route('/machine/new', methods=['GET', 'POST'])
def new_machine():
    if request.method == 'POST':
        new_id = max([m["id"] for m in machines]) + 1 if machines else 1
        name = request.form['name']
        status = request.form['status']
        machines.append({"id": new_id, "name": name, "status": status})
        return redirect(url_for('monitor.dashboard'))
    return render_template('monitor/machine_form.html', machine=None)

@monitor_bp.route('/machine/<int:machine_id>/delete', methods=['POST'])
def delete_machine(machine_id):
    global machines
    machines = [m for m in machines if m["id"] != machine_id]
    return redirect(url_for('monitor.dashboard'))

@monitor_bp.route('/sectors')
def sectors():
    sectors = [
        {"id": 1, "name": "Sector 1"},
        {"id": 2, "name": "Sector 2"},
    ]
    return render_template('monitor/sectors.html', sectors=sectors)

@monitor_bp.route('/sector/<int:sector_id>')
def sector_detail(sector_id):
    sector = {"id": sector_id, "name": f"Sector {sector_id}"}
    return render_template('monitor/sector_detail.html', sector=sector)

@monitor_bp.route('/alerts')
def alerts():
    alerts = []
    return render_template('monitor/alerts.html', alerts=alerts)

@monitor_bp.route('/reports')
def reports():
    reports = []
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