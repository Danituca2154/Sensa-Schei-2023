from libBNO055 import BNO055
from time import sleep
import RPi.GPIO as GPIO
import asyncio
import cv2
import numpy as np
import pytesseract
from PIL import Image
import time
import RPi.GPIO as GPIO
import random
from piastre import piastre

class Sensore:
    #import RPi.GPIO as GPIO
    def init(self):
        from time import sleep
        import board
        import busio
        import smbus
        from smbus import SMBus
        import adafruit_vl6180x
        import adafruit_tca9548a
        from libBNO055 import BNO055
        #import RPi.GPIO as GPIO
        #import RPi.GPIO as GPIO
        self.arduino = 0x10
        self.bus = SMBus(1)
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.tca = adafruit_tca9548a.TCA9548A(self.i2c)
        self.piastre = piastre()
        self.bno = BNO055()
        if self.bno.begin() is not True:
            print("Error initializing device")
            exit()
        sleep(1)
        
        self.ds_fronte = adafruit_vl6180x.VL6180X(self.tca[0], offset=2)
        self.ds_sinistra_davanti = adafruit_vl6180x.VL6180X(self.tca[1], offset=25)
        self.ds_destra_dietro = adafruit_vl6180x.VL6180X(self.tca[2], offset=20)
        self.ds_destra_davanti = adafruit_vl6180x.VL6180X(self.tca[3], offset=0)
        self.ds_retro = adafruit_vl6180x.VL6180X(self.tca[4], offset=5)
        self.ds_sinistra_dietro = adafruit_vl6180x.VL6180X(self.tca[5], offset=10)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.OUT)# buzz
        GPIO.setup(22, GPIO.OUT)# led scivoli sinistra
        GPIO.setup(27, GPIO.OUT) #led scivolidestra

        GPIO.setup(16, GPIO.IN) #DIETRO SINISTRA
        GPIO.setup(20, GPIO.IN) # dietro mezzo
        GPIO.setup(21, GPIO.IN) #dietro destra
        GPIO.setup(26, GPIO.IN) #davanti destra
        GPIO.setup(19, GPIO.IN) #davanti centro
        GPIO.setup(13, GPIO.IN) #davanti sinistra

        GPIO.output(23, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)

        self.Finecorsa_BS = 16
        self.Finecorsa_BM = 20
        self.Finecorsa_BD = 21
        self.Finecorsa_FD = 26
        self.Finecorsa_FM = 19
        self.Finecorsa_FS = 13
        self.LED_D = 27
        self.LED_S = 22
        self.BUZZ = 23
        check = 0
        self.sus = 0
        self.assedritto = 0
        self.stato = 0
        self.byte_fermo = 0
        self.byte_avanti = 0x1
        self.byte_30cm = 0x2
        self.byte_5cm = 0x3
        self.byte_destra = 0x05
        self.byte_sinistra = 0x06
        self.byte_indietro = 0x07
        self.byte_correzzione_destra = 0x08
        self.byte_correzzione_sinistra = 0x09
        self.byte_carroarmato_destra = 0x11
        self.byte_carroarmato_sinistra = 0x12
        self.byte_ripartidestra = 0x13
        self.byte_ripartisinistra = 0x14
        self.byte_addossoalmurosinistra = 0x15
        self.byte_addossoalmurodestra = 0x16
        self.byte_stop = 0x17
        self.byte_aspetta5secvittima = 0x18
        self.byte_10cmindietro = 0x20
        self.byte_sinistralenta = 0x21
        self.byte_destralenta = 0x22
        self.byte_ostacolosinistra = 0x23
        self.byte_ostacolodestra = 0x24
        self.byte_att = 0
        self.c = 0
        self.conteggio = 0
        self.conteggio2 = 0
        self.controllo = 0
        self.controllopiastre = 0
        self.nero=0
    def sensori_check(self):
        check=0
        self.inclinazione = self.bno.inclinazione()
        self.amogus = self.piastre.prova()
        #destra
        if(self.ds_fronte.range<120) and (self.ds_sinistra_davanti.range<160) and (self.ds_sinistra_dietro.range<160) and (self.ds_destra_davanti.range>120) and (self.ds_destra_dietro.range>120):   #per fare girare a destra
            check=1
            self.controllo = 1
        #sinistra
        elif(self.ds_fronte.range<120) and (self.ds_destra_davanti.range<160) and (self.ds_destra_dietro.range<160) and (self.ds_sinistra_davanti.range>120) and (self.ds_sinistra_dietro.range>120): #per girare a sinistra
            check=2
            self.controllo = 1
        #solo muro--> destra
        elif(self.ds_fronte.range<120) and (self.ds_destra_davanti.range>120) and (self.ds_destra_dietro.range>120) and (self.ds_sinistra_davanti.range>120) and (self.ds_sinistra_dietro.range>120):  # solo muro
            check=3
            self.controllo = 1
        #davanti libero, destra libera, sinistra libera, retro libero  --> destra
        elif(self.ds_fronte.range > 190) and (self.ds_destra_davanti.range>160) and (self.ds_destra_dietro.range>160) and (self.ds_sinistra_davanti.range>160) and (self.ds_sinistra_dietro.range>160) and (self.ds_retro.range>160) and self.controllo==0:
            check=4
            self.controllo=1
        #davanti libero, destra libera, sinistra occupata, retro libero --> destra
        elif(self.ds_fronte.range > 190) and (self.ds_destra_davanti.range>120) and (self.ds_destra_dietro.range>120) and (self.ds_sinistra_davanti.range<160) and (self.ds_sinistra_dietro.range<160) and (self.ds_retro.range>120) and self.controllo==0:
            check=5
            self.controllo=1
        #davanti libero, destra occupata, sinistra libera, retro libero -->30cm
        elif(self.ds_fronte.range > 190) and (self.ds_destra_davanti.range<160) and (self.ds_destra_dietro.range<160) and (self.ds_sinistra_davanti.range>160) and (self.ds_sinistra_dietro.range>160) and (self.ds_retro.range>120) and self.controllo==0:
            check=100
            self.controllo=1
            self.controllopiastre=0
        #davanti libero, destra occupata, sinistra occupata, retro libero --> 30cm
        elif(self.ds_fronte.range>190) and (self.ds_destra_davanti.range<160) and (self.ds_destra_dietro.range<160) and (self.ds_sinistra_davanti.range<160) and (self.ds_sinistra_dietro.range<160) and self.controllo==0:  # solo muro
            check=100
            self.controllo = 1
            self.controllopiastre=0
        #tiene conto di una salita e quindi la macchina non torna indietro
        elif(self.ds_retro.range<120) and (self.inclinazione>12):
            check=100
            self.controllopiastre=0
        #riposizionamento (retro occupato)
        elif(self.ds_retro.range<120) and (self.c==0) and (self.inclinazione<12):
            check=6
        #vicolo cieco--> destra destra
        elif(self.ds_fronte.range<120) and (self.ds_destra_davanti.range<160) and (self.ds_destra_dietro.range<160) and (self.ds_sinistra_davanti.range<160) and (self.ds_sinistra_dietro.range<160):  #vicolo cieco
            check=7
        
        else:
            check=100
            #print("condizione strana")
            self.controllopiastre=0
        if(self.conteggio==2):
            check=8
            self.conteggio=0
            self.controllopiastre=0
        if(self.conteggio2 ==2):
            check=9
            self.conteggio2=0
            self.controllopiastre=0
        if (self.ds_fronte.range < 160 and self.ds_fronte.range > 120):
            check=10
            self.controllopiastre=0
        if self.amogus == 2 and self.controllopiastre == 0 :
            print("piastra blu 5sec")
            sleep(5)
            self.controllopiastre = 1
        return check

    def destra(self):
        self.bno.begin()
        gradi = self.bno.readAngle()
        while (gradi < 85) or (358 <= gradi <= 360) or (gradi < 1) or (gradi > 361):
            if (self.byte_att != self.byte_destralenta):
                self.byte_att = self.byte_destralenta
                self.bus.write_byte(self.arduino, self.byte_destralenta)
            gradi = self.bno.readAngle()
        # print(gradi)
        if (self.byte_att != self.byte_fermo):
            self.byte_att = self.byte_fermo
            self.bus.write_byte(self.arduino, self.byte_fermo)
            sleep(0.5)
        print("girato a destra")

    def sinistra(self):
        self.bno.begin()
        gradi = self.bno.readAngle()
        while (gradi > 275) or (0 <= gradi <= 2) or (gradi < 1) or (gradi > 361):
            if (self.byte_att != self.byte_sinistralenta):
                self.byte_att = self.byte_sinistralenta
                self.bus.write_byte(self.arduino, self.byte_sinistralenta)
                sleep(0.1)
            gradi = self.bno.readAngle()
        if (self.byte_att != self.byte_fermo):
            self.byte_att = self.byte_fermo
            self.bus.write_byte(self.arduino, self.byte_fermo)
            sleep(0.5)
        print("girato a sinistra")

    def riposizionamento(self):
        # while (GPIO.input(self.Finecorsa_BS) and GPIO.input(self.Finecorsa_BM) and GPIO.input(self.Finecorsa_BD)) == False:
        while GPIO.input(self.Finecorsa_BM) == False:
            if (self.byte_att != self.byte_indietro):
                self.byte_att = self.byte_indietro
                self.bus.write_byte(self.arduino, self.byte_indietro)
            GPIO.output(self.LED_D, GPIO.HIGH)
            GPIO.output(self.LED_S, GPIO.HIGH)
            GPIO.output(self.LED_D, GPIO.LOW)
            GPIO.output(self.LED_S, GPIO.LOW)
        if (self.byte_att != self.byte_fermo):
            self.byte_att = self.byte_fermo
            self.bus.write_byte(self.arduino, self.byte_fermo)
        sleep(0.1)
        if (self.byte_att != self.byte_5cm):
            self.byte_att = self.byte_5cm
            self.bus.write_byte(self.arduino, self.byte_5cm)
        self.bus.write_byte(self.arduino, 0x1)
        self.c = (self.bus.read_byte(self.arduino))
        if self.c == 0x6:
            self.byte_att = self.byte_fermo
            self.bus.write_byte(self.arduino, self.byte_fermo)
            sleep(0.1)
    def inmezzo(self):
		#caso in cui è storta:
        if(self.ds_sinistra_davanti.range <120 and self.ds_sinistra_dietro.range>90 and self.ds_sinistra_dietro.range<160):
            while((self.ds_sinistra_davanti.range/self.ds_sinistra_dietro.range)<0.95):
                self.byte_att = self.byte_carroarmato_destra
                self.bus.write_byte(self.arduino, self.byte_carroarmato_destra)
        self.byte_att = self.byte_fermo
        self.bus.write_byte(self.arduino, self.byte_fermo)
        sleep(0.1)
        if(self.ds_sinistra_dietro.range <120 and self.ds_sinistra_davanti.range>90 and self.ds_sinistra_davanti.range<160):
            while((self.ds_sinistra_dietro.range/self.ds_sinistra_davanti.range)<0.95):
                self.byte_att = self.byte_carroarmato_sinistra
                self.bus.write_byte(self.arduino, self.byte_carroarmato_sinistra)
        self.byte_att = self.byte_fermo
        self.bus.write_byte(self.arduino, self.byte_fermo)
        sleep(0.1)
        if(self.ds_destra_davanti.range <120 and self.ds_destra_dietro.range>90 and self.ds_destra_dietro.range<160):
            while((self.ds_destra_davanti.range/self.ds_destra_dietro.range)<0.95):
                self.byte_att = self.byte_carroarmato_sinistra
                self.bus.write_byte(self.arduino, self.byte_carroarmato_sinistra)
        self.byte_att = self.byte_fermo
        self.bus.write_byte(self.arduino, self.byte_fermo)
        sleep(0.1)
        if(self.ds_destra_dietro.range <120 and self.ds_destra_davanti.range>90 and self.ds_destra_davanti.range<160):
            while((self.ds_destra_dietro.range/self.ds_destra_davanti.range)<0.95):
                self.byte_att = self.byte_carroarmato_destra
                self.bus.write_byte(self.arduino, self.byte_carroarmato_destra)
        self.byte_att = self.byte_fermo
        self.bus.write_byte(self.arduino, self.byte_fermo)
        sleep(0.1)
        #----------------------------------------------------------------------------------------------------------------------------------------------------
        #caso in cui è troppo vicina o lontana dai muri:
        if(self.ds_sinistra_dietro.range >110 and self.ds_sinistra_davanti.range>110 and self.ds_sinistra_dietro.range <165 and self.ds_sinistra_davanti.range<165):
            self.sinistra()
            while(self.ds_fronte.range > 80):
                self.bus.write_byte(self.arduino, self.byte_avanti)
            self.bus.write_byte(self.arduino, self.byte_fermo)
            self.destra()
        if(self.ds_destra_dietro.range >110 and self.ds_destra_davanti.range>110 and self.ds_destra_dietro.range <165 and self.ds_destra_davanti.range<165):
            self.destra()
            while(self.ds_fronte.range > 80):
                self.bus.write_byte(self.arduino, self.byte_avanti)
            self.bus.write_byte(self.arduino, self.byte_fermo)
            self.sinistra()
        if(self.ds_destra_dietro.range <70 and self.ds_destra_davanti.range<70):
            self.destra()
            sleep(1)
            self.sinistra()
        if(self.ds_sinistra_dietro.range <70 and self.ds_sinistra_davanti.range<70):
            self.destra()
            sleep(1)
            self.sinistra()   
        #-----------------------------------------------------------------------------------------------------------------------------------------------------
        #caso in cui è storta:
        if(self.ds_sinistra_davanti.range <100 and self.ds_sinistra_dietro.range>90 and self.ds_sinistra_dietro.range<160):
            while((self.ds_sinistra_davanti.range/self.ds_sinistra_dietro.range)<0.93):
                self.byte_att = self.byte_carroarmato_destra
                self.bus.write_byte(self.arduino, self.byte_carroarmato_destra)
        self.byte_att = self.byte_fermo
        self.bus.write_byte(self.arduino, self.byte_fermo)
        sleep(0.1)
        if(self.ds_sinistra_dietro.range <100 and self.ds_sinistra_davanti.range>90 and self.ds_sinistra_davanti.range<160):
            while((self.ds_sinistra_dietro.range/self.ds_sinistra_davanti.range)<0.93):
                self.byte_att = self.byte_carroarmato_sinistra
                self.bus.write_byte(self.arduino, self.byte_carroarmato_sinistra)
        self.byte_att = self.byte_fermo
        self.bus.write_byte(self.arduino, self.byte_fermo)
        sleep(0.1)
        if(self.ds_destra_davanti.range <100 and self.ds_destra_dietro.range>90 and self.ds_destra_dietro.range<160):
            while((self.ds_destra_davanti.range/self.ds_destra_dietro.range)<0.93):
                self.byte_att = self.byte_carroarmato_sinistra
                self.bus.write_byte(self.arduino, self.byte_carroarmato_sinistra)
        self.byte_att = self.byte_fermo
        self.bus.write_byte(self.arduino, self.byte_fermo)
        sleep(0.1)
        if(self.ds_destra_dietro.range <100 and self.ds_destra_davanti.range>90 and self.ds_destra_davanti.range<160):
            while((self.ds_destra_dietro.range/self.ds_destra_davanti.range)<0.93):
                self.byte_att = self.byte_carroarmato_destra
                self.bus.write_byte(self.arduino, self.byte_carroarmato_destra)
        self.byte_att = self.byte_fermo
        self.bus.write_byte(self.arduino, self.byte_fermo)
        sleep(0.1)         
        
    ferma_cicli = False
    async def first_task(self):
        byte_ritorno = 0
        ferma_cicli = False
        while (self.ferma_cicli == False):
            byte_ritorno = self.bus.read_byte(self.arduino)
            #print(byte_ritorno)  
            await asyncio.sleep(0.001)
            if byte_ritorno == 5:
                self.ferma_cicli = True
                self.byte_att = self.byte_stop
                self.bus.write_byte(self.arduino, self.byte_stop)
                break
        self.byte_att = self.byte_stop
        self.bus.write_byte(self.arduino, self.byte_stop)      
        #print("finito1")
        return byte_ritorno

    async def second_task(self):
        sus = 0
        suk = 1
        sup = 1
        while (self.ferma_cicli == False):
            self.inclinazione = self.bno.inclinazione()
            self.nero = self.piastre.prova()
            if self.nero==3:
                sus = 6
                print("piastra nera")
                self.ferma_cicli = True
            if (GPIO.input(self.Finecorsa_FD) == True or GPIO.input(self.Finecorsa_FM) == True or GPIO.input(self.Finecorsa_FS) == True):
                self.byte_att = self.byte_stop
                self.bus.write_byte(self.arduino, self.byte_stop)
                sus = 5
                print("eccoococo")
                self.ferma_cicli = True
            if ((self.inclinazione < -3) and (suk > 0)):
                self.conteggio2 = self.conteggio2 + 1
                suk = 0
            else:
                if (self.inclinazione >= -3):
                    self.conteggio2 = 0

            if ((self.inclinazione > 3) and (sup > 0)):
                self.conteggio = self.conteggio + 1
                sup = 0
            else:
                if (self.inclinazione <= 3):
                    self.conteggio = 0
            await asyncio.sleep(0.001)
            #print("finito2")
        return sus

    async def main(self):
        results = await asyncio.gather(self.first_task(), self.second_task())
        self.first_task_result, self.second_task_result = results
        self.ferma_cicli = False
        
    def cm30(self):
        self.byte_att = self.byte_30cm
        self.bus.write_byte(self.arduino, self.byte_30cm)
        self.first_task_result = 0
        self.second_task_result = 0
        # self.third_task_result = 0
        while True:
            asyncio.run(self.main())
            if (self.first_task_result == 5) or (self.second_task_result == 5) or (self.second_task_result == 6):
                break
        if self.second_task_result == 6:
            self.c=0
            self.byte_att = self.byte_10cmindietro
            self.bus.write_byte(self.arduino, self.byte_10cmindietro)
            while self.c != 0x6:
               self.c = (self.bus.read_byte(self.arduino))
            self.byte_att = self.byte_fermo
            self.bus.write_byte(self.arduino, self.byte_fermo)
            sleep(0.6)
            self.destra()
            sleep(0.4)
            #self.ds_fronte = adafruit_vl6180x.VL6180X(self.tca[0], offset=2)
            print(self.ds_fronte.range)
            if self.ds_fronte.range<160:
                self.destra()
            else:			
               self.cm30()
        while (GPIO.input(self.Finecorsa_FD) == True and GPIO.input(self.Finecorsa_FS) == False):
             if self.byte_att != self.byte_ostacolodestra:
                    self.byte_att = self.byte_ostacolodestra
                    self.bus.write_byte(self.arduino, self.byte_ostacolodestra)
             sleep(0.4)
             if GPIO.input(self.Finecorsa_FM) == True:
                 break
        while (GPIO.input(self.Finecorsa_FD) == False and GPIO.input(self.Finecorsa_FS) == True):
            if self.byte_att != self.byte_ostacolosinistra:
                    self.byte_att = self.byte_ostacolosinistra
                    self.bus.write_byte(self.arduino, self.byte_ostacolosinistra)
            sleep(0.4)
            if GPIO.input(self.Finecorsa_FM) == True:
                break
             
        # print(self.conteggio)
        # print(self.conteggio2)
        if (self.conteggio2 == 2):
            print("tagliocorto2")
        elif (self.conteggio == 2):
            print("tagliocorto")
            # per evitare di farla fermare ancora semplicemente la faccio andare avanti fino alla fine della salita
        else:
            self.byte_att = self.byte_stop
            self.bus.write_byte(self.arduino, self.byte_stop)
            if self.byte_att != self.byte_fermo:
                self.byte_att = self.byte_fermo
                self.bus.write_byte(self.arduino, self.byte_fermo)
                # print("avanti")
                sleep(0.1)
            self.inmezzo()
            if self.byte_att != self.byte_fermo:
                self.byte_att = self.byte_fermo
                self.bus.write_byte(self.arduino, self.byte_fermo)
                sleep(0.5)
        self.c = 0
        self.controllo = 0
        self.controllopiastre =0
        return 20

    def avvio(self):
        check = self.sensori_check()
        print(check)
        if check == 1:
            self.destra()
            self.inmezzo()	
            self.riposizionamento()
            self.cm30()
            self.inmezzo()	
        elif check == 2:
            self.sinistra()
            self.inmezzo()	
            return 1
        elif check == 3:
            self.destra()
            self.inmezzo()	
            self.cm30()
        elif check == 4:
            self.destra()
            self.inmezzo()	
            return 1
        elif check == 5:
            self.destra()
            self.inmezzo()	
            return 1
        elif check == 6:
            self.riposizionamento()
            return 1
        elif check == 7:
            self.destra()
            self.destra()
            self.inmezzo()	
            return 1
        elif check == 8:
            inclinazione = self.bno.inclinazione()
            while (inclinazione>3 or inclinazione<-3) and (-90<inclinazione<90):
                if self.byte_att != self.byte_avanti:
                    self.byte_att = self.byte_avanti
                    self.bus.write_byte(self.arduino, self.byte_avanti)
                inclinazione = self.bno.inclinazione()
            if self.byte_att != self.byte_fermo:
                self.byte_att = self.byte_fermo
                self.bus.write_byte(self.arduino, self.byte_fermo)
                sleep(0.1)
            self.inmezzo()	
            return 1
        elif check == 9:
            inclinazione = self.bno.inclinazione()
            while (inclinazione>3 or inclinazione<-3) and (-90<inclinazione<90):
                if self.byte_att != self.byte_avanti:
                    self.byte_att = self.byte_avanti
                    self.bus.write_byte(self.arduino, self.byte_avanti)
                inclinazione = self.bno.inclinazione()
            if self.byte_att != self.byte_fermo:
                self.byte_att = self.byte_fermo
                self.bus.write_byte(self.arduino, self.byte_fermo)
                sleep(0.1)
            self.inmezzo()	
            return 20
        elif check == 100:
            self.cm30()
            return 20
        elif check == 10:
            while(self.ds_fronte.range < 160 and self.ds_fronte.range > 120):
                if self.byte_att != self.byte_avanti:
                    self.byte_att = self.byte_avanti
                    self.bus.write_byte(self.arduino, self.byte_avanti)
            if self.byte_att != self.byte_fermo:
                self.byte_att = self.byte_fermo
                self.bus.write_byte(self.arduino, self.byte_fermo)
                sleep(0.1)
            self.inmezzo()	
            return 20
        
                

if __name__ == '__main__':
    sn = Sensore()
    sn.init()
    while True:
        sn.avvio()
        '''
        try:
            #sn.sensori_check()
            sn.avvio()
        except Exception as e:
            print ("errore", e)
        '''
