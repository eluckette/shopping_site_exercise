"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, request
import jinja2
from decimal import *

import model


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melons = model.Melon.get_all()
    return render_template("all_melons.html",
                           melon_list=melons)


@app.route("/melon/<int:id>")
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = model.Melon.get_by_id(id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""
    order = session.values()

    total = 0
    for item in order:
        total = total + item[3]

    return render_template("cart.html", order=order, total=total)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """
    order = model.Melon.get_by_id(id)

    if order:
        if str(id) in session:
            session[str(order.id)] = [order.common_name, order.price, session[str(order.id)][2] + 1, session[str(order.id)][3] + order.price]
            print "TRYING TO FIGURE THIS OUT: ", session[str(order.id)][2]
        else:
            session[str(order.id)] = [order.common_name, order.price, 1, order.price]

        # order = {key:session[key]for key in session if key != 'logged_in_customer_email'}
        order = session.values()
        
        total = 0

        for item in order:
            total = total + item[3]
    
    return render_template('cart.html', order=order, total=total)


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    error = None
    if request.method == 'POST':
        
        customer = model.Customer.get_by_email(request.form['email'])

        if customer and (customer.password == request.form['password']):
            # session['logged_in_customer_email'] = request.form['email']
            print 'SESSION: ', session
            return render_template('homepage.html')
        else:
            error = 'Invalid email/password'
            return render_template('login.html', error=error)
    


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
