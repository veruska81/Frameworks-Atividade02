from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testuser:toledo22@localhost:3306/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    password = db.Column(db.String(256))
    address = db.Column(db.String(256))

    def __init__(self, name, email, password, address):
        self.name = name
        self.email = email
        self.password = password
        self.address = address

class Category(db.Model):
    __tablename__ = "categoria"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.String(256))

    def __init__(self, name, description):
        self.name = name
        self.description = description

class Ad(db.Model):
    __tablename__ = "anuncio"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.String(256))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, description, quantity, price, category_id, user_id):
        self.title = title
        self.description = description
        self.quantity = quantity
        self.price = price
        self.category_id = category_id
        self.user_id = user_id

@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html')

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register/user", methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        new_user = User(
            name=request.form['nome'],
            email=request.form['email'],
            password=request.form['senha'],
            address=request.form['endereço']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('list_users'))
    return render_template('register_user.html')

@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)

@app.route("/user/<int:id>")
def detail_user(id):
    user = User.query.get(id)
    return render_template('detail_user.html', user=user)

@app.route("/user/edit/<int:id>", methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get(id)
    if request.method == 'POST':
        user.name = request.form['nome']
        user.email = request.form['email']
        user.password = request.form['senha']
        user.address = request.form['endereço']
        db.session.commit()
        return redirect(url_for('list_users'))
    return render_template('edit_user.html', user=user)

@app.route("/user/delete/<int:id>")
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))

@app.route("/register/ad", methods=['GET', 'POST'])
def register_ad():
    categories = Category.query.all()
    if request.method == 'POST':
        new_ad = Ad(
            title=request.form['title'],
            description=request.form['description'],
            quantity=int(request.form['quantity']),
            price=float(request.form['price']),
            category_id=int(request.form['category']),
            user_id=1
        )
        db.session.add(new_ad)
        db.session.commit()
        return redirect(url_for('list_ads'))
    return render_template('register_ad.html', categories=categories)

@app.route("/ads")
def list_ads():
    ads = Ad.query.all()
    return render_template('list_ads.html', ads=ads)

@app.route("/register/category", methods=['GET', 'POST'])
def register_category():
    if request.method == 'POST':
        new_category = Category(
            name=request.form['name'],
            description=request.form['description']
        )
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('list_categories'))
    return render_template('register_category.html')

@app.route("/categories")
def list_categories():
    categories = Category.query.all()
    return render_template('list_categories.html', categories=categories)

@app.route("/reports/sales")
def sales_report():
    return render_template('sales_report.html')

@app.route("/reports/purchases")
def purchases_report():
    return render_template('purchases_report.html')

with app.app_context():
    db.create_all()

if __name__ == "Verenxovais":
    app.run(debug=True)