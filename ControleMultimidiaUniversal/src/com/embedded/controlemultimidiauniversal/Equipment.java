package com.embedded.controlemultimidiauniversal;

/**
 * Lista de equipamentos a serem controlados.
 * 
 * @author felipemm
 * 
 */
public enum Equipment {
	TV("tv"), SOM("som");

	String equipment;

	Equipment(String equipment) {
		this.equipment = equipment;
	}

	public String toString() {
		return equipment;
	}
}