package com.vonage.uploadapp;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Environment;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
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

    private static final String RECORDED_DEVICE_DIR = "/Music";
    private Button sendButton;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE)
                != PackageManager.PERMISSION_GRANTED) {
            // Permission is not granted
            // Should we show an explanation?
            if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                    Manifest.permission.READ_CONTACTS)) {
                // Show an explanation to the user *asynchronously* -- don't block
                // this thread waiting for the user's response! After the user
                // sees the explanation, try again to request the permission.
            } else {
                // No explanation needed; request the permission
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.READ_EXTERNAL_STORAGE, Manifest.permission.WRITE_EXTERNAL_STORAGE},1);

                // MY_PERMISSIONS_REQUEST_READ_CONTACTS is an
                // app-defined int constant. The callback method gets the
                // result of the request.
            }
        } else {
            // Permission has already been granted
            Log.e("Info", "Permission is  granted");
        }



        this.sendButton = (Button)this.findViewById(R.id.send);
        this.sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                uploadFile();

            }
        });
    }
    //----------------------------------------------------------------------
    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String[] permissions, int[] grantResults) {
        switch (requestCode) {
            case 1: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    // permission was granted, yay! Do the
                    // contacts-related task you need to do.
                } else {
                    // permission denied, boo! Disable the
                    // functionality that depends on this permission.
                }
                return;
            }

            // other 'case' lines to check for other
            // permissions this app might request.
        }
    }
    //----------------------------------------------------------------------
    private void uploadFile(){


        String encodedFile = "";
        try {

            String baseDir = Environment.getExternalStorageDirectory().getAbsolutePath();
            String fileName = "/MyTest.wav";
            String fullPath = baseDir + RECORDED_DEVICE_DIR + fileName;
            // Not sure if the / is on the path or not
            File f = new File(fullPath);
            //FileInputStream fiStream = new FileInputStream(f);

            //byte[] bytes = null;

            // You might not get the whole file, lookup File I/O examples for Java
            //fiStream.read(bytes);
            //fiStream.close();
            encodedFile = encodeFileToBase64Binary(f);
            //encodedFile = Base64.encodeToString(source.getBytes("utf-8"), Base64.DEFAULT);

        }
        catch (IOException ioException) {
            //Logger.get().debug(ILogger.eTag.ACTIVITIES,"Error load and encoding file");
            Log.e("Encode", ioException.toString());
        }
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
        client.updateTest("wav_test",encodedFile,new Callback<JSONObject>() {
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
    //----------------------------------------------------------------------
    private static String encodeFileToBase64Binary(File file)
            throws IOException {

        byte[] bytes = loadFile(file);
        byte[] encoded = Base64.encode(bytes ,DEFAULT);
        String encodedString = new String(encoded);

        return encodedString;
    }
    //----------------------------------------------------------------------
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
