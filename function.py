from linebot.models import (
    ImageCarouselColumn, ImageCarouselTemplate,
    TemplateSendMessage, URIAction, CameraAction
)
def register_for_access():
    flex_template = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://github.com/waterontheway/yb_chatbot_resource/blob/main/register_for_access.png?raw=True",
        "size": "full",
        "aspectRatio": "18:6",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "label": "Line",
        "uri": "https://linecorp.com/"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "ลงทะเบียนด้วยเบอร์มือถือ",
                "weight": "bold",
                "size": "lg",
                "align": "center",
                "contents": []
            },
            {
                "type": "text",
                "text": "ตัวอย่างการป้อนข้อมูล",
                "color": "#929292FF",
                "align": "center",
                "margin": "sm",
                "contents": []
            },
            {
                "type": "text",
                "text": "08X-XXX-XXXX",
                "size": "md",
                "color": "#929292FF",
                "align": "center",
                "margin": "sm",
                "contents": []
            }
            ]
        }
        ]
    }
    }
    return flex_template

def save_survey_data(code_farm,latitude,longitude,disease_percent,symptom,picture_by):
    flex_template = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://github.com/waterontheway/yb_chatbot_resource/blob/main/save_survey_data.png?raw=True",
        "size": "full",
        "aspectRatio": "18:6",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "label": "Line",
        "uri": "https://linecorp.com/"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "margin": "none",
            "contents": [
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "Code Farm",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "flex": 2,
                    "contents": []
                },
                {
                    "type": "text",
                    "text": code_farm,
                    "size": "sm",
                    "color": "#666666",
                    "flex": 5,
                    "wrap": True,
                    "contents": []
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "Latitude",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "flex": 2,
                    "contents": []
                },
                {
                    "type": "text",
                    "text": latitude,
                    "size": "sm",
                    "color": "#666666",
                    "flex": 5,
                    "wrap": True,
                    "contents": []
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "Longitude",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "flex": 2,
                    "contents": []
                },
                {
                    "type": "text",
                    "text": longitude,
                    "size": "sm",
                    "color": "#666666",
                    "flex": 5,
                    "wrap": True,
                    "contents": []
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "Disease Percent",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "flex": 4,
                    "contents": []
                },
                {
                    "type": "text",
                    "text": disease_percent,
                    "size": "sm",
                    "color": "#666666",
                    "flex": 5,
                    "wrap": True,
                    "contents": []
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "Symptom",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "flex": 2,
                    "contents": []
                },
                {
                    "type": "text",
                    "text": symptom,
                    "size": "sm",
                    "color": "#666666",
                    "flex": 5,
                    "wrap": True,
                    "contents": []
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "Picture By",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "flex": 2,
                    "contents": []
                },
                {
                    "type": "text",
                    "text": picture_by,
                    "size": "sm",
                    "color": "#666666",
                    "flex": 5,
                    "wrap": True,
                    "contents": []
                }
                ]
            }
            ]
        }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "flex": 0,
        "spacing": "sm",
        "contents": [
        {
            "type": "button",
            "action": {
            "type": "message",
            "label": "บันทึกข้อมูล",
            "text": "บันทึกข้อมูล"
            },
            "color": "#3E6244",
            "style": "primary"
        }
        ]
    }
    }
    return flex_template

def upload_photo_to_database():
    flex_template = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://github.com/waterontheway/yb_chatbot_resource/blob/main/upload_photo_to_database.png?raw=True",
        "size": "full",
        "aspectRatio": "18:6",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "label": "Line",
        "uri": "https://linecorp.com/"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "โปรดส่งรูปภาพที่ต้องการเก็บข้อมูล",
            "weight": "regular",
            "color": "#000000FF",
            "align": "center",
            "contents": []
        },
        {
            "type": "text",
            "text": "MIN. 1 - MAX. 10",
            "weight": "regular",
            "color": "#AAAAAAFF",
            "align": "center",
            "margin": "sm",
            "wrap": True,
            "contents": []
        }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "flex": 0,
        "spacing": "sm",
        "contents": [
        {
            "type": "button",
            "action": {
            "type": "message",
            "label": "ล้างข้อมูล",
            "text": "ล้างข้อมูล"
            },
            "color": "#3E6244",
            "style": "primary"
        }
        ]
    }
    }
    return flex_template

def survey_data_information(code_farm,latitude,longitude,disease_percent,symptom,picture_by):
    flex_template = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://github.com/waterontheway/yb_chatbot_resource/blob/main/survey_data_information.png?raw=True",
        "size": "full",
        "aspectRatio": "18:6",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "label": "Line",
        "uri": "https://linecorp.com/"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "margin": "none",
            "contents": [
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "Code Farm",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "flex": 2,
                    "contents": []
                },
                {
                    "type": "text",
                    "text": code_farm,
                    "size": "sm",
                    "color": "#666666",
                    "flex": 5,
                    "wrap": True,
                    "contents": []
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "Latitude",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "flex": 2,
                    "contents": []
                },
                {
                    "type": "text",
                    "text": latitude,
                    "size": "sm",
                    "color": "#666666",
                    "flex": 5,
                    "wrap": True,
                    "contents": []
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "Longitude",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "flex": 2,
                    "contents": []
                },
                {
                    "type": "text",
                    "text": longitude,
                    "size": "sm",
                    "color": "#666666",
                    "flex": 5,
                    "wrap": True,
                    "contents": []
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "Disease Percent",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "flex": 4,
                    "contents": []
                },
                {
                    "type": "text",
                    "text": disease_percent,
                    "size": "sm",
                    "color": "#666666",
                    "flex": 5,
                    "wrap": True,
                    "contents": []
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "Symptom",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "flex": 2,
                    "contents": []
                },
                {
                    "type": "text",
                    "text": symptom,
                    "size": "sm",
                    "color": "#666666",
                    "flex": 5,
                    "wrap": True,
                    "contents": []
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "Picture By",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "flex": 2,
                    "contents": []
                },
                {
                    "type": "text",
                    "text": picture_by,
                    "size": "sm",
                    "color": "#666666",
                    "flex": 5,
                    "wrap": True,
                    "contents": []
                }
                ]
            }
            ]
        }
        ]
    }
    }
    return flex_template

def create_image_carousel():
    image_carousel_template = ImageCarouselTemplate(columns=[
        ImageCarouselColumn(image_url='https://github.com/waterontheway/yb_chatbot_resource/blob/main/true_1_full.png?raw=true',
                             action=CameraAction(label='📷 ถ่ายภาพ')),
        ImageCarouselColumn(image_url='https://github.com/waterontheway/yb_chatbot_resource/blob/main/false_1_full.png?raw=true',
                             action=CameraAction(label='📷 ถ่ายภาพ')),
        ImageCarouselColumn(image_url='https://github.com/waterontheway/yb_chatbot_resource/blob/main/true_2_full.png?raw=true',
                             action=CameraAction(label='📷 ถ่ายภาพ')),
        ImageCarouselColumn(image_url='https://github.com/waterontheway/yb_chatbot_resource/blob/main/false_2_full.png?raw=true',
                             action=CameraAction(label='📷 ถ่ายภาพ'))

    ])
    template_message = TemplateSendMessage(alt_text='Image Carousel', template=image_carousel_template)
    return template_message

def create_image_carousel_second():
    image_carousel_template = ImageCarouselTemplate(columns=[
        ImageCarouselColumn(image_url='https://github.com/waterontheway/yb_chatbot_resource/blob/main/true_1_blur.png?raw=true',
                             action=CameraAction(label='📷 ถ่ายภาพ')),
        ImageCarouselColumn(image_url='https://github.com/waterontheway/yb_chatbot_resource/blob/main/false_1_blur.png?raw=true',
                             action=CameraAction(label='📷 ถ่ายภาพ')),
        ImageCarouselColumn(image_url='https://github.com/waterontheway/yb_chatbot_resource/blob/main/true_2_blur.png?raw=true',
                             action=CameraAction(label='📷 ถ่ายภาพ')),
        ImageCarouselColumn(image_url='https://github.com/waterontheway/yb_chatbot_resource/blob/main/false_2_blur.png?raw=true',
                             action=CameraAction(label='📷 ถ่ายภาพ'))

    ])
    template_message = TemplateSendMessage(alt_text='Image Carousel', template=image_carousel_template)
    return template_message

def photo_guide():
    flex_template = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://github.com/waterontheway/yb_chatbot_image/blob/main/photo_guide_func.png?raw=true",
        "size": "full",
        "aspectRatio": "18:6",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "label": "Line",
        "uri": "https://linecorp.com/"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "คู่มือการถ่ายภาพ",
                "weight": "bold",
                "size": "lg",
                "align": "start",
                "decoration": "underline",
                "contents": []
            },
            {
                "type": "text",
                "text": "ลักษณะของภาพถ่ายที่เหมาะสมมีดังนี้",
                "size": "md",
                "color": "#000000FF",
                "align": "start",
                "margin": "xs",
                "contents": []
            },
            {
                "type": "text",
                "text": "1. ภาพควรชัดเจน (ไม่เบลอ)",
                "size": "md",
                "color": "#000000FF",
                "align": "start",
                "contents": []
            },
            {
                "type": "text",
                "text": "2. ภาพควรเห็นเต็มใบ",
                "color": "#000000FF",
                "contents": []
            }
            ]
        },
        {
            "type": "text",
            "text": "ตัวอย่างภายถ่ายที่เหมาะสม / ตัวอย่างภาพถ่ายที่ไม่เหมาะสม ดูได้ด้านล่าง",
            "color": "#A0A0A0FF",
            "margin": "sm",
            "wrap": True,
            "contents": []
        }
        ]
    }
    }
    return flex_template