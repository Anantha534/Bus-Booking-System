from flask import Flask, render_template, redirect, url_for, request, make_response

app = Flask(__name__)

bookings = []
temp_seats = ""   # holds seats between pages

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/seat')
def seat():
    return render_template('seat.html')

# STEP 1: receive seats → show payment page
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    global temp_seats

    if request.method == 'POST' and 'method' not in request.form:
        # coming from seat page
        temp_seats = request.form.get('seats')
        return render_template('payment.html')

    elif request.method == 'POST' and 'method' in request.form:
        # coming from payment page
        method = request.form.get('method')

        booking = {
            "id": len(bookings),
            "from": "Selected City",
            "to": "Selected City",
            "date": "2026-01-01",
            "seats": temp_seats,
            "method": method,
            "price": len(temp_seats.split(",")) * 500
        }

        bookings.append(booking)
        temp_seats = ""

        return redirect(url_for('confirmation'))

    return render_template('payment.html')


@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')


@app.route('/tickets')
def tickets():
    return render_template('my_tickets.html', bookings=bookings)


# ✅ FIX 2 — Proper 40% penalty
@app.route('/cancel/<int:id>')
def cancel(id):
    for b in bookings:
        if b["id"] == id:
            original = b["price"]
            penalty = int(original * 0.4)
            refund = original - penalty

            b["price"] = refund
            b["status"] = f"Cancelled (40% penalty ₹{penalty})"
    return redirect(url_for('tickets'))


@app.route('/delete/<int:id>')
def delete(id):
    global bookings
    bookings = [b for b in bookings if b["id"] != id]
    return redirect(url_for('tickets'))


@app.route('/receipt/<int:id>')
def receipt(id):
    for b in bookings:
        if b["id"] == id:
            content = f"""
Bus Booking System Receipt

Seats: {b['seats']}
Payment Method: {b['method']}
Price: ₹{b['price']}
Status: {b.get('status','Confirmed')}

Thank you!
"""
            response = make_response(content)
            response.headers['Content-Disposition'] = 'attachment; filename=receipt.txt'
            return response

    return "Not Found"


if __name__ == '__main__':
    app.run(debug=True)