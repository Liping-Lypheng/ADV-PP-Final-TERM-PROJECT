from app import app, db
from sqlalchemy import text
from flask import render_template, request, Flask, jsonify
from model import *
from werkzeug.utils import secure_filename

@app.get('/invoice/list')
def invoice_list():
    return get_invoice_info(invoice_id=0)


@app.get('/invoice/list/<int:invoice_id>')
def invoice_list_by_id(invoice_id):
    return get_invoice_info(invoice_id=invoice_id)


def get_invoice_info(invoice_id: int = 0):
    if invoice_id == 0:
        sql_str = text("select * from invoice")
        pre_sql = db.session.execute(sql_str).fetchall()
        if not pre_sql:
            return {'message': 'Invoice table is emply!'}
        return [dict(row._mapping) for row in pre_sql]

    if invoice_id != 0:
        sql_str = text("select * from invoice where id = :invoice_id")
        pre_sql = db.session.execute(sql_str, {"invoice_id": invoice_id}).fetchone()
        if not pre_sql:
            return {'message': 'invoice not found!'}
        return dict(pre_sql._mapping)


@app.post('/invoice/create')
def create_invoice():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data received!'}), 400

    invoice_id = data.get('invoice_no')

    if not invoice_id:
        return jsonify({'message': 'Duplicate invoice_No!'}), 400

    try:
        # Create new invoice
        invoice = Invoice(
            invoice_no=data.get('invoice_no'),
            customer_name=data.get('customer_name'),
            total_amount=0,
            created_by=data.get('created_by'),
            created_at=datetime.utcnow(),
            status='draft'
        )
        db.session.add(invoice)
        db.session.flush()  # Get invoice.id before commit

        total_amount = 0

        # Loop through items in JSON
        for item in data.get('items', []):
            product_id = item['product_id']
            qty = item['qty']
            unit_price = item['unit_price']
            subtotal = qty * unit_price
            total_amount += subtotal

            invoice_item = InvoiceItem(
                invoice_id=invoice.id,
                product_id=product_id,
                qty=qty,
                unit_price=unit_price,
                subtotal=subtotal
            )
            db.session.add(invoice_item)

        # Update total amount and commit
        invoice.total_amount = total_amount
        db.session.commit()

        # Return JSON response
        return{
            'message': 'Invoice created successfully!',
        }, 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Invoice number already exists",
            "details": str(e.orig)
        }), 400

@app.post('/invoice/delete')
def invoice_delete():
    form = request.get_json()
    if not form:
        return {'message': 'No form was submitted!'},400

    is_exists = get_invoice_info(form.get('invoice_id'))
    if is_exists.get('message'):
        return {'message': 'invoice not found!'},400

    invoice = Invoice.query.get(form.get('invoice_id'))
    db.session.delete(invoice)
    db.session.commit()
    return {
        'message': 'invoice has been delete!',
    },200


@app.put('/invoice/update')
def update_invoice():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data received!'}), 400

    invoice_id = data.get('invoice_id')
    if not invoice_id:
        return jsonify({'message': 'Missing invoice_id!'}), 400

    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({'message': 'Invoice not found!'}), 404

    try:
        # Update invoice fields
        invoice.customer_name = data.get('customer_name', invoice.customer_name)
        invoice.status = data.get('status', invoice.status)

        total_amount = 0

        # If items are included, replace them
        if 'items' in data:
            # Remove old items
            InvoiceItem.query.filter_by(invoice_id=invoice.id).delete()

            # Add new items
            for item in data['items']:
                product_id = item['product_id']
                qty = item['qty']
                unit_price = item['unit_price']
                subtotal = qty * unit_price
                total_amount += subtotal

                new_item = InvoiceItem(
                    invoice_id=invoice.id,
                    product_id=product_id,
                    qty=qty,
                    unit_price=unit_price,
                    subtotal=subtotal
                )
                db.session.add(new_item)

        invoice.total_amount = total_amount
        db.session.commit()

        return {
            'message': 'Invoice updated successfully!',
        }, 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
