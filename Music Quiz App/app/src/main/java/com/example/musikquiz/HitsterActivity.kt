package com.example.musikquiz

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.activity.ComponentActivity
import com.google.zxing.integration.android.IntentIntegrator
import com.google.zxing.integration.android.IntentResult
import com.spotify.android.appremote.api.ConnectionParams
import com.spotify.android.appremote.api.Connector
import com.spotify.android.appremote.api.SpotifyAppRemote
import com.spotify.protocol.client.Subscription
import com.spotify.protocol.types.Image
import com.spotify.protocol.types.PlayerState
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.io.IOException


class HitsterActivity : ComponentActivity() {

    private var spotifyAppRemote: SpotifyAppRemote? = null
    private var playerStateSubscription: Subscription<PlayerState>? = null
    private var accessToken: String? = null

    private lateinit var artistTextView: TextView
    private lateinit var songNameTextView: TextView
    private lateinit var releaseYearTextView: TextView
    private lateinit var albumCoverImageView: ImageView
    private lateinit var playPauseButton: ImageButton

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
        albumCoverImageView = findViewById(R.id.album_cover)
        playPauseButton = findViewById(R.id.play_pause_button)

        accessToken = intent.getStringExtra("ACCESS_TOKEN")

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

        playPauseButton.setOnClickListener {
            togglePlayPause()
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
                fetchTrackDetails(uri)
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
                    updateTrackCoverArt(playerState)
                    updatePlayPauseButton(playerState)
                }
            }
        }
    }

    private fun updateTrackCoverArt(playerState: PlayerState) {
        spotifyAppRemote?.imagesApi
            ?.getImage(playerState.track.imageUri, Image.Dimension.LARGE)
            ?.setResultCallback { bitmap ->
                albumCoverImageView.setImageBitmap(bitmap)
            }
    }

    private fun updatePlayPauseButton(playerState: PlayerState) {
        if (playerState.isPaused) {
            playPauseButton.setImageResource(R.drawable.ic_play)  // Set to play icon if paused
        } else {
            playPauseButton.setImageResource(R.drawable.ic_pause)  // Set to pause icon if playing
        }
    }

    private fun togglePlayPause() {
        spotifyAppRemote?.playerApi?.playerState?.setResultCallback { playerState ->
            if (playerState.isPaused) {
                spotifyAppRemote?.playerApi?.resume()
                playPauseButton.setImageResource(R.drawable.ic_pause)  // Update to pause icon
            } else {
                spotifyAppRemote?.playerApi?.pause()
                playPauseButton.setImageResource(R.drawable.ic_play)  // Update to play icon
            }
        }
    }

    private fun fetchTrackDetails(uri: String) {
        val trackId = uri.split(":").last()
        val url = "https://api.spotify.com/v1/tracks/$trackId"

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer $accessToken")  // Use the valid access token
            .build()

        client.newCall(request).enqueue(object : okhttp3.Callback {
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                Log.e(TAG, "Failed to fetch track details", e)
            }

            override fun onResponse(call: okhttp3.Call, response: okhttp3.Response) {
                if (!response.isSuccessful) {
                    Log.e(TAG, "Failed to fetch track details: ${response.code}")
                    return
                }

                val responseBody = response.body?.string()
                if (responseBody != null) {
                    val jsonObject = JSONObject(responseBody)
                    val releaseDate = jsonObject.getJSONObject("album").getString("release_date")

                    runOnUiThread {
                        releaseYearTextView.text = "Release Year: ${releaseDate.substring(0, 4)}"
                    }
                }
            }
        })
    }

    override fun onStop() {
        super.onStop()
        SpotifyAppRemote.disconnect(spotifyAppRemote)
    }
}
