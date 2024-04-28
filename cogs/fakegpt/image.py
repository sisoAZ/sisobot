import io
import os
from PIL import Image, ImageDraw, ImageFont

items_path = os.getcwd() + "/files/gpt/"

def generate(user_text, gpt_text, output_path="output.png", user_name="You", user_image=None):
    # Create a blank image with a white background
    base = Image.new('RGB', (800, 600), color = (255, 255, 255))
    base_layer = Image.open(items_path + "base.png")
    base.paste(base_layer, (0, 0))

    #username and image
    #user_image = Image.open(user_image)
    user_image = user_image.resize((40, 40))

    base.paste(user_image, (44, 30))

    font = ImageFont.truetype(items_path + "NotoSansJP-Bold.ttf", 30)
    d = ImageDraw.Draw(base)
    d.text((100,25), user_name, fill=(255,255,255), font=font)

    # Draw the text

    font = ImageFont.truetype(items_path + "NotoSansJP-Regular.ttf", 20)
    d = ImageDraw.Draw(base)
    text_list = split_text(d, user_text, font)
    for i, text in enumerate(text_list):
        d.text((100, 80 + i * 30), text, fill=(255,255,255), font=font)
    #GPT side
    text_list = split_text(d, gpt_text, font)
    for i, text in enumerate(text_list):
        d.text((100, 370 + i * 30), text, fill=(255,255,255), font=font)
    
    byte_arr = io.BytesIO()
    base.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    return byte_arr

def split_text(draw_obj: ImageDraw.ImageDraw, text, font):
    split_text_list = []
    split_text = ""
    for i in range(0, len(text), 5):
        temp_text = split_text + text[i:i+5]
        text_length = draw_obj.textlength(temp_text, font=font)
        if text_length >= 618:
            split_text_list.append(split_text)
            split_text = text[i:i+5]
        else:
            split_text = temp_text
    split_text_list.append(split_text)
    return split_text_list
