from flask import Flask, render_template, request
import re

ucastnici = []

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
    if request.method == 'POST':
        nick = request.form.get('nick')
        kanoe_kamarad = request.form.get('kanoe_kamarad')
        je_plavec = request.form.get('je_plavec')

        if je_plavec:
            if checkReg(nick):
                if kanoe_kamarad is None and not checkReg(kanoe_kamarad):
                    kanoe_kamarad = "-"
                ucastnici.append(
                    {
                        "nick": nick,
                        "kanoe_kamarad": kanoe_kamarad,
                        "je_plavec": "Ano"
                    }
                )
            else:
                chyba = "Použij pouze písmena nebo čísla"
        else:
            chyba = "Musíš být plavec"

        if not je_plavec and not checkReg(nick):
            return render_template('registrace.html', chyba=chyba), 400

    return render_template('registrace.html'), 200



@app.route('/kontrola/<nick>', methods=['GET'])
def kontrola(nick):
    safe = True
    for ucastnik in ucastnici:
        if nick in ucastnik.values():
            safe = False
            break
    return str(safe)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
