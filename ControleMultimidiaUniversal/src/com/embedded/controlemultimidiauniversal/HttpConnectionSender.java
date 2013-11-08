package com.embedded.controlemultimidiauniversal;

import java.security.InvalidParameterException;
import java.util.Map;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;

import android.net.Uri;
import android.net.Uri.Builder;
import android.os.AsyncTask;
import android.util.Log;

public class HttpConnectionSender extends AsyncTask<String, Void, Boolean> {

	/**
	 * M&eacute;todo que gera uma URL v&aacute;lida apartir de um Map.
	 * 
	 * @param params
	 *            Um Map com as seguintes chaves, sendo que a chave "address" &eacute; obrigat&oacute;ria:
	 *            <ul>
	 *            <li><b>address</b> - O endere&ccedil;o;</li>
	 *            <li><b>path</b> - Caminho dentro do endere&ccedil;o.</li>
	 *            </ul>
	 * @return Uma URL apartir dos dados informados.
	 * @throws InvalidParameterException
	 *             Se alguma chave for omitida no Map.
	 */
	public static String createURL(Map<String, String> params)
			throws InvalidParameterException {

		if (params.containsKey("address")) {
			Builder uriBuilder = Uri.parse(params.get("address")).buildUpon();
			uriBuilder.scheme("http");
			params.remove("address");

			if (params.containsKey("path")) {
				uriBuilder.path(params.get("path"));
				params.remove("path");

				if (params.size() > 0) {
					for (Map.Entry<String, String> e : params.entrySet())
						uriBuilder.appendQueryParameter(e.getKey().toString(),
								e.getValue().toString());
				}
				Log.i("info", uriBuilder.toString());
			}
			return uriBuilder.toString();
		} else {
			throw new InvalidParameterException("Parametro url ausente");
		}
	}

	@Override
	protected Boolean doInBackground(String... params) {
		try {

			if (params.length == 2) {
				HttpResponse response;
				HttpClient client = new DefaultHttpClient();

				String method = params[0];
				String url = params[1];

				Log.i("info", url);

				if (method.equals("get")) {
					HttpGet requestGet = new HttpGet(url);
					response = client.execute(requestGet);
				} else if (method.equals("post")) {
					HttpPost requestPost = new HttpPost(url);
					response = client.execute(requestPost);
				}

				/*
				 * Retirar o comentário caso deseje visualizar retorno do
				 * servidor.
				 * 
				 * BufferedReader rd = new BufferedReader(new InputStreamReader(
				 * response.getEntity().getContent()));
				 * 
				 * 
				 * String webServiceInfo = "";
				 * 
				 * while ((webServiceInfo = rd.readLine()) != null) {
				 * Log.d("info", webServiceInfo); }
				 */
				return true;
			}
		} catch (Exception e) {
			Log.e("info", e.getMessage());
			return false;
		}
		return false;
	}
}
