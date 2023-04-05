from flask import Flask, render_template, request, redirect
import csv
import os



app = Flask(__name__)
print(__name__)


@app.route("/")
def home_page():
    return render_template('index.html' )


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


# Função que recebe dados do formulário
def write_to_file(data):
    with open('database.txt', 'a') as db:
        for key, value in data.items():
            db.write(f'{key}: {value}\n')
    return 'Data saved successfully!!!'


def write_to_csv(data, file):
    with open(file, 'a', newline='') as db_csv:
        # Cria um objeto escritor CSV
        writer = csv.writer(db_csv)

        # Se o arquivo CSV estiver vazio, escreva a linha de cabeçalho com os nomes das colunas
        if os.stat(file).st_size == 0:
            writer.writerow(['Key', 'Value'])

        for key, value in data.items():
            writer.writerow([f'{key}: {value}'])
        db_csv.write('*' * 30 + '\n')

    return 'Data saved successfully!!!'


def read_csv_data(file):
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            print(line)



@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_file(data)
            write_to_csv(data, 'database.csv')
            read_csv_data('database.csv')
            return redirect('thankyou.html')
        except:
            return 'Data was not saved on database!'
    else:
        return 'Something went wrong! Try Again.'


if __name__ == '__main__':
    app.run(debug=True)
