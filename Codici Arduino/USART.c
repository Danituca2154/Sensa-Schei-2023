/*
 * USART.c
 *
 * Created: 04/01/2013 11.13.17
 *  Author: roby
 */ 
#define F_CPU 16000000UL
#include <avr/io.h>
#include <avr/delay.h>

void USART_Init(unsigned int BAUD)
{
	// setta baud rate
	//unsigned int val;
	//val=(F_CPU/16/BAUD)-1;
	//UBRR0=val;
	
	UBRR0H= (unsigned char) (BAUD>>8);
	UBRR0L=(unsigned char) (BAUD);
	// UBRR0 = BAUD
	// abilita Tx e Rx
	UCSR0B=(1<<RXEN0) | (1<<TXEN0);
	// settaggio frame : 1 bit stop, 8 bit dati, nessuna parità:
	UCSR0C=(0<<USBS0) | (1<<UCSZ01) | (1<<UCSZ00) | (0<<UPM01) |(0<UPM00);
	//      bit stop            8 bit dati             parità : NONE
}

void USART_Tx(unsigned char data)
{
	// aspetta finchè il buffer di Tx non è vuoto
	while( !(UCSR0A & (1<<UDRE0)));
	UDR0=data;
}

 unsigned char USART_Rx(void)
{
	// aspetta finchè il buffer di Rx non è vuoto
    	while(!(UCSR0A & (1<<RXC0)));
    //if (!(UCSR0A & (1<<RXC0)))   // se non c'è nulla in ricezione ---> oppure commentare il while e scommentare l'if
    //{
		//return 0;			
    //}
	//else 
	//{
       return UDR0;
	//}	
}

int8_t USART_In(void)
{
	int8_t b;
	b=0;
	if ( UCSR0A & (1<<RXC0) ){ b=1;}
	return b;
}

void USART_Flush(void)
{
	unsigned char dummy;
	while(UCSR0A & (1<<RXC0)) dummy=UDR0;
}

void USART_Send_String(char* str)
{
	while(*str)				// molto sintetica
	{
		USART_Tx(*str);
		str++;
	}	
}
void USART_Send_CRLF()
{
	USART_Tx(13);
	USART_Tx(10);
}

void sendCRLF()
{
	USART_Send_CRLF();
}
void sendStr(char *str)
{
	USART_Send_String(str);
}

char* USART_Receive_String()
{
	char str[10];
	char rec;
	char i=0;
	while(USART_In()) 
	
	{    
		PORTA=2;
		_delay_ms(500);
		PORTA=0;
		_delay_ms(500);
        rec=USART_Rx();
		//str[i++]=rec;
	}
	return str;
}

void USART_Send_Uint(int32_t num)
{
    if(num<0)
    {
        USART_Send_String("-");
        num=-num;
    }
    if(num==0) {USART_Send_String("0");}
else{
    char str[10];
    char i;
    for(i=0;i<10;i++) str[i]=0; // cancella la stringa ( 0000000000 )
    i=9;
    while (num)
    {
        str[i]=num%10+'0';
        num/=10;
        i--;
    }
    for (i=0;i<10;i++)
        if (str[i]) USART_Tx(str[i]);
 }
}

void sendUint(uint32_t num)
{
	USART_Send_Uint(num);
}

void USART_Send_Double(double num)
{
	
}

void USART_Send_float(float num)
{
	if(num<0){
		USART_Send_String("-");
		num=-num;
	}
	int size=3;
	int var=num;
	float num1=num*pow(10,size);
	USART_Send_Uint(var);
	USART_Send_String(".");
	var=var*pow(10,size);
	num1=num1-var;
	var=num1;
	if (var<100){USART_Send_String("0");}
	if (var<10){USART_Send_String("0");}
	USART_Send_Uint(var);
}
