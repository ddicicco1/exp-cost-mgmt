from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/ecm_prototype'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
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

# Invoice Upload Route
@app.route('/upload-invoice', methods=['POST'])
def upload_invoice():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Mock OCR Processing
    extracted_data = mock_ocr_service(filepath)

    # Create invoice record in the database
    new_invoice = Invoice(
        vendor=extracted_data['vendor'],
        date=extracted_data['date'],
        amount=extracted_data['amount'],
        location_id=extracted_data['location_id'],
        description=extracted_data.get('description', '')
    )
    db.session.add(new_invoice)
    db.session.commit()

    return jsonify({'message': 'Invoice uploaded and processed successfully', 'invoice_id': new_invoice.id})

# Fetch All Invoices
@app.route('/invoices', methods=['GET'])
def get_invoices():
    invoices = Invoice.query.all()
    invoice_list = []
    for invoice in invoices:
        invoice_list.append({
            'id': invoice.id,
            'vendor': invoice.vendor,
            'date': str(invoice.date),
            'amount': invoice.amount,
            'location': invoice.location.name,
            'status': invoice.status,
            'description': invoice.description
        })
    return jsonify(invoice_list)

# Mock OCR Processing Service
def mock_ocr_service(filepath):
    # Simulates OCR extraction from a PDF. This is mock data and should be replaced with real OCR logic.
    return {
        'vendor': 'Mock Vendor',
        'date': '2025-05-01',
        'amount': 123.45,
        'location_id': 1,
        'description': 'Mock OCR extracted description'
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')