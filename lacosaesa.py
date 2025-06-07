from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from webpush_handler import trigger_push_notifications_for_subscriptions  # lo veremos luego

app = Flask(__name__, instance_relative_config=True)

# Configurando desde archivo externo
app.config.from_pyfile('application.cfg.py')

# Base de datos SQLite en memoria 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)

# Modelo para almacenar las suscripciones push
class PushSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscription_json = db.Column(db.Text, nullable=False)

# Creación de tablas
with app.app_context():
    db.create_all()

# Página principal que muestra el index.html con notificaciones
@app.route("/")
def inicio():
    return render_template('index.html', vapid_public_key=app.config['VAPID_PUBLIC_KEY'])

# Página de administración
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Guardar suscripción push
@app.route('/api/push-subscriptions', methods=['POST'])
def subscribe():
    json_data = request.get_json()
    sub = PushSubscription.query.filter_by(subscription_json=json_data['subscription_json']).first()
    if not sub:
        sub = PushSubscription(subscription_json=json_data['subscription_json'])
        db.session.add(sub)
        db.session.commit()
    return jsonify({'status': 'success'})

# Enviar notificaciones a las suscripciones guardadas
@app.route('/api/send', methods=['POST'])
def send():
    data = request.get_json()
    subs = PushSubscription.query.all()
    results = trigger_push_notifications_for_subscriptions(subs, data['title'], data['body'])
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
