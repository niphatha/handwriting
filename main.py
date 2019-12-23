import cv2
import label_image
import numpy as np
import operator
from PIL import ImageFont, ImageDraw, Image

dataMap = {
    '00': 'ก',
    '01': 'ข',
    '02': 'ซ',
    '03': 'ค',
    '04': 'ฅ',
    '05': 'ฆ',
    '06': 'ง',
    '07': 'จ',
    '08': 'ฉ',
    '09': 'ช',
    '10': 'ซ',
    '11': 'ฌ',
    '12': 'ญ',
    '13': 'ฎ',
    '14': 'ฏ',
    '15': 'ฐ',
    '16': 'ฑ',
    '17': 'ฒ',
    '18': 'ณ',
    '19': 'ด',
    '20': 'ต',
    '21': 'ถ',
    '22': 'ท',
    '23': 'ธ',
    '24': 'น',
    '25': 'บ',
    '26': 'ป',
    '27': 'ผ',
    '28': 'ฝ',
    '29': 'พ',
    '30': 'ฟ',
    '31': 'ภ',
    '32': 'ม',
    '33': 'ย',
    '34': 'ร',
    '35': 'ล',
    '36': 'ว',
    '37': 'ศ',
    '38': 'ษ',
    '39': 'ส',
    '40': 'ห',
    '41': 'ฬ',
    '42': 'อ',
    '43': 'ฮ',
    '44': 'ฤ',
    '45': 'ฦ',
    '46': 'ะ',
    '47': 'า',
    '48': 'ฯ',
    '49': 'ๆ',
    '50': 'เ',
    '51': 'แ',
    '52': 'โ',
    '53': 'ใ',
    '54': 'ไ',
}

fontpath = "./Nithan.ttf"
font = ImageFont.truetype(fontpath, 32)

def recog(filename):
    input_image = filename
    image = cv2.imread(input_image)

    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    ret, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((10,10),np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # cv2.imshow('f_name', closing)
    # cv2.waitKey(0)
    # cv2.destroyWindow('f_name')

    kernel2 = np.ones((1,1),np.uint8)
    closing2 = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel2)

    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    data_res = {}

    if len(contours) > 0:
        for ctr in contours: 
            if cv2.contourArea(ctr) > 70:
                x,y,w,h = cv2.boundingRect(ctr)
                if h > 5 and w > 5:
                    cv2.rectangle(image,(x,y),( x + w, y + h ),(0,255,0),2)
                    # sub_image = closing2[y - 5:y+h + 5, x - 5:x+w + 5]
                    sub_image = closing2[y:y+h, x:x+w]
                    img = cv2.resize(sub_image,(27,27))
                    cv2.imwrite('input.' + input_image.split('.')[-1], img)
                    result = label_image.main('input.' + input_image.split('.')[-1])
                    if len(result):
                        res = sorted(result.items(), key=operator.itemgetter(1))[-1]
                        if res[1] > 0.4:
                            print('"{}" : {}'.format(dataMap[res[0]], res[1]))
                            
                            img_pil = Image.fromarray(image)
                            draw = ImageDraw.Draw(img_pil)
                            draw.text((x, y), dataMap[res[0]], font = font, fill = (255,0,0,0))
                            image = np.array(img_pil)
                            data_res[x] = dataMap[res[0]]
                            # cv2.putText(image, 'ก', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)

    text_res = ''
    for i in sorted(data_res):  
        text_res += data_res[i]
    # print(text_res)
    # cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
    # cv2.imshow('closing', image)
    cv2.imwrite('static/output.' + input_image.split('.')[-1], image)
    return text_res, 'static/output.' + input_image.split('.')[-1]
    # if cv2.waitKey(0) & 0xff == 27:  
    #     cv2.destroyAllWindows()