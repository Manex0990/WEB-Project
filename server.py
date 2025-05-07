from flask import render_template, redirect, url_for, Flask
from data import db_session
from data.groups import Group
from data.users import User
from form.user import RegisterForm, LoginForm, GroupForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db_session.global_init("db/web.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


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
    if current_user.teacher:
        return render_template('base.html', current_user=current_user)
    else:
        return redirect(url_for('student_groups'))


@app.route('/group/create', methods=['GET', 'POST'])
@login_required
def group_create():
    if not current_user.teacher:
        return render_template('base.html', title='Нет прав')

    form = GroupForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        group = Group(
            name=form.name.data,
            member_id=current_user.id,
            is_teacher=True
        )
        db_sess.add(group)
        db_sess.commit()
        return redirect('/groups')
    return render_template('group_create.html', title='Создание группы', form=form)


@app.route('/groups')
@login_required
def view_groups():
    if not current_user.teacher:
        return render_template('base.html', title='Нет прав')
    db_sess = db_session.create_session()
    groups = db_sess.query(Group).filter(Group.member_id == current_user.id, Group.is_teacher == True).all()
    return render_template('groups.html', title='Мои группы', groups=groups)


@app.route('/group/<int:group_id>')
@login_required
def view_group(group_id):
    db_sess = db_session.create_session()
    group = db_sess.query(Group).filter(Group.id == group_id).first()

    is_teacher_in_group = db_sess.query(Group).filter(Group.member_id == current_user.id, Group.is_teacher == True,
                                                      Group.id == group_id).first()
    if not is_teacher_in_group:
        return render_template('base.html', title='Нет прав')

    members = db_sess.query(Group).filter(Group.id == group_id).all()

    all_users = db_sess.query(User).all()
    members_ids = [member.member_id for member in members]
    available_users = [user for user in all_users if user.id not in members_ids]

    return render_template('group_details.html', group=group, members=members, title='Группа',
                           available_users=available_users)


@app.route('/group/join/<invite_link>')
@login_required
def join_group(invite_link):
    db_sess = db_session.create_session()
    group = db_sess.query(Group).filter(Group.invite_link == invite_link).first()

    if not group:
        return render_template('base.html', title='Такой группы нет')

    if db_sess.query(Group).filter(Group.id == group.id, Group.member_id == current_user.id).first():
        return render_template('base.html', title='Ты уже в группе')

    new_member = Group(name=group.name,
                       member_id=current_user.id,
                       is_teacher=False,
                       points=0)
    db_sess.add(new_member)
    db_sess.commit()

    return redirect(f'/group/{group.id}')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/student_groups')
@login_required
def student_groups():
    if current_user.teacher:
        return render_template('base.html', title='Нет прав')

    db_sess = db_session.create_session()
    groups = db_sess.query(Group).filter(Group.member_id == current_user.id).all()
    return render_template('student_groups.html', groups=groups, title='Мои группы')


@app.route('/student_group/<int:group_id>')
@login_required
def view_student_group(group_id):
    db_sess = db_session.create_session()

    group = db_sess.query(Group).filter(Group.id == group_id).first()
    if not group:
        return render_template('base.html', title='Группа не найдена')

    is_member = db_sess.query(Group).filter(Group.id == group_id, Group.member_id == current_user.id).first()
    if not is_member:
        return render_template('base.html', title='Нет прав')

    members = db_sess.query(Group).filter(Group.id == group_id).all()

    return render_template('student_group_details.html', group=group, members=members, title='Участники группы')


def main():
    app.run()


if __name__ == '__main__':
    main()
