from flask import Flask, render_template, redirect, request, jsonify, url_for, Markup
import requests
import json
from random import choice
from string import digits
from qrtools.qrtools import QR
app = Flask(__name__)
#app = Flask(static_folder='static')


@app.route("/")
def home():
    if_person, if_test, test_type = [request.args.get("if_person"), request.args.get("if_test"), request.args.get("type")]
    
    html = '<form action="/check" method="POST"><input type="submit" value="Submit"></form>'
    return render_template('home.html', html=Markup(html), if_person=if_person, if_test=if_test, test_type=test_type)

@app.route("/check", methods=["POST"])
def check():
    if_person = True #Saved for If_person check function
    if_test = True #Saved for test regarding face is true
    test_type = "smiling"

    if [if_person, if_test] == [True, True]:
        return redirect(url_for(".checkout"))
    elif [if_person, if_test] == [False, False]:
        return redirect(url_for(".home", if_person="False", if_test="False", type=test_type))
    elif if_person is False:
        return redirect(url_for(".home", if_person="False", if_test="True", type=test_type))
    elif if_test is False:
        return redirect(url_for(".home", if_person="True", if_test="False", type=test_type))
    else:
        return redirect(url_for(".home", error="hmm"))

@app.route("/checkout")
def checkout():
    return PaymentTransfer()

#@app.route("/merchantPaymentTransfer")
def PaymentTransfer():
    url = "http://127.0.0.1:8080/merchantPaymentTransfer"
    headers = {'Content-type': 'application/json'}
    data = return_json("paymenttransfer.json")
    data["merchant_transfer"]["transfer_reference"] = "ref_{}".format(''.join(choice(digits) for i in range(10)))
    #print("------\n{}\n-------".format(data["merchant_transfer"]["transfer_reference"]))
    r = requests.post(url, data=json.dumps(data), headers=headers)
    QR_data = QRCode("static/qrcode.png")
    data = r.json()

    return render_template("checkout.html", json=data, qr=QR_data) #https://files.slack.com/files-pri/T019WDZ0A5T-F01C7PJD2F4/qr_sample_for_mastercardqr.png

def return_json(file):
    with open(file) as f:
        data = json.load(f)
    return data

def QRCode(file):
    qr = qrtools.QR()
    qr.decode(file)
    return my_QR.data

if __name__ == "__main__":
    app.run(debug=True)