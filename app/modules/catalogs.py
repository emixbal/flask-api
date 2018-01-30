import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from app import db, app
from app.models.catalogs import Product
 
catalog = Blueprint('catalog', __name__)

@catalog.route('/products2_page')
def home():
    return "Welcome to the Catalog Home."

@catalog.route('/products2', methods=['GET'])
def get_product(id=None, page=1):
    products = Product.query.paginate(page, 10).items
    res = {}
    for product in products:
        res[product.id] = {
            'name': product.name,
            'price': str(product.price),
        }
    return jsonify(res)

@catalog.route('/products2/<int:id>', methods=['GET'])
def get_product_detail(id, page=1):
    product = Product.query.filter_by(id=id).first()
    if not product:
        abort(404)
    res = {
        'name': product.name,
        'price': str(product.price),
    }
    return jsonify(res)

@catalog.route('/products2', methods=['POST'])
def product_new():
    name = request.form.get('name')
    price = request.form.get('price')
    product = Product(name, price)
    db.session.add(product)
    db.session.commit()
    return jsonify({product.id: {
        'name': product.name,
        'price': str(product.price),
    }})    

@catalog.route('/products2/<int:id>', methods=['DELETE'])
def product_delete(id):
    Product.query.filter_by(id=id).delete()
    db.session.commit()

    res = {'status' : 'succeed'}
    return jsonify(res)

@catalog.route('/products2/<int:id>', methods=['PUT'])
def product_update(id):
    product = Product.query.get(id)
    product.name = request.form.get('name')
    product.price = float(request.form.get('price'))
    db.session.commit()

    res = {
        'name': product.name,
        'price': str(product.price),
    }
    return jsonify(res)

class ProductView(MethodView):
 
    def get(self, id=None, page=1):
        if not id:
            products = Product.query.paginate(page, 10).items
            res = {}
            for product in products:
                res[product.id] = {
                    'name': product.name,
                    'price': str(product.price),
                }
        else:
            product = Product.query.filter_by(id=id).first()
            if not product:
                abort(404)
            res = {
                'name': product.name,
                'price': str(product.price),
            }
        return jsonify(res)
 
    def post(self):
        name = request.form.get('name')
        price = request.form.get('price')
        product = Product(name, price)
        db.session.add(product)
        db.session.commit()
        return jsonify({product.id: {
            'name': product.name,
            'price': str(product.price),
        }})
 
    def put(self, id):
        # Update the record for the provided id
        # with the details provided.
        product = Product.query.get(id)
        product.name = request.form.get('name')
        product.price = float(request.form.get('price'))
        db.session.commit()

        res = {
            'name': product.name,
            'price': str(product.price),
        }
        return jsonify(res)
 
    def delete(self, id):
        # Delete the record for the provided id.
        Product.query.filter_by(id=id).delete()
        db.session.commit()

        res = {'status' : 'succeed'}
        return jsonify(res)
 
 
product_view =  ProductView.as_view('product_view')


app.add_url_rule(
    '/products/', view_func=product_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/products/<int:id>', view_func=product_view, methods=['GET', 'PUT', 'DELETE']
)

