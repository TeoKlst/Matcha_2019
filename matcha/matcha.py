from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
        'title': 'Some1 Title',
        'name':  'Name1'
    },
    {
        'title': 'Some2 Title',
        'name':  'Name2'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts = posts)


@app.route('/about')
def about():
    return render_template('about.html', title = 'About')


if __name__ == '__main__':
    app.run(debug=True)
