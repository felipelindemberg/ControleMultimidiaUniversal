package com.embedded.controlemultimidiauniversal.net;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import org.apache.http.HttpResponse;

import com.embedded.controlemultimidiauniversal.MainActivity;

import android.util.Log;

public class NetUtils {

	private static final int STATUS_FAILED = -1;

	/**
	 * Return the HttpStatus of the network request
	 * 
	 * @param response
	 *            The HttpResponse object
	 * @return The HttpStatus code
	 */
	public static int getHttpResponse(HttpResponse response) {
		 int status = STATUS_FAILED;
	        if (response != null && response.getStatusLine() != null) {
	            status = response.getStatusLine().getStatusCode();
	        }
	        return status;
	}

	public static String readResponse(HttpResponse response) {
		BufferedReader rd;
		String webServiceInfo = "";
		String message = "";
		try {
			rd = new BufferedReader(new InputStreamReader(response.getEntity()
					.getContent()));
			while ((webServiceInfo = rd.readLine()) != null) {
				Log.d("info", webServiceInfo);
				message += webServiceInfo;
			}
		} catch (Exception e) {
			if (MainActivity.D)
				Log.d(MainActivity.TAG, e.getMessage());
		}

		return message;
	}
}
