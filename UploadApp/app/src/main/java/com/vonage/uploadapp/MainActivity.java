package com.vonage.uploadapp;

import android.content.Context;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.google.gson.JsonObject;
import com.squareup.okhttp.Interceptor;
import com.squareup.okhttp.OkHttpClient;

import org.json.JSONObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.net.URI;
import java.net.URLEncoder;

import retrofit.Callback;
import retrofit.RestAdapter;
import retrofit.RetrofitError;
import retrofit.client.OkClient;
import retrofit.client.Request;
import retrofit.client.Response;

import static android.util.Base64.DEFAULT;

public class MainActivity extends AppCompatActivity {

    private Button sendButton;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //restCallPut();

        this.sendButton = (Button)this.findViewById(R.id.send);
        this.sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //restCallGet();
                restCallPut();

            }
        });
    }

    //---------------------------------REST-----------------------------------------------------//
    private void restCallGet() {

        //Creating a rest adapter
        RestAdapter.Builder builder =
                new RestAdapter.Builder()
                        .setEndpoint(RestCall.BASEURL)
                        .setClient(
                                new OkClient(new OkHttpClient())
                        );

        RestAdapter adapter = builder.build();
        RestCall.VMos client = adapter.create(RestCall.VMos.class);

        //Defining the method
        client.getTest(new Callback<JSONObject>() {
            @Override
            public void success(JSONObject json_response, Response response) {
                if (json_response != null) {

                }
                Log.e("Response", response.toString());
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e("Failed to Connect REST", "" + error.getCause());
            }
        });
    }
    private void restCallPut(){
        //Creating a rest adapter
        RestAdapter.Builder builder =
                new RestAdapter.Builder()
                        .setEndpoint(RestCall.BASEURL)
                        .setClient(
                                new OkClient(new OkHttpClient())
                        );

        RestAdapter adapter = builder.build();
        RestCall.VMos client = adapter.create(RestCall.VMos.class);

        String source = "Hi Alon";

        String encodedFile = "";
        try {
            //encodedFile = encodeFileToBase64Binary(file);
            encodedFile = Base64.encodeToString(source.getBytes("utf-8"), Base64.DEFAULT);

        }
        catch (IOException ioException) {
            //Logger.get().debug(ILogger.eTag.ACTIVITIES,"Error load and encoding file");
            Log.e("Encode", ioException.toString());
        }
        //Defining the method
        //client.updateVMOSResult("","",RestCall.WAV_ENCODE,new Callback<JSONObject>() {
        client.updateTest("wav_test",source,new Callback<JSONObject>() {
            @Override
            public void success(JSONObject json_response, Response response) {
                if (json_response != null) {

                }
                Log.e("Response", response.toString());
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e("Failed to Connect REST", "" + error.getCause());
            }
        });

    }

        //---------------------*** END REST ***-----------------------------------------------------//
    /*

        private static void uploadToS3(Context context, String bucket, String dir, File file) {
        //Logger.get().debug(ILogger.eTag.ACTIVITIES, "VoxipDevModeHandler:uploadToS3() with dir: " + dir + " bucket: " + bucket + " file: " + file.getName());

        if (!file.exists()) {
            //Logger.get().warn(ILogger.eTag.ACTIVITIES, "VoxipDevModeHandler:uploadToS3 current File: " + file + " does not exists");
            return;
        }
        String encodedFile = "";
        try {
            encodedFile = encodeFileToBase64Binary(file);
        }
        catch (IOException ioException) {
            //Logger.get().debug(ILogger.eTag.ACTIVITIES,"Error load and encoding file");
        }

        String fileToUploadKey = dir + file.getName();
        //Replace to request
        //Logger.get().debug(ILogger.eTag.ACTIVITIES,"Start upload file");
        String API_BASE_URL = "https://tbaxwkhma4.execute-api.us-east-1.amazonaws.com/beta/";

        OkHttpClient client = new OkHttpClient();

        client.interceptors().add(new  Interceptor(){
            @Override
            public Response intercept(Chain chain) throws IOException{

                Request request = chain.request();
                Response response = chain.proceed(request);
                response.code();//status code
                return response;

            }});
        String encodedFileName = "";
        try {
            encodedFileName = URLEncoder.encode(fileToUploadKey, "UTF-8");
        }
        catch (UnsupportedEncodingException e){
            //Logger.get().debug(ILogger.eTag.ACTIVITIES,e.getMessage());
        }

        RestAdapter.Builder builder =
                new RestAdapter.Builder()
                        .setEndpoint(API_BASE_URL)
                        .setClient(new OkClient(client));

        RestAdapter adapter = builder.build();

        VonageMOSNetworkAPI adapterClient = adapter.create(VonageMOSNetworkAPI.class);
        JsonObject jsonRet = adapterClient.updateVMOSResult( bucket ,encodedFileName, encodedFile);
        //Logger.get().debug(ILogger.eTag.ACTIVITIES,jsonRet.getAsString());
        //Logger.get().debug(ILogger.eTag.ACTIVITIES,"**** Done upload file ****");
    }
*/
    private static String encodeFileToBase64Binary(File file)
            throws IOException {

        byte[] bytes = loadFile(file);
        byte[] encoded = Base64.encode(bytes ,DEFAULT);
        String encodedString = new String(encoded);

        return encodedString;
    }

    private static byte[] loadFile(File file) throws IOException {
        InputStream is = new FileInputStream(file);

        long length = file.length();
        if (length > Integer.MAX_VALUE) {
            // File is too large
        }
        byte[] bytes = new byte[(int)length];

        int offset = 0;
        int numRead = 0;
        while (offset < bytes.length
                && (numRead=is.read(bytes, offset, bytes.length-offset)) >= 0) {
            offset += numRead;
        }

        if (offset < bytes.length) {
            throw new IOException("Could not completely read file "+file.getName());
        }

        is.close();
        return bytes;
    }
}
