from flask import Flask, render_template, redirect, request, jsonify, url_for, Markup
import requests
app = Flask(__name__)

partner_id = "partnerId = ptnr_1lzs0zD6uWo7k-OdUXjLW_pFgX3"
PaymentTransferJson = {}

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
    PaymentTransfer()
    return "Template for verification is successful"

#@app.route("/merchantPaymentTransfer")
def PaymentTransfer():
    if PaymentTransferJson == {}:
        url = "https://sandbox.api.mastercard.com/send/static/v1/partners/{}/merchant/transfers/payment".format(partner_id)
        r = requests.get(url)
        print(r.status_code)



if __name__ == "__main__":
    app.run(debug=True)