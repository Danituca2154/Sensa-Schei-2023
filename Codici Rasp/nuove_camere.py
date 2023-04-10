import cv2
import numpy as np
import pytesseract
import time
from PIL import Image
import RPi.GPIO as GPIO

cap = cv2.VideoCapture(0) #sinistra?
cap.set(3,300)
cap.set(4,300)
cap1 = cv2.VideoCapture(4) #destra?
cap1.set(3,300)
cap1.set(4,300)
K = np.load("/home/sensaschei2/Desktop/GARE/dist_coeffs.1.npy")
D = np.load("/home/sensaschei2/Desktop/GARE/dist_coeffs.2.npy")

class videocamere:
    def telecamere(self):
        t0 = time.time()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(17, GPIO.OUT)
        #GPIO.output(17, GPIO.HIGH)
        while True:
            ret, frame = cap.read()
            ret1, frame1 = cap1.read()
            map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, (300, 300), cv2.CV_16SC2)
            undistorted_frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            rgb = cv2.cvtColor(undistorted_frame, cv2.COLOR_BGR2BGRA)
            undistorted_frame1 = cv2.remap(frame1, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            rgb1 = cv2.cvtColor(undistorted_frame1, cv2.COLOR_BGR2BGRA)   
            #cv2.imshow('undistorted_frame', rgb)
            #cv2.imshow('undistorted_frame1', rgb1)
            t1 = time.time()  # time
            timeRunning = (t1 - t0)
            cv2.waitKey(1)
            if timeRunning >= 0.5:  # 2 seconds
                out = cv2.imwrite('/home/sensaschei2/Desktop/GARE/immagine/capture.jpg', rgb)
                out1 = cv2.imwrite('/home/sensaschei2/Desktop/GARE/immagine/capture1.jpg', rgb1)
                break
        #cv2.destroyAllWindows()

        img = cv2.imread('immagine/capture.jpg', 1)    # show immagine catturata
        img1 = cv2.imread('immagine/capture1.jpg', 1)
        return img,img1  
            
    def get_color(self, img, lato):
        yellow_lower = np.array([22, 60, 200])
        yellow_upper = np.array([60, 255, 255])

        low_green = np.array([50, 70, 130])
        upp_green = np.array([90, 250, 255])

        low_red = np.array([0, 100, 195])
        upp_red = np.array([8, 255, 255])

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        yellow = cv2.inRange(hsv, yellow_lower, yellow_upper) #maschera
        green = cv2.inRange(hsv, low_green, upp_green)
        red = cv2.inRange(hsv, low_red, upp_red)


        kernel_size = 5
        yellow_d = cv2.GaussianBlur(yellow, (kernel_size, kernel_size), 0)
        green_d = cv2.GaussianBlur(green, (kernel_size, kernel_size), 0)
        red_d = cv2.GaussianBlur(red, (kernel_size, kernel_size), 0)

        immagini = [yellow_d, green_d, red_d]
        colore = ''
        for i in range(len(immagini)):
            (contours, hierarchy) = cv2.findContours(immagini[i], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # contours = array con coordinate (x,y);   #hierarchy = array of four values
            for pic, contour in enumerate(contours):  # enumerate prende contours e x = pic, y = contour
                area = cv2.contourArea(contour)  # definisce il contorno dell'area
                if area > 1000:
                    #x, y, w, h = cv2.boundingRect(contour)  # ritorna quattro valori in grado di crearmi un rettangolo
                    #img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 3)
                    if i == 0:
                        colore = 'giallo'
                    elif i == 1:
                        colore = 'verde'
                    elif i == 2:
                        colore = 'rosso'
        if (colore == 'giallo' and lato == 'sinistra'): #sinistra giallo
            lettera_t=1
        elif(colore == 'rosso' and lato == 'sinistra'): #sinistra rosso
            lettera_t=2
        elif(colore == 'verde' and lato == 'sinistra'): #sinistra verde
            lettera_t=3
        elif(colore == 'giallo' and lato == 'destra'): #destra giallo
            lettera_t=4
        elif(colore == 'rosso' and lato == 'destra'): #destra rosso
            lettera_t=5
        elif(colore == 'verde' and lato == 'destra'): #destra verde
            lettera_t=6
            
        else:
            lettera_t = 40 
               
        return lettera_t
        
    def get_letter(self, img, lato):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        kernel_size = 5
        blur = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
        global edges
        edges = cv2.Canny(blur, 50, 150)

        # Trova i contorni nell'immagine
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        right_contour = []
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])  # misura l'area attraverso i contorni
            if 750 < area < 7500:
                right_contour = contours[i]
                
        letter = ''
        if len(right_contour) != 0:
            x, y, w, h = cv2.boundingRect(right_contour)

            # Calcolare i vertici del rettangolo
            pt1 = (x, y)
            pt2 = (x + w, y)
            pt3 = (x + w, y + h)
            pt4 = (x, y + h)

            # Calcolare i punti medi dei lati del rettangolo
            mid_pt1 = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
            mid_pt2 = ((pt2[0] + pt3[0]) // 2 - 1, (pt2[1] + pt3[1]) // 2)
            mid_pt3 = ((pt3[0] + pt4[0]) // 2, (pt3[1] + pt4[1]) // 2)
            mid_pt4 = ((pt4[0] + pt1[0]) // 2 + 1, (pt4[1] + pt1[1]) // 2)
            #cv2.rectangle(img, pt1, pt3, (255, 0, 0), 2)

            # Disegnare le direttrici del rettangolo
            #cv2.line(img, mid_pt1, mid_pt3, (255, 0, 255), 2)  # verticale
            #cv2.line(img, mid_pt2, mid_pt4, (255, 0, 255), 2)  # orrizontale
            length_ver = mid_pt3[1] - mid_pt1[1]
            length_or = mid_pt2[0] - mid_pt4[0]

            length_max = 0
            edges_right = [0, 0]
            epsilon = 0.0075 * cv2.arcLength(right_contour, True)
            approx = cv2.approxPolyDP(right_contour, epsilon, True)
            #cv2.drawContours(img, [approx], 0, (0, 0, 255), 2)

            for i in range(len(approx)):  # ricerca del lato piÃ¹ lungo
                if i != len(approx) - 1:
                    x1, y1 = approx[i][0]
                    x2, y2 = approx[i+1][0]
                else:
                    x1, y1 = approx[i][0]
                    x2, y2 = approx[0][0]
                length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if length > length_max:
                    length_max = length
                    edges_right[0] = (x1, y1)
                    edges_right[1] = (x2, y2)
            (x1, y1) = edges_right[0]
            (x2, y2) = edges_right[1]

            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            if angle < 0:
                angle = 180 + angle
            #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            diff = length_ver - length_max
            prob_letter = ''
            if diff < 7 and 75 < angle < 100:  # diff < 6.5
                prob_letter = 'H'
            elif 15 < diff < 35 and 75 < angle < 100:  # 10.5 < diff < 28
                prob_letter = 'U'
            elif 20 < diff < 60 and 10 < angle < 50:  # 20 < diff < 40
                prob_letter = 'S'

            punti_ver = cambio_color(mid_pt1, mid_pt3, 'verticale')
            punti_or = cambio_color(mid_pt4, mid_pt2, 'orizzontale')
            terzo_ver = length_ver / 3
            terzo_or = length_or / 3
            letter = ''
            counter = 0
            
            if prob_letter == 'H':
                if len(punti_ver) == 2 and len(punti_or) == 2:  # len(punti_or) might be 1
                    for point in punti_ver:
                        if terzo_ver + mid_pt1[1] < point[1] < terzo_ver * 2 + mid_pt1[1]:  # se zona media
                            counter += 1
                    for point in punti_or:
                        if point == punti_or[0] and mid_pt4[0] <= point[0] <= terzo_or + mid_pt4[0]:  # zona sinistra
                            counter += 1
                        elif point == punti_or[1] and terzo_or * 2 + mid_pt4[0] <= point[0] <= mid_pt2[0]:  # zona destra
                            counter += 1
                    if counter == len(punti_or) + len(punti_ver):
                        letter = 'H'

            elif prob_letter == 'U':
                if len(punti_ver) == 2 and 2 < len(punti_or) < 5:
                    for point in punti_ver:
                        if terzo_ver * 2 + mid_pt1[1] < point[1] <= mid_pt3[1]:  # se zona bassa
                            counter += 1
                    for point in punti_or:
                        if len(punti_or) == 3:
                            if point == punti_or[0] and mid_pt4[0] <= point[0] <= terzo_or + mid_pt4[0]:  # zona sinistra
                                counter += 1
                            elif punti_or.index(point) > 0 and terzo_or * 2 + mid_pt4[0] <= point[0] <= mid_pt2[0]:  # zona destra
                                counter += 1
                        else:
                            if punti_or.index(point) < 2 and mid_pt4[0] <= point[0] <= terzo_or + mid_pt4[0]:  # zona sinistra
                                counter += 1
                            elif punti_or.index(point) > 1 and terzo_or * 2 + mid_pt4[0] <= point[0] <= mid_pt2[0]:  # zona destra
                                counter += 1
                    if counter == len(punti_or) + len(punti_ver):
                        letter = 'U'

            elif prob_letter == 'S':
                if len(punti_ver) == 6 and len(punti_or) == 2:
                    for point in punti_ver:
                        if punti_ver.index(point) < 2 and mid_pt1[1] <= point[1] <= terzo_ver + mid_pt1[1]:  # zona alta
                            counter += 1
                        elif 1 < punti_ver.index(point) < 4 and terzo_ver + mid_pt1[1] <= point[1] <= terzo_ver * 2 + mid_pt1[1]:  # zona media
                            counter += 1
                        elif punti_ver.index(point) > 3 and terzo_ver * 2 + mid_pt1[1] <= point[1] <= mid_pt3[1]:  # zona bassa
                            counter += 1
                    for point in punti_or:
                        if point == punti_or[0] and mid_pt4[0] <= point[0] <= terzo_or + mid_pt4[0]:  # zona sinistra
                            counter += 1
                        if point == punti_or[1] and terzo_or * 2 + mid_pt4[0] <= point[0] <= mid_pt2[0]:  # zona destra
                            counter += 1
                    if counter == len(punti_or) + len(punti_ver):
                        letter = 'S'
                        
        if(letter == 'U' and lato == 'sinistra'): #sinistra 
            lettera_t=7
        elif(letter == 'H' and lato == 'sinistra'): #sinistra 
            lettera_t=8
        elif(letter == 'S' and lato == 'sinistra'): #sinistra 
            lettera_t=9
        elif(letter == 'U' and lato == 'destra'): #destra 
            lettera_t=10
        elif(letter == 'H' and lato == 'destra'): #destra 
            lettera_t=11
        elif(letter == 'S' and lato == 'destra'): #destra 
            lettera_t=12
        else:
            lettera_t=40
            
        return lettera_t
            
    def definitivo(self, val_s, val_d):
	    if val_s != 40:
		    return val_s
	    elif val_d != 40:
		    return val_d 
	    else:
		    return 40
			
def cambio_color(punto1, punto2, direttrice):
    color_start = 0
    minima_dist = 4
    punti = []
    if direttrice == 'verticale':
        for coo in range(punto1[1], punto2[1] + 1):
            color = cv2.getRectSubPix(edges, (1, 1), (punto1[0], coo))  # ottieni il colore
            if color != color_start and minima_dist > 3:  # se il colore Ã¨ diverso da quello precedente (il primo nero)
                #cv2.circle(img, (punto1[0], coo), 5, (125, 125, 125), -1)  # disegna il puntino
                minima_dist = 0
                punti.append((punto1[0], coo))
            color_start = color
            minima_dist += 1
        return punti
    if direttrice == 'orizzontale':
        for coo in range(punto1[0], punto2[0] + 1):
            color = cv2.getRectSubPix(edges, (1, 1), (coo, punto1[1]))
            if color != color_start and minima_dist > 3:
                #cv2.circle(img, (coo,  punto1[1]), 5, (125, 125, 125), -1)
                punti.append((coo, punto1[1]))
                minima_dist = 0
            color_start = color
            minima_dist += 1
        return punti

            
if __name__ == '__main__':
    vid = videocamere()
    
    while True:
        #img,img1 = vid.telecamere()
        img, img1 = vid.telecamere()
        lettera = vid.get_letter(img, 'sinistra')
        lettera1 = vid.get_letter(img1, 'destra')
        lettera_def = vid.definitivo(lettera, lettera1)
        print(lettera, lettera1)
        if lettera_def == 40:
            color = vid.get_color(img, 'sinistra')
            color1 = vid.get_color(img1, 'destra')
            color_def = vid.definitivo(color, color1)
        #print(vid.get_letter(img1, destra))
        #vid.telecamere()
