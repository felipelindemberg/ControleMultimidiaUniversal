package com.embedded.controlemultimidiauniversal.net;

import java.net.InetAddress;
import java.net.NetworkInterface;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.conn.util.InetAddressUtils;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.os.AsyncTask;
import android.util.Log;

import com.embedded.controlemultimidiauniversal.ApplicationManager;
import com.embedded.controlemultimidiauniversal.DefinedIP;
import com.embedded.controlemultimidiauniversal.MainActivity;
import com.embedded.controlemultimidiauniversal.R;

public class SearchResidence extends AsyncTask<Void, Void, String> {

	private ProgressDialog pd = null;
	private final String DEFAULT_IP = "192.168.2.5";
	private DefinedIP activityMain;
	private ApplicationManager applicationManager;

	public SearchResidence(DefinedIP activityMain,
			ApplicationManager activityContextApplication) {
		this.activityMain = activityMain;
		this.applicationManager = activityContextApplication;
	}

	@Override
	protected void onPreExecute() {

		pd = ProgressDialog.show(
				applicationManager.getContext(),
				applicationManager.getContext().getString(
						R.string.progress_dialog_searchTitle),
				applicationManager.getContext().getString(
						R.string.progress_dialog_searchText), true);
		pd.setCancelable(false);

	}

	private String getIPv4() {
		try {
			List<NetworkInterface> interfaces = Collections
					.list(NetworkInterface.getNetworkInterfaces());
			for (NetworkInterface intf : interfaces) {
				List<InetAddress> addrs = Collections.list(intf
						.getInetAddresses());
				for (InetAddress addr : addrs) {
					if (!addr.isLoopbackAddress()) {
						String sAddr = addr.getHostAddress();
						boolean isIPv4 = InetAddressUtils.isIPv4Address(sAddr);
						if (isIPv4)
							return sAddr;
					}
				}
			}
		} catch (Exception ex) {
		}
		return "";
	}

	private String getFormatedIPv4() {
		String ipV4 = getIPv4();
		String[] ipSplited = ipV4.split("\\.");
		return ipSplited[0] + "." + ipSplited[1] + ".";
	}

	@Override
	protected String doInBackground(Void... params) {
		Map<String, String> param = new HashMap<String, String>();
		String url;
		String ipV4 = (!MainActivity.D ? getFormatedIPv4() : DEFAULT_IP);
		try {
			for (int i = 0; i <= 3; i++) {
				for (int j = 0; j <= 255; j++) {
					param.put("address", "http://" + ipV4 + String.valueOf(i)
							+ "." + String.valueOf(j) + ":5432");
					url = HttpSenderTask.createURL(param);

					HttpClientConnection httpClientConnection;
					HttpResponse response = null;

					httpClientConnection = new HttpClientConnection(url,
							HttpProtocol.GET);
					response = httpClientConnection.execute();
					Log.d(MainActivity.TAG, url);
					int statusCode = NetUtils.getHttpResponse(response);
					if (statusCode == HttpStatus.SC_OK) {
						try {
							String message = NetUtils.readResponse(response);
							if (message
									.equals("Welcome to Control multimedia Universal!")) {
								return url;
							}
						} catch (Exception e) {
							return null;
						}
					}
				}
			}

		} catch (Exception e) {
			Log.e("info", e.getMessage());
			return null;
		}
		return null;
	}

	@Override
	protected void onPostExecute(String result) {
		pd.dismiss();
		if (result != null) {
			activityMain.setIP(result);
		} else {
			final AlertDialog.Builder builder = new AlertDialog.Builder(
					applicationManager.getContext());
			builder.setMessage(
					applicationManager.getContext().getString(
							R.string.confirm_dialog_searchTitle))
					.setPositiveButton(
							applicationManager.getContext().getString(
									R.string.confirm_dialog_yes),
							new DialogInterface.OnClickListener() {
								public void onClick(DialogInterface dialog,
										int id) {
									builder.create();
									onCancelled();
									new SearchResidence(activityMain,
											applicationManager).execute();
								}
							})
					.setNegativeButton(
							applicationManager.getContext().getString(
									R.string.confirm_dialog_no),
							new DialogInterface.OnClickListener() {
								public void onClick(DialogInterface dialog,
										int id) {
									applicationManager.closeApplication();
								}
							});
			builder.setCancelable(false);
			builder.show();
		}
	}

}
