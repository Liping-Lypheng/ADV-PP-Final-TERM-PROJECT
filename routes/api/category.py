from flask_jwt_extended import jwt_required

from app import app , db
from sqlalchemy import text
from flask import request
from model import Category
from werkzeug.security import generate_password_hash

@app.get('/category/list')
@jwt_required()
def category_list():
    return get_category_info(category_id=0)
@app.get('/category/list/<int:category_id>')
def category_list_by_id(category_id):
    return get_category_info(category_id=category_id)
@app.post('/category/create')
def category_create():
    form = request.get_json()
    if not form:
        return 'no data'


    category = Category(
        id=form.get('category_id'),
        name=form.get('name'),
    )
    db.session.add(category)
    db.session.commit()
    return {
        'message': ' category have been created',
        'category': get_category_info(category.id)
    }, 200
@app.post('/category/delete')
def category_delete():
    form = request.get_json()
    if not form:
        return {
            'message': 'no data',
        }
    is_exist = get_category_info(form.get('category_id'))
    if is_exist.get('message'):
        return {
            'message': 'category not found!',
        } , 400
    sql_str = text("""delete from category where id = :category_id""")
    result = db.session.execute(sql_str,
                                {
                                    "category_id": form.get('category_id'),
                                })
    db.session.commit()
    return {
        'message': ' category have been deleted',
    }, 200
@app.put('/category/update')
def category_update():
    form = request.get_json()
    if not form:
        return {
            'message': 'no data',
        } , 400
    is_exist = get_category_info(form.get('category_id'))
    if is_exist.get('message'):
        return {
            'message': 'Category not found!',
        } , 400

    category = Category.query.get(form.get('category_id'))
    category.branch_id = form.get('branch_id')
    category.name = form.get('name')

    db.session.commit()

    return {
        'message': ' category have been updated'
    }, 200

def get_category_info(category_id: int = 0):
    if category_id == 0:
        sql_str = text("select * from category")
        result = db.session.execute(sql_str).fetchall()
        if not result:
            return {'message': 'category table is empty!'}
        return [dict(row._mapping) for row in result]

    if category_id != 0:
        sql_str = text("select * from category where id = :category_id")
        result = db.session.execute(sql_str , {"category_id": category_id}).fetchone()
        if not result:
            return {'message' : 'category is not found'}
    return dict(result._mapping)
