package com.embedded.controlemultimidiauniversal;

import java.util.HashMap;
import java.util.Map;

import com.embedded.controlemultimidiauniversal.net.Command;
import com.embedded.controlemultimidiauniversal.net.HttpConnectionSender;

import android.os.Bundle;
import android.app.Activity;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.webkit.WebView.FindListener;
import android.widget.CheckBox;
import android.widget.RadioButton;

public class MainActivity extends Activity {

	private RadioButton checkTv, checkSom;
	private String nameRoom;
	private String address;
	private Equipment equipment = Equipment.TV;

	public static boolean D = true;
	public static final String TAG = "Debug_Controle";

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		if (D) {
			address = "http://192.168.2.2:5432";
			nameRoom = "Teste";
		}
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	public void onClick_checkBox(View view) {
	    boolean checked = ((RadioButton) view).isChecked();
	    
	    switch(view.getId()) {
	        case R.id.checkBoxTv:
	            if (checked)
	            	equipment = Equipment.TV;
	            break;
	        case R.id.checkBoxSom:
	            if (checked)
	            	equipment = Equipment.SOM;
	            break;
	    }
	


		if (D)
			Log.d(TAG, "Equipamento alterado: " + equipment.toString());
	}

	public void onClick_buttonControlEquipment(View view) {
		Map<String, String> params = new HashMap<String, String>();
		Command command = null;
		String url;

		params.put("address", address);
		params.put("path", "sendCommand");

		switch (view.getId()) {
		/*
		 * case R.id.buttonPower: command = Command.POWER;
		 */
		case R.id.buttonUpVolume:
			command = Command.UPVOLUME;
			break;
		case R.id.buttonDownVolume:
			command = Command.DOWNVOLUME;
			break;
		case R.id.buttonUpChannel:
			command = Command.UPCHANNEL;
			break;
		case R.id.buttonDownChannel:
			command = Command.DOWNCHANNEL;
			break;
		case R.id.buttonMute:
			command = Command.DOWNCHANNEL;
			break;
		}

		if (D)
			Log.d(TAG, "Enviando comando: " + command.toString());

		params.put("command", command.toString());
		params.put("nameRoom", nameRoom);

		url = HttpConnectionSender.createURL(params, nameRoom, equipment,
				command);
		new HttpConnectionSender().execute("post", url);
	}

}
