from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    services = {
        '1': {'name': 'Оптимизация сайта', 'price': 1100},
        '2': {'name': 'SMM', 'price': 950},
        '3': {'name': 'Управление репутацией', 'price': 950},
        '4': {'name': 'Таргетированная реклама', 'price': 1100},
        '5': {'name': 'Медийная реклама', 'price': 1000},
        '6': {'name': 'Контекстная реклама', 'price': 1200},
    }

    service_id = request.form.get('services')
    duration = int(request.form.get('duration'))
    extra = int(request.form.get('extra', 0))
    profit = int(request.form.get('profit'))
    competition = int(request.form.get('competition', 0))
    employee = request.form.get('employee_answer') == 'yes'
    new_client = request.form.get('client_status') == 'new'

    service = services.get(service_id, {'name': 'default_service', 'price': 0})
    price = service['price'] * duration

    if 1 <= duration <= 3:
        discount = 0
    elif 4 <= duration <= 6:
        price *= 0.95
        discount = 0.05 * price
    elif 7 <= duration <= 12:
        price *= 0.9
        discount = 0.1 * price
    else:
        price *= 0.85
        discount = 0.15 * price

    if competition == 1:
        price += 300
        competition_str = 'high'
    elif competition == 2:
        price += 200
        competition_str = 'medium'
    elif competition == 3:
        price += 100
        competition_str = 'low'
    else:
        competition_str = 'unknown'

    if employee:
        price -= 50

    if new_client:
        price *= 0.9

    if extra > 0:
        price += 0.2 * price

    total_profit = profit * 0.01 * 0.3 * duration
    final_price = price - discount
    total_service_price = price + (300 if competition_str
    == 'high' else 200 if competition_str == 'medium' else 100 if competition_str == 'low' else 0) + extra

    jsonify({
        'service': service['name'],
        'duration': duration,
        'competition': competition_str,
        'employee': employee,
        'new_client': new_client,
        'price': price,
        'extra': extra,
        'profit': profit,
        'total_profit': total_profit,
        'discount': discount,
        'final_price': final_price,
        'total_income': final_price + extra,
        'total_service_price': total_service_price
    })

    # передача переменной total_service_price в шаблон result.html
    service_name = service['name']
    service_price = total_service_price + 200

    return render_template('index.html', service_name=service_name, service_price=service_price,
                           total_service_price=total_service_price)


if __name__ == '__main__':
    app.run(debug=True)
