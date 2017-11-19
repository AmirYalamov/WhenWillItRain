from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('mainpage.html')

@app.route('/weatheresult',methods = ['POST', 'GET'])
def weatheresult():
   if request.method == 'POST':
      result = request.form
      return render_template("weatheresult.html",result=result)

@app.route('/testpage')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)
