/*
 * USART.h
 *
 * Created: 04/01/2013 11.13.28
 *  Author: roby
 */ 


#ifndef USART_H_
#define USART_H_
extern void USART_Send_float(float num);
extern void USART_Init(unsigned int BAUD);			// inizializza USART
extern void USART_Tx(unsigned char data);			// trasmetti singolo byte
extern  char USART_Rx(void);						// riceve singolo byte
extern void USART_Flush(void);						// cancella bufer di Rx
extern int8_t USART_In(void);						// c'è qualcosa in arrivo sul buffer di Rx?

extern void USART_Send_String( char* str);			// trasmetti una stringa - appoggio
extern void sendStr( char *str);					// trasmetti una stringa
extern char* USART_Receive_String(void);

extern void USART_Send_Uint(uint32_t num);			// trasmetti numero intero UNSIGNED INT 32 bit - appoggio
extern void sendUint(uint32_t num);					// trasmetti numero intero UNSIGNED INT 32 bit 

extern void USART_Send_Double(double num);			// trasmetti numero con virgola DOUBLE - appoggio

extern void USART_Send_CRLF(void);
extern void sendCRLF(void);							// trasmette il carattere CR-LF ( 0x0D+0x0A)


#endif /* USART_H_ */
