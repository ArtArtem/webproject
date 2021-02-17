from flask_wtf import FlaskForm
from flask import Flask, redirect, render_template, session
from db import DB, UserModel, ItemsModel
from loginform import LoginForm
from additemsform import AddItemsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db = DB()
ItemsModel(db.get_connection()).init_table()
UserModel(db.get_connection()).init_table()
#UserModel(db.get_connection()).insert('1', '1')

@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    news = ItemsModel(db.get_connection()).get_all(session['user_id'])
    return render_template('index.html', username=session['username'],
                           news=news)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UserModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/index")
    return render_template('login.html', title='Autorisation', form=form)


@app.route('/add_items', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    form = AddItemsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        nm = ItemsModel(db.get_connection())
        nm.insert(title,content,session['user_id'])
        return redirect("/index")
    return render_template('add_items.html', title='Добавление товара',
                           form=form, username=session['username'])
 
@app.route('/delete_items/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = ItemsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")







if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
