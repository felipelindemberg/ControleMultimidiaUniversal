package com.embedded.controlemultimidiauniversal.net;

/**
 * Lista de comandos para controlar os aparelhos do cômodo.
 * 
 * @author felipemm
 * 
 */
public enum Command {
	POWER("power"), UP_VOLUME("upVolume"), DOWN_VOLUME("downVolume"), UP_CHANNEL(
			"upChannel"), DOWN_CHANNEL("downChannel"), MUTE("mute");

	String command;

	Command(String command) {
		this.command = command;
	}

	public String toString() {
		return command;
	}
}