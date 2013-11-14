package com.embedded.controlemultimidiauniversal.net;

/**
 * Lista de comandos para controlar os aparelhos do cômodo.
 * 
 * @author felipemm
 * 
 */
public enum Command {
	POWER("power"), UPVOLUME("upVolume"), DOWNVOLUME("downVolume"), UPCHANNEL(
			"upChannel"), DOWNCHANNEL("downChannel"), MUTE("mute");

	String command;

	Command(String command) {
		this.command = command;
	}

	public String toString() {
		return command;
	}
}