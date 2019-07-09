import fc
import json
from flask import Flask, render_template, request,send_from_directory
from werkzeug.utils import secure_filename
from flask import jsonify
from flask import Response
import qrcode_qpi as qr
import time
from random import randint
import db_helper as db
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER']='data/uploads/'

@app.route('/upload')
def home():
   return render_template('/upload.html')
	


def registerImage(image):
   resp= dict()
   try:
      qr_code="data/"+qr.generateQrCode()
      unique_id=randint(99999,1000000)
      image.filename="img_"+str(unique_id)+".png"
      tempImage=image
      encodings=fc.getEncodings(tempImage)
      fileName=secure_filename(image.filename)
      imageFilePath="/data/uploads"+str(image.filename)
      image.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
      #db.insertIntoFcr(enc=encodings.tolist(),img_path=imageFilePath,qr_code=qr_code,unique_id=unique_id)
      resp['image']=imageFilePath
      resp['qr']=qr_code
      resp['unique_id']=unique_id
      resp['error']="None"
      return resp
   except Exception as e:
      print("inside register image")
      print(e)
      resp['error']=str(e)
      return resp

@app.route('/uploader', methods = ['POST'])
def upload_file():
   print("Inside upload method")
   resp=dict()
   if request.method == 'POST':
      try:
         checkImage = request.files['check']
         verifyImage = request.files['verify']
         if checkImage== None or verifyImage==None:
          resp['Message']="Please provide valid images."  
          return Response(json.dumps(resp),mimetype="application/json",status=403)
         startTime=time.time()
         #resp['Message']=str(fc.checkImage(checkImage,verifyImage)[0])
         resp=registerImage(checkImage)
         endTime=time.time()
         print(endTime-startTime)
         checkImage.close()
         verifyImage.close()
         return Response(json.dumps(resp),mimetype="application/json",status=200)
      except Exception as e:
         print(e)
         resp['Message']="There is some exception "+str(e)
         return Response(json.dumps(resp),mimetype="application/json",status=500)



@app.route('/verify', methods = ['GET'])
def verifyImagePage():
   return render_template('/verify.html')

@app.route('/verify', methods = ['POST'])
def checkImage():
   print("Inside upload method")
   resp=dict()
   if request.method == 'POST':
      try:
         checkImage = request.files['check']
         if checkImage== None:
          resp['Message']="Please provide valid images."  
          return Response(json.dumps(resp),mimetype="application/json",status=403)
         rows=fc.verifyImage(checkImage)
         return Response(json.dumps(rows),mimetype="application/json",status=200)
      except Exception as e:
         resp['Message']="There is some exception "+str(e)
         return Response(json.dumps(resp),mimetype="application/json",status=500)


@app.route('/qrcode')
def getQrCodePath():
   resp= dict()
   try:
      resp['Message']="data/%s" %(qr.generateQrCode())
      return Response(json.dumps(resp),mimetype="application/json",status=200)
   except Exception as e:
      print(e)
      resp['Message']="There was some error"
      return Response(json.dumps(resp),mimetype="application/json",status=500)


@app.route('/data/<path:filepath>')
def getQrCode(filepath):
   return send_from_directory('data', filepath)
   

   
if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8080,debug = True)
