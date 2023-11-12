from flask import Flask, render_template, request, session, redirect
import random
import datetime
import time
from fhict_cb_01.custom_telemetrix import CustomTelemetrix
# import winsound
import threading
# import serial

app = Flask(__name__)
app.secret_key = 'your_secret_key'
# ser = serial.Serial()


pizzas = ["Margherita", "Pepperoni", "Hawaiian", "BBQ Chicken", "Meat Lovers", "Four Cheese (Quattro Formaggi)", "White Pizza","Sicilian", "Neapolitan", "Pesto", "Barbecue Bacon"]
sizes = ["Small (6 slices)", "Medium (8 slices)", "Large (12 pieces)", "Jumbo (16 pieces)"]
Staff = [{'username': 'mario@gmail.com', 'password': '123456789', 'person':'Mario'},{'username': 'luigi@gmail.com', 'password': '987654321', 'person':'Luigi'}]
orders = []
basket = []
order_numbers = []
countdowns = [30]*len(orders)


pizza_details = {
    "Margherita": {
        "Size": {
            "Small (6 slices)": "$5.00",
            "Medium (8 slices)": "$7.00",
            "Large (12 pieces)": "$10.50",
            "Jumbo (16 pieces)": "$15.00",
        },
        "Ingredients": "Fresh Tomatoes, Fresh Mozzarella, Fresh Basil",
        "ImageURL":"/static/Margherita.png"
    },
    "Pepperoni": {
        "Size": {
            "Small (6 slices)": "$6.50",
            "Medium (8 slices)": "$8.50",
            "Large (12 pieces)": "$12.00",
            "Jumbo (16 pieces)": "$16.50",
        },
        "Ingredients": "Pepperoni, Cheese, Tomato Sauce",
        "ImageURL":"/static/Pepperoni.png"
    },
    "Hawaiian": {
        "Size": {
            "Small (6 slices)": "$7.50",
            "Medium (8 slices)": "$9.50",
            "Large (12 pieces)": "$13.00",
            "Jumbo (16 pieces)": "$18.00",
        },
        "Ingredients": "Ham, Pineapple, Cheese, Tomato Sauce",
        "ImageURL":"/static/Hawaii.png"
    },
    "BBQ Chicken": {
        "Size": {
            "Small (6 slices)": "$8.00",
            "Medium (8 slices)": "$10.00",
            "Large (12 pieces)": "$14.00",
            "Jumbo (16 pieces)": "$20.00",
        },
        "Ingredients": "BBQ Chicken, Onions, Cheese, BBQ Sauce",
        "ImageURL":"/static/BBQchicken.png"
    },
    "Meat Lovers": {
        "Size": {
            "Small (6 slices)": "$9.00",
            "Medium (8 slices)": "$11.00",
            "Large (12 pieces)": "$16.00",
            "Jumbo (16 pieces)": "$22.00",
        },
        "Ingredients": "Pepperoni, Sausage, Bacon, Cheese, Tomato Sauce",
        "ImageURL":"/static/Meatlovers.png"
    },
    "Four Cheese": {
        "Size": {
            "Small (6 slices)": "$7.50",
            "Medium (8 slices)": "$9.50",
            "Large (12 pieces)": "$13.00",
            "Jumbo (16 pieces)": "$18.00",
        },
        "Ingredients": "Mozzarella, Gorgonzola, Parmesan, Ricotta",
        "ImageURL":"/static/FourCheese.png"
    },
    "White Pizza": {
        "Size": {
            "Small (6 slices)": "$7.50",
            "Medium (8 slices)": "$9.50",
            "Large (12 pieces)": "$13.00",
            "Jumbo (16 pieces)": "$18.00",
        },
        "Ingredients": "Olive Oil, Garlic, Ricotta, Mozzarella, Spinach",
        "ImageURL":"/static/Spinach.png"
    },
    "Sicilian": {
        "Size": {
            "Small (6 slices)": "$8.50",
            "Medium (8 slices)": "$10.50",
            "Large (12 pieces)": "$15.00",
            "Jumbo (16 pieces)": "$21.00",
        },
        "Ingredients": "Thick Crust, Tomato Sauce, Mozzarella, Parmesan",
        "ImageURL":"/static/Sicilian.png"
    },
    "Neapolitan": {
        "Size": {
            "Small (6 slices)": "$7.00",
            "Medium (8 slices)": "$9.00",
            "Large (12 pieces)": "$12.50",
            "Jumbo (16 pieces)": "$17.50",
        },
        "Ingredients": "Thin Crust, Tomato Sauce, Mozzarella, Basil",
        "ImageURL":"/static/Neapolitan.png"
    },
    "Pesto": {
        "Size": {
            "Small (6 slices)": "$8.00",
            "Medium (8 slices)": "$10.00",
            "Large (12 pieces)": "$14.00",
            "Jumbo (16 pieces)": "$20.00",
        },
        "Ingredients": "Pesto Sauce, Mozzarella, Tomatoes, Garlic",
        "ImageURL":"/static/Pesto.png"
    },
    "Barbecue Bacon": {
        "Size": {
            "Small (6 slices)": "$8.50",
            "Medium (8 slices)": "$10.50",
            "Large (12 pieces)": "$15.00",
            "Jumbo (16 pieces)": "$21.00",
        },
        "Ingredients": "Barbecue Sauce, Bacon, Onion, Mozzarella",
        "ImageURL":"/static/BBQbacon.png"
    },
}

@app.route('/')
def index():
    basket.clear()
    return render_template('index.html')

@app.route('/TakeAway.html',methods = ['GET', 'POST'])
def TakeAway():
    Total = sum(pizza['Price'] for pizza in basket)
    error = None
    action10 = request.form.get('action')
    if action10 == 'submit':
        if not basket:
            error = "Your basket is empty"
            return render_template('TakeAway.html', error = error, Total = Total, pizza_details = pizza_details, pizzas = pizzas, sizes = sizes, basket = basket)
        else:
            return render_template('/AwayVsHouse.html', basket = basket, Total = Total)
    return render_template('TakeAway.html', Total = Total, pizza_details = pizza_details, pizzas = pizzas, sizes = sizes, basket = basket)

@app.route('/remove_from_basket/<int:index>', methods=['GET','POST'])
def remove_from_basket(index):
    action11 = request.form.get('action')
    if action11 == "remove":
        basket.pop(index)
 
    return redirect ('/TakeAway.html')
 
@app.route('/LogIn.html')
def LogIn():
    return render_template('LogIn.html')

@app.route('/AwayVsHouse.html',methods = ['GET', 'POST'])
def Location():
    error = None
    Total = 0
    Total = sum(pizza['Price'] for pizza in basket)
    print(basket)
    print(orders)
 
    if basket:
        if request.method == "POST":
            action4 = request.form.get('ToMenu')
            location1 = request.form.get('action')
            location2 = request.form.get('away')
            if location1 == 'Confirm':
                TableNumber = request.form.get('TableNumber')
                print(TableNumber)
                tnum = int(TableNumber)
                for pizza in basket:
                    order = {
                        'TableNumber': tnum,
                        'Pizza': pizza['Pizza'],
                        'Size': pizza['Size'],
                        'Amount': pizza['Amount'],
                        'Price': pizza['Price'],
                    }
                    if 'Comments' in pizza:
                        order['Comments'] = pizza['Comments']

                    Total = sum(pizza['Price'] for pizza in basket)
                    order['TotalPrice'] = (f'{Total}')
                    order['Timer'] = 30
                    order['Status'] = "In progress"
                    orders.append(order)

                print(orders)
                return render_template('OrderWaitRoom.html', tnum = tnum, basket = basket, Total = Total)

            elif location2 == 'TakeAway':
                tnum = random.randint(20,1000)

                for pizza in basket:
                    order = {
                        'TableNumber': tnum,
                        'Pizza': pizza['Pizza'],
                        'Size': pizza['Size'],
                        'Amount': pizza['Amount'],
                        'Price': pizza['Price'],
                    }
                    if 'Comments' in pizza:
                        order['Comments'] = pizza['Comments']

                    Total = sum(pizza['Price'] for pizza in basket)
                    order['TotalPrice'] = (f'{Total}')
                    order['Timer'] = 30
                    order['Status'] = "In progress"
                    orders.append(order)
                    print(orders)
                return render_template('OrderWaitRoom.html', tnum = tnum, basket = basket, Total = Total)

            elif action4 == 'BackToMenu':

                Total = sum(pizza['Price'] for pizza in orders)
                order['TotalPrice'] = Total

                return render_template('TakeAway.html', orders = orders, basket = basket, Total = Total)
        print(orders)
        return render_template('/AwayVsHouse.html', basket = basket, Total = Total, error = error)
    else:
        return redirect('/TakeAway.html')
    
