import cv2
import numpy as np
import os, glob
import uuid

list_line_1 = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']
list_line_2 = ['23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45']
list_line_3 = ['46', '47', '48', '49', '50', '51', '52', '53', '54']
list_line = []
data_dir = 'crop/03/'
success = []
fail = []
max_len = 23

def load_image(f_name):
    image = cv2.imread(data_dir + f_name)
    if data_dir == 'crop/03/':
        image = image[0: , 0:500]
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    ret, thresh = cv2.threshold(image_gray, 215, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((20,10),np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    kernel2 = np.ones((1,1),np.uint8)
    closing2 = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel2)

    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    data = []
    if len(contours) > 0:
        for contour in contours:
            if cv2.contourArea(contour) > 50 and cv2.contourArea(contour) < 1000:
                res = {}
                x,y,w,h = cv2.boundingRect(contour)
                
                if w < 100 and h < 60:
                    # cv2.rectangle(image,(x-5,y-5),( x + w + 5, y + h + 5 ),(0,255,0),2)
                    cv2.rectangle(image,(x,y),( x + w, y + h),(0,255,0),2)
                    res['x'] = x
                    res['y'] = y
                    res['w'] = w
                    res['h'] = h
                    res['area'] = cv2.contourArea(contour)
                    data.append(res)
    if len(data):
        data = sorted(data, key = lambda i: i['x'])
        # cv2.imshow(f_name, image)
        # cv2.waitKey(0)
        # cv2.destroyWindow(f_name)
        if len(data) != max_len:
            fail.append(f_name)
        elif len(data) == max_len:
            success.append(f_name)
            for i in range(len(data)):
                dir_name = './data/' + list_line[i] + '/'
                filename = dir_name + f_name.split('.')[0] + '.png'
                # filename = dir_name + f_name
                print(filename)
                os.makedirs(os.path.dirname(dir_name), exist_ok=True)
  
  
                x = data[i]['x']
                y = data[i]['y']
                w = data[i]['w']
                h = data[i]['h']
                # sub_image = closing2[y - 5:y + h + 5, x - 5:x + w + 5]
                sub_image = closing2[y:y + h, x:x + w]
                img = cv2.resize(sub_image,(27,27))
                cv2.imwrite(filename, img)
                # cv2.imshow(f_name, image)
                # cv2.waitKey(0)
                # cv2.destroyWindow(f_name)

if __name__ == "__main__":
    try:
        os.mkdir('./data')
    except:
        pass
    if data_dir == 'crop/01/':
        list_line = list_line_1
    elif data_dir == 'crop/02/':
        list_line = list_line_2
    elif data_dir == 'crop/03/':
        list_line = list_line_3
        max_len = 9

    for file in os.listdir(data_dir):
        load_image(file)
    print('success: ' + str(len(success)))
    print('fail: ' + str(len(fail)))
