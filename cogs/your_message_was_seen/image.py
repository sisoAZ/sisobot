from PIL import Image
import numpy as np
import env
import os

items_path = os.getcwd() + "/files/seen/"

def mergeImage(image: Image):

    #image = Image.open(file).convert("RGBA") debug
    background_image = Image.open(items_path + "bg.png")
    #paste_width = int(abs(background_image.size[0] / 3.229)) #480 550
    paste_width = int(abs(background_image.size[0] / 3.5))
    #paste_height = int(abs(background_image.size[1] / 1.727)) #1070 800
    paste_height = int(abs(background_image.size[1] / 1.9)) #1070 800

    base = Image.new('RGBA', (background_image.size[0], background_image.size[1]), (255, 255, 255, 0))
    resize_image = scale_to_width(image, 700)
    (w, h) = resize_image.size
    coeffs = find_coeffs(
        [(0, 0 + h * 0.01), (w, 0 - h * 0.1), (w, h + h * 0.1), (0, h - h * 0.01)],
        [(0, 0), (w, 0), (w, h), (0, h)])

    resize_image.putalpha(200)
    rotated_image = resize_image.transform(resize_image.size, Image.BILINEAR, coeffs, Image.BILINEAR)
    rotated_image = rotated_image.rotate(-2.5, expand=True)
    fff = Image.new('RGBA', rotated_image.size, color=(248, 245, 233, 255))
    # create a composite image using the alpha layer of rot as a mask
    out = Image.composite(rotated_image, fff, rotated_image)

    

    #rotated_image = resize_image.rotate(-2.5, expand=True)

    #rotated_image = resize_image.rotate(20)
    base.paste(background_image, (0, 0))
    base.paste(out, (paste_width, paste_height))
    
    return base

#アスペクト比を保つ関数
def scale_to_width(img, width):
    height = round(img.height * width / img.width)
    return img.resize((width, height))

def find_coeffs(pa, pb):
  # http://umejan.hatenablog.com/entry/2016/04/27/225553
  matrix = []
  for p1, p2 in zip(pa, pb):
    matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
    matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

  A = np.matrix(matrix, dtype=np.float)
  B = np.array(pb).reshape(8)

  res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
  ret = np.array(res).reshape(8)
  wk = []
  for v in ret :
    wk.append(round(v, 3))
  (alpha,beta) = (wk[6]+1, wk[7]+1)
  (x0,y0) = (wk[2], wk[5])
  (x1,y1) = (round((wk[0]+x0)/alpha,3), round((wk[3]+y0)/alpha,3))
  (x2,y2) = (round((wk[1]+x0)/beta,3), round((wk[4]+y0)/beta,3))
  return ret


#mergeImage("test2.png")
#im = Image.open("test.png")
#(w, h) = im.size
#
#coeffs = find_coeffs(
#  [(0, 0 + h * 0.25), (w, 0), (w, h), (0, h + h * 0)],
#  [(0, 0), (w, 0), (w, h), (0, h)])
#
#im_new = im.transform(im.size, Image.PERSPECTIVE, coeffs, Image.BILINEAR)
#
#im_new.show()