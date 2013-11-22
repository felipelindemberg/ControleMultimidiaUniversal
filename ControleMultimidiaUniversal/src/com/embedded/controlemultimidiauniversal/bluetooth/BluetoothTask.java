package com.embedded.controlemultimidiauniversal.bluetooth;

import java.io.IOException;
import java.io.InputStream;
import java.util.UUID;

import com.embedded.controlemultimidiauniversal.IApplicationManager;
import com.embedded.controlemultimidiauniversal.INamedRoom;
import com.embedded.controlemultimidiauniversal.MainActivity;
import com.embedded.controlemultimidiauniversal.net.SearchResidenceTask;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.os.AsyncTask;
import android.util.Log;

public class BluetoothTask extends AsyncTask<Void, Void, String> {

	private final String mSERVICE_NAME = "Controll_Service";
	private final UUID mSEVICE_UUID = UUID
			.fromString("5b731005-45cc-4225-bb8e-7df99c1e25cc");

	private final MainActivity activityNamedRoom;

	private BluetoothServerSocket serverSocket = null;
	private BluetoothSocket socket = null;

	public BluetoothTask(MainActivity activityNamedRoom) {
		this.activityNamedRoom = activityNamedRoom;
	}

	@Override
	protected String doInBackground(Void... params) {

		BluetoothAdapter bluetoothAdapter = BluetoothAdapter
				.getDefaultAdapter();
		try {
			serverSocket = bluetoothAdapter
					.listenUsingInsecureRfcommWithServiceRecord(mSERVICE_NAME,
							mSEVICE_UUID);
		} catch (IOException e) {
			Log.d("Deb", e.getMessage());
		}

		while (!Thread.interrupted()) {
			try {
				socket = serverSocket.accept();
				if (socket != null) {
					InputStream inputStream = socket.getInputStream();
					return getStringFromInputStrem(inputStream);
				}
			} catch (Exception e) {
			}
		}
		return null;
	}

	private static String getStringFromInputStrem(InputStream inputStream) {
		byte[] buffer = new byte[1024];
		int bytes;
		String readMessage = "";
		try {
			bytes = inputStream.read(buffer);
			readMessage = new String(buffer, 0, bytes);
		} catch (IOException e) {
		}
		return readMessage;
	}

	@Override
	protected void onPostExecute(String result) {
		try {
			socket.close();
		} catch (Exception e) {
		}
		activityNamedRoom.setNameRoom(result);
	}
}
