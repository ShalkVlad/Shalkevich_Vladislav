from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///services.db'
db = SQLAlchemy(app)

services = {
    "1": {"name": "Оптимизация сайта", "price": 1100},
    "2": {"name": "SMM", "price": 950},
    "3": {"name": "Управление репутацией", "price": 950},
    "4": {"name": "Таргетированная реклама", "price": 1100},
    "5": {"name": "Медийная реклама", "price": 1000},
    "6": {"name": "Контекстная реклама", "price": 1200}
}


class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    service_number = db.Column(db.String(10), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    competition = db.Column(db.String(10), nullable=False)
    newsletter = db.Column(db.String(10), nullable=False)
    employee_state = db.Column(db.String(10), nullable=False)
    new_client = db.Column(db.String(10), nullable=False)
    service_name = db.Column(db.String(50), nullable=False)
    total_service_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<ServiceRequest %r>' % self.username


@app.route('/')
def index():
    return render_template('index.html', services=services)


@app.route('/calculate', methods=['POST'])
def calculate():
    username = request.form['fullname']
    service_number = request.form['services']
    duration = int(request.form['duration'])
    competition = request.form['competition']
    newsletter = request.form['advertising-report']
    employee_state = request.form['employee_answer']
    new_client = request.form['client_status']

    service_price = services[service_number]['price']

    if duration <= 3:
        total_service_price = service_price
    elif duration <= 6:
        total_service_price = service_price * 0.95
    elif duration <= 12:
        total_service_price = service_price * 0.9
    else:
        total_service_price = service_price * 0.85

    if competition == 'высокий':
        total_service_price += 100
    elif competition == 'средний':
        total_service_price += 50
    elif competition == 'низкий':
        total_service_price += 25

    if newsletter == 'еженедельно':
        total_service_price += 50
    elif newsletter == 'ежемесячно':
        total_service_price += 25

    if employee_state == 'да':
        total_service_price += 50

    if new_client == 'да':
        total_service_price *= 0.9

    service_name = services[service_number]['name']
    service_price = total_service_price + 500

    service_request = ServiceRequest(
        username=username,
        phone=request.form['phone'],
        email=request.form['email'],
        service_number=service_number,
        duration=duration,
        competition=competition,
        newsletter=newsletter,
        employee_state=employee_state,
        new_client=new_client,
        service_name=service_name,
        total_service_price=service_price
    )
    db.session.add(service_request)
    db.session.commit()

    result_html = """
     <div id="result-window" class="popup-overlay">
         <div class="popup-content">
         {username}<br> 
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
     """.format(service_name=service_name, username=username, total_service_price=total_service_price,
                service_price=service_price)

    return render_template('index.html', result_html=result_html)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
