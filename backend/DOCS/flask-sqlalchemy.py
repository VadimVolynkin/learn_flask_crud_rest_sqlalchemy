from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

# создаем экземпляр приложения
app = Flask(__name__)


# ================================================================================================================================
# CLI SQLAlchemy
# ================================================================================================================================

# константа определяет вид используемой СУБД (в данном случае SQLite). Другие варианты:
# postgresql://user:password@localhost/mydatabase
# mysql://user:password@localhost/mydatabase
# oracle://user:password@127.0.0.1:1521/mydatabase 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# создание экземпляра SQLAlchemy через который осуществляется работа с БД
db = SQLAlchemy(app)


# ================================================================================================================================
# DB MODEL SQLAlchemy
# ================================================================================================================================
# класс Model - базовый класс, который превращает класс Users в модель таблицы для SQLAlchemy
# класс Column - указывает SQLAlchemy воспринимать переменные как поля таблицы
# имя таблицы = имя класса малыми буквами, имена полей таблицы = имена переменных в классе
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)                # уникальный ключ
    email = db.Column(db.String(50), unique=True)               # должно быть уникальным              
    psw = db.Column(db.String(500), nullable=False)             # не должно быть пустым
    date = db.Column(db.DateTime, default=datetime.utcnow)
 
    # отображение класса в консоли
    def __repr__(self):
        return f"<users {self.id}>"



# создаем базу
@app.before_first_request
def create_table():
    db.create_all()

# ================================================================================================================================
# ТИПЫ ПОЛЕЙ SQLAlchemy
# ================================================================================================================================

Integer          # целочисленный
String(size)     # строка максимальной длиной size
Text             # текст (в формате Unicode)
DateTime         # дата и время представленные в формате объекта datetime
Float            # число с плавающей точкой (вещественное)
Boolean          # логическое значение
LargeBinary      # для больших произвольных бинарных данных (например, изображений) 

