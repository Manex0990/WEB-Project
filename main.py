from flask import Flask, render_template, request, redirect, make_response
from maths import MyMath
from task import TaskForm
from flask_login import current_user

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
    return render_template('task_window.html')


@app.route('/task/sum')
def open_change_level_window_sum():
    res = make_response(render_template('change_level_window.html', name='sum'))
    res.set_cookie('cur_task_ex', '', max_age=0)
    return res


@app.route('/task/min')
def open_change_level_window_min():
    res = make_response(render_template('change_level_window.html', name='min'))
    res.set_cookie('cur_task_ex', '', max_age=0)
    return res


@app.route('/task/mul')
def open_change_level_window_mul():
    res = make_response(render_template('change_level_window.html', name='mul'))
    res.set_cookie('cur_task_ex', '', max_age=0)
    return res


@app.route('/task/crop')
def open_change_level_window_crop():
    res = make_response(render_template('change_level_window.html', name='crop'))
    res.set_cookie('cur_task_ex', '', max_age=0)
    return res


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
