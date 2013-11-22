package com.embedded.controlemultimidiauniversal;

import java.util.HashMap;
import java.util.Map;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Fragment;
import android.app.FragmentManager;
import android.content.Context;
import android.content.DialogInterface;
import android.content.res.Configuration;
import android.os.Bundle;
import android.support.v4.app.ActionBarDrawerToggle;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.RadioButton;
import android.widget.Toast;

import com.embedded.controlemultimidiauniversal.bluetooth.BluetoothTask;
import com.embedded.controlemultimidiauniversal.net.Command;
import com.embedded.controlemultimidiauniversal.net.HttpSenderTask;
import com.embedded.controlemultimidiauniversal.net.SearchResidenceTask;

public class MainActivity extends Activity implements IDefinedIP,
		IApplicationManager, INamedRoom {

	private String nameRoom;
	private String address;
	private Equipment equipment = Equipment.TV;

	private DrawerLayout mDrawerLayout;
	private ListView mDrawerList;
	private ActionBarDrawerToggle mDrawerToggle;

	private Context context;

	private CharSequence mDrawerTitle;
	private CharSequence mTitle;
	private String[] optionsTitles;

	public static boolean D = false;
	public static final String TAG = "Debug_Controle";

	@Override
	public void setIP(String ipAdrress) {
		address = ipAdrress;
	}

	@Override
	public Context getContext() {
		return context;
	}

	@Override
	public void setNameRoom(String nameRoom) {
		if (nameRoom != null && !nameRoom.isEmpty()) {
			Log.d("CONNECTED", "Name "+nameRoom);
			this.nameRoom = nameRoom;
			Log.d("CONNECTED", "This "+nameRoom);
			Toast.makeText(getBaseContext(),getString(R.string.text_roomChanged), Toast.LENGTH_SHORT).show();
			setTitle(nameRoom);
		}
	}

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		context = this;
		new BluetoothTask(this).execute();
		//new SearchResidence(this, this).execute();
		createMenu();
		if (D) {
			nameRoom = "Teste";
		}
	}

	private void createMenu() {
		loadParametersForMenu();
		createActionBarDrawerToggle();
		showControlScreenFragment();
	}

	private void loadParametersForMenu() {
		mTitle = mDrawerTitle = getTitle();
		optionsTitles = getResources().getStringArray(R.array.options_array);
		mDrawerLayout = (DrawerLayout) findViewById(R.id.drawer_layout);
		mDrawerList = (ListView) findViewById(R.id.left_drawer);

		mDrawerLayout.setDrawerShadow(R.drawable.drawer_shadow,
				GravityCompat.START);

		mDrawerList.setAdapter(new ArrayAdapter<String>(this,
				R.layout.drawer_list_item, optionsTitles));
		mDrawerList.setOnItemClickListener(new DrawerItemClickListener());
		mDrawerLayout.setDrawerListener(mDrawerToggle);
	}

	private void createActionBarDrawerToggle() {
		getActionBar().setDisplayHomeAsUpEnabled(true);
		getActionBar().setHomeButtonEnabled(true);
		mDrawerToggle = new ActionBarDrawerToggle(this, mDrawerLayout,
				R.drawable.ic_drawer, R.string.drawer_open,
				R.string.drawer_close) {
			public void onDrawerClosed(View view) {
				getActionBar().setTitle(mTitle);
				invalidateOptionsMenu();
			}

			public void onDrawerOpened(View drawerView) {
				getActionBar().setTitle(mDrawerTitle);
				invalidateOptionsMenu();
			}
		};
	}

	private void showControlScreenFragment() {
		Fragment fragment = new ControlScreen();

		FragmentManager fragmentManager = getFragmentManager();
		fragmentManager.beginTransaction()
				.replace(R.id.content_frame, fragment).commit();
	}

	public static class ControlScreen extends Fragment {

		@Override
		public View onCreateView(LayoutInflater inflater, ViewGroup container,
				Bundle savedInstanceState) {
			View rootView = inflater.inflate(R.layout.control_screen,
					container, false);
			return rootView;
		}
	}

	public void onClick_checkBox(View view) {
		boolean checked = ((RadioButton) view).isChecked();

		switch (view.getId()) {
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

		case R.id.buttonPower:
			command = Command.POWER;
			break;
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
			command = Command.MUTE;
			break;
		}

		if (D)
			Log.d(TAG, "Enviando comando: " + command.toString());

		params.put("command", command.toString());
		params.put("nameRoom", nameRoom);

		url = HttpSenderTask.createURL(params, nameRoom, equipment, command);
		new HttpSenderTask().execute("post", url);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.main, menu);
		return super.onCreateOptionsMenu(menu);
	}

	@Override
	public boolean onPrepareOptionsMenu(Menu menu) {
		return super.onPrepareOptionsMenu(menu);
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		if (mDrawerToggle.onOptionsItemSelected(item)) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}

	private class DrawerItemClickListener implements
			ListView.OnItemClickListener {
		@Override
		public void onItemClick(AdapterView<?> parent, View view, int position,
				long id) {
			selectItem(position);
		}
	}

	private void selectItem(int position) {
		switch (position) {
		case 0:
			initiatePopup(R.layout.popup_sleep);
			break;
		case 1:
			initiatePopup(R.layout.popup_list_rooms);
			break;
		}
		mDrawerList.setItemChecked(position, true);
		setTitle(optionsTitles[position]);
		mDrawerLayout.closeDrawer(mDrawerList);
	}

	@Override
	public void setTitle(CharSequence title) {
		if (nameRoom == null)
			mTitle = title;
		else
			mTitle = nameRoom;
		getActionBar().setTitle(mTitle);
	}

	@Override
	protected void onPostCreate(Bundle savedInstanceState) {
		super.onPostCreate(savedInstanceState);
		mDrawerToggle.syncState();
	}

	@Override
	public void onConfigurationChanged(Configuration newConfig) {
		super.onConfigurationChanged(newConfig);
		mDrawerToggle.onConfigurationChanged(newConfig);
	}

	private void initiatePopup(int layoutId) {
		try {
			AlertDialog.Builder builder = new AlertDialog.Builder(this);

			LayoutInflater inflater = this.getLayoutInflater();

			builder.setView(inflater.inflate(layoutId, null))
					.setPositiveButton("Confirmar",
							new DialogInterface.OnClickListener() {
								@Override
								public void onClick(DialogInterface dialog,
										int id) {
									setTitle(getString(R.string.app_name));
								}
							})
					.setNegativeButton("Cancelar",
							new DialogInterface.OnClickListener() {
								public void onClick(DialogInterface dialog,
										int id) {
									setTitle(getString(R.string.app_name));
								}
							});
			builder.create();
			builder.show();

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Override
	public void closeApplication() {
		finish();
	}

}
