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

    service_id = request.form.get('service')
    duration = int(request.form.get('duration'))
    extra = int(request.form.get('extra', 0))
    profit = int(request.form.get('profit'))
    competition = int(request.form.get('competition', 0))
    employee = request.form.get('employee', 0)
    new_client = request.form.get('new_client', 0)

    service = services.get(service_id, {'name': 'default_service', 'price': 0})
    price = service['price'] * duration

    if duration >= 4 and duration <= 6:
        price *= 0.95
    elif duration >= 7 and duration <= 12:
        price *= 0.9
    elif duration >= 13:
        price *= 0.85

    if competition == 'high':
        price += 300
    elif competition == 'medium':
        price += 200
    elif competition == 'low':
        price += 100

    if employee:
        price -= 50

    if new_client:
        price *= 0.9

    if extra > 0:
        price *= 1.2

    total_profit = profit * 0.01 * 0.3 * duration
    discount = 0
    if employee:
        discount += 50
    if new_client:
        discount += 0.1 * price

    final_price = price - discount

    # вычисляем сумму доходов и сумму услуги
    total_service_price = price + competition + extra

    jsonify({
        'service': service['name'],
        'duration': duration,
        'competition': competition,
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
    return render_template('result.html', price=final_price, total_service_price=total_service_price)


if __name__ == '__main__':
    app.run(debug=True)
