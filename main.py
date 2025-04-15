from flask import Flask, render_template
from maths import MyMath

app = Flask(__name__)
ex = MyMath()
names = {'square': 'Квадратное уравнение',
         'line': 'Линейное уравнение',
         'sum': 'Пример на сложение',
         'min': 'Пример на вычитание',
         'mul': 'Пример на умножение',
         'crop': 'Пример на деление'}
funcs = {'Квадратное уравнение': ex.generate_square_x,
         'Линейное уравнение': ex.generate_line_x,
         'Пример на сложение': ex.generate_sum_stage_1,
         'Пример на вычитание': ex.generate_min_stage_1,
         'Пример на умножение': ex.generate_multiply_stage_1,
         'Пример на деление': ex.generate_crop_stage_1}


@app.route('/task/<title>')
def open_task(title):
    task = funcs[names[title]]()
    title_html = names[title]
    return render_template('task_opened.html', title=title_html, task=task)


@app.route('/task/<title>/solution')
def open_solution(title):
    task = funcs[names[title]]()
    title_html = names[title]
    solution_generation = {'Квадратное уравнение': ['Сначала найдем дискриминант квадратного уравнения:',
                                                    'Если дискриманант больше нуля, то будет 2 корня',
                                                    'Если равен нулю, то будет 1 корень',
                                                    'Если меньше нуля, то Корней нет.',
                                                    f'D = b\u00B2 - 4ac; D = {ex.find_discriminant(task)}',
                                                    'Теперь можно найти корни(корень) уравнения',
                                                    'x1 = (-b - \u221AD) / 2a',
                                                    'x2 = (-b + \u221AD) / 2a',
                                                    f'Ответ: {ex.answer_square_x(task)}'
                                                    ]}
    return render_template('solution.html', title=title_html, task=task,
                           solution_log=solution_generation[title_html])


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
