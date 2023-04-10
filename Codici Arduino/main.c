
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "I2CSlave.h"
#define I2C_ADDR 0x10

volatile uint8_t data;
volatile uint8_t data1;


float x=0, y=0, z=0, d=0, s=0;
volatile float conta=0, conta2=0, conta3=0, conta4=0, marti1=0, marti2=0, marti3=0, marti4=0, martimedia=0, sus=0;
float Kp=14.0, Ki=6.1, Kd=0.55;              //prima kp poi il resto
float e=0.0, I=0.0 ,P=0.0, D=0.0, C=0.0;
float e2=0.0, I2=0.0, P2=0.0, D2=0.0, C2=0.0;
float e3=0.0, I3=0.0, P3=0.0, D3=0.0, C3=0.0;
float e4=0.0, I4=0.0, P4=0.0, D4=0.0, C4=0.0;
float a=0.0, a2=0.0, a3=0.0, a4=0.0, sD=0.4, sS=0.4; //sD è il setpoint delle ruote a destra
int destra=0, sinistra=0, w=0;                      //sS è il setpoint delle ruote di sinistra
ISR(INT2_vect){ //OCR1C
	conta++;
	marti1++;
}
ISR(INT3_vect){ //OCR3A
	conta2++;
	marti2++;
}
ISR(INT4_vect){ //OCR1A
	conta3++;
	marti3++;
}
ISR(INT5_vect){ //OCR1B
	conta4++;
	marti4++;
}
ISR(TIMER5_COMPA_vect){ //timer dichiarato fuori p.102 datasheet
	a=conta/25;
	a2=conta2/25;
	a3=conta3/25;
	a4=conta4/25;
	e=sS-a;
	e2=sD-a2;
	e3=sS-a3;
	e4=sD-a4;
	P=e*Kp;
	P2=e2*Kp;
	P3=e3*Kp;
	P4=e4*Kp;
	I=e*Ki;
	I2=e2*Ki;
	I3=e3*Ki;
	I4=e4*Ki;
	D=e*Kd;
	D2=e2*Kd;
	D3=e3*Kd;
	D4=e4*Kd;
	C=P+I;
	C=P+I+D;
	C2=P2+I2+D2;
	C3=P3+I3+D3;
	C4=P4+I4+D4;
	if (((PINF&0b00001000)==0) || (data==0) || (PORTA==0))
	{
		C=0;
		C2=0;
		C3=0;
		C4=0;
	}
	if((OCR1A+C3)>=1023){
		OCR1A=1023;
	}
	else OCR1A=OCR1A+C3;


	if((OCR3A+C2)>=1023){
		OCR3A=1023;
	}
	else OCR3A=OCR3A+C2;


	if((OCR1C+C)>=1023){
		OCR1C=1023;
	}
	else OCR1C=OCR1C+C;


	if((OCR1B+C4)>=1023){
		OCR1B=1023;
	}
	else OCR1B=OCR1B+C4;
	conta=0;
	conta2=0;
	conta3=0;
	conta4=0;
	TCNT5=0; //ricorda azzerramento
	
}




void I2C_received(uint8_t received_data)
{
	data = received_data;
}

void I2C_requested()
{
	I2C_transmitByte(data1);
}

void I2Csetup()
{
	// imposta received/requested callbacks
	I2C_setCallbacks(I2C_received, I2C_requested);

	// init I2C
	I2C_init(I2C_ADDR);
}



