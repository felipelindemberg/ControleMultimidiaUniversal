package com.embedded.controlemultimidiauniversal;

import java.util.HashMap;
import java.util.Map;

import android.app.Activity;
import android.app.Fragment;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.RadioGroup;
import android.widget.RadioGroup.OnCheckedChangeListener;

import com.embedded.controlemultimidiauniversal.bluetooth.BluetoothServiceReceive;
import com.embedded.controlemultimidiauniversal.bluetooth.BluetoothServiceSender;
import com.embedded.controlemultimidiauniversal.net.Command;
import com.embedded.controlemultimidiauniversal.net.HttpSenderTask;
import com.embedded.controlemultimidiauniversal.net.SearchResidence;

public class ControlFragment extends Fragment {

	private Equipment equipment = Equipment.TV;
	private String address;
	private String nameRoom = "Teste";
	private MainActivity mainActivity;
	private Activity activity;

	private BluetoothServiceReceive bluetoothServiceReceive;

	public ControlFragment(MainActivity mainActivity) {
		this.mainActivity = mainActivity;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		activity = super.getActivity();
		
		View view = inflater.inflate(R.layout.control, container, false);
		createRadioGroupEvent(view);
		createButtonsEvent(view);
		createBluetoothServiceIntent();
		callSearchResidence();
		return view;
	}

	private void createBluetoothServiceIntent() {
		IntentFilter filter = new IntentFilter(
				BluetoothServiceReceive.BLUETOOTH_RESULT);
		filter.addCategory(Intent.CATEGORY_DEFAULT);
		bluetoothServiceReceive = new BluetoothServiceReceive(activity);
		activity.registerReceiver(bluetoothServiceReceive, filter);

		Intent msgIntent = new Intent(activity,
				BluetoothServiceSender.class);
		activity.startService(msgIntent);
	}

	public void callSearchResidence() {
		ApplicationManager applicationManager = new ApplicationManager() {

			@Override
			public Context getContext() {
				return mainActivity;
			}

			@Override
			public void closeApplication() {
				mainActivity.finish();
			}
		};

		SetableAddressRoom setableAddressRoom = new SetableAddressRoom() {

			@Override
			public void onAddressDiscovery(String addressRoom) {
				address = addressRoom;
			}
		};

		SearchResidence searchResidence = new SearchResidence(
				setableAddressRoom, applicationManager);
		searchResidence.execute();

	}

	private void createRadioGroupEvent(View view) {
		RadioGroup equipmentGroup = (RadioGroup) view
				.findViewById(R.id.radioGroupEquipments);
		equipmentGroup
				.setOnCheckedChangeListener(new OnCheckedChangeListener() {

					@Override
					public void onCheckedChanged(RadioGroup group, int checkedId) {
						switch (group.getCheckedRadioButtonId()) {
						case R.id.radioButtonTv:
							equipment = Equipment.TV;
							break;
						case R.id.radioButtonSom:
							equipment = Equipment.SOM;
							break;
						}
						if (MainActivity.D)
							Log.d(getClass().getSimpleName(),
									"Equipamento alterado: "
											+ equipment.toString());
					}
				});
	}

	private void createButtonsEvent(View view) {
		ImageButton btn_power = (ImageButton) view
				.findViewById(R.id.buttonPower);
		btn_power.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				sendCommand(Command.POWER);
			}
		});

		ImageButton btn_upChannel = (ImageButton) view
				.findViewById(R.id.buttonUpChannel);
		btn_upChannel.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				sendCommand(Command.UP_CHANNEL);
			}
		});

		ImageButton btn_doButtonChannel = (ImageButton) view
				.findViewById(R.id.buttonDownChannel);
		btn_doButtonChannel.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				sendCommand(Command.DOWN_CHANNEL);
			}
		});

		ImageButton btn_upVolume = (ImageButton) view
				.findViewById(R.id.buttonUpVolume);
		btn_upVolume.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				sendCommand(Command.UP_VOLUME);
			}
		});

		ImageButton btn_downButton = (ImageButton) view
				.findViewById(R.id.buttonDownVolume);
		btn_downButton.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				sendCommand(Command.DOWN_VOLUME);
			}
		});

		ImageButton btn_mute = (ImageButton) view.findViewById(R.id.buttonMute);
		btn_mute.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				sendCommand(Command.MUTE);
			}
		});
	}

	private void sendCommand(Command command) {
		Map<String, String> params = new HashMap<String, String>();
		String url;

		Log.i("Info", address + " " + command.toString() + " " + nameRoom + " "
				+ equipment);

		params.put("address", address);
		params.put("path", "sendCommand");

		params.put("command", command.toString());
		params.put("nameRoom", nameRoom);

		url = HttpSenderTask.createURL(params, nameRoom, equipment, command);
		new HttpSenderTask().execute("post", url);
	}
}