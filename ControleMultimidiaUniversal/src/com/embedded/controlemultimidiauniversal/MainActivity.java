package com.embedded.controlemultimidiauniversal;

import java.util.HashMap;
import java.util.Map;

import android.app.Activity;
import android.app.Fragment;
import android.app.FragmentManager;
import android.content.Context;
import android.content.res.Configuration;
import android.os.Bundle;
import android.support.v4.app.ActionBarDrawerToggle;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.PopupWindow;
import android.widget.RadioButton;

import com.embedded.controlemultimidiauniversal.net.Command;
import com.embedded.controlemultimidiauniversal.net.HttpConnectionSender;

public class MainActivity extends Activity {

	private String nameRoom;
	private String address;
	private Equipment equipment = Equipment.TV;

	private DrawerLayout mDrawerLayout;
	private ListView mDrawerList;
	private ActionBarDrawerToggle mDrawerToggle;

	private CharSequence mDrawerTitle;
	private CharSequence mTitle;
	private String[] mPlanetTitles;

	public static boolean D = true;
	public static final String TAG = "Debug_Controle";

	private PopupWindow popupWindow;
	private Button btnClosePopup;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		createMenu();

		if (D) {
			address = "http://192.168.2.5:5432";
			nameRoom = "Teste";
		}
	}

	private void createMenu() {
		mTitle = mDrawerTitle = getTitle();
		mPlanetTitles = getResources().getStringArray(R.array.options_array);
		mDrawerLayout = (DrawerLayout) findViewById(R.id.drawer_layout);
		mDrawerList = (ListView) findViewById(R.id.left_drawer);

		mDrawerLayout.setDrawerShadow(R.drawable.drawer_shadow,
				GravityCompat.START);

		mDrawerList.setAdapter(new ArrayAdapter<String>(this,
				R.layout.drawer_list_item, mPlanetTitles));
		mDrawerList.setOnItemClickListener(new DrawerItemClickListener());

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
		mDrawerLayout.setDrawerListener(mDrawerToggle);

		showControlScreenFragment();
	}

	public void showControlScreenFragment() {
		Fragment fragment = new ControlScreen();

		FragmentManager fragmentManager = getFragmentManager();
		fragmentManager.beginTransaction()
				.replace(R.id.content_frame, fragment).commit();
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

	public static class ControlScreen extends Fragment {
		public static final String ARG_PLANET_NUMBER = "planet_number";

		public ControlScreen() {
		}

		@Override
		public View onCreateView(LayoutInflater inflater, ViewGroup container,
				Bundle savedInstanceState) {
			View rootView = inflater.inflate(R.layout.control_screen,
					container, false);
			return rootView;
		}
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
			Log.i("Info", String.valueOf(position));
			selectItem(position);
		}
	}

	private void selectItem(int position) {
		switch (position) {
		case 0:
			initiatePopup(R.layout.popup_sleep, R.id.popupSleepElement,
					R.id.btn_close_popupSleep);
			break;

		case 1:
			initiatePopup(R.layout.popup_list_rooms, R.id.popupListRoomsElement,
					R.id.btn_close_popupListRooms);
			break;
		}
		mDrawerList.setItemChecked(position, true);
		setTitle(mPlanetTitles[position]);
		mDrawerLayout.closeDrawer(mDrawerList);
	}

	@Override
	public void setTitle(CharSequence title) {
		mTitle = title;
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

	private void initiatePopup(int layoutId, int popupElementId, int btnCloseId) {
		try {
			LayoutInflater inflater = (LayoutInflater) MainActivity.this
					.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
			View layout = inflater.inflate(layoutId,
					(ViewGroup) findViewById(popupElementId));
			popupWindow = new PopupWindow(layout, 300, 370, true);
			popupWindow.showAtLocation(layout, Gravity.CENTER, 0, 0);

			btnClosePopup = (Button) layout
					.findViewById(btnCloseId);
			btnClosePopup.setOnClickListener(cancel_button_popup);

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private OnClickListener cancel_button_popup = new OnClickListener() {
		public void onClick(View v) {
			popupWindow.dismiss();
			setTitle(getResources().getString(R.string.app_name));
		}
	};
}
