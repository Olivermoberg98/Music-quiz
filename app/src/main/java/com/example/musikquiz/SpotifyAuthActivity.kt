package com.example.spotifysdktest

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.spotify.sdk.android.auth.AuthorizationResponse

class SpotifyAuthActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // No layout needed for this activity
        handleAuthorizationResponse(intent)
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        handleAuthorizationResponse(intent)
    }

    private fun handleAuthorizationResponse(intent: Intent) {
        val uri: Uri? = intent.data
        uri?.let {
            val response = AuthorizationResponse.fromUri(uri)
            when (response.type) {
                AuthorizationResponse.Type.TOKEN -> {
                    // Handle successful response
                    val accessToken = response.accessToken
                    Log.d("SpotifyAuth", "Access Token: $accessToken")
                    // Use the access token to interact with the Spotify API
                }
                AuthorizationResponse.Type.ERROR -> {
                    Log.e("SpotifyAuth", "Error: ${response.error}")
                }
                else -> {
                    Log.d("SpotifyAuth", "Authorization canceled or failed")
                }
            }
        }
    }
}