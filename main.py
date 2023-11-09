from flask import Flask, render_template, request, redirect
import re
import os
import json

participants = []
file_path_participants = "participants.json"



# On start, load all users to lists
try:
    if os.path.getsize(file_path_participants) >= 5:
        with open(file_path_participants, "r") as json_file:
            participants = json.load(json_file)
except FileNotFoundError:
    print(f"File path not found. Starting with an empty list.")

# Write new participants to file
def write_participants():
    with open(file_path_participants, "w") as json_file:
        json.dump(participants, json_file)



# Check regex of nick, and friend
def checkReg(val):
    if val is not None:
        if re.match(r'^[a-zA-Z\u00C0-\u017F\s]+$', val):
            return True
        else:
            return False



app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', participants=participants), 200

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    chyba = None
    if request.method == 'GET':
        return render_template('registration.html'), 200
    elif request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pass')
        school_class = request.form.get('school_class')
        friend = request.form.get('friend')
        swimmer = request.form.get('swimmer')
        gdpr = request.form.get('gdpr')

        if swimmer and gdpr:
            if school_class != "separator":
                if nickcheck(name) == "True":
                    if checkReg(name):
                        if friend is None and not checkReg(friend):
                            friend = "X"

                        participants.append(
                            {
                                "name": name,
                                "email": email,
                                "pass": password,
                                "school_class": school_class,
                                "friend": friend,
                                "swimmer": "Ano",
                                "gdpr": "Souhlas udělen"
                            }
                        )
                        write_participants()
                    else:
                        chyba = "Použij pouze písmena"
                else:
                    chyba = "Toto jméno je už použito"
            else:
                chyba = "Vyber si validní třídu"
        else:
            chyba = "Musíš být být plavec a souhasit s GDPR"


        if chyba is None:
            return redirect('/')
        else:
            return render_template('registration.html', chyba=chyba), 400



@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'GET':
        return render_template('table.html'), 200

    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')

        ok = False
        for p in participants:
            if p['email'] == email and p['pass'] == password:
                ok = True

        if ok:
            return render_template('table.html', participants = participants), 200
        else:
            return render_template('table.html'), 400

@app.route('/nickcheck/<nick>', methods=['GET'])
def nickcheck(val):
    safe = True
    for p in participants:
        if val.lower() in p["name"].lower():
            safe = False
            break
    return str(safe)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
