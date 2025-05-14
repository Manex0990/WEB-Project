from flask import Flask, render_template
from maths import MyMath

app = Flask(__name__)
ex = MyMath()


@app.route('/task/<title>')
def open_task(title):
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
    task = funcs[names[title]]()
    title_html = names[title]
    return render_template('solution.html', title=title_html, task=task)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
