package com.embedded.controlemultimidiauniversal;


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
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

public class MainActivity extends Activity implements ApplicationManager {

	private String nameRoom;

	private DrawerLayout mDrawerLayout;
	private ListView mDrawerList;
	private ActionBarDrawerToggle mDrawerToggle;

	private Context context;

	private CharSequence mDrawerTitle;
	private CharSequence mTitle;
	private String[] optionsTitles;

	public static boolean D = false;
	public static boolean RUN_IN_DEVICE = false;
	public static final String TAG = "Debug_Controle";

	@Override
	public Context getContext() {
		return context;
	}

	public void setNameRoom(String nameRoom) {
		if (nameRoom != null && !nameRoom.isEmpty()) {
			this.nameRoom = nameRoom;
			Toast toast = Toast.makeText(context,
					getString(R.string.text_roomChanged), Toast.LENGTH_SHORT);
			toast.show();
			setTitle(nameRoom);
		}
	}

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		context = this;
		new  ControlFragment(this);
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
		ControlFragment fragment = new ControlFragment(this);

		FragmentManager fragmentManager = getFragmentManager();
		fragmentManager.beginTransaction()
				.replace(R.id.content_frame, fragment).commit();
	}

	public static class ControlScreen extends Fragment {

		@Override
		public View onCreateView(LayoutInflater inflater, ViewGroup container,
				Bundle savedInstanceState) {
			View rootView = inflater
					.inflate(R.layout.control, container, false);
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
			builder.setCancelable(false);
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
