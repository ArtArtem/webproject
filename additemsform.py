from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask import Flask, redirect, render_template
 
class AddItemsForm(FlaskForm):
    title = StringField('Название товара и цена', validators=[DataRequired()])
    content = TextAreaField('Описание товара', validators=[DataRequired()])
    submit = SubmitField('Добавить')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/', methods=['GET', 'POST'])
@app.route('/add_items', methods=['GET', 'POST'])
def add_news():
    form = AddItemsForm()
    return render_template('add_items.html', title='Добавление товара',form=form)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
