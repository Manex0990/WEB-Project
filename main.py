from flask import Flask, render_template, request, redirect
from maths import MyMath
from task import TaskForm

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
c_sq, c_line, c_ex = 0, 0, 0
count_control = {'Квадратное уравнение': c_sq,
                 'Линейное уравнение': c_line,
                 'Пример': c_ex}
temp_sq, temp_line, temp_ex = '', '', ''


@app.route('/task/square', methods=['GET', 'POST'])
def open_task_square():
    global c_sq
    global temp_sq
    title = 'square'
    form = TaskForm()
    if c_sq == 0:
        task = funcs[names[title]][0]()
        temp_sq = task
    title_html = names[title]
    solution_generation = ['Сначала найдем дискриминант квадратного уравнения:',
                           'Если дискриманант больше нуля, то будет 2 корня',
                           'Если равен нулю, то будет 1 корень',
                           'Если меньше нуля, то Корней нет.',
                           f'D = b\u00B2 - 4ac; D = {ex.find_discriminant(temp_sq)}',
                           'Теперь можно найти корни(корень) уравнения',
                           'x1 = (-b - \u221AD) / 2a',
                           'x2 = (-b + \u221AD) / 2a',
                           f'Ответ: {ex.answer_square_x(temp_sq)}']
    if request.method == 'POST':
        user_answer = form.answer.data
        verdict = funcs[names[title]][1](temp_sq, user_answer)
        solution(title_html, temp_sq, form, solution_generation, verdict)
    c_sq += 1
    return render_template('task_opened.html', title=title_html, task=temp_sq, form=form)


@app.route('/task/line', methods=['GET', 'POST'])
def open_task_line():
    global c_line
    global temp_line
    title = 'line'
    form = TaskForm()
    if c_line == 0:
        task = funcs[names[title]][0]()
        temp_line = task
    title_html = names[title]
    solution_generation = ['Для того, чтобы решить линейное уравнение нужно все коэффициенты с "х"',
                           'перенести в одну часть уравнения, а остальные в другую.',
                           f'Ответ: {ex.answer_line_x(temp_line)}']
    if request.method == 'POST':
        user_answer = form.answer.data
        verdict = funcs[names[title]][1](temp_line, user_answer)
        solution(title_html, temp_line, form, solution_generation, verdict)
    c_line += 1
    return render_template('task_opened.html', title=title_html, task=temp_line, form=form)


@app.route('/task/<title>/<level>', methods=['GET', 'POST'])
def open_task_examples_all_stages(title, level):
    global c_ex
    global temp_ex
    form = TaskForm()
    full_name = '_'.join([title, level])
    if c_ex == 0:
        task = funcs[names[full_name]][0]()
        temp_ex = task
    title_html = names[full_name]
    solution_generation = {'Пример на сложение': ['Просто сложим все коэффициенты',
                                                  f'Ответ: {ex.answer_for_all_stages(temp_ex)}'],
                           'Пример на вычитание': ['Просто вычтем все коэффициенты',
                                                   f'Ответ: {ex.answer_for_all_stages(temp_ex)}'],
                           'Пример на умножение': ['Просто перемножим все коэффициенты',
                                                   f'Ответ: {ex.answer_for_all_stages(temp_ex)}'],
                           'Пример на деление': ['Просто разделим по порядку все коэффициенты',
                                                 f'Ответ: {ex.answer_for_all_stages(temp_ex)}']}
    if request.method == 'POST':
        user_answer = form.answer.data
        verdict = funcs[names[full_name]][1](temp_ex, user_answer)
        solution(title_html, temp_ex, form, solution_generation[title_html[:-10]], verdict)
    c_ex += 1
    return render_template('task_opened.html', title=title_html, task=temp_ex, form=form)


# придумать как сократить копипасту в функции open_task_square и open_task_line (после строки if request.method == 'POST') !!!!!!!!
# возможен баг с проверкой примеров из-за (не 5 а 5.0)
def solution(title, task, form, solution_log, verdict):
    if verdict[1]:
        count_update(title)
        return render_template('solution.html', title=title, task=task, form=form,
                               solution_log=solution_log, message=verdict[0])
    else:
        count_update(title)
        return render_template('solution.html', title=title, task=temp_ex, form=form,
                               solution_log=['Дайте верный ответ, чтоб получить решение'],
                               message=verdict[0])


def count_update(title):
    if 'пример' in title.lower():
        count_control['Пример'] += 1
    else:
        count_control[title] += 1


@app.route('/task')
def open_task_menu():
    global c_sq, c_line, c_ex
    global temp_sq, temp_line, temp_ex
    c_sq, c_line, c_ex = 0, 0, 0
    temp_sq, temp_line, temp_ex = '', '', ''
    return render_template('task_window.html')


# нужно разделить обработчики для решения квадратного, линейного, примеров.
# засунуть все в функцию open_task
# @app.route('/task/<title>/solution')
# def open_solution(title):
#    task = funcs[names[title]][0]()
#    title_html = names[title]
#    solution_generation = {'Квадратное уравнение': ['Сначала найдем дискриминант квадратного уравнения:',
#                                                    'Если дискриманант больше нуля, то будет 2 корня',
#                                                    'Если равен нулю, то будет 1 корень',
#                                                    'Если меньше нуля, то Корней нет.',
#                                                    f'D = b\u00B2 - 4ac; D = {ex.find_discriminant(task)}',
#                                                    'Теперь можно найти корни(корень) уравнения',
#                                                    'x1 = (-b - \u221AD) / 2a',
#                                                    'x2 = (-b + \u221AD) / 2a',
#                                                    f'Ответ: {ex.answer_square_x(task)}'],
#                           'Линейное уравнение': ['Решим линейное уравнение'],
#                           'Пример на сложение': ['Просто сложим все коэффициенты',
#                                                  f'Ответ: {ex.answer_for_all_stages(task)}'],
#                           'Пример на вычитание': ['Просто вычтем все коэффициенты',
#                                                   f'Ответ: {ex.answer_for_all_stages(task)}'],
#                           'Пример на умножение': ['Просто перемножим все коэффициенты',
#                                                   f'Ответ: {ex.answer_for_all_stages(task)}'],
#                           'Пример на деление': ['Просто разделим по порядку все коэффициенты',
#                                                 f'Ответ: {ex.answer_for_all_stages(task)}']}
#    return render_template('solution.html', title=title_html, task=task,
#                           solution_log=solution_generation[title_html])


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
