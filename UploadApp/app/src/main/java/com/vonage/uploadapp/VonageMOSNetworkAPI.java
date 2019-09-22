package com.vonage.uploadapp;

import com.google.gson.JsonObject;

import retrofit.http.Body;
import retrofit.http.PUT;
import retrofit.http.Path;

interface VonageMOSNetworkAPI {

    @PUT("{bucket_key}/{file_name}")
    JsonObject updateVMOSResult(@Path("bucket_key") String bucketKey,
                                @Path("file_name") String fileName,
                                @Body String encoded_string);

}
//public interface VonageMOSNetworkAPI {
//}


