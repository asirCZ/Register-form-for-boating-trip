from flask import Flask, render_template, request, redirect
import re
import os
import json

# Initialize Flask application
app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# Initialize list to store participants' information
participants = []

# Path to the JSON file storing participants' information
file_path_participants = "participants.json"

# On start, load all users from the file (if it exists)
try:
    # Check if the file exists and has a size greater than or equal to 5 bytes
    if os.path.getsize(file_path_participants) >= 5:
        with open(file_path_participants, "r") as json_file:
            # Load participants from the file
            participants = json.load(json_file)
except FileNotFoundError:
    # If the file is not found, start with an empty list
    print(f"File path not found. Starting with an empty list.")


def write_participants():
    """
    Write participants' information to the JSON file.
    """
    with open(file_path_participants, "w") as json_file:
        json.dump(participants, json_file)


def check_reg(val):
    """
    Check if the given string matches the specified regex pattern.

    :param val: The string to be checked.
    :return: True if the string matches the pattern, False otherwise.
    """
    if val is not None:
        if re.match(r'^[a-zA-Z\u00C0-\u017F\s]+$', val):
            return True
        else:
            return False


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Render the home page with participants' information.
    """
    return render_template('index.html', participants=participants), 200


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    """
    Handle participant registration.

    :return: Redirect to the home page on success, render the registration form with an error message on failure.
    """
    chyba = None
    if request.method == 'GET':
        # Render the registration form for GET requests
        return render_template('registration.html'), 200
    elif request.method == 'POST':
        # Handle form submission for POST requests
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
                    if check_reg(name):
                        if friend is None and not check_reg(friend):
                            friend = "X"

                        # Add participant to the list
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
                        # Write participants to the file
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
            # Redirect to the home page on success
            return redirect('/')
        else:
            # Render the registration form with an error message on failure
            return render_template('registration.html', chyba=chyba), 400


@app.route('/table', methods=['GET', 'POST'])
def table():
    """
    Render the participant table.

    :return: Render the table for GET requests, render the table with participants on successful login, render the table with an error message on unsuccessful login.
    """
    if request.method == 'GET':
        return render_template('table.html'), 200
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')

        ok = False
        # Check if the entered email and password match any participant
        for p in participants:
            if p['email'] == email and p['pass'] == password:
                ok = True

        if ok:
            # Render the table with participants on successful login
            return render_template('table.html', participants=participants), 200
        else:
            # Render the table with an error message on unsuccessful login
            return render_template('table.html'), 400


@app.route('/nickcheck/<nick>', methods=['GET'])
def nickcheck(val):
    """
    Check the availability of a nickname.

    :param val: The nickname to be checked.
    :return: True if the nickname is available, False otherwise.
    """
    safe = True
    for p in participants:
        if val.lower() in p["name"].lower():
            safe = False
            break
    return str(safe)


if __name__ == '__main__':
    """
    Run the Flask application.
    """
    app.run(host='0.0.0.0', port=8080)
