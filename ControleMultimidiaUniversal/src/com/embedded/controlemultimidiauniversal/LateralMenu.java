package com.embedded.controlemultimidiauniversal;

import android.app.Activity;
import android.app.Fragment;
import android.app.FragmentManager;
import android.content.Context;
import android.content.res.Configuration;
import android.os.Bundle;
import android.support.v4.app.ActionBarDrawerToggle;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.PopupWindow;

public class LateralMenu extends Activity {

	private CharSequence mDrawerTitle;
	private CharSequence mTitle;
	private String[] optionsTitles;
	private DrawerLayout mDrawerLayout;
	private ListView mDrawerList;
	private ActionBarDrawerToggle mDrawerToggle;

	private PopupWindow popupWindow;
	private Button btnClosePopup;

	private ApplicationManager activityContextApplication;

	public LateralMenu(ApplicationManager activityContextApplication) {
		this.activityContextApplication = activityContextApplication;
	}
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		loadParametersForMenu();
		createActionBarDrawerToggle();
		showControlScreenFragment();
	}

	private void loadParametersForMenu() {
		mTitle = mDrawerTitle = getTitle();
		optionsTitles = activityContextApplication.getContext().getResources()
				.getStringArray(R.array.options_array);
		mDrawerLayout = (DrawerLayout) ((Activity) activityContextApplication
				.getContext()).findViewById(R.id.drawer_layout);
		mDrawerList = (ListView) ((Activity) activityContextApplication
				.getContext()).findViewById(R.id.left_drawer);

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
			initiatePopup(R.layout.popup_sleep, R.id.popupSleepElement,
					R.id.btn_close_popupSleep);
			break;
		case 1:
			initiatePopup(R.layout.popup_list_rooms,
					R.id.popupListRoomsElement, R.id.btn_close_popupListRooms);
			break;
		}
		mDrawerList.setItemChecked(position, true);
		setTitle(optionsTitles[position]);
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
			LayoutInflater inflater = (LayoutInflater) activityContextApplication
					.getContext().getSystemService(
							Context.LAYOUT_INFLATER_SERVICE);
			View layout = inflater.inflate(layoutId,
					(ViewGroup) findViewById(popupElementId));
			popupWindow = new PopupWindow(layout, 300, 370, true);
			popupWindow.showAtLocation(layout, Gravity.CENTER, 0, 0);

			btnClosePopup = (Button) layout.findViewById(btnCloseId);
			btnClosePopup.setOnClickListener(cancel_button_popup);

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private OnClickListener cancel_button_popup = new OnClickListener() {
		@Override
		public void onClick(View v) {
			popupWindow.dismiss();
			setTitle(getResources().getString(R.string.app_name));
		}
	};
}
