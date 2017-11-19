from flask import Flask, render_template, request

import PelmorexInterpreter

app = Flask(__name__)

#loc = PelmorexInterpreter. nextPrecipToString()

@app.route('/')
def index():
    return render_template('mainpage.html')

@app.route('/weatheresult',methods = ['POST', 'GET'])
def weatheresult():
   if request.method == 'POST':
      result = request.form

      for i, j in result.items():
          s = j

      loc = PelmorexInterpreter.nextPrecipToString(s)

      return render_template("weatheresult.html",result=result, loc=loc)


if __name__ == '__main__':
    app.run(debug=True)
