from flask import Flask, render_template, request, redirect
app = Flask(__name__)


jets = [
    {'side':'124', 'parking':1, 'fuel':15.1, 'ordnance':'SCL-3', 'up':True},
    {'side':'123', 'parking':5, 'fuel':16.1, 'ordnance':'SCL-2', 'up':True},
    {'side':'126', 'parking':7, 'fuel':4.1, 'ordnance':'SCL-3', 'up':True},
    {'side':'102', 'parking':3, 'fuel':15.4, 'ordnance':'SCL-4', 'up':True},
    {'side':'134', 'parking':2, 'fuel':3.1, 'ordnance':'SCL-3', 'up':False},
    {'side':'155', 'parking':12, 'fuel':15.1, 'ordnance':'SCL-3', 'up':True}
]



def order_jets(jets):
    jets = sorted(jets,key=lambda i: i['side'])
    return jets

def fill_jets(jet_list):
    jet_list = jet_list[:]
    exists = False
    for i in range(1,31):
        for jet in jet_list:
            if jet['parking']==i:
                exists = True
                break
        if not exists:
            jet_list.append({'side':'-','parking':i})
        exists = False

    jet_list.sort(key=lambda i: i['parking'])

    return jet_list



jets = order_jets(jets)

@app.route('/')
@app.route('/schedule')
def hello_world():
    return render_template('index.html')


@app.route('/parking')
def parking_map():
    return render_template('parking.html',jets=fill_jets(jets))


@app.route('/jets', methods=['GET'])
def jet_list():
    if request.method == 'GET':
        return render_template('jets.html', jets=jets )

@app.route('/jets/add', methods=['POST'])  
def add_jet():      
    jets.insert(0,{'side':'Side', 'parking':0, 'fuel':0, 'ordnance':'SCL-3', 'up':False})
    return render_template('edit.html', jet=jets[int(0)],index = 0)

@app.route("/remove/<i>",methods=['GET'])
def remove_jet(i):
    jets.pop(int(i))
    return render_template('jets.html', jets=jets )



@app.route("/edit/<i>",methods=['POST','GET'])
def edit_jet(i):
    if request.method == 'GET':
        return render_template('edit.html', jet=jets[int(i)],index = int(i))
    if request.method == 'POST':
        jets[int(i)]={
            "side":request.form.get("side"),
            "parking":int(request.form.get("parking")),
            "fuel":float(request.form.get("fuel")),
            "ordnance":request.form.get("ordnance"),
            "up":bool(request.form.get("up"))


        }
        return redirect("/jets")


