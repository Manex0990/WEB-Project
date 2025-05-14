from flask import Flask, render_template, redirect, url_for, flash, request
from data import db_session
from data.users import User
from data.groups import Group
from data.group_members import GroupMember
from form.user import RegisterForm, LoginForm, GroupForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db_session.global_init("db/web.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    db_sess.close()
    return user


@app.route('/')
@login_required
def index():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message="Пароли не совпадают")

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            db_sess.close()
            return render_template('register.html', form=form, message="Такой пользователь уже есть")

        user = User()
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        db_sess.close()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message="Неверный логин или пароль", form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/group/create', methods=['GET', 'POST'])
@login_required
def group_create():
    if not current_user.teacher:
        flash("Нет прав для создания группы")
        return redirect('/')
    form = GroupForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        group = Group(name=form.name.data)
        db_sess.add(group)
        db_sess.commit()
        teacher_entry = GroupMember(group_id=group.id, user_id=current_user.id, is_teacher=True)
        db_sess.add(teacher_entry)
        db_sess.commit()
        db_sess.close()
        return redirect(url_for('view_group', group_id=group.id))
    return render_template('group_create.html', form=form)


@app.route('/group/join/<invite_link>')
@login_required
def join_group(invite_link):
    db_sess = db_session.create_session()
    group = db_sess.query(Group).filter(Group.invite_link == invite_link).first()
    if not group:
        db_sess.close()
        return render_template('base.html', title='Такой группы нет')

    exists = db_sess.query(GroupMember).filter(GroupMember.group_id == group.id,
                                               GroupMember.user_id == current_user.id).first()

    if exists:
        db_sess.close()
        return redirect(url_for('view_student_group', group_id=group.id))

    new_member = GroupMember(group_id=group.id, user_id=current_user.id, is_teacher=False)
    db_sess.add(new_member)
    db_sess.commit()
    db_sess.close()
    return redirect(url_for('view_student_group', group_id=group.id))


from sqlalchemy.orm import joinedload


@app.route('/group/<int:group_id>')
@login_required
def view_group(group_id):
    db_sess = db_session.create_session()

    group = db_sess.query(Group).filter(Group.id == group_id).first()
    if not group:
        db_sess.close()
        return render_template('base.html', title='Группа не найдена')

    teacher = db_sess.query(GroupMember).filter_by(
        group_id=group_id,
        user_id=current_user.id,
        is_teacher=True
    ).first()

    if not teacher:
        db_sess.close()
        return render_template('base.html', title='Нет доступа')

    members = db_sess.query(GroupMember).options(joinedload(GroupMember.user)).filter_by(group_id=group_id).all()
    db_sess.close()

    return render_template('group_details.html', group=group, members=members)


@app.route('/group/<int:group_id>/remove/<int:user_id>', methods=['POST'])
@login_required
def remove_member(group_id, user_id):
    db_sess = db_session.create_session()
    if not current_user.teacher:
        return render_template('base.html', title='Нет прав')
    member = db_sess.query(GroupMember).filter_by(group_id=group_id, user_id=user_id).first()
    if member:
        db_sess.delete(member)
        db_sess.commit()
    return redirect(url_for('view_group', group_id=group_id))


@app.route('/group/<int:group_id>/points/<int:user_id>', methods=['POST'])
@login_required
def add_points(group_id, user_id):
    if not current_user.teacher:
        return render_template('base.html', title='Нет прав')
    points = int(request.form.get('points', 0))
    db_sess = db_session.create_session()
    member = db_sess.query(GroupMember).filter_by(group_id=group_id, user_id=user_id).first()
    if member:
        member.points += points
        db_sess.commit()
    db_sess.close()
    return redirect(url_for('view_group', group_id=group_id))


@app.route('/group/<int:group_id>/regenerate_link', methods=['POST'])
@login_required
def regenerate_invite_link(group_id):
    db_sess = db_session.create_session()
    group = db_sess.query(Group).filter(Group.id == group_id).first()
    if not group:
        return render_template('base.html', title='Группа не найдена')
    group.invite_link = str(uuid.uuid4())
    db_sess.commit()
    return redirect(url_for('view_group', group_id=group.id))


@app.route('/student_group/<int:group_id>')
@login_required
def view_student_group(group_id):
    db_sess = db_session.create_session()
    member = db_sess.query(GroupMember).filter_by(group_id=group_id, user_id=current_user.id).first()
    if not member:
        return render_template('base.html', title='Нет доступа')
    group = db_sess.query(Group).filter(Group.id == group_id).first()
    members = db_sess.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    return render_template('student_group_details.html', group=group, members=members)


@app.route('/groups')
@login_required
def view_groups():
    if not current_user.teacher:
        return render_template('student_groups.html')

    db_sess = db_session.create_session()

    teacher_memberships = db_sess.query(GroupMember).filter_by(user_id=current_user.id, is_teacher=True).all()
    group_ids = [i.group_id for i in teacher_memberships]

    groups = db_sess.query(Group).filter(Group.id.in_(group_ids)).all()

    return render_template('groups.html', groups=groups, title='Мои группы')


@app.route('/student_groups')
@login_required
def student_groups():
    if current_user.teacher:
        return render_template('base.html', title='Нет доступа')

    db_sess = db_session.create_session()

    student_memberships = db_sess.query(GroupMember).filter_by(user_id=current_user.id, is_teacher=False).all()
    group_ids = [i.group_id for i in student_memberships]

    groups = db_sess.query(Group).filter(Group.id.in_(group_ids)).all()

    return render_template('student_groups.html', groups=groups, title='Мои группы')


def main():
    app.run()


if __name__ == '__main__':
    main()
