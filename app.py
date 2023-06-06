from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/prediction', methods=['POST'])
def predict():
    # 나이 입력 받아오기
    age = int(request.form['age'])

    # 예측 결과 계산하기 (이 부분은 실제 코드로 대체)

    # 예측 결과를 HTML 페이지에 렌더링
    return render_template('prediction.html', table=age)  


if __name__ == '__main__':
    app.run()