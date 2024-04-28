from __future__ import unicode_literals
import unicodedata
from flask import (
    Flask, request, abort,
    send_from_directory
)
from werkzeug.middleware.proxy_fix import (
    ProxyFix
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage,
    LocationMessage, StickerMessage, FollowEvent,
    TextSendMessage, FlexSendMessage, QuickReply,
    QuickReplyButton, MessageAction, LocationAction,
    ImageSendMessage
)
from function import (
    register_for_access, save_survey_data, upload_photo_to_database,
    survey_data_information, create_image_carousel, create_image_carousel_second,
    photo_guide
)
import mysql.connector
import os, warnings, datetime, re, requests
from dotenv import (
    load_dotenv
)

# KU - KPS Library Requirement -------
from werkzeug.middleware.proxy_fix import ProxyFix
from utils.plots import (
    Annotator, colors
)
from pathlib import Path
import os, sys, cv2, torch, base64, errno, tempfile
from flask import (
    send_from_directory
)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
from PIL import Image
import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np
import torch.nn as nn
from torch.nn import functional as F

### YOLOv5 ###
# Setup
# weights, view_img, save_txt, imgsz = 'yolov5s.pt', False, False, 640
conf_thres = 0.6 
iou_thres = 0.45
classes = None
agnostic_nms = False
save_conf = False
save_img = True
line_thickness = 3

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')



# Load model
model = torch.hub.load('./', 'custom', path='best.pt', source='local', force_reload=True)
model.conf = 0.4
#--------------------CNN-----------------#
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
data_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
modelCNN = models.resnet50(weights=None).to(device)
modelCNN.fc = nn.Sequential(
               nn.Linear(2048, 128),
               nn.ReLU(inplace=True),
               nn.Linear(128, 2)).to(device)
modelCNN.load_state_dict(torch.load('./models/weights.h5', map_location=torch.device('cpu'))) #แก้path weight ด้วย
modelCNN.eval()

# Turn OFF Warning ---------------------
warnings.filterwarnings('ignore')

# Load environment from .env file ------
load_dotenv()

# Authorization API Key ----------------
line_bot_api = LineBotApi(os.getenv('channel_access_token'))
handler = WebhookHandler(os.getenv('channel_secret'))

# SQL Function -------------------------
def active_db(): # Active Database 
    db = mysql.connector.connect(host="127.0.0.1",
                                       user="root",
                                       password="",
                                       database="chatbotdb")
    return db

def insert_db(table_name,columns,values): # Add Data To Database | Query -> INSERT INTO (Table Name) (Columns) VALUES (Values)
    db = active_db()
    mycursor = db.cursor()
    SQL = f"INSERT INTO {table_name} {columns} VALUES {values}"
    mycursor.execute(SQL)
    db.commit()
    mycursor.close()
    db.close()

def delete_db(table_name,columns_first,values_first): # Dev Tools
    db = active_db()
    mycursor = db.cursor()
    SQL = f"DELETE FROM {table_name} WHERE {columns_first} = '{values_first}'"
    mycursor.execute(SQL)
    db.commit()
    mycursor.close()
    db.close()

def get_value_db(columns,table_name,condition):  # Fetch Data From Database | Query -> SELECT (Columns) FROM (Table Name) WHERE (Condition)
    db = active_db()
    mycursor = db.cursor()
    SQL = f'SELECT {columns} FROM {table_name} WHERE {condition}'
    mycursor.execute(SQL)
    data_from_db = mycursor.fetchall()
    db.commit()
    mycursor.close()
    db.close()
    if not data_from_db:
        return None
    return data_from_db

def update_db(table_name, command, column_index_first, column_val_first):
    db = active_db()
    mycursor = db.cursor()
    SQL = f"UPDATE {table_name} SET {command} WHERE {column_index_first} = '{column_val_first}'"
    mycursor.execute(SQL)
    db.commit()
    mycursor.close()
    db.close()

# Chatbot Function ---------------------
def get_current_time():
    time = datetime.datetime.now()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def create_user_db(event):
    if(get_value_db('*','userdb',f'user_id = "{event.source.user_id}"') == None):
        columns = '(registration_time,user_id,user_name)'
        values = f'("{get_current_time()}","{event.source.user_id}","{line_bot_api.get_profile(event.source.user_id).display_name}")'
        insert_db('userdb',columns,values)
        return True
    elif(get_value_db('*','userdb',f'user_id = "{event.source.user_id}"') != None):
        return False

def is_phone_number(event):
    pattern = r'^\d{3}-\d{3}-\d{4}$'
    if re.match(pattern, event.message.text):
        return True
    else:
        return False
    
def check_registration_status(event):
    for columns in get_value_db('*','userdb',f'user_id = "{event.source.user_id}"'):
        registration_time = columns[1]
        user_id = columns[2]
        user_name = columns[3]
        registration_status = columns[4]
        user_role = columns[5]
        phone_number = columns[6]
    if(registration_status == 'Registration Complete'):
        return True
    elif(registration_status == 'Not Registered' and event.message.type == 'text'):
        if(is_phone_number(event) == True):
            update_db('userdb',f'registration_status = "Registration Complete"','user_id',event.source.user_id)
            update_db('userdb',f'phone_number = "{event.message.text}"','user_id',event.source.user_id)
            if(get_value_db('*','researcherdb',f'phone_number = "{event.message.text}"') != None):
                #change_richmenu_function(event)
                update_db('userdb',f'user_role = "Researcher"','user_id',event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text='✅ ลงทะเบียนการใช้งานเสร็จสมบูรณ์'),
                    TextSendMessage(text='ท่านสามารถเข้าใช้งานฟังก์ชั่นของแชทบอทได้ในเมนูด้านล่าง 📝')
                ]
            )
            return True
        elif(is_phone_number(event) == False):
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text='❗กรุณาตรวจสอบการป้อนข้อมูล'),
                    TextSendMessage(text="📱 ตัวอย่างการป้อนข้อมูล 08X-XXX-XXXX (จำเป็นต้องมี '-')")
                ]
            )
            return False
    elif(registration_status == 'Not Registered' and event.message.type != 'text'):
        line_bot_api.reply_message(
            event.reply_token,[
                TextSendMessage(text='❗กรุณาตรวจสอบการป้อนข้อมูล'),
                TextSendMessage(text="📱 ตัวอย่างการป้อนข้อมูล 08X-XXX-XXXX (จำเป็นต้องมี '-')")
            ]
        )
        return False
    
def photo_guide_function(event):
    line_bot_api.reply_message(
        event.reply_token,[
            FlexSendMessage(alt_text='💬คู่มือการถ่ายภาพ',contents=photo_guide()),
            create_image_carousel_second(),
            create_image_carousel()
        ]
        )
    
def send_image_predict_disease(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text='📷 สามารถดำเนินการส่งรูปภาพใบยางได้เลยครับ')
        ]
        )

def menu_default(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text='❌ ฟังก์ชั่นนี้ยังไม่ถูกเปิดใช้งาน ขออภัยในความไม่สะดวก')
        ]
        )

def ask_question(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text='❌ ฟังก์ชั่นนี้ยังไม่ถูกเปิดใช้งาน ขออภัยในความไม่สะดวก')
        ]
        )
    
def get_user_role(event):
    for columns in get_value_db('*','userdb',f'user_id = "{event.source.user_id}"'):
        user_role = columns[5]
    return user_role

def change_richmenu_function(event):
    url = f'https://api.line.me/v2/bot/user/{event.source.user_id}/richmenu/richmenu-8e012f4047b24f01b9e137db648f5969'
    headers = {
        'Authorization': 'Bearer ' + os.getenv('channel_access_token')
    }
    response = requests.post(url, headers=headers)

# Flask --------------------------------
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)

@app.route('/',methods=['GET'])
def default():
    return 'Hello World!'

@app.route("/callback",methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except Exception as error:
        print(error)
        abort(400)
    return 'OK', 200

@handler.add(FollowEvent)
def handle_add_user(event):
    if(create_user_db(event) == True):
        line_bot_api.reply_message(
            event.reply_token,[
                TextSendMessage(text="ยินดีตอบทุกข้อสงสัยของท่าน ส่งข้อความหาเราได้เลยน้า เริ่มต้นการใช้งาน กรุณากด ' เข้าใช้งาน ' บน Yangbot Menu"),
                FlexSendMessage(alt_text='Flex Message',contents=register_for_access())
            ]
        )
    elif(create_user_db(event) == False):
        line_bot_api.reply_message(
            event.reply_token,[
                TextSendMessage(text="ยินดีตอบทุกข้อสงสัยของท่าน ส่งข้อความหาเราได้เลยน้า เริ่มต้นการใช้งาน กรุณากด ' เข้าใช้งาน ' บน Yangbot Menu")
            ]
        )

@handler.add(MessageEvent,message=TextMessage) # Text Message (Event)
def handle_text_message(event):
    if(check_registration_status(event) == True):
        if(get_user_role(event) == 'User'):
            user_message = event.message.text
            user_name = line_bot_api.get_profile(event.source.user_id).display_name
            if(user_message =='✨สอบถามข้อมูลโรคใบยาง'):
                ask_question(event)
            if(user_message =='🎈เมนูเข้าใช้งาน "น้องใบยาง"'):
                menu_default(event)
            if(user_message =='📷ส่งรูปภาพวิเคราะห์โรค'):
                send_image_predict_disease(event)
            if(user_message == '💬คู่มือการถ่ายภาพ'):
                photo_guide_function(event)
        elif(get_user_role(event) == 'Researcher'):
            return

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    if(check_registration_status(event) == True):
        if(get_user_role(event) == 'User'):
            message_content = line_bot_api.get_message_content(event.message.id)
            with tempfile.NamedTemporaryFile(delete=False, dir='static/tmp', suffix='.jpg') as temp_file:
                for chunk in message_content.iter_content():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            # Rename Temporary File in 'tmp' Folder
            new_filename = f'{line_bot_api.get_profile(event.source.user_id).display_name}_{event.timestamp}.jpg'
            distination_path = os.path.join('static/tmp', new_filename)
            os.rename(temp_file_path, distination_path)

            # Get Image File
            image_file = open(distination_path, "rb")
            original_image = cv2.imread(image_file)

            image = Image.open(distination_path).convert('RGB')
            ####--------------------------------DO CNN NT , T--------------------------------###
            img_preprocessed = data_transform(image).unsqueeze(0)
            #modelCNN.eval()
            out = modelCNN(img_preprocessed.to(device))
            pred_probs = F.softmax(out, dim=1).cpu().data.numpy()
            answer = np.argmax(pred_probs, axis=1)
            if answer == 0:
                line_bot_api.reply_message(
                    event.reply_token,[
                        TextSendMessage(text='❌ ภาพนี้ไม่ใช่ภาพใบยาง\nโปรดตรวจสอบและทำการส่งใหม่อีกครั้ง')
                    ]
                )
            elif answer == 1:
                # Save Image to Input Folder
                cv2.imwrite(f'static/images/input/' + new_filename, original_image)
                image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
                results = model(image, size=640)
                annotator = Annotator(original_image, line_width=line_thickness)
                Confidence_Healthy = 0
                Confidence_Disease = 0
                Confidence_Other = 0
                df = results.pandas().xyxy[0]
                for idx, r in df.iterrows():
                    c = int(r['class'])  # integer class
                    name = r['name']
                    label = f'{name} {r.confidence:.2f}'
                    confidence = round(r.confidence * 100)
                    annotator.box_label((r.xmin, r.ymin, r.xmax, r.ymax), label, color=colors(c, True))
                    if name == "Healthy":
                        nameth = 'สุขภาพดี'
                        Confidence_Healthy = max(confidence,Confidence_Healthy)
                    elif name == "Disease":
                        nameth =  'โรคใบร่วงอุบัติชนิดใหม่' 
                        Confidence_Disease = max(confidence,Confidence_Disease)
                    elif name == "Other Disease":
                        nameth = 'โรคอื่นๆ'
                        Confidence_Other = max(confidence,Confidence_Other)

                message = '📷 ผลการจำแนก:\n'
                if Confidence_Disease > 0:
                    message += f"โรคใบร่วงชนิดใหม่ ค่าความมั่นใจ {Confidence_Disease}%"

                if Confidence_Other > 0:
                    message += f"โรคอื่นๆ ค่าความมั่นใจ {Confidence_Other}%"    

                if Confidence_Healthy > 0 and Confidence_Disease == 0 and Confidence_Other == 0:
                    message += f"สุขภาพดี ค่าความมั่นใจ {Confidence_Healthy}%"

                if Confidence_Disease == 0 and Confidence_Other == 0 and Confidence_Healthy == 0:
                    message += "ไม่สามารถจำแนกได้ กรุณาศึกษาคู่มือการถ่ายภาพ"
                
                save_path = str('static/images/output/' +f"{line_bot_api.get_profile(event.source.user_id).display_name}_{event.timestamp}_test.jpg") 
                cv2.imwrite(save_path, original_image) # Save Label Image
                url = request.url_root + '/' + save_path 
                line_bot_api.reply_message(
                    event.reply_token,[
                    ImageSendMessage(url, url),
                    TextSendMessage(text=message)]
                )
            os.remove(distination_path)
            # Call User API Here
            url = 'https://example.com/api/endpoint'


            #
        elif(get_user_role(event) == 'Researcher'):
            return
        
@handler.add(MessageEvent,message=LocationMessage) # Location Message (Event)
def handle_location_message(event):
    if(check_registration_status(event) == True):
        if(get_user_role(event) == 'User'):
            return
        elif(get_user_role(event) == 'Researcher'):
            return


@handler.add(MessageEvent,message=StickerMessage) # Sticker Message (Event)
def handle_sticker_message(event):
    if(check_registration_status(event) == True):
        if(get_user_role(event) == 'User'):
            return
        elif(get_user_role(event) == 'Researcher'):
            return
    
if __name__ == '__main__':
    app.run(port=8080,debug=True)