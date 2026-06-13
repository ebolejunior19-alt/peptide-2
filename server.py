import os
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')

ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'support@timerpeptides.com')
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
FROM_EMAIL = os.environ.get('FROM_EMAIL', SMTP_USER or ADMIN_EMAIL)
USE_SSL = os.environ.get('SMTP_USE_SSL', 'false').lower() in ('1', 'true', 'yes')


def send_email(subject: str, body: str, recipient: str) -> None:
    if not SMTP_USER or not SMTP_PASS:
        raise RuntimeError('SMTP_USER and SMTP_PASS must be set in environment variables.')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = recipient
    msg.set_content(body)

    if USE_SSL:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
    else:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)


@app.route('/api/contact', methods=['POST'])
def contact_form():
    data = request.get_json(silent=True) or {}
    name = str(data.get('name', '')).strip()
    email = str(data.get('email', '')).strip()
    message = str(data.get('message', '')).strip()

    if not name or not email or not message:
        return jsonify({'ok': False, 'message': 'Name, email, and message are required.'}), 400

    subject = f'Contact request from Timer Peptides site: {name}'
    body = (
        f'Admin: Timer Peptides\n'
        f'Name: {name}\n'
        f'Email: {email}\n'
        f'Message:\n{message}\n'
        f'Source: Timer Peptides contact page\n'
    )

    send_email(subject, body, ADMIN_EMAIL)
    return jsonify({'ok': True, 'message': 'Contact message delivered to admin.'})


@app.route('/api/order', methods=['POST'])
def order_notification():
    data = request.get_json(silent=True) or {}
    product = str(data.get('product', '')).strip()
    price = data.get('price')
    dosage = str(data.get('dosage', '')).strip()
    quantity = data.get('quantity')
    total = data.get('total')
    customer = data.get('customer', {})

    if not product or price is None or total is None or not isinstance(customer, dict):
        return jsonify({'ok': False, 'message': 'Product, price, total, and customer details are required.'}), 400

    subject = f'New order from Timer Peptides site: {product}'
    body = (
        f'Admin: Timer Peptides\n'
        f'Product: {product}\n'
        f'Price: ${price:.2f}\n'
        f'Dosage: {dosage}\n'
        f'Quantity: {quantity}\n'
        f'Total: ${total:.2f}\n\n'
        f'Customer: {customer.get("firstName", "")} {customer.get("lastName", "")}\n'
        f'Email: {customer.get("email", "")}\n'
        f'Phone: {customer.get("phone", "")}\n'
        f'Address: {customer.get("address", "")}, {customer.get("city", "")}, {customer.get("state", "")} {customer.get("zip", "")}, {customer.get("country", "")}\n'
        f'Order timestamp: {data.get("timestamp", "")}\n'
    )

    send_email(subject, body, ADMIN_EMAIL)
    return jsonify({'ok': True, 'message': 'Order notification delivered to admin.'})


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_file(path):
    if os.path.exists(path) and not os.path.isdir(path):
        return send_from_directory('.', path)
    return send_from_directory('.', 'index.html')


if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '5000')), debug=debug)