@app.route('/remove_from_basket2/<int:index>', methods=['GET','POST'])
def remove_from_basket2(index):
    action11 = request.form.get('action')
    if action11 == "remove":
        basket.pop(index)
    return redirect ('/AwayVsHouse.html')

@app.route('/OrderWaitRoom.html')
def WaitRoom():
    return render_template('OrderWaitRoom.html',basket = basket)


@app.route('/Margherita.html/<pizza_name>', methods = ['GET', 'POST'])
def Margherita(pizza_name):
    global basket
    Total = 0
    error = None
    pizza_info = pizza_details.get(pizza_name)

    if request.method == 'POST':
        action = request.form.get('action')
        action2 = request.form.get('ToMenu')

        if action == 'add':
            size = request.form.get('SelectedSize')
            if size:
                amount = request.form['UpdatedQuantity']
                if amount:
                    try:
                        amount = int(amount)
                    except ValueError:
                        error_message = "Please select a valid amount."
                        return render_template('Margherita.html', pizza_details=pizza_details, basket=basket, error=error_message,pizza_name=pizza_name)
                else:
                    amount = 1

                PricePerOne = pizza_details.get(pizza_name, {}).get("Size", {}).get(size, None)
                PricePerOne_float = float(PricePerOne.replace("$",""))
                price = PricePerOne_float * amount

                comments = request.form.get('AdditionalComments', '')
                if comments:
                    selected_pizza = {
                        'Pizza': pizza_name,
                        'Size': size,
                        'Amount': amount,
                        'Comments': comments,
                        'Price': price,
                    }
                    basket.append(selected_pizza)
                    print(basket)

                else:
                    selected_pizza = {
                        'Pizza': pizza_name,
                        'Size': size,
                        'Amount': amount,
                        'Price': price,
                    }
                    basket.append(selected_pizza)
                    print(basket)

            else:
                error = "Please select a size"
            
        elif action2 == 'BackToMenu':
            Total = sum(pizza['Price'] for pizza in basket)
            return render_template('TakeAway.html', basket=basket, Total=Total)
        
    Total = sum(pizza['Price'] for pizza in basket)
    return render_template('Margherita.html',pizza_info = pizza_info, pizza_details=pizza_details, basket=basket, error=error,pizza_name=pizza_name, Total=Total)

@app.route('/LogIn.html', methods = ['GET','POST'])
def ToStaffPage():
    error = None
    if request.method == 'POST':
        Action5 = request.form.get('action')
        if Action5 == 'add':
            Username = request.form['username']
            Password = request.form['password']
            authenticated = False

            for i in Staff:
                for i in Staff:
                    if Username == i.get('username') and Password == i.get('password'):
                        authenticated = True
                        Person = i.get('person')
                        session['authenticated'] = True
                        session['username'] = Username
                        session['person'] = i['person']
                        break

            if authenticated:
                if Username == 'mario@gmail.com':
                    return redirect('/StaffPageMario.html')
                elif Username == 'luigi@gmail.com':
                    return redirect('/StaffPageLuigi.html')
            elif not authenticated: 
                error = "Incorrect data"
                return render_template('LogIn.html', error=error)

