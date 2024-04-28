from flask import (
    Flask, request, abort
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
    QuickReplyButton, MessageAction, LocationAction
)
from function import (
    register_for_access, save_survey_data, upload_photo_to_database,
    survey_data_information
)
import mysql.connector
import os, warnings, datetime, re, requests
from dotenv import (
    load_dotenv
)

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
def researcher_upload_function(event):
    if(event.message.type == 'image'):
        columns = '(user_id,user_name,image_path,picture_by)'
        values = f'("{event.source.user_id}","{line_bot_api.get_profile(event.source.user_id).display_name}","localhost/Ua44dad8cb61750b5c3a7bacf5d453de0","{line_bot_api.get_profile(event.source.user_id).display_name}")'
        insert_db('tempdb',columns,values)
        for columns in get_value_db('*','tempdb',f'user_id = "{event.source.user_id}"'):
            user_id = columns[1]
            user_name = columns[2]
            image_path = columns[3]
            code_farm = columns[4]
            latitude = columns[5]
            longitude = columns[6]
            disease_percent = columns[7]
            symptom = columns[8]
            picture_by = columns[9]

        line_bot_api.reply_message(
            event.reply_token,[
                FlexSendMessage(alt_text='Flex Message',contents=save_survey_data(code_farm,latitude,longitude,disease_percent,symptom,picture_by)),
                TextSendMessage(text="❗️กรุณากรอกรายละเอียดแปลงสำรวจ หากดำเนินการเสร็จสิ้นให้กด ' บันทึกข้อมูล ' ข้อมูลจะถูกอัพโหลดลงฐานข้อมูล"),
                TextSendMessage(text="🖊 ท่านสามารถเพิ่ม-แก้ไขข้อมูลได้โดยการเลือกเมนูด้านล่าง",quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="🪪Code Farm", text="Edit# Code Farm")),
                        QuickReplyButton(action=MessageAction(label="📍Location", text="Edit# Location")),
                        QuickReplyButton(action=MessageAction(label="🦠Disease Percent", text="Edit# Disease Percent")),
                        QuickReplyButton(action=MessageAction(label="💬Symptom", text="Edit# Symptom")),
                        QuickReplyButton(action=MessageAction(label="❌Clearing ", text="ล้างข้อมูล")),
                    ]
                )
                )
            ]
        )
    elif(event.message.type == 'text' and event.message.text == 'อัพโหลดข้อมูลสำรวจแปลง'):
        line_bot_api.reply_message(
            event.reply_token,[
                FlexSendMessage(alt_text='Flex Message',contents=upload_photo_to_database()),
                TextSendMessage(text="📷 หากท่านดำเนินการส่งภาพถ่ายเสร็จสิ้นแล้วกรุณากรอกรายละเอียด และดำเนินการตามขั้นตอนต่อไป"),
                TextSendMessage(text="❌ ท่านสามารถล้างข้อมูลโดยการกด ' ล้างข้อมูล ' โดยข้อมูลทั้งหมดจะไม่ถูกจัดเก็บลงฐานข้อมูล")
            ]
        )
    elif(get_value_db('*','tempdb',f'user_id = "{event.source.user_id}"') != None):
        for columns in get_value_db('*','tempdb',f'user_id = "{event.source.user_id}"'):
            user_id = columns[1]
            user_name = columns[2]
            image_path = columns[3]
            code_farm = columns[4]
            latitude = columns[5]
            longitude = columns[6]
            disease_percent = columns[7]
            symptom = columns[8]
            picture_by = columns[9]
        
        if(event.message.type == 'text' and code_farm == 'Waiting for Update...'):
            input_code_farm = event.message.text
            update_db('tempdb',f'code_farm = "{input_code_farm}"','user_id',event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,[
                    FlexSendMessage(alt_text='Flex Message',contents=save_survey_data(input_code_farm,latitude,longitude,disease_percent,symptom,picture_by)),
                    TextSendMessage(text="❗️กรุณากรอกรายละเอียดแปลงสำรวจ หากดำเนินการเสร็จสิ้นให้กด ' บันทึกข้อมูล ' ข้อมูลจะถูกอัพโหลดลงฐานข้อมูล",quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=MessageAction(label="🪪Code Farm", text="Edit# Code Farm")),
                            QuickReplyButton(action=MessageAction(label="📍Location", text="Edit# Location")),
                            QuickReplyButton(action=MessageAction(label="🦠Disease Percent", text="Edit# Disease Percent")),
                            QuickReplyButton(action=MessageAction(label="💬Symptom", text="Edit# Symptom")),
                            QuickReplyButton(action=MessageAction(label="❌Clearing ", text="ล้างข้อมูล")),
                        ]
                    )
                    )
                ]
            )
        elif(event.message.type == 'text' and event.message.text == 'บันทึกข้อมูล'):
            line_bot_api.reply_message(
                event.reply_token,[
                    FlexSendMessage(alt_text='Flex Message',contents=survey_data_information(code_farm,latitude,longitude,disease_percent,symptom,picture_by)),
                    TextSendMessage(text="บันทึกข้อมูลเสร็จสมบูรณ์ ✅"),
                    TextSendMessage(text="🖥 ท่านสามารถตรวจสอบข้อมูลผ่าน http://158.108.101.28/dashboard"),
                ]
            )
            delete_db('tempdb','user_id',event.source.user_id)
        elif(event.message.type == 'text' and event.message.text == 'ล้างข้อมูล'):
            delete_db('tempdb','user_id',event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text="ล้างข้อมูลเสร็จสิ้น ❌"),
                    TextSendMessage(text="🖥 ท่านสามารถตรวจสอบข้อมูลผ่าน http://158.108.101.28/dashboard"),
                ]
            )
        elif(event.message.type == 'text' and disease_percent == 'Waiting for Update...'):
            input_disease_percent = event.message.text
            update_db('tempdb',f'disease_percent = "{input_disease_percent}"','user_id',event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,[
                    FlexSendMessage(alt_text='Flex Message',contents=save_survey_data(code_farm,latitude,longitude,input_disease_percent,symptom,picture_by)),
                    TextSendMessage(text="❗️กรุณากรอกรายละเอียดแปลงสำรวจ หากดำเนินการเสร็จสิ้นให้กด ' บันทึกข้อมูล ' ข้อมูลจะถูกอัพโหลดลงฐานข้อมูล",quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=MessageAction(label="🪪Code Farm", text="Edit# Code Farm")),
                            QuickReplyButton(action=MessageAction(label="📍Location", text="Edit# Location")),
                            QuickReplyButton(action=MessageAction(label="🦠Disease Percent", text="Edit# Disease Percent")),
                            QuickReplyButton(action=MessageAction(label="💬Symptom", text="Edit# Symptom")),
                            QuickReplyButton(action=MessageAction(label="❌Clearing ", text="ล้างข้อมูล")),
                        ]
                    )
                    )
                ]
            )
        elif(event.message.type == 'text' and symptom == 'Waiting for Update...'):
            input_symptom = event.message.text
            update_db('tempdb',f'symptom = "{input_symptom}"','user_id',event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,[
                    FlexSendMessage(alt_text='Flex Message',contents=save_survey_data(code_farm,latitude,longitude,disease_percent,input_symptom,picture_by)),
                    TextSendMessage(text="❗️กรุณากรอกรายละเอียดแปลงสำรวจ หากดำเนินการเสร็จสิ้นให้กด ' บันทึกข้อมูล ' ข้อมูลจะถูกอัพโหลดลงฐานข้อมูล",quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=MessageAction(label="🪪Code Farm", text="Edit# Code Farm")),
                            QuickReplyButton(action=MessageAction(label="📍Location", text="Edit# Location")),
                            QuickReplyButton(action=MessageAction(label="🦠Disease Percent", text="Edit# Disease Percent")),
                            QuickReplyButton(action=MessageAction(label="💬Symptom", text="Edit# Symptom")),
                            QuickReplyButton(action=MessageAction(label="❌Clearing ", text="ล้างข้อมูล")),
                        ]
                    )
                    )
                ]
            )
        elif(event.message.type == 'location' and latitude == 'Waiting for Update...' and longitude == 'Waiting for Update...'):
            input_latitude = str(event.message.latitude)
            input_longitude = str(event.message.longitude)
            update_db('tempdb',f'latitude = "{input_latitude}"','user_id',event.source.user_id)
            update_db('tempdb',f'longitude = "{input_longitude}"','user_id',event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,[
                    FlexSendMessage(alt_text='Flex Message',contents=save_survey_data(code_farm,input_latitude,input_longitude,disease_percent,symptom,picture_by)),
                    TextSendMessage(text="❗️กรุณากรอกรายละเอียดแปลงสำรวจ หากดำเนินการเสร็จสิ้นให้กด ' บันทึกข้อมูล ' ข้อมูลจะถูกอัพโหลดลงฐานข้อมูล",quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=MessageAction(label="🪪Code Farm", text="Edit# Code Farm")),
                            QuickReplyButton(action=MessageAction(label="📍Location", text="Edit# Location")),
                            QuickReplyButton(action=MessageAction(label="🦠Disease Percent", text="Edit# Disease Percent")),
                            QuickReplyButton(action=MessageAction(label="💬Symptom", text="Edit# Symptom")),
                            QuickReplyButton(action=MessageAction(label="❌Clearing ", text="ล้างข้อมูล")),
                        ]
                    )
                    )
                ]
            )
        elif(event.message.type == 'text' and event.message.text == 'Edit# Code Farm'):
            update_db('tempdb',f'code_farm = "Waiting for Update..."','user_id',event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text='ขอทราบรหัสแปลงอันใหม่ด้วยครับ!?')
                ]
            )
        elif(event.message.type == 'text' and event.message.text == 'Edit# Location'):
            update_db('tempdb',f'latitude = "Waiting for Update..."','user_id',event.source.user_id)
            update_db('tempdb',f'longitude = "Waiting for Update..."','user_id',event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text="กรุณาแชร์ Location!?",quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=LocationAction(label="Share Location"))
                        ]
                    )
                    )
                ]
            )
        elif(event.message.type == 'text' and event.message.text == 'Edit# Disease Percent'):
            update_db('tempdb',f'disease_percent = "Waiting for Update..."','user_id',event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text="กรุณาป้อนเปอร์เซ็นความรุนแรง!?",quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=MessageAction(label="⚪25%", text="25%")),
                            QuickReplyButton(action=MessageAction(label="🟢50%", text="50%")),
                            QuickReplyButton(action=MessageAction(label="🟡75%", text="75%")),
                            QuickReplyButton(action=MessageAction(label="🔴100%", text="100%")),
                            QuickReplyButton(action=MessageAction(label="❌Clearing ", text="ล้างข้อมูล")),
                        ]
                    )
                    )
                ]
            )
        elif(event.message.type == 'text' and event.message.text == 'Edit# Symptom'):
            update_db('tempdb',f'symptom = "Waiting for Update..."','user_id',event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text='กรุณาป้อนอาการ!?')
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

def get_current_time():
    time = datetime.datetime.now()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def is_phone_number(event):
    pattern = r'^\d{3}-\d{3}-\d{4}$'
    if re.match(pattern, event.message.text):
        return True
    else:
        return False
    
def create_user_db(event):
    if(get_value_db('*','userdb',f'user_id = "{event.source.user_id}"') == None):
        columns = '(registration_time,user_id,user_name)'
        values = f'("{get_current_time()}","{event.source.user_id}","{line_bot_api.get_profile(event.source.user_id).display_name}")'
        insert_db('userdb',columns,values)
        return True
    elif(get_value_db('*','userdb',f'user_id = "{event.source.user_id}"') != None):
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
            update_db('userdb',f'phone_number = "{event.message.text}"','user_id',event.source.user_id)
            if(get_value_db('*','researcherdb',f'phone_number = "{event.message.text}"') != None):
                change_richmenu_function(event)
                update_db('userdb',f'user_role = "Researcher"','user_id',event.source.user_id)
            update_db('userdb',f'registration_status = "Registration Complete"','user_id',event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text='ลงทะเบียนการใช้งานเสร็จสมบูรณ์')
                ]
            )
            return True
        elif(is_phone_number(event) == False):
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text='กรุณาตรวจสอบการป้อนข้อมูล')
                ]
            )
            return False
    elif(registration_status == 'Not Registered' and event.message.type != 'text'):
        line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text='กรุณาตรวจสอบการป้อนข้อมูล')
                ]
        )
        return False
        
# Flask --------------------------------
app = Flask(__name__)
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
            return
        elif(get_user_role(event) == 'Researcher'):
            researcher_upload_function(event)

    if(event.message.text == 'Deactivate'): # Dev Tools
        delete_db('userdb','user_id',event.source.user_id)



@handler.add(MessageEvent,message=ImageMessage) # Image Message (Event)
def handle_image_message(event):
    if(check_registration_status(event) == True):
        if(get_user_role(event) == 'User'):
            return
        elif(get_user_role(event) == 'Researcher'):
            researcher_upload_function(event)
            return
    return

@handler.add(MessageEvent,message=LocationMessage) # Location Message (Event)
def handle_location_message(event):
    if(check_registration_status(event) == True):
        if(get_user_role(event) == 'User'):
            return
        elif(get_user_role(event) == 'Researcher'):
            researcher_upload_function(event)
            return
    return

@handler.add(MessageEvent,message=StickerMessage) # Sticker Message (Event)
def handle_sticker_message(event):
    if(check_registration_status(event) == True):
        if(get_user_role(event) == 'User'):
            return
        elif(get_user_role(event) == 'Researcher'):
            return
    return


if __name__ == '__main__':
    app.run(port=8080,debug=True)