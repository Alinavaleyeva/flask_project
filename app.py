from flask import Flask #импортируем класс
from flask import render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__) #директива, передающая файл для работы с основнм файлом, который и будет app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' #элемент словаря config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) #в конструктор передает объект, созданнй на основе flask (в котром уже подключение к баз еданных присутствует)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True) #параменты поля - число (int), ключ - поле уникальное, если True
    db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False) #название
    intro = db.Column(db.String(300), nullable=False)#строка макс длина 300, нельзя создать пустое значение
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)#для больших объемов - текст, utcnow - для дефолтного ввремени (когда статья создана)

    def __repr__(self): #когда будем выбирать объект класса, то будет выдаваться объект и id этого объекта
        return '<Article %r' % self.id

@app.route('/') #декоратор для отслеживания URL (для главной странички)
@app.route('/home') #можно добавить еще один адрес для отслеживания (чтобы не было повтора кода)
def index():
    #render_template - для рендеринга HTML-шаблонов (шаблонизотор Jinja2)
    return render_template("index.html") #index.html - шаблон


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/posts')
def posts():
    # query - метод, который помогает обратиться чрез определенную модель к БД
    #all - получит ВСЕ записи из БД
    #order_by - по какому полю будем сортировать все полученные записи
    #desc() - сортировка сначала новые, потом старые
    articles = Article.query.order_by(Article.date.desc()).all()

    #переменную articles называем articles для обращения так к ней в шаблоне posts
    return render_template("posts.html", articles=articles)

@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)

@app.route('/create-article', methods=['GET', 'POST']) #данные из формы либо прямой заход на страничку
def create_artical():
    if request.method == "POST": #если через формочку, то рассмотрим, как принять эти данные
        #создаем перемнные для записи данных из формочки
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        #теперь полученные данные для нового объекта передаем в класс Article
        article = Article(title=title, intro=intro, text=text)
        #потом сохраняем созданный объект в базу данных
        try:
            #сохранение объекта через др объект, принадлежащий к базе данных
            db.session.add(article)#добавляем объект
            db.session.commit()#сохраняем
            return redirect('/posts')#при успешном завершении перекинет пользователя на главную странцы
        except:
            return "При добавлении статьи произошла ошибка"

    else: #иначе просто отображаем запрос
        return render_template("create-artical.html")

# @app.route('/about/alina')
# def alina():
#     return "My name is alina!"

#
# @app.route('/user/<string:name>/<int:id>') # для вывода параметров
# def user(name, id):
#     return 'UserPage' + name + "-" + str(id)




if __name__ == "__main__": #проверка, что запускаем файл через app.py
    app.run(debug=True) #запустить локальный сервер, фласк проект, True - показывать ошибки на страничке, False - на сервере
    #находимся при запуске на локальном сервере (на главной страниче)
