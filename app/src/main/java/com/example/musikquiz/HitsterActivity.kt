package com.example.musikquiz

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.ComponentActivity
import com.google.zxing.integration.android.IntentIntegrator
import com.google.zxing.integration.android.IntentResult
import com.spotify.android.appremote.api.ConnectionParams
import com.spotify.android.appremote.api.Connector
import com.spotify.android.appremote.api.SpotifyAppRemote
import com.spotify.protocol.client.Subscription
import com.spotify.protocol.types.PlayerState

class HitsterActivity : ComponentActivity() {

    private var spotifyAppRemote: SpotifyAppRemote? = null
    private var playerStateSubscription: Subscription<PlayerState>? = null

    private lateinit var artistTextView: TextView
    private lateinit var songNameTextView: TextView
    private lateinit var releaseYearTextView: TextView

    companion object {
        private const val CLIENT_ID = "fa6a760e4e794ecb8c642e8d3de00b50"
        private const val REDIRECT_URI = "musikquiz://callback"
        private const val TAG = "HitsterActivity"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_hitster)

        artistTextView = findViewById(R.id.artistTextView)
        songNameTextView = findViewById(R.id.songNameTextView)
        releaseYearTextView = findViewById(R.id.releaseYearTextView)

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
        super.onActivityResult(requestCode, resultCode, data)
        val result: IntentResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, data)
        if (result != null) {
            if (result.contents == null) {
                Toast.makeText(this, "Cancelled", Toast.LENGTH_LONG).show()
            } else {
                // Handle the scanned result (result.contents contains the QR code data)
                Toast.makeText(this, "Scanned: ${result.contents}", Toast.LENGTH_LONG).show()

                // Check if the scanned content is a Spotify URI
                if (result.contents.startsWith("spotify:") || result.contents.startsWith("https://open.spotify.com/")) {
                    val uri = convertToSpotifyUri(result.contents)
                    openSpotify(uri)
                } else {
                    Toast.makeText(this, "Not a valid Spotify link", Toast.LENGTH_SHORT).show()
                }
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data)
        }
    }

    private fun convertToSpotifyUri(link: String): String {
        return if (link.startsWith("https://open.spotify.com/")) {
            val uriPart = link.split("/").last().split("?").first()
            "spotify:track:$uriPart"
        } else {
            link
        }
    }

    private fun openSpotify(uri: String) {
        connectToSpotifyAppRemote {
            spotifyAppRemote?.let {
                it.playerApi.play(uri)
                subscribeToPlayerState()
            }
        }
    }

    private fun connectToSpotifyAppRemote(onConnected: () -> Unit) {
        val connectionParams = ConnectionParams.Builder(CLIENT_ID)
            .setRedirectUri(REDIRECT_URI)
            .showAuthView(true)
            .build()

        SpotifyAppRemote.connect(this, connectionParams, object : Connector.ConnectionListener {
            override fun onConnected(appRemote: SpotifyAppRemote) {
                spotifyAppRemote = appRemote
                Log.d(TAG, "Connected to Spotify App Remote!")
                onConnected()
            }

            override fun onFailure(throwable: Throwable) {
                Log.e(TAG, "Failed to connect to Spotify App Remote", throwable)
            }
        })
    }

    private fun subscribeToPlayerState() {
        spotifyAppRemote?.let { remote ->
            playerStateSubscription = remote.playerApi.subscribeToPlayerState()
            playerStateSubscription?.setEventCallback { playerState ->
                val track = playerState.track
                if (track != null) {
                    artistTextView.text = "Artist: ${track.artist.name}"
                    songNameTextView.text = "Song: ${track.name}"
                    //releaseYearTextView.text = "Release Year: ${track.re}"
                }
            }
        }
    }

    override fun onStop() {
        super.onStop()
        SpotifyAppRemote.disconnect(spotifyAppRemote)
    }
}
