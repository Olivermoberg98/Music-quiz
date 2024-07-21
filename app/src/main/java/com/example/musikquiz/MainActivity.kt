package com.example.musikquiz

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import androidx.activity.ComponentActivity
import com.spotify.android.appremote.api.ConnectionParams
import com.spotify.android.appremote.api.Connector
import com.spotify.android.appremote.api.SpotifyAppRemote
import com.spotify.sdk.android.auth.AuthorizationClient
import com.spotify.sdk.android.auth.AuthorizationRequest
import com.spotify.sdk.android.auth.AuthorizationResponse

class MainActivity : ComponentActivity() {

    private val REQUEST_CODE = 1337
    private val REDIRECT_URI = "musikquiz://callback"
    private val CLIENT_ID = "fa6a760e4e794ecb8c642e8d3de00b50"
    private var spotifyAppRemote: SpotifyAppRemote? = null
    private var accessToken: String? = null
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val hitsterButton: Button = findViewById(R.id.hitsterButton)
        val categoriesButton: Button = findViewById(R.id.categoriesButton)
        val duelButton: Button = findViewById(R.id.duelButton)

        hitsterButton.setOnClickListener {
            val intent = Intent(this, HitsterActivity::class.java)
            intent.putExtra("ACCESS_TOKEN", accessToken)
            startActivity(intent)
        }

        categoriesButton.setOnClickListener {
            val intent = Intent(this, CategoriesActivity::class.java)
            intent.putExtra("ACCESS_TOKEN", accessToken)
            startActivity(intent)
        }

        duelButton.setOnClickListener {
            val intent = Intent(this, DuelActivity::class.java)
            intent.putExtra("ACCESS_TOKEN", accessToken)
            startActivity(intent)
        }

        val loginButton: Button = findViewById(R.id.login_button)
        loginButton.setOnClickListener {
            val builder = AuthorizationRequest.Builder(CLIENT_ID, AuthorizationResponse.Type.TOKEN, REDIRECT_URI)
            builder.setScopes(arrayOf("streaming"))
            val request = builder.build()
            AuthorizationClient.openLoginActivity(this, REQUEST_CODE, request)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, intent: Intent?) {
        super.onActivityResult(requestCode, resultCode, intent)

        if (requestCode == REQUEST_CODE) {
            val response = AuthorizationClient.getResponse(resultCode, intent)
            when (response.type) {
                AuthorizationResponse.Type.TOKEN -> {
                    accessToken = response.accessToken
                    Log.d("MainActivity", "Access token: $accessToken")
                    connectToSpotifyAppRemote()
                }
                AuthorizationResponse.Type.ERROR -> {
                    Log.e("MainActivity", "Auth error: ${response.error}")
                }
                else -> {
                    // Handle other cases
                }
            }
        }
    }

    override fun onStart() {
        super.onStart()
        if (accessToken != null) {
            connectToSpotifyAppRemote()
        }
    }
    private fun connectToSpotifyAppRemote() {
        val connectionParams = ConnectionParams.Builder(CLIENT_ID)
            .setRedirectUri(REDIRECT_URI)
            //.setAccessToken(accessToken)
            .showAuthView(true)
            .build()

        SpotifyAppRemote.connect(this, connectionParams, object : Connector.ConnectionListener {
            override fun onConnected(appRemote: SpotifyAppRemote) {
                spotifyAppRemote = appRemote
                Log.d("MainActivity", "Connected to Spotify App Remote!")
            }

            override fun onFailure(throwable: Throwable) {
                Log.e("MainActivity", "Failed to connect to Spotify App Remote", throwable)
            }
        })
    }
}
