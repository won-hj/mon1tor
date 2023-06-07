from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/past_graph1')
def past_graph1():
    return render_template('past_graph1.html')

@app.route('/past_graph2')
def past_graph2():
    return render_template('past_graph2.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

if __name__ == "__main__":
    app.run()
