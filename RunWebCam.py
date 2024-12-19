
from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
import numpy as np
from tkinter import simpledialog
from tkinter import filedialog
import os
import cv2
import pymysql
import time
import json
from web3 import Web3, HTTPProvider
import traceback

main = tkinter.Tk()
main.title("Certificate Verification and Validation using Blockchain") #designing main screen
main.geometry("1300x1200")

global details

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

def validateDetails(data):
    readDetails('certificate')
    arr = details.split("\n")
    flag = 0
    for i in range(len(arr)-1):
        array = arr[i].split("#")
        print(str(array[0])+" == "+data)   
        if array[0].strip() == data.strip():
            text.delete('1.0', END)
            text.update_idletasks()
            print(str(array[0])+" ****** "+data)   
            text.insert(END,'Student ID      : '+array[0]+"\n")
            text.insert(END,'Student Name    : '+array[1]+"\n")
            text.insert(END,'Course Name     : '+array[2]+"\n")
            text.insert(END,'Contact No      : '+array[3]+"\n")
            text.insert(END,'Address Details : '+array[4]+"\n")
            text.insert(END,'Date & Time     : '+array[5]+"\n")
            text.insert(END,'Certificate Signature (Hash Code) : '+array[6])
            text.update_idletasks()
            flag = 1
            break
    if flag == 0:
        text.delete('1.0', END)
        text.insert(END,"Certificate Verification Failed. QR Code does not exists")
        text.update_idletasks()

def runWebCam():
    global emp_id, present_date
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    try:
        while True:
            _, img = cap.read()
            data, bbox, _ = detector.detectAndDecode(img)
            if bbox is not None:
                for i in range(len(bbox)):
                    cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
            if data:
                validateDetails(str(data))
            cv2.imshow("QR Code Scanner", img)
            if cv2.waitKey(1) == ord("q"):
                break
    except Exception:
        traceback.print_exc()
        pass
    cap.release()
    cv2.destroyAllWindows()        
            
def exit():
    main.destroy()

font = ('times', 13, 'bold')
title = Label(main, text='Certificate Verification and Validation using Blockchain')
title.config(bg='LightGoldenrod1', fg='medium orchid')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 12, 'bold')
text=Text(main,height=20,width=100)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=480,y=100)
text.config(font=font1)


font1 = ('times', 12, 'bold')
uploadButton = Button(main, text="Start Webcam", command=runWebCam)
uploadButton.place(x=50,y=100)
uploadButton.config(font=font1)  

exitButton = Button(main, text="Exit", command=exit)
exitButton.place(x=50,y=150)
exitButton.config(font=font1) 


main.config(bg='pink')
main.mainloop()