int main(void)
{
	I2Csetup();
	TCCR5A=0;
	TCCR5B=(1<<CS52);
	TIMSK5=(1<<OCIE5A);
	OCR5A=625; //0.01 sec
	TCCR1A=(0<<WGM11)|(0<<WGM10)|(1<<COM1A1)|(0<<COM1A0)|(1<<COM1B1)|(0<<COM1B0)|(1<<COM1C1)|(0<<COM1C0);
	TCCR1B=(1<<WGM13)|(0<<WGM12)|(1<<CS12)|(0<<CS11)|(0<<CS10); //mode 8
	TCCR3A=(0<<WGM31)|(0<<WGM30)|(1<<COM3A1)|(0<<COM3A0)|(1<<COM3B1)|(0<<COM3B0)|(1<<COM3C1)|(0<<COM3C0);
	TCCR3B=(1<<WGM33)|(0<<WGM32)|(1<<CS32)|(0<<CS31)|(0<<CS30); //mode 8
	ICR1=1023;
	ICR3=1023;
	//DDRC=0x00;
	DDRA=0xFF;
	//DDRL=0xFF;
	DDRB=(1<<PB5) | (1<<PB6) | (1<<PB7);
	DDRE=(1<<PE3);
	
	DDRF = 0;

	EICRA=(1<<ISC20)|(1<<ISC21)|(1<<ISC30)|(1<<ISC31);
	EICRB=(1<<ISC40)|(1<<ISC41)|(1<<ISC50)|(1<<ISC51);          //RISING EDGE
	EIMSK=(1<<INT2)|(1<<INT3)|(1<<INT4)|(1<<INT5);  // ABILITA INT0     USANDO sei() richiamo il set enable interrupt
	sei();
	
	
	
	void avanti(){
		PORTA = (1<<PA1)|(1<<PA3)|(1<<PA4)|(1<<PA7);
	}
	void sinistra(){
		PORTA = (1<<PA0)|(1<<PA6)|(1<<PA3)|(1<<PA4);
	}

	void destra(){
		PORTA = (1<<PA1)|(1<<PA7)|(1<<PA2)|(1<<PA5);
	}

	void indietro(){
		sD=0.2;
		sS=0.2;
		Kp=4.60, Ki=2.24, Kd=0.35;
		PORTA = (1<<PA0)|(1<<PA2)|(1<<PA5)|(1<<PA6);
	}
	
	void retromarcia(){
		sD=0.2;
		sS=0.2;
		Kp=4.60, Ki=2.24, Kd=0.35;
		PORTA = (1<<PA0)|(1<<PA2)|(1<<PA5)|(1<<PA6);
	}

	void fermo(){
		PORTA = 0;
		e=0.0, I=0.0 ,P=0.0, D=0.0, C=0.0;
		e2=0.0, I2=0.0, P2=0.0, D2=0.0, C2=0.0;
		e3=0.0, I3=0.0, P3=0.0, D3=0.0, C3=0.0;
		e4=0.0, I4=0.0, P4=0.0, D4=0.0, C4=0.0;
	}
	void cm30(){
		sD=0.4;
		sS=0.4;
		Kp=14.0, Ki=6.1, Kd=0.55;
		marti1=0;
		marti2=0;
		marti3=0;
		marti4=0;
		data1=0x0;
		int stop_loop = 0;
		while((stop_loop==0)&&(martimedia<1000)&&(PINF&0b00001000)!=0){
			PORTA = (1<<PA1)|(1<<PA3)|(1<<PA4)|(1<<PA7);
			martimedia=(marti1+marti2+marti3+marti4)/4;
			if(data==0x17){
				martimedia=1000;
			}
			if(data==0x18){
				martimedia=1000;
			}
			while(martimedia>=850){
				data1=5;
				I2C_transmitByte(data1);
				stop_loop=1;
				if(data == 0x17){
					PORTA=0;
					break;
				}
			}
		}
		martimedia=0;
		
	}
	void cm5(){
		
		marti1=0;
		marti2=0;
		marti3=0;
		marti4=0;
		data1=0x0;
		while(martimedia<150){
			PORTA = (1<<PA1)|(1<<PA3)|(1<<PA4)|(1<<PA7);
			martimedia=(marti1+marti2+marti3+marti4)/4;
			data1=0x6;
		}
		I2C_transmitByte(data1);
		martimedia=0;
	}
	
	void carroarmatodestra(){
		sD=0.2;
		sS=0.2;
		Kp=4.60, Ki=2.24, Kd=0.35;
		PORTA = (1<<PA1)|(1<<PA7)|(1<<PA2)|(1<<PA5);
		_delay_ms(15);
		PORTA = 0;
		_delay_ms(25);
		PORTA = (1<<PA1)|(1<<PA7)|(1<<PA2)|(1<<PA5);
		_delay_ms(1);
	}
	
	void carroarmatosinistra(){
		sD=0.2;
		sS=0.2;
		Kp=4.60, Ki=2.24, Kd=0.35;
		PORTA = (1<<PA0)|(1<<PA6)|(1<<PA3)|(1<<PA4);
		_delay_ms(15);
		PORTA = 0;
		_delay_ms(25);
		PORTA = (1<<PA0)|(1<<PA6)|(1<<PA3)|(1<<PA4);
		_delay_ms(1);
	}
	
	void addossoalmurosinistra(){
		sD=0.2;
		sS=0.2;
		Kp=4.60, Ki=2.24, Kd=0.35;
		PORTA = (1<<PA1)|(1<<PA7)|(1<<PA2)|(1<<PA5);  //destra
		_delay_ms(240);
		PORTA = (1<<PA0)|(1<<PA6)|(1<<PA3)|(1<<PA4);  //sinistra
		_delay_ms(100);
		PORTA = 0;
	}
	
	void addossoalmurodestra(){
		sD=0.2;
		sS=0.2;
		Kp=4.60, Ki=2.24, Kd=0.35;
		PORTA = (1<<PA0)|(1<<PA6)|(1<<PA3)|(1<<PA4);  //sinistra
		_delay_ms(240);
		PORTA = (1<<PA1)|(1<<PA7)|(1<<PA2)|(1<<PA5);  //destra
		_delay_ms(140);
		PORTA = 0;
	}
	void stop(){
		PORTA=0;
		e=0.0, I=0.0 ,P=0.0, D=0.0, C=0.0;
		e2=0.0, I2=0.0, P2=0.0, D2=0.0, C2=0.0;
		e3=0.0, I3=0.0, P3=0.0, D3=0.0, C3=0.0;
		e4=0.0, I4=0.0, P4=0.0, D4=0.0, C4=0.0;
	}
	void ripartidestra(){
	}
	void ripartisinistra(){
	}

	void aspetta5secvittima(){
		e=0.0, I=0.0 ,P=0.0, D=0.0, C=0.0;
		e2=0.0, I2=0.0, P2=0.0, D2=0.0, C2=0.0;
		e3=0.0, I3=0.0, P3=0.0, D3=0.0, C3=0.0;
		e4=0.0, I4=0.0, P4=0.0, D4=0.0, C4=0.0;
		int xavier=0;
		if (PORTA==(1<<PA0)|(1<<PA6)|(1<<PA3)|(1<<PA4)){
			xavier=1;
		}
		if (PORTA== (1<<PA1)|(1<<PA7)|(1<<PA2)|(1<<PA5)){
			xavier=2;
		}
		PORTA=0;
		_delay_ms(5000);
		if (xavier==1){
			PORTA=(1<<PA0)|(1<<PA6)|(1<<PA3)|(1<<PA4);
		}
		if (xavier==2){
			PORTA=(1<<PA1)|(1<<PA7)|(1<<PA2)|(1<<PA5);
		}
	}
	void cm5indietro(){
		sD=0.4;
		sS=0.4;
		Kp=14.0, Ki=6.1, Kd=0.55;
		marti1=0;
		marti2=0;
		marti3=0;
		marti4=0;
		data1=0x0;
		while(martimedia<550){
			PORTA = (1<<PA0)|(1<<PA2)|(1<<PA5)|(1<<PA6);
			martimedia=(marti1+marti2+marti3+marti4)/4;
			data1=0x6;
		}
		I2C_transmitByte(data1);
		martimedia=0;
	}
	void sinistralenta(){
		PORTA = (1<<PA0)|(1<<PA6)|(1<<PA3)|(1<<PA4);
		sD=0.28;
		sS=0.28;
		Kp=4.60, Ki=2.24, Kd=0.35;
	}
	void destralenta(){
		PORTA = (1<<PA1)|(1<<PA7)|(1<<PA2)|(1<<PA5);
		sD=0.28;
		sS=0.28;
		Kp=4.60, Ki=2.24, Kd=0.35;
		
	}
	void ostacolodestra(){
		sD=0.4;
		sS=0.4;
		Kp=14.0, Ki=6.1, Kd=0.55;
		marti1=0;
		marti2=0;
		marti3=0;
		marti4=0;
		data1=0x0;
		while(martimedia<350){
			PORTA = (1<<PA0)|(1<<PA2)|(1<<PA5)|(1<<PA6);
			martimedia=(marti1+marti2+marti3+marti4)/4;
			data1=0x6;
		}
		PORTA = (1<<PA0)|(1<<PA6)|(1<<PA3)|(1<<PA4);
		_delay_ms(200);
		I2C_transmitByte(data1);
		martimedia=0;
		
	}
	void ostacolosinistra(){
		sD=0.4;
		sS=0.4;
		Kp=14.0, Ki=6.1, Kd=0.55;
		marti1=0;
		marti2=0;
		marti3=0;
		marti4=0;
		data1=0x0;
		while(martimedia<350){
			PORTA = (1<<PA0)|(1<<PA2)|(1<<PA5)|(1<<PA6);
			martimedia=(marti1+marti2+marti3+marti4)/4;
			data1=0x6;
		}
		PORTA = (1<<PA1)|(1<<PA7)|(1<<PA2)|(1<<PA5);
		_delay_ms(200);
		I2C_transmitByte(data1);
		martimedia=0;
		
	}
	while(1){

		while((PINF&0b00001000)!=0){
			if (data==0x1)    //AVANTI
			{
				avanti();
			}

			if (data==0){       //fermo
				fermo();
				sS=0.4;
				sD=0.4;
			}
			
			if (data==0x05){		//DESTRA
				destra();
			}
			
			if (data==0x06){		//SINISTRA
				sinistra();
			}
			
			if (data==0x07){		//INDIETRO
				indietro();
			}
			
			if (data==0x2){		//FAI 30 CM PRECISI
				cm30();
				
			}
			
			if (data==0x3){		//fai 5 cm precisi
				cm5();
			}
			
			if (data==0x4){		//CORREZZIONE A SINISTRA
				retromarcia();
			}
			
			if (data==0x11){		//CORREZZIONE A SINISTRA
				carroarmatodestra();
			}
			
			if (data==0x12){		//CORREZZIONE A SINISTRA
				carroarmatosinistra();
			}
			
			if (data==0x13){
				ripartidestra();   //faccio ripartire con correzione del pid
			}
			if (data==0x14){
				ripartisinistra();  //faccio ripartire con correzione del pid
			}
			
			if (data==0x16){
				addossoalmurosinistra();
			}
			
			if (data==0x15){
				addossoalmurodestra();
			}
			if (data==0x17){
				stop();
				data1=0x6;
				I2C_transmitByte(data1);
			}
			if (data==0x18){
				aspetta5secvittima();
			}
			if (data==0x20){
				cm5indietro();
			}
			if (data==0x21){
				Kp=4.60, Ki=2.24, Kd=0.35;
				sinistralenta();
			}
			if (data==0x22){
				Kp=4.60, Ki=2.24, Kd=0.35;
				destralenta();
			}
			if (data==0x23){
				ostacolosinistra();
			}
			if (data==0x24){
				ostacolodestra();
			}
		}
		PORTA=0;
		data1=0;
	}
}