from flask import Flask, render_template, redirect, request, make_response, abort
from data import db_session
from data.groups import Group
from data.users import User
from form.user import RegisterForm, LoginForm, GroupForm
from form.task import TaskForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from maths import MyMath
#from data.users import User
#from data.groups import Group

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web_project'
ex = MyMath()
names = {'square': 'Квадратное уравнение',
         'line': 'Линейное уравнение',
         'sum_1': 'Пример на сложение (простой)',
         'sum_2': 'Пример на сложение (средний)',
         'sum_3': 'Пример на сложение (сложный)',
         'min_1': 'Пример на вычитание (простой)',
         'min_2': 'Пример на вычитание (средний)',
         'min_3': 'Пример на вычитание (сложный)',
         'mul_1': 'Пример на умножение (простой)',
         'mul_2': 'Пример на умножение (средний)',
         'mul_3': 'Пример на умножение (сложный)',
         'crop_1': 'Пример на деление (простой)',
         'crop_2': 'Пример на деление (средний)',
         'crop_3': 'Пример на деление (сложный)'}
funcs = {'Квадратное уравнение': [ex.generate_square_x, ex.check_answer_square_x],
         'Линейное уравнение': [ex.generate_line_x, ex.check_answer_line_x],
         'Пример на сложение (простой)': [ex.generate_sum_stage_1, ex.check_answer_for_all_stages],
         'Пример на сложение (средний)': [ex.generate_sum_stage_2, ex.check_answer_for_all_stages],
         'Пример на сложение (сложный)': [ex.generate_sum_stage_3, ex.check_answer_for_all_stages],
         'Пример на вычитание (простой)': [ex.generate_min_stage_1, ex.check_answer_for_all_stages],
         'Пример на вычитание (средний)': [ex.generate_min_stage_2, ex.check_answer_for_all_stages],
         'Пример на вычитание (сложный)': [ex.generate_min_stage_3, ex.check_answer_for_all_stages],
         'Пример на умножение (простой)': [ex.generate_multiply_stage_1, ex.check_answer_for_all_stages],
         'Пример на умножение (средний)': [ex.generate_multiply_stage_2, ex.check_answer_for_all_stages],
         'Пример на умножение (сложный)': [ex.generate_multiply_stage_3, ex.check_answer_for_all_stages],
         'Пример на деление (простой)': [ex.generate_crop_stage_1, ex.check_answer_for_all_stages],
         'Пример на деление (средний)': [ex.generate_crop_stage_2, ex.check_answer_for_all_stages],
         'Пример на деление (сложный)': [ex.generate_crop_stage_3, ex.check_answer_for_all_stages]}

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


@app.route('/task/square', methods=['GET', 'POST'])
def open_task_square():
    task = str(request.cookies.get('cur_task_square', funcs[names['square']][0]()))
    form = TaskForm()
    title_html = names['square']
    page = make_response(render_template('task_opened.html', title=title_html,
                                         task=task, form=form))
    page.set_cookie('cur_task_square', value=str(task), max_age=60 * 60 * 24 * 365 * 2)
    solution_generation = ['Сначала найдем дискриминант квадратного уравнения:',
                           'Если дискриманант больше нуля, то будет 2 корня',
                           'Если равен нулю, то будет 1 корень',
                           'Если меньше нуля, то Корней нет.',
                           f'D = b\u00B2 - 4ac; D = {ex.find_discriminant(task)}',
                           'Теперь можно найти корни(корень) уравнения',
                           'x1 = (-b - \u221AD) / 2a',
                           'x2 = (-b + \u221AD) / 2a',
                           f'Ответ: {ex.answer_square_x(task)}']
    if request.method == 'POST':
        user_answer = form.answer.data
        verdict = funcs[names['square']][1](task, user_answer)
        if verdict[1]:
            #update_points(verdict[2])
            res = make_response(
                render_template('task_opened.html', title=title_html, task=task,
                                form=form, solution_log=solution_generation, message=verdict[0]))
            res.set_cookie('cur_task_square', '', max_age=0)
        else:
            res = make_response(
                render_template('task_opened.html', title=title_html, task=task,
                                form=form, solution_log=['Дайте верный ответ, чтобы получить решение.'],
                                message=verdict[0]))
        return res
    return page


@app.route('/task/line', methods=['GET', 'POST'])
def open_task_line():
    task = str(request.cookies.get('cur_task_line', funcs[names['line']][0]()))
    form = TaskForm()
    title_html = names['line']
    page = make_response(render_template('task_opened.html', title=title_html,
                                         task=task, form=form))
    page.set_cookie('cur_task_line', value=str(task), max_age=60 * 60 * 24 * 365 * 2)
    solution_generation = ['Для того, чтобы решить линейное уравнение нужно все коэффициенты с "х"',
                           'перенести в одну часть уравнения, а остальные в другую.',
                           f'Ответ: {ex.answer_line_x(task)}']
    if request.method == 'POST':
        user_answer = form.answer.data
        verdict = funcs[names['line']][1](task, user_answer)
        if verdict[1]:
            #update_points(verdict[2])
            res = make_response(
                render_template('task_opened.html', title=title_html, task=task,
                                form=form, solution_log=solution_generation, message=verdict[0]))
            res.set_cookie('cur_task_line', '', max_age=0)
        else:
            res = make_response(
                render_template('task_opened.html', title=title_html, task=task,
                                form=form, solution_log=['Дайте верный ответ, чтобы получить решение.'],
                                message=verdict[0]))
        return res
    return page


@app.route('/task/<title>/<level>', methods=['GET', 'POST'])
def open_task_examples_all_stages(title, level):
    full_name = '_'.join([title, level])
    task = str(request.cookies.get('cur_task_ex', funcs[names[full_name]][0]()))
    form = TaskForm()
    title_html = names[full_name]
    page = make_response(render_template('task_opened.html', title=title_html,
                                         task=task, form=form))
    page.set_cookie('cur_task_ex', value=str(task), max_age=60 * 60 * 24 * 365 * 2)
    solution_generation = {'Пример на сложение': ['Просто сложим все коэффициенты',
                                                  f'Ответ: {ex.answer_for_all_stages(task)}'],
                           'Пример на вычитание': ['Просто вычтем все коэффициенты',
                                                   f'Ответ: {ex.answer_for_all_stages(task)}'],
                           'Пример на умножение': ['Просто перемножим все коэффициенты',
                                                   f'Ответ: {ex.answer_for_all_stages(task)}'],
                           'Пример на деление': ['Просто разделим по порядку все коэффициенты',
                                                 f'Ответ: {ex.answer_for_all_stages(task)}']}
    if request.method == 'POST':
        user_answer = form.answer.data
        verdict = funcs[names[full_name]][1](task, user_answer)
        if verdict[1]:
            #update_points(verdict[2])
            res = make_response(
                render_template('task_opened.html', title=title_html, task=task, form=form,
                                solution_log=solution_generation[title_html[:-10]], message=verdict[0]))
            res.set_cookie('cur_task_ex', '', max_age=0)
        else:
            res = make_response(
                render_template('task_opened.html', title=title_html, task=task,
                                form=form, solution_log=['Дайте верный ответ, чтобы получить решение.'],
                                message=verdict[0]))
        return res
    return page


# возможен баг с проверкой примеров из-за (не 5 а 5.0)
@app.route('/task')
def open_task_menu():
    res = make_response(render_template('task_window.html'))
    res.set_cookie('cur_task_square', '', max_age=0)
    res.set_cookie('cur_task_line', '', max_age=0)
    return res


@app.route('/task/<name>')
def open_change_level_window(name):
    res = make_response(render_template('change_level_window.html', name=name))
    res.set_cookie('cur_task_ex', '', max_age=0)
    return res


def main():
    app.run()


@app.route('/')
@login_required
def index():
    return render_template('base.html', current_user=current_user)


#def update_points(param):
#    points_data = {'square_x': 20, 'line_x': 15, 'sum_1': 5, 'sum_2': 8, 'sum_3': 10,
#                   'min_1': 5, 'min_2': 8, 'min_3': 10, 'mul_1': 7,
#                   'mul_2': 10, 'mul_3': 12, 'crop_1': 10, 'crop_2': 12, 'crop_3': 15}
#    db_session.global_init('db/web.db')
#    db_sess = db_session.create_session()
#    if current_user.is_authenticated:
#        groups = db_sess.query(User.groups).filter(User == current_user)
#        for group in groups:
#            db_session.global_init(group)
#            db_sess = db_session.create_session()
#            groups = db_sess.query(Group).filter(Group.id == current_user.id).first()
#            groups.points = int(groups.points) + points_data[param]
#            db_sess.commit()
#    else:
#        abort(404)


if __name__ == '__main__':
    main()
