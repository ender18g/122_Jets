from flask import Flask, render_template
app = Flask(__name__)


jets = [
    {'side':'124', 'parking':1, 'fuel':15.1, 'ordnance':'SCL-3', 'up':True},
    {'side':'123', 'parking':5, 'fuel':16.1, 'ordnance':'SCL-2', 'up':True},
    {'side':'126', 'parking':7, 'fuel':4.1, 'ordnance':'SCL-3', 'up':True},
    {'side':'102', 'parking':3, 'fuel':15.4, 'ordnance':'SCL-4', 'up':True},
    {'side':'134', 'parking':2, 'fuel':3.1, 'ordnance':'SCL-3', 'up':False},
    {'side':'155', 'parking':12, 'fuel':15.1, 'ordnance':'SCL-3', 'up':True}
]
jets.sort(key=lambda i: i['parking'])


@app.route('/')
@app.route('/schedule')
@app.route('/jets')
def hello_world():
    return render_template('index.html')


@app.route('/parking')
def parking_map():
    return render_template('parking.html',jets=jets)








