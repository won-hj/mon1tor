from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world'

@app.route('/demo') #<//!-- methods=['POST'] --> 
def demo():
    return render_template('demo.html')

if __name__ == '__main__':
    app.run()

