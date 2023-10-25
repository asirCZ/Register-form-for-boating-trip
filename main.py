from flask import Flask, render_template, request, redirect
import re
import os
import json

ucastnici = []
file_path_ucastnici = "ucastnici.json"

try:
    if os.path.getsize(file_path_ucastnici) >= 5:
        with open(file_path_ucastnici, "r") as json_file:
            ucastnici = json.load(json_file)
except FileNotFoundError:
    print(f"File '{file_path_ucastnici}' not found. Starting with an empty list.")

def write_ucastnici():
    with open(file_path_ucastnici, "w") as json_file:
        json.dump(ucastnici, json_file)




def checkReg(val):
    if val is not None:
        if re.match(r'^[a-zA-Z0-9]+$', val):
            return True
        else:
            return False





app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', ucastnici = ucastnici), 200

@app.route('/registrace', methods=['GET', 'POST'])
def registrace():
    chyba = None
    if request.method == 'GET':
        return render_template('registrace.html'), 200
    elif request.method == 'POST':
        nick = request.form.get('nick')
        jmenoprijimeni = request.form.get('jmenoprijimeni')
        trida = request.form.get('trida')
        kanoe_kamarad = request.form.get('kanoe_kamarad')
        je_plavec = request.form.get('je_plavec')

        if je_plavec:
            if trida != "separator":
                if kontrola(jmenoprijimeni) == "True" and kontrola(nick) == "True":
                    if checkReg(nick):
                        if kanoe_kamarad is None and not checkReg(kanoe_kamarad):
                            kanoe_kamarad = "X"
                        ucastnici.append(
                            {
                                "nick": nick,
                                "jmenoprijimeni": jmenoprijimeni,
                                "trida": trida,
                                "kanoe_kamarad": kanoe_kamarad,
                                "je_plavec": "Ano"
                            }
                        )
                        write_ucastnici()
                    else:
                        chyba = "Použij pouze písmena nebo čísla"
                else:
                    chyba = "Toto jméno je už použito"
            else:
                chyba = "Vyber si třídu"
        else:
            chyba = "Musíš být plavec"

        if chyba is None:
            return redirect('/')
        else:
            return render_template('registrace.html', chyba=chyba), 400



@app.route('/kontrola/<nick>', methods=['GET'])
def kontrola(val):
    safe = True
    for ucastnik in ucastnici:
        if val in ucastnik.values():
            safe = False
            break
    return str(safe)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
