package com.example.musikquiz

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.Toast
import androidx.activity.ComponentActivity
import com.google.zxing.integration.android.IntentIntegrator
import com.google.zxing.integration.android.IntentResult
import com.spotify.android.appremote.api.ConnectionParams
import com.spotify.android.appremote.api.Connector
import com.spotify.android.appremote.api.SpotifyAppRemote
import com.spotify.protocol.types.Track
import com.spotify.protocol.client.Subscription;
import com.spotify.protocol.types.PlayerState;

class MainActivity : ComponentActivity() {

    private val clientId = "fa6a760e4e794ecb8c642e8d3de00b50"
    private val redirectUri = "musikquiz://callback"
    private var spotifyAppRemote: SpotifyAppRemote? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val scanCardButton: Button = findViewById(R.id.scanCardButton)
        scanCardButton.setOnClickListener {
            Toast.makeText(this, "Scan card button clicked", Toast.LENGTH_SHORT).show()
            val integrator = IntentIntegrator(this)
            integrator.setDesiredBarcodeFormats(IntentIntegrator.QR_CODE)
            integrator.setPrompt("Scan a QR code")
            integrator.setCameraId(0)  // Use a specific camera of the device
            integrator.setOrientationLocked(true)  // Lock orientation to portrait
            integrator.setBarcodeImageEnabled(true)
            integrator.initiateScan()
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        val result: IntentResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, data)
        if (result != null) {
            if (result.contents == null) {
                Toast.makeText(this, "Cancelled", Toast.LENGTH_LONG).show()
            } else {
                // Handle the scanned result (result.contents contains the QR code data)
                Toast.makeText(this, "Scanned: ${result.contents}", Toast.LENGTH_LONG).show()

                // Check if the scanned content is a Spotify URI
                if (result.contents.startsWith("spotify:") || result.contents.startsWith("https://open.spotify.com/")) {
                    playTrack(result.contents)
                } else {
                    Toast.makeText(this, "Not a valid Spotify link", Toast.LENGTH_SHORT).show()
                }
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data)
        }
    }

    private fun playTrack(uri: String) {
        if (spotifyAppRemote != null) {
            spotifyAppRemote?.let {
                it.playerApi.play(uri).setResultCallback {
                    Log.d("MainActivity", "Track started: $uri")
                }.setErrorCallback {
                    Log.e("MainActivity", "Failed to play track: $uri", it)
                }
            }
        } else {
            Toast.makeText(this, "Spotify not connected", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onStart() {
        super.onStart()
        val connectionParams = ConnectionParams.Builder(clientId)
            .setRedirectUri(redirectUri)
            .showAuthView(true)
            .build()

        SpotifyAppRemote.connect(this, connectionParams, object : Connector.ConnectionListener {
            override fun onConnected(appRemote: SpotifyAppRemote) {
                spotifyAppRemote = appRemote
                Log.d("MainActivity", "Connected! Yay!")
                // Now you can start interacting with App Remote
                connected()
            }

            override fun onFailure(throwable: Throwable) {
                Log.e("MainActivity", throwable.message, throwable)
                // Something went wrong when attempting to connect! Handle errors here
            }
        })
    }

    private fun connected() {
        spotifyAppRemote?.let {
            // You can subscribe to player state to get updates about playback
            it.playerApi.subscribeToPlayerState().setEventCallback { playerState ->
                val track: Track = playerState.track
                Log.d("MainActivity", "Now playing: ${track.name} by ${track.artist.name}")
            }
        }
    }

    override fun onStop() {
        super.onStop()
        spotifyAppRemote?.let {
            SpotifyAppRemote.disconnect(it)
        }
    }
}
