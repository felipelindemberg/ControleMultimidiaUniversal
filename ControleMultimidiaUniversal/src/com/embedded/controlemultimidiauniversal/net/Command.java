package com.embedded.controlemultimidiauniversal.net;

/**
 * Lista de comandos para controlar os aparelhos do cômodo.
 * 
 * @author felipemm
 * 
 */
public enum Command {
	POWER("POWER"), UPVOLUME("UPVOLUME"), DOWNVOLUME("DOWNVOLUME"), UPCHANNEL(
			"UPCHANNEL"), DOWNCHANNEL("DOWNCHANNEL"), MUTE("MUTE");

	private String name;

	private Command(String stringVal) {
		name = stringVal;
	}

	public String toString() {
		return name;
	}

	public static String getEnumByString(String code) {
		for (Command e : Command.values()) {
			if (code == e.name)
				return e.name();
		}
		return null;
	}
}