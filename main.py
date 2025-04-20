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
c = 0
temp = ''


@app.route('/task/<title>', methods=['GET', 'POST'])
def open_task(title):
    global c
    global temp
    form = TaskForm()
    if c == 0:
        task = funcs[names[title]][0]()
        temp = task
    title_html = names[title]
    solution_generation = {'Квадратное уравнение': ['Сначала найдем дискриминант квадратного уравнения:',
                                                    'Если дискриманант больше нуля, то будет 2 корня',
                                                    'Если равен нулю, то будет 1 корень',
                                                    'Если меньше нуля, то Корней нет.',
                                                    f'D = b\u00B2 - 4ac; D = {ex.find_discriminant(temp)}',
                                                    'Теперь можно найти корни(корень) уравнения',
                                                    'x1 = (-b - \u221AD) / 2a',
                                                    'x2 = (-b + \u221AD) / 2a',
                                                    f'Ответ: {ex.answer_square_x(temp)}'],
                           'Линейное уравнение': ['Решим линейное уравнение'],
                           'Пример на сложение': ['Просто сложим все коэффициенты',
                                                  f'Ответ: {ex.answer_for_all_stages(temp)}'],
                           'Пример на вычитание': ['Просто вычтем все коэффициенты',
                                                   f'Ответ: {ex.answer_for_all_stages(temp)}'],
                           'Пример на умножение': ['Просто перемножим все коэффициенты',
                                                   f'Ответ: {ex.answer_for_all_stages(temp)}'],
                           'Пример на деление': ['Просто разделим по порядку все коэффициенты',
                                                 f'Ответ: {ex.answer_for_all_stages(temp)}']}
    if request.method == 'POST':
        user_answer = form.answer.data
        verdict = funcs[names[title]][1](temp, user_answer)
        if verdict[1]:
            c += 1
            return render_template('solution.html', title=title_html, task=temp, form=form,
                                   solution_log=solution_generation[title_html], message=verdict[0])
        else:
            c += 1
            return render_template('solution.html', title=title_html, task=temp, form=form,
                                   solution_log=['Дайте верный ответ, чтоб получить решение'],
                                   message=verdict[0])
    c += 1
    return render_template('task_opened.html', title=title_html, task=temp, form=form)


# нужно разделить обработчики для решения квадратного, линейного, примеров.
# засунуть все в функцию open_task
@app.route('/task/<title>/solution')
def open_solution(title):
    task = funcs[names[title]][0]()
    title_html = names[title]
    solution_generation = {'Квадратное уравнение': ['Сначала найдем дискриминант квадратного уравнения:',
                                                    'Если дискриманант больше нуля, то будет 2 корня',
                                                    'Если равен нулю, то будет 1 корень',
                                                    'Если меньше нуля, то Корней нет.',
                                                    f'D = b\u00B2 - 4ac; D = {ex.find_discriminant(task)}',
                                                    'Теперь можно найти корни(корень) уравнения',
                                                    'x1 = (-b - \u221AD) / 2a',
                                                    'x2 = (-b + \u221AD) / 2a',
                                                    f'Ответ: {ex.answer_square_x(task)}'],
                           'Линейное уравнение': ['Решим линейное уравнение'],
                           'Пример на сложение': ['Просто сложим все коэффициенты',
                                                  f'Ответ: {ex.answer_for_all_stages(task)}'],
                           'Пример на вычитание': ['Просто вычтем все коэффициенты',
                                                   f'Ответ: {ex.answer_for_all_stages(task)}'],
                           'Пример на умножение': ['Просто перемножим все коэффициенты',
                                                   f'Ответ: {ex.answer_for_all_stages(task)}'],
                           'Пример на деление': ['Просто разделим по порядку все коэффициенты',
                                                 f'Ответ: {ex.answer_for_all_stages(task)}']}
    return render_template('solution.html', title=title_html, task=task,
                           solution_log=solution_generation[title_html])


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
