package com.vonage.uploadapp;
import com.google.gson.JsonObject;

import org.json.JSONObject;

import retrofit.Callback;
import retrofit.http.Body;
import retrofit.http.GET;
import retrofit.http.PUT;
import retrofit.http.Path;

public class RestCall {

    public static String BASEURL = "http://192.168.1.104:8000";
    // public static String BASEURL="https://tbaxwkhma4.execute-api.us-east-1.amazonaws.com/beta";

    public static String WAV_ENCODE = "Hi Alon";

    public interface VMos {
        @GET("/bins/1w1ac") // specify the sub url for the base url
        void getData(Callback<JSONObject> callback); // will give you the json data
        @PUT("/{bucket_key}/{file_name}")
        void updateVMOSResult(@Path("bucket_key") String bucketKey,
                              @Path("file_name") String fileName,
                              @Body String encoded_string,
                              Callback<JSONObject> callback);
        @GET("/")
        void getTest(Callback<JSONObject> callback);
        @PUT("/{file_name}")
        void updateTest( @Path("file_name") String filename,
                         @Body String encoded_string,
                         Callback<JSONObject> callback);
    }

}


