from flask import Flask, render_template, request, redirect
import json
app = Flask(__name__)
app.testing = True

def load_jets():
    try: 
        with open("jets.txt","r") as data_file:
            jets = json.load(data_file)
    except:
        print("loading DEFAULT JETS")
        jets = [
            {'side':124, 'parking':1, 'fuel':15.1, 'ordnance':'SCL-3', 'up':True},
            {'side':123, 'parking':5, 'fuel':16.1, 'ordnance':'SCL-2', 'up':True},
            {'side':126, 'parking':7, 'fuel':4.1, 'ordnance':'SCL-3', 'up':True},
            {'side':102, 'parking':3, 'fuel':15.4, 'ordnance':'SCL-4', 'up':True},
            {'side':134, 'parking':2, 'fuel':3.1, 'ordnance':'SCL-3', 'up':False},
            {'side':155, 'parking':12, 'fuel':15.1, 'ordnance':'SCL-3', 'up':True}
        ]
    return jets

def save_jets(jets):
    with open("jets.txt", "w") as data_file:
        json.dump(jets, data_file, indent=2)
    return None

def order_jets(jet_list):
    global jets
    jets = sorted(jet_list,key=lambda i: i['side'])
    for i in range(len(jets)):
        jets[i].update({"serial":i})
    return jets

def fill_jets(jet_list):
    jet_list = jet_list[:]
    parked_jets = []
    flying_jets = []

    for jet in jet_list:
        if jet['parking']==0:
            flying_jets.append(jet)
        else:
            parked_jets.append(jet)
    
    exists = False
    for i in range(1,31):
        for jet in parked_jets:
            if jet['parking']==i:
                exists = True
                break
        if not exists:
            parked_jets.append({'side':'-','parking':i})
        exists = False

    parked_jets.sort(key=lambda i: i['parking'])
    flying_jets

    return [parked_jets,flying_jets]


jets = load_jets()
jets = order_jets(jets)

@app.route('/')
@app.route('/schedule')
def hello_world():
    return render_template('index.html')


@app.route('/parking')
def parking_map():
    [parked_jets,flying_jets] = fill_jets(jets)
    return render_template('parking.html',jets=parked_jets, all_jets = jets)


@app.route('/jets', methods=['GET'])
def jet_list():
    if request.method == 'GET':
        return render_template('jets.html', jets=jets )

@app.route('/jets/add', methods=['POST'])  
def add_jet():      
    jets.append({'side':'000', 'parking':0, 'fuel':0, 'ordnance':'SCL-3', 'up':False})
    return redirect("/edit/" + str(len(jets)-1))

@app.route("/remove/<i>",methods=['GET'])
def remove_jet(i):
    jets.pop(int(i))
    return render_template('jets.html', jets=jets )

@app.route("/fly/<i>",methods=['GET'])
def fly_jet(i):
    global jets
    jets[int(i)].update({'parking':0})
    jets = order_jets(jets)
    save_jets(jets)
    return redirect("/parking")

@app.route("/park/<i>",methods=['POST'])
def park_jet(i):
    global jets
    jets[int(request.form.get("serial_landed"))].update({'parking':int(i)})
    jets = order_jets(jets)
    save_jets(jets)
    return redirect("/parking")



@app.route("/edit/<i>",methods=['POST','GET'])
def edit_jet(i):
    global jets
    if request.method == 'GET':
        return render_template('edit.html', jet=jets[int(i)],index = int(i))
    if request.method == 'POST':
        jets[int(i)]={
            "side":int(request.form.get("side")),
            "parking":int(request.form.get("parking")),
            "fuel":float(request.form.get("fuel")),
            "ordnance":request.form.get("ordnance"),
            "up":bool(request.form.get("up"))
        }
        jets = order_jets(jets)
        save_jets(jets)
        return redirect("/jets")


app.run(debug=True)