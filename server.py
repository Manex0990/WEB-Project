from flask import Flask, render_template, redirect
from data import db_session
from data.groups import Group
from data.users import User
from form.user import RegisterForm, LoginForm, GroupForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
db_session.global_init("db/web.db")
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User(
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            patronymic=form.patronymic.data,
            teacher=form.teacher.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
@login_required
def index():
    return render_template('index.html', current_user=current_user)


@app.route('/group/create', methods=['GET', 'POST'])
@login_required
def group_create():
    if not current_user.teacher:
        print("У вас нет прав для создания групп")
        return redirect("/")

    form = GroupForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        group = Group()
        group.name = form.name.data
        group.description = form.description.data
        group.teacher_id = current_user.id
        db_sess.add(group)
        db_sess.commit()
        print('Группа создана')
        return redirect('/')
    return render_template('group_create.html', title='Создание группы', form=form)


@app.route('/groups')
@login_required
def view_groups():
    if not current_user.teacher:
        print("У вас нет прав для просмотра групп.")
        return redirect("/")
    db_sess = db_session.create_session()
    groups = db_sess.query(Group).filter(Group.teacher_id == current_user.id).all()
    return render_template('groups.html', title='Мои группы', groups=groups)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


def main():
    app.run()


@app.route('/')
def index():
    return render_template('base.html')


if __name__ == '__main__':
    main()
