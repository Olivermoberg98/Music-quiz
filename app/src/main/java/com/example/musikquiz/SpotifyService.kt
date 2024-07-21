package com.example.musikquiz

import android.app.Service
import android.content.Intent
import android.os.Binder
import android.os.IBinder
import android.util.Log
import com.spotify.android.appremote.api.ConnectionParams
import com.spotify.android.appremote.api.Connector
import com.spotify.android.appremote.api.SpotifyAppRemote

class SpotifyService : Service() {

    private val binder = LocalBinder()
    private var spotifyAppRemote: SpotifyAppRemote? = null
    private var clientId: String? = null
    private var redirectUri: String? = null

    override fun onBind(intent: Intent?): IBinder {
        return binder
    }

    inner class LocalBinder : Binder() {
        fun getService(): SpotifyService = this@SpotifyService
    }

    fun initialize(clientId: String, redirectUri: String) {
        this.clientId = clientId
        this.redirectUri = redirectUri
    }

    fun connectSpotify() {
        if (clientId == null || redirectUri == null) {
            Log.e("SpotifyService", "Client ID or Redirect URI is not set")
            return
        }

        val connectionParams = ConnectionParams.Builder(clientId!!)
            .setRedirectUri(redirectUri!!)
            .showAuthView(true)
            .build()

        SpotifyAppRemote.connect(this, connectionParams, object : Connector.ConnectionListener {
            override fun onConnected(appRemote: SpotifyAppRemote) {
                spotifyAppRemote = appRemote
                Log.d("SpotifyService", "Connected to Spotify")
            }

            override fun onFailure(throwable: Throwable) {
                Log.e("SpotifyService", "Failed to connect to Spotify", throwable)
            }
        })
    }

    fun disconnectSpotify() {
        SpotifyAppRemote.disconnect(spotifyAppRemote)
    }

    fun getSpotifyAppRemote(): SpotifyAppRemote? {
        return spotifyAppRemote
    }

    override fun onDestroy() {
        super.onDestroy()
        disconnectSpotify()
    }
}