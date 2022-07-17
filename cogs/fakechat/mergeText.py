from PIL import Image, ImageDraw, ImageFont
import os

async def drawText(file, textList):
    image = Image.open(file)
    image = image.convert("RGBA")

    x = image.size[0]
    y = image.size[1]
    txt = Image.new('RGBA', image.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt)
    font = ImageFont.truetype(os.getcwd() + "/cogs/fakechat/BitmapMc.ttf", size=round(y / 40))

    #黒い背景描画
    yLineAndText = y / 1.15
    addY = round(y / (y / (y / 45)))
    for text in textList:
        draw.line(xy=((0, yLineAndText), (x / 2, yLineAndText)), fill=(0, 0, 0, 160), width=round(addY * 1.3))
        draw.text((2, yLineAndText - (addY / 1.5)), text, fill=(255, 255, 255), font=font)
        yLineAndText -= round(addY * 1.25)

    combined = Image.alpha_composite(image, txt)
    filename = os.path.splitext(file)[0]
    combined.save(filename + "_fakechat.png")
    return filename + "_fakechat.png"


#textList = ["Lixy: OverKill"]
#drawText("./1.png", textList)