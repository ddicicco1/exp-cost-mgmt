from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/ecm_prototype'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor = db.Column(db.String(128), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    status = db.Column(db.String(32), default="Pending")
    description = db.Column(db.String(256))

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    invoices = db.relationship('Invoice', backref='location', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    role = db.Column(db.String(64), nullable=False)

# Routes
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

# CRUD Endpoints
@app.route('/invoices', methods=['GET'])
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([{
        'id': invoice.id,
        'vendor': invoice.vendor,
        'date': str(invoice.date),
        'amount': invoice.amount,
        'location': invoice.location.name,
        'status': invoice.status,
        'description': invoice.description
    } for invoice in invoices])

@app.route('/invoices', methods=['POST'])
def create_invoice():
    data = request.json
    location = Location.query.get(data['location_id'])
    if not location:
        return jsonify({'error': 'Invalid location ID'}), 400

    new_invoice = Invoice(
        vendor=data['vendor'],
        date=data['date'],
        amount=data['amount'],
        location_id=data['location_id'],
        status=data.get('status', 'Pending'),
        description=data.get('description', '')
    )
    db.session.add(new_invoice)
    db.session.commit()
    return jsonify({'message': 'Invoice created successfully'}), 201

@app.route('/invoices/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    data = request.json
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404

    invoice.vendor = data.get('vendor', invoice.vendor)
    invoice.date = data.get('date', invoice.date)
    invoice.amount = data.get('amount', invoice.amount)
    invoice.status = data.get('status', invoice.status)
    invoice.description = data.get('description', invoice.description)
    db.session.commit()
    return jsonify({'message': 'Invoice updated successfully'})

@app.route('/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404

    db.session.delete(invoice)
    db.session.commit()
    return jsonify({'message': 'Invoice deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')