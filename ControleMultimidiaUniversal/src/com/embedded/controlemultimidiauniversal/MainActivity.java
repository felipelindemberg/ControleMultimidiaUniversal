package com.embedded.controlemultimidiauniversal;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.CheckBox;

public class MainActivity extends Activity {

	private CheckBox checkTv, checkSom;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		setUpSelectSom();
		setUpSelectTv();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	private void setUpSelectTv() {
		checkTv = (CheckBox) findViewById(R.id.checkBoxTv);
		checkTv.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				checkTv.setChecked(true);

				checkSom = (CheckBox) findViewById(R.id.checkBoxSom);
				checkSom.setChecked(false);

			}
		});

	}

	private void setUpSelectSom() {
		checkSom = (CheckBox) findViewById(R.id.checkBoxSom);
		checkSom.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				checkSom.setChecked(true);
				checkTv = (CheckBox) findViewById(R.id.checkBoxTv);
				checkTv.setChecked(false);

			}
		});

	}

}
