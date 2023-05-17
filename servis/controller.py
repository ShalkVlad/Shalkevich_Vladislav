from flask import Flask, render_template, request

app = Flask(__name__)

services = {
    "1": {"name": "Оптимизация сайта", "price": 1100},
    "2": {"name": "SMM", "price": 950},
    "3": {"name": "Управление репутацией", "price": 950},
    "4": {"name": "Таргетированная реклама", "price": 1100},
    "5": {"name": "Медийная реклама", "price": 1000},
    "6": {"name": "Контекстная реклама", "price": 1200}
}


@app.route('/')
def index():
    return render_template('index.html', services=services)


@app.route('/calculate', methods=['POST'])
def calculate():
    service_id = request.form['services']
    duration = int(request.form['duration'])
    competition = int(request.form['competition'])
    advertising_report = int(request.form['advertising-report'])
    employee_answer = request.form['employee_answer']
    client_status = request.form['client_status']

    service_price = services[service_id]['price']

    if duration <= 3:
        total_service_price = service_price
    elif duration <= 6:
        total_service_price = service_price * 0.95
    elif duration <= 12:
        total_service_price = service_price * 0.9
    else:
        total_service_price = service_price * 0.85

    total_service_price += competition + advertising_report

    if employee_answer == 'yes':
        total_service_price += 50

    if client_status == 'new':
        total_service_price *= 0.9

    service_name = services[service_id]['name']
    service_price = total_service_price + 500
    result_html = """
     <div id="result-window" class="popup-overlay">
         <div class="popup-content">
             <p>Стоимость услуги «{service_name}» составит: <br> 
             от {total_service_price}-{service_price} бел.рублей*
             </p>
             <br><br>
             <p class="text">*Для получения подробной информации, свяжитесь с нашим менеджером</p>
             <form>
                 <button class="popup-close" onclick="closePopup(event)">Закрыть</button>
             </form>
         </div>
     </div>
     """.format(service_name=service_name, total_service_price=total_service_price, service_price=service_price)

    return render_template('index.html', result_html=result_html)


if __name__ == '__main__':
    app.run(debug=True)
