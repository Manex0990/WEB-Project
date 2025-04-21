from flask import Flask, render_template, request, redirect
from maths import MyMath
from task import TaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web_project'
ex = MyMath()
names = {'square': 'Квадратное уравнение',
         'line': 'Линейное уравнение',
         'sum': 'Пример на сложение',
         'min': 'Пример на вычитание',
         'mul': 'Пример на умножение',
         'crop': 'Пример на деление'}
funcs = {'Квадратное уравнение': [ex.generate_square_x, ex.check_answer_square_x],
         'Линейное уравнение': [ex.generate_line_x, ex.check_answer_line_x],
         'Пример на сложение': [ex.generate_sum_stage_1, ex.check_answer_for_all_stages],
         'Пример на вычитание': [ex.generate_min_stage_1, ex.check_answer_for_all_stages],
         'Пример на умножение': [ex.generate_multiply_stage_1, ex.check_answer_for_all_stages],
         'Пример на деление': [ex.generate_crop_stage_1, ex.check_answer_for_all_stages]}
c_sq, c_line = 0, 0
temp_sq, temp_line = '', ''


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
        if verdict[1]:
            c_sq += 1
            return render_template('solution.html', title=title_html, task=temp_sq, form=form,
                                   solution_log=solution_generation, message=verdict[0])
        else:
            c_sq += 1
            return render_template('solution.html', title=title_html, task=temp_sq, form=form,
                                   solution_log=['Дайте верный ответ, чтоб получить решение'],
                                   message=verdict[0])
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
        if verdict[1]:
            c_line += 1
            return render_template('solution.html', title=title_html, task=temp_line, form=form,
                                   solution_log=solution_generation, message=verdict[0])
        else:
            c_line += 1
            return render_template('solution.html', title=title_html, task=temp_line, form=form,
                                   solution_log=['Дайте верный ответ, чтоб получить решение'],
                                   message=verdict[0])
    c_line += 1
    return render_template('task_opened.html', title=title_html, task=temp_line, form=form)


# придумать как сократить копипасту в функции open_task_square и open_task_line (после строки if request.method == 'POST')
def solution():
    pass


@app.route('/task')
def open_task_menu():
    global c_sq, c_line
    global temp_sq, temp_line
    c_sq, c_line = 0, 0
    temp_sq, temp_line = '', ''
    return render_template('task_window.html')


# нужно разделить обработчики для решения квадратного, линейного, примеров.
# засунуть все в функцию open_task
#@app.route('/task/<title>/solution')
#def open_solution(title):
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
