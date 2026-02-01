from app import app , db
from sqlalchemy import text
from flask import request
from model import Product
from werkzeug.utils import secure_filename


@app.get('/product/list')
def product_list():
    return get_product_info(product_id=0)
@app.get('/product/list/<int:product_id>')
def product_list_by_id(product_id):
    return get_product_info(product_id=product_id)
@app.post('/product/create')
def product_create():
    form = request.form
    file = request.files.get('image')
    image = None
    if not form:
        return 'no data'

    if file and file.filename != '':
        file = request.files['image']
        filename = f"{form.get('name')}_{secure_filename(file.filename)}"
        file.save(f'./static/assets/images/product/{filename}')
        image = filename


    product = Product(
        id=form.get('product_id'),
        name = form.get('name'),
        category_id = form.get('category_id'),
        cost = form.get('cost'),
        price = form.get('price'),
        image = image,
        stock = form.get('stock'),
        description = form.get('description'),
    )
    db.session.add(product)
    db.session.commit()
    return {
        'message': ' product have been created',
        'product': get_product_info(product.id)
    }, 200
@app.post('/product/delete')
def product_delete():
    form = request.get_json()
    if not form:
        return {
            'message': 'no data',
        }
    is_exist = get_product_info(form.get('product_id'))
    if is_exist.get('message'):
        return {
            'message': 'product not found!',
        } , 400
    sql_str = text("""delete from product where id = :product_id""")
    result = db.session.execute(sql_str,
                                {
                                    "product_id": form.get('product_id'),
                                })
    db.session.commit()
    return {
        'message': ' product have been deleted',
    }, 200
@app.put('/product/update')
def product_update():
    form = request.get_json()
    if not form:
        return {'message': 'no data'}, 400

    is_exist = get_product_info(form.get('product_id'))
    if is_exist.get('message'):
        return {'message': 'product not found!'}, 400

    product = Product.query.get(form.get('product_id'))
    product.name = form.get('name')
    product.cost = form.get('cost')
    product.price = form.get('price')
    product.stock = form.get('stock')
    product.description = form.get('description')

    db.session.commit()

    return {'message': 'product has been updated'}, 200

def get_product_info(product_id: int = 0):
    if product_id == 0:
        sql_str = text("select * from product")
        result = db.session.execute(sql_str).fetchall()
        if not result:
            return {'message': 'product table is empty!'}
        return [dict(row._mapping) for row in result]

    if product_id != 0:
        sql_str = text("select * from product where id = :product_id")
        result = db.session.execute(sql_str , {"product_id": product_id}).fetchone()
        if not result:
            return {'message' : 'product is not found'}
    return dict(result._mapping)
