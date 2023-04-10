#include <util/twi.h>
#include <avr/interrupt.h>

#include "I2CSlave.h"

static void (*I2C_recv)(uint8_t);
static void (*I2C_req)();

void I2C_setCallbacks(void (*recv)(uint8_t), void (*req)())
{
	I2C_recv = recv;
	I2C_req = req;
}

void I2C_init(uint8_t address)
{
	cli();
	// carica indirizzo in TWI
	TWAR = address << 1;
	// impostare TWCR per abilitare la corrispondenza degli indirizzi in  TWI, pulire TWINT, abilitare TWI interrupt
	TWCR = (1<<TWIE) | (1<<TWEA) | (1<<TWINT) | (1<<TWEN);
	sei();
}

void I2C_stop(void)
{
	// abilita bit e pulisci dati
	cli();
	TWCR = 0;
	TWAR = 0;
	sei();
}

ISR(TWI_vect)
{
	switch(TW_STATUS)
	{
		case TW_SR_DATA_ACK:
		//dati ricevuti da master, richiama il receive callback
		I2C_recv(TWDR);
		TWCR = (1<<TWIE) | (1<<TWINT) | (1<<TWEA) | (1<<TWEN);
		break;
		case TW_ST_SLA_ACK:
		// master irchiede dati, richiama il receive callback
		I2C_req();
		TWCR = (1<<TWIE) | (1<<TWINT) | (1<<TWEA) | (1<<TWEN);
		break;
		case TW_ST_DATA_ACK:
		// master irchiede dati, richiama il receive callback
		I2C_req();
		TWCR = (1<<TWIE) | (1<<TWINT) | (1<<TWEA) | (1<<TWEN);
		break;
		case TW_BUS_ERROR:
		// qualsiasi stato di errore, preparea TWI per essere reimpostato
		TWCR = 0;
		TWCR = (1<<TWIE) | (1<<TWINT) | (1<<TWEA) | (1<<TWEN);
		break;
		default:
		TWCR = (1<<TWIE) | (1<<TWINT) | (1<<TWEA) | (1<<TWEN);
		break;
	}
}