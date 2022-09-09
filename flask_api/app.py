from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime

# Init app

app = Flask(__name__)

#Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db = SQLAlchemy(app)

#Init ma
ma = Marshmallow(app)

@app.before_first_request
def create_table():
    db.create_all()



class Customer(db.Model):
    id = db.Column(db.String(5), primary_key=True)
    company_name = db.Column(db.String(40), nullable=False)
    contact_name = db.Column(db.String(30), nullable=False)
    contact_title = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(15), nullable=False)
    region = db.Column(db.String(15), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(15), nullable=False)
    phone = db.Column(db.String(24), nullable=False)
    fax = db.Column(db.String(24), nullable=False)

    def __init__(self, customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax):
        self.id = customer_id
        self.company_name = company_name
        self.contact_name = contact_name
        self.contact_title = contact_title
        self.address = address
        self.city = city
        self.region = region
        self.postal_code = postal_code
        self.country = country
        self.phone = phone
        self.fax = fax
        
    def output(self):
        return {
            "customer_id" : self.id,
            "company_name" : self.company_name,
            "contact_name" : self.contact_name,
            "contact_title" : self.contact_title,
            "address" : self.address,
            "city" : self.city,
            "region" : self.region,
            "postal_code" : self.postal_code,
            "country" : self.country,
            "phone" : self.phone,
            "fax" : self.fax
        }



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    required_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    shipped_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    freight = db.Column(db.Numeric(4,10), nullable=False)
    ship_name = db.Column(db.String(40), nullable=False)
    ship_address = db.Column(db.String(60), nullable=False)
    ship_city = db.Column(db.String(15), nullable=False)
    ship_region = db.Column(db.String(15), nullable=False)
    ship_postal_code = db.Column(db.String(10), nullable=False)
    ship_country = db.Column(db.String(15), nullable=False)
    customer_id = db.Column(db.String, db.ForeignKey('customer.id'), nullable=False)

    def __init__(self, order_id, order_date, required_date, shipped_date, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country, customer_id):
        self.id = order_id
        self.order_date = order_date
        self.required_date = required_date
        self.shipped_date = shipped_date
        self.freight = freight
        self.ship_name = ship_name
        self.ship_address = ship_address
        self.ship_city = ship_city
        self.ship_region = ship_region
        self.ship_postal_code = ship_postal_code
        self.ship_country = ship_country
        self.customer_id = customer_id

    def output(self):
        return {
            "order_id" : self.id,
            "order_date" : self.order_date,
            "required_date" : self.required_date,
            "shipped_date" : self.shipped_date,
            "freight" : self.freight,
            "ship_name" : self.ship_name,
            "ship_address" : self.ship_address,
            "ship_city" : self.ship_city,
            "ship_region" : self.ship_region,
            "ship_postal_code" : self.ship_postal_code,
            "ship_country" : self.ship_country,
            "customer_id" : self.customer_id
        }

class OrderDetails(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    unit_price = db.Column(db.Numeric(4,10), nullable=False)
    quantity = db.Column(db.SmallInteger, nullable=False)
    discount = db.Column(db.Numeric(0,8), nullable=False)

    def __init__(self, order_id, product_id, unit_price, quantity, discount):
        self.order_id = order_id
        self.product_id = product_id
        self.unit_price = unit_price
        self.quantity = quantity
        self.discount = discount
    
    def output(self):
        return {
            "order_id" : self.order_id,
            "product_id" : self.product_id,
            "unit_price" : self.unit_price,
            "quantity" : self.quantity,
            "discount" : self.discount
        }



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(40), nullable=False)
    quantity_per_unit = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    units_in_stock = db.Column(db.SmallInteger, nullable=False)
    units_on_order = db.Column(db.SmallInteger, nullable=False)
    reorder_level = db.Column(db.SmallInteger, nullable=False)
    discontinued = db.Column(db.Boolean, nullable=False)

    def __init__(self, product_id, product_name, quantity_per_unit, unit_price, units_in_stock, units_on_order, reorder_level, discontinued):
        self.id = product_id
        self.product_name = product_name
        self.quantity_per_unit = quantity_per_unit
        self.unit_price = unit_price
        self.units_in_stock = units_in_stock
        self.units_on_order = units_on_order
        self.reorder_level = reorder_level
        self.discontinued = discontinued

    def output(self):
        return {
            "product_id" :  self.id,
            "product_name" : self.product_name,
            "quantity_per_unit" : self.quantity_per_unit,
            "unit_price" : self.unit_price,
            "units_in_stock" : self.units_in_stock,
            "units_on_order" : self.units_on_order,
            "reorder_level" : self.reorder_level,
            "discontinued" : self.discontinued
        }



# Creating customer schema

class CustomersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'company_name', 'contact_name', 'contact_title', 'address', 'city', 'region', 'postal_code', 'country', 'phone', 'fax')

customer_schema = CustomersSchema()
customers_schema = CustomersSchema(many=True)


# Creating order schema

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'order_date', 'required_date', 'shipped_date', 'freight', 'ship_name', 'ship_address', 'ship_city', 'ship_region', 'ship_postal_code', 'ship_country', 'customer_id')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


# Creating product schema

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'product_name', 'quantity_per_unit', 'unit_price', 'units_in_stock', 'units_on_order', 'reorder_level', 'discontinued')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# ------ CUSTOMER QUERIES ------- #

# Get all customers

@app.route('/customers', methods=['GET'])
def get_customer():
    all_customers = Customer.query.all()
    result = customers_schema.dump(all_customers)
    return jsonify(result)


# Get a single customer

@app.route('/customer/<id>', methods=['GET'])
def get_customer_by_id(id):
    customer = Customer.query.get(id)
    return customer_schema.jsonify(customer)


# Adding a customer

@app.route('/customer', methods=['POST'])
def put_customer():
    if request.content_type == 'application/json':
        customer_id = request.json['customer_id']
        company_name = request.json['company_name']
        contact_name = request.json['contact_name']
        contact_title = request.json['contact_title']
        address = request.json['address']
        city = request.json['city']
        region = request.json['region']
        postal_code = request.json['postal_code']
        country = request.json['country']
        phone = request.json['phone']
        fax = request.json['fax']

        new_customer = Customer(customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)

        db.session.add(new_customer)
        db.session.commit()

        # return customer_schema.jsonify(new_customer)
        return new_customer.output()
    
    return jsonify('Something went terribly wrong')


# Updating a customer

@app.route('/customer/<id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get(id)

    customer_id = request.json['customer_id']
    company_name = request.json['company_name']
    contact_name = request.json['contact_name']
    contact_title = request.json['contact_title']
    address = request.json['address']
    city = request.json['city']
    region = request.json['region']
    postal_code = request.json['postal_code']
    country = request.json['country']
    phone = request.json['phone']
    fax = request.json['fax']

    customer.id = customer_id
    customer.company_name = company_name
    customer.contact_name = contact_name
    customer.contact_title = contact_title
    customer.address = address
    customer.city = city
    customer.region = region
    customer.postal_code = postal_code
    customer.country = country
    customer.phone = phone
    customer.fax = fax

    db.session.commit()

    return customer_schema.jsonify(customer)


# Deleting a customer
@app.route('/customer/<id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    db.session.delete(customer)

    db.session.commit()

    return product_schema.jsonify(customer)


# ------ ORDER QUERIES ------- #

# Get all orders

@app.route('/orders', methods=['GET'])
def get_order():
    all_orders = Order.query.all()
    result = orders_schema.dump(all_orders)
    return jsonify(result)

# Get a single order

@app.route('/order/<id>', methods=['GET'])
def get_order_by_id(id):
    order = Order.query.get(id)
    return order_schema.jsonify(order)

# Adding an order

@app.route('/order', methods=['POST'])
def put_order():
    if request.content_type == 'application/json':
        order_id = request.json['order_id']
        order_date = request.json['order_date']
        required_date = request.json['required_date']
        shipped_date = request.json['shipped_date']
        freight = request.json['freight']
        ship_name = request.json['ship_name']
        ship_address = request.json['ship_address']
        ship_city = request.json['ship_city']
        ship_region = request.json['ship_region']
        ship_postal_code = request.json['ship_postal_code']
        ship_country = request.json['ship_country']
        customer_id = request.json['customer_id']

        new_order = Order(order_id, order_date, required_date, shipped_date, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country, customer_id)

        db.session.add(new_order)
        db.session.commit()

        # return product_schema.jsonify(new_product)
        return new_order.output()
    
    return jsonify('Something went wrong')

# Updating an order

@app.route('/order/<id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get(id)

    order_id = request.json['order_id']
    year = request.json['order_date'][:4]
    month = request.json['order_date'][5:7]
    date = request.json['order_date'][8:10]
    order_date = datetime(year, month, date)
    required_date = request.json['required_date']
    shipped_date = request.json['shipped_date']
    freight = request.json['freight']
    ship_name = request.json['ship_name']
    ship_address = request.json['ship_address']
    ship_city = request.json['ship_city']
    ship_region = request.json['ship_region']
    ship_postal_code = request.json['ship_postal_code']
    ship_country = request.json['ship_country']
    customer_id = request.json['customer_id']

    order.id = order_id
    order.order_date = order_date
    order.required_date = required_date
    order.shipped_date = shipped_date
    order.freight = freight
    order.ship_name = ship_name
    order.ship_address = ship_address
    order.ship_city = ship_city
    order.ship_region = ship_region
    order.ship_postal_code = ship_postal_code
    order.ship_country = ship_country
    order.customer_id = customer_id

    db.session.commit()

    return order_schema.jsonify(order)

# Deleting an order
@app.route('/order/<id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    db.session.delete(order)

    db.session.commit()

    return product_schema.jsonify(order)


# ----- PRODUCT QUERIES ----- #

# Get all products

@app.route('/products', methods=['GET'])
def get_product():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Get a single product

@app.route('/product/<id>', methods=['GET'])
def get_product_by_id(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Adding a product

@app.route('/product', methods=['POST'])
def put_product():
    if request.content_type == 'application/json':
        product_id = request.json['product_id']
        product_name = request.json['product_name']
        quantity_per_unit = request.json['quantity_per_unit']
        unit_price = request.json['unit_price']
        units_in_stock = request.json['units_in_stock']
        units_on_order = request.json['units_on_order']
        reorder_level = request.json['reorder_level']
        discontinued = request.json['discontinued']

        new_product = Product(product_id, product_name, quantity_per_unit, unit_price, units_in_stock, units_on_order, reorder_level, discontinued)

        db.session.add(new_product)
        db.session.commit()

        # return product_schema.jsonify(new_product)
        return new_product.output()
    
    return jsonify('Something went terribly wrong')

# Updating a product

@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    product_id = request.json['product_id']
    product_name = request.json['product_name']
    quantity_per_unit = request.json['quantity_per_unit']
    unit_price = request.json['unit_price']
    units_in_stock = request.json['units_in_stock']
    units_on_order = request.json['units_on_order']
    reorder_level = request.json['reorder_level']
    discontinued = request.json['discontinued']

    product.id = product_id
    product.product_name = product_name
    product.quantity_per_unit = quantity_per_unit
    product.unit_price = unit_price
    product.units_in_stock = units_in_stock
    product.units_on_order = units_on_order
    product.reorder_level = reorder_level
    product.discontinued = discontinued

    db.session.commit()

    return product_schema.jsonify(product)

# Deleting a product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)

    db.session.commit()

    return product_schema.jsonify(product)


# ----- ORDER HISTORY ----- #

@app.route('/orderhistory/<id>', methods=['GET'])
def get_customer_order_history(id):
    customer = Customer.query.get(id)
    result = orders_schema.dump(customer.orders)
    return jsonify(result.data)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)