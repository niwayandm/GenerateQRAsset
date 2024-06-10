#!D:/Python/Python37/python.exe
# coding: utf-8

print("Content-Type: application/json")
print()

import base64
import cgi
import os
import json
import qrcode
from PIL import Image

def authenticate():
    auth_header = os.environ.get('HTTP_AUTHORIZATION')
    # print(auth_header)

    if auth_header and auth_header.startswith("Basic "):
        credential = auth_header.split(" ")[1]

        decoded_credential = base64.b64decode(credential).decode("utf-8")
        supplied_username, supplied_password = decoded_credential.split(":")

        if supplied_username == username and supplied_password == password:
            return True

    return False

username = "username"
password = "pass"

parameters = cgi.FieldStorage()
md5   = parameters.getvalue('code')
type  = parameters.getvalue('type')

authenticated = authenticate()

if authenticated and md5 and type:
    try:
        Logo_link = r'\\path\to\asset\img\fix-assets-logo.png'
        img = Image.open(Logo_link)

        # Resize the logo to the given width
        basewidth = 80
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        if 'P' in img.mode:
            logo = img.convert("RGB")
            logo = logo.resize((basewidth, hsize), resample=Image.LANCZOS,box=None)
            logo = logo.convert("P",dither=Image.NONE, palette=Image.ADAPTIVE) 
        else:
            logo = img.resize((basewidth, hsize), resample=Image.LANCZOS,box=None)
            
        if(type == 'locator'):
            pathDocker = '//path/to/asset/img/QR/Locator/'+md5+'.png'
        if(type == 'asset'):
            pathDocker = '//path/to/asset/img/QR/Asset/'+md5+'.png'
        
        # Create QR code if it doesn't exist
        if not(os.path.exists(pathDocker)):
            QRcode = qrcode.QRCode(
                version=None,
                box_size=6,
                border=3,
                error_correction=qrcode.constants.ERROR_CORRECT_H
            )
            
            # Add hashKdLocator to QRcode
            url = md5
            QRcode.add_data(url)
            QRcode.make()
            
            # Adding color to QR code
            QRimg = QRcode.make_image(
                fill_color=(0,0,0), back_color=(255,255,255))

            # Resize and paste logo to QRimg
            QRimg = QRimg.resize((330, 330), Image.NEAREST)
            pos = ((QRimg.size[0] - logo.size[0]) // 2,
                (QRimg.size[1] - logo.size[1]) // 2)
            QRimg.paste(logo, pos)

            # Save the QR code generated
            QRimg.save(pathDocker)
            response = {
                "status": "S",
                "message": "QR "+type+" image generated"
            }
        
        else:
            response = {
                "status": "E",
                "message": "Error: QR image already exist",
            }
            
    except Exception as e:
        response = {
            "status": "E",
            "message": "Error: "+str(e),
        }
        
    img.close()
else:
    response = {
        "status": "E",
        "message": "Invalid Auth",
    }
 
        
# Mengubah respon menjadi format JSON
json_response = json.dumps(response)

# Menampilkan respon dalam format JSON dengan header yang sesuai
print(json_response)

 


