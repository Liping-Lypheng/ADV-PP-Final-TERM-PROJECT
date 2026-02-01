
from app import app , db
from sqlalchemy import text
from flask import request
from model import Branch
from werkzeug.utils import secure_filename

@app.get('/branch/list')
def branch_list():
    return get_branch_info(branch_id=0)
@app.get('/branch/list/<int:branch_id>')
def branch_list_by_id(branch_id):
    return get_branch_info(branch_id=branch_id)
@app.post('/branch/create')
def branch_create():
    form = request.form
    file = request.files.get('logo')
    logo = None
    if not form:
        return 'no data'

    if file and file.filename != '':
        file = request.files['logo']
        filename = f"{form.get('name')}_{form.get('phone')}_{secure_filename(file.filename)}"
        file.save(f'./static/assets/images/branch/{filename}')
        logo = filename


    branch = Branch(
        name=form.get('name'),
        phone=form.get('phone'),
        address=form.get('address'),
        description=form.get('description'),
        logo = logo
    )
    db.session.add(branch)
    db.session.commit()
    return {
        'message': ' branch have been created',
        'branch': get_branch_info(branch.id)
    }, 200
@app.post('/branch/delete')
def branch_delete():
    form = request.get_json()
    if not form:
        return {
            'message': 'no data',
        }
    is_exist = get_branch_info(form.get('branch_id'))
    if is_exist.get('message'):
        return {
            'message': 'branh not found!',
        } , 400
    sql_str = text("""delete from branch where id = :branch_id""")
    result = db.session.execute(sql_str,
                                {
                                    "branch_id": form.get('branch_id'),
                                })
    db.session.commit()
    return {
        'message': ' branch have been deleted',
    }, 200
@app.put('/branch/update')
def branch_update():
    form = request.form
    if not form:
        return {
            'message': 'no data',
        } , 400
    is_exist = get_branch_info(form.get('branch_id'))
    if is_exist.get('message'):
        return {
            'message': 'branh not found!',
        } , 400
    branch = Branch.query.get(form.get('branch_id'))
    branch.name = form.get('name')
    branch.phone = form.get('phone')
    branch.address = form.get('address')
    branch.description = form.get('description')
    branch.logo = form.get('logo')
    db.session.commit()
    return {
        'message': ' branch have been updated'
    }, 200

def get_branch_info(branch_id: int = 0):
    if branch_id == 0:
        sql_str = text("select * from branch")
        result = db.session.execute(sql_str).fetchall()
        if not result:
            return {'message': 'branch table is empty!'}
        return [dict(row._mapping) for row in result]

    if branch_id != 0:
        sql_str = text("select * from branch where id = :branch_id")
        result = db.session.execute(sql_str , {"branch_id": branch_id}).fetchone()
        if not result:
            return {'message' : 'Branch is not found'}
    return dict(result._mapping)