@app.route('/Order_competed/<int:index>', methods=['GET','POST'])
def Order_competed(index):
    current_datetime = datetime.datetime.now()
    time1 = current_datetime.time()
    ftime = time1.strftime("%H:%M:%S")
    if request.method == "POST":
        if 'authenticated' in session and session.get('username') == 'mario@gmail.com':
            action7 = request.form.get('action')
            if action7 == "completed":
                orders[index]['Status'] = 'Completed'


    return render_template ('/StaffPageMario.html', orders = orders, ftime = ftime)


@app.route('/StaffPageMario.html', methods = ['GET','POST'])
def StaffPageMario():
    if 'authenticated' in session and session['authenticated']:
        current_datetime = datetime.datetime.now()
        time1 = current_datetime.time()
        ftime = time1.strftime("%H:%M:%S")
        Total = sum(pizza['Price'] for pizza in orders)
        return render_template('StaffPageMario.html', ftime = ftime, pizza_details = pizza_details, basket = basket, orders = orders, Total = Total)
    else:
        return redirect('/LogIn.html')

# arduino_port = 'COM3'
# baud_rate = 9600

# ser = serial.Serial(arduino_port, baud_rate)

# def send_signal_to_arduino():
#     ser.write(b'Signal\n')


def update_timer(index):
    while orders[index]['Timer'] > 0:
        orders[index]['Timer'] = orders[index]['Timer'] - 1
        time.sleep(1)
        print(orders[index]['Timer'])
        if orders[index]['Timer'] == 0:
            orders[index]['Status'] = 'Ready'
            # board.digital_write(LED1, 0)  # red off
            # board.digital_write(LED2, 1)  # green on
            # board.digital_write(LED3, 0)  # yellow off
            # board.displayShow(orders[index]['TableNumber'])
            # winsound.PlaySound('pizzeria/Sunshine.wav', winsound.SND_FILENAME)

@app.route('/change_status/<int:index>', methods=['GET','POST'])
def change_status(index):
    current_datetime = datetime.datetime.now()
    time1 = current_datetime.time()
    ftime = time1.strftime("%H:%M:%S")
    if request.method == "POST":
        if 'authenticated' in session and session.get('username') == 'luigi@gmail.com':
            action6 = request.form.get('action')
            if action6 == "add":
                if 0 <= index < len(orders):
                    orders[index]['Status'] = 'In Oven'

                    timer_thread = threading.Thread(target=update_timer, args=(index,))
                    timer_thread.start()
                    # board.digital_write(LED1, 0)  # red off
                    # board.digital_write(LED2, 0)  # green off
                    # board.digital_write(LED3, 1)  # yellow on

    return render_template ('/StaffPageLuigi.html', orders = orders, ftime = ftime)


@app.route('/StaffPageLuigi.html', methods=['GET','POST'])
def StaffPageLuigi():
    if 'authenticated' in session and session['authenticated']:
        current_datetime = datetime.datetime.now()
        time1 = current_datetime.time()
        ftime = time1.strftime("%H:%M:%S")
        Total = sum(pizza['Price'] for pizza in orders)
        return render_template('StaffPageLuigi.html', countdowns = countdowns, ftime = ftime, pizza_details = pizza_details, basket = basket, orders = orders, Total = Total)
    else:
        return redirect('/LogIn.html')
    
if __name__ == '__main__':
    app.run()
    

# # Arduino code - in order to run it, the board should be connected to a Smart Rich Shield

# LED1 = 4 #red
# LED2 = 5 #green
# LED3 = 7 #yellow
# button1_pressed = False

# def ButtonChanged1(data):
#     global button1_pressed
#     if data[2] == 0:
#         button1_pressed = True

# def setup():
#     global board
#     board = CustomTelemetrix()
#     board.displayOn()
#     board.set_pin_mode_digital_output(LED1)
#     board.set_pin_mode_digital_output(LED2)
#     board.set_pin_mode_digital_output(LED3)
#     time.sleep(0.1)

# setup()
# while True:

     # if __name__ == '__main__':
        #     app.run()