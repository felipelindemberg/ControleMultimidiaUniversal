package com.embedded.controlemultimidiauniversal.net;

import java.io.IOException;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;

import android.util.Log;

import com.embedded.controlemultimidiauniversal.MainActivity;

public class HttpClientConnection {
	private HttpClient mHttpClient;
	private HttpGet mGet;
	private HttpPost mPost;
	private final int TIMEOUT_CONNECTION = 50;
	private final int TIMEOUT_SOCKET = 50;

	public HttpClientConnection(String url, HttpProtocol httpProtocol) {

		HttpParams httpParameters = new BasicHttpParams();
		HttpConnectionParams.setConnectionTimeout(httpParameters,
				TIMEOUT_CONNECTION);
		HttpConnectionParams.setSoTimeout(httpParameters, TIMEOUT_SOCKET);

		mHttpClient = new DefaultHttpClient(httpParameters);

		switch (httpProtocol) {
		case GET:
			mGet = new HttpGet(url);
			break;

		case POST:
			mPost = new HttpPost(url);
			break;
		}

	}

	public HttpResponse execute() {
		try {
			if (mGet != null) {
				return mHttpClient.execute(mGet);
			} else if (mPost != null) {
				return mHttpClient.execute(mPost);
			}
		} catch (ClientProtocolException e) {
			if (MainActivity.D)
				Log.d(getClass().getSimpleName(), "ClientProtocolException");
			return null;
		} catch (IOException e) {
			if (MainActivity.D)
				Log.d(getClass().getSimpleName(), "IOException");
			return null;
		}
		return null;
	}
}
