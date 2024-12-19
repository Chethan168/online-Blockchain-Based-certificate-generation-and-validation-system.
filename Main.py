from flask import Flask, render_template, request, redirect, url_for, session,send_from_directory
import json
from web3 import Web3, HTTPProvider
import hashlib
from hashlib import sha256
import os
import datetime
import pyqrcode
import png
from pyqrcode import QRCode

app = Flask(__name__)

app.secret_key = 'welcome'
global uname, details, sid

def readDetails(contract_type):
    global details
    details = ""
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'CertificateVerification.json' #certification verification contract code
    deployed_contract_address = '0x1C1E0c5Ff25122BcAE9321c8bf00A8f6a1A0Db09' #hash address to access certification verification contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'company':
        details = contract.functions.getCompanyDetails().call()
    if contract_type == 'certificate':
        details = contract.functions.getCertificateDetails().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]    
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'CertificateVerification.json' #certification verification contract file
    deployed_contract_address = '0x1C1E0c5Ff25122BcAE9321c8bf00A8f6a1A0Db09' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'company':
        details+=currentData
        msg = contract.functions.setCompanyDetails(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'certificate':
        details+=currentData
        msg = contract.functions.setCertificateDetails(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', msg='')

@app.route('/Login', methods=['GET', 'POST'])
def Login():
   return render_template('Login.html', msg='')

@app.route('/AdminLogin', methods=['GET', 'POST'])
def AdminLogin():
   return render_template('AdminLogin.html', msg='')

@app.route('/AdminLoginAction', methods=['GET', 'POST'])
def AdminLoginAction():
    global uname
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        if user == "G24" and password == "g24":
            return render_template('AdminScreen.html', msg="Welcome "+user)
        else:
            return render_template('Login.html', msg="Invalid login details /n Please enter valid details")

@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    return render_template('Signup.html', msg='')

@app.route('/LoginAction', methods=['GET', 'POST'])
def LoginAction():
    global uname
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        status = "none"
        readDetails('company')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == user and array[1] == password:
                uname = user
                status = "success"
                break
        if status == "success":
            return render_template('UserScreen.html', msg="Welcome "+uname)
        else:
            return render_template('Login.html', msg="Invalid login details /n Please enter valid details")

@app.route('/ViewCertificates', methods=['GET', 'POST'])
def ViewCertificates():
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Student ID', 'Student Name', 'Course Name', 'Contact No', 'Address Details', 'Date & Time', 'Certificate Signature (Hashcode)', 'QR Code']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('certificate')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            output += "<tr><td>"+font+array[0]+"</td>"
            output += "<td>"+font+array[1]+"</td>"
            output += "<td>"+font+array[2]+"</td>"
            output += "<td>"+font+array[3]+"</td>"
            output += "<td>"+font+array[4]+"</td>"
            output += "<td>"+font+array[5]+"</td>"
            output += "<td>"+font+array[6]+"</td>"
            output+='<td><img src="/static/qrcode/'+array[0]+'.png" width="200" height="200"></img></td>'
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewCertificates.html', msg=output)         

@app.route('/ViewCompanies', methods=['GET', 'POST'])
def ViewCompanies():
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Company Username', 'Password', 'Phone No', 'Email ID', 'Company Address']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('company')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            output += "<tr><td>"+font+array[0]+"</td>"
            output += "<td>"+font+array[1]+"</td>"
            output += "<td>"+font+array[2]+"</td>"
            output += "<td>"+font+array[3]+"</td>"
            output += "<td>"+font+array[4]+"</td>"            
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewCertificates.html', msg=output) 
        
        
@app.route('/SignupAction', methods=['GET', 'POST'])
def SignupAction():
    if request.method == 'POST':
        global details
        uname = request.form['t1']
        password = request.form['t2']
        phone = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        status = "none"
        readDetails('company')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == uname:
                status = uname+" Username already exists"
                break
        if status == "none":
            data = uname+"#"+password+"#"+phone+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"company")
            context = "Company signup task completed"
            return render_template('Signup.html', msg=context)
        else:
            return render_template('Signup.html', msg=status)

@app.route('/Logout')
def Logout():
    return render_template('index.html', msg='')

@app.route('/AddCertificate', methods=['GET', 'POST'])
def AddCertificate():
   return render_template('AddCertificate.html', msg='')

@app.route('/DownloadAction', methods=['GET', 'POST'])
def DownloadAction():
    if request.method == 'POST':
        global sid
        print("===="+sid)
        return send_from_directory('static/qrcode/', sid+'.png', as_attachment=True)

def checkID(student_id):
    readDetails('certificate')
    arr = details.split("\n")
    flag = False
    for i in range(len(arr)-1):
        array = arr[i].split("#")
        if array[0] == student_id:
            flag = true
            break
    return flag  
    

@app.route('/AddCertificateAction', methods=['GET', 'POST'])
def AddCertificateAction():
    if request.method == 'POST':
        global sid
        sid = request.form['t1']
        sname = request.form['t2']
        course = request.form['t3']
        contact = request.form['t4']
        address = request.form['t5']
        certificate = request.files['t6']
        contents = certificate.read()
        current_time = datetime.datetime.now()
        flag = checkID(sid)
        if flag == False:
            digital_signature = sha256(contents).hexdigest();
            url = pyqrcode.create(sid)
            url.png('static/qrcode/'+sid+'.png', scale = 6)
            data = sid+"#"+sname+"#"+course+"#"+contact+"#"+address+"#"+str(current_time)+"#"+digital_signature+"\n"
            saveDataBlockChain(data,"certificate")
            context = "Certificate details added with id : "+sid+"<br/>Generated Digital Signatures : "+digital_signature+"<br/>Download QR CODE"
            return render_template('Download.html', msg=context)
        else:
            context = "Given "+sid+"already exists"
            return render_template('Download.html', msg=context)
        
@app.route('/AuthenticateScan', methods=['GET', 'POST'])
def AuthenticateScan():
   return render_template('AuthenticateScan.html', msg='')


@app.route('/AuthenticateScanAction', methods=['GET', 'POST'])
def AuthenticateScanAction():
    if request.method == 'POST':
        barcode = request.files['t1']
        contents = barcode.read()
        digital_signature = sha256(contents).hexdigest();
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Student ID', 'Student Name', 'Course Name', 'Contact No', 'Address Details', 'Date & Time', 'Certificate Signature (Hash Code)', 'Status']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('certificate')
        arr = details.split("\n")
        flag = 0
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[6] == digital_signature:
                flag = 1
                output += "<tr><td>"+font+array[0]+"</td>"
                output += "<td>"+font+array[1]+"</td>"
                output += "<td>"+font+array[2]+"</td>"
                output += "<td>"+font+array[3]+"</td>"
                output += "<td>"+font+array[4]+"</td>"
                output += "<td>"+font+array[5]+"</td>"
                output += "<td>"+font+array[6]+"</td>"
                output += "<td>"+font+"Authentication Successfull"+"</td>"
        if flag == 0:
            output += "<tr><td>Uploaded Certificate Authentication Failed</td></tr>"
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewDetails.html', msg=output)


if __name__ == '__main__':
    app.run()










