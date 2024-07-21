package com.example.musikquiz

import android.animation.Animator
import android.animation.AnimatorListenerAdapter
import android.animation.AnimatorSet
import android.animation.ObjectAnimator
import android.graphics.Color
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.ComponentActivity
import com.example.musikquiz.R
import com.spotify.android.appremote.api.ConnectionParams
import com.spotify.android.appremote.api.Connector
import com.spotify.android.appremote.api.SpotifyAppRemote
import com.spotify.protocol.client.Subscription
import com.spotify.protocol.types.PlayerState
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.spotify.protocol.types.Track
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.io.IOException
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.ServiceConnection
import android.os.IBinder


data class TrackInfo(val id: String, val name: String, val uri: String, val artists: List<String>)

class DuelActivity : ComponentActivity() {

    private var spotifyService: SpotifyService? = null
    private var isBound = false

    private val connection = object : ServiceConnection {
        override fun onServiceConnected(name: ComponentName?, service: IBinder?) {
            val binder = service as SpotifyService.LocalBinder
            spotifyService = binder.getService()
            spotifyService?.initialize(CLIENT_ID, REDIRECT_URI)
            spotifyService?.connectSpotify()
            isBound = true
        }

        override fun onServiceDisconnected(name: ComponentName?) {
            spotifyService = null
            isBound = false
        }
    }

    private var spotifyAppRemote: SpotifyAppRemote? = null

    private lateinit var counterTextView: TextView
    private lateinit var newGameButton: Button
    private lateinit var playPauseButton: ImageButton
    private lateinit var showInfoButton: Button
    private lateinit var songInfoButton: Button
    private lateinit var nextSongButton: Button
    private lateinit var finishGameButton: Button
    private lateinit var resetButton: Button

    private lateinit var urlEditText: EditText
    private lateinit var sendUrlButton: ImageButton
    private lateinit var urlInputContainer: LinearLayout

    private lateinit var playlistId: String
    private var accessToken: String? = null
    private var songsPlayedInCurrentRound = 0

    private val playedSongs = mutableSetOf<String>()
    private var allTracks = mutableListOf<TrackInfo>()

    companion object {
        private const val CLIENT_ID = "fa6a760e4e794ecb8c642e8d3de00b50"
        private const val REDIRECT_URI = "musikquiz://callback"
        private const val TAG = "DuelActivity"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_duel)

        counterTextView = findViewById(R.id.songCounterTextView)
        newGameButton = findViewById(R.id.newGameButton)
        playPauseButton = findViewById(R.id.playPauseButton)
        showInfoButton = findViewById(R.id.showInfoButton)
        songInfoButton = findViewById(R.id.songInfoButton)
        nextSongButton = findViewById(R.id.nextSongButton)
        finishGameButton = findViewById(R.id.finishGameButton)
        resetButton = findViewById(R.id.resetButton)

        urlEditText = findViewById(R.id.urlEditText)
        sendUrlButton = findViewById(R.id.sendUrlButton)
        urlInputContainer = findViewById(R.id.urlInputContainer)

        accessToken = intent.getStringExtra("ACCESS_TOKEN")
        playlistId = "3vTOyIODEpC95tQEVt0Q0D" // Default playlist

        newGameButton.setOnClickListener { startNewGame() }
        playPauseButton.setOnClickListener { togglePlayPause() }
        showInfoButton.setOnClickListener { flipCard(toBack = true) }
        songInfoButton.setOnClickListener { flipCard(toBack = false) }
        nextSongButton.setOnClickListener { playNextSong() }
        finishGameButton.setOnClickListener { finishGame() }
        resetButton.setOnClickListener { resetPlayedSongs() }

        sendUrlButton.setOnClickListener { updatePlaylistIdFromUrl() }

        urlEditText.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}

            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                if (s.isNullOrEmpty()) {
                    sendUrlButton.setColorFilter(Color.GRAY)
                } else {
                    sendUrlButton.setColorFilter(Color.BLACK)
                }
            }

            override fun afterTextChanged(s: Editable?) {}
        })

        val scale = applicationContext.resources.displayMetrics.density
        showInfoButton.cameraDistance = 8000 * scale
        songInfoButton.cameraDistance = 8000 * scale

        connectToSpotifyAppRemote()
        loadPlayedSongs()

        val intent = Intent(this, SpotifyService::class.java)
        bindService(intent, connection, Context.BIND_AUTO_CREATE)
    }

    private fun connectToSpotifyAppRemote() {
        val connectionParams = ConnectionParams.Builder(CLIENT_ID)
            .setRedirectUri(REDIRECT_URI)
            .showAuthView(true)
            .build()

        SpotifyAppRemote.connect(this, connectionParams, object : Connector.ConnectionListener {
            override fun onConnected(appRemote: SpotifyAppRemote) {
                spotifyAppRemote = appRemote
                Log.d(TAG, "Connected to Spotify App Remote!")
                updatePlayPauseButton()
                fetchPlaylistTracks()
            }

            override fun onFailure(throwable: Throwable) {
                Log.e(TAG, "Failed to connect to Spotify App Remote", throwable)
            }
        })
    }

    private fun updatePlaylistIdFromUrl() {
        val url = urlEditText.text.toString()
        val regex = Regex("playlist/([a-zA-Z0-9]+)")
        val matchResult = regex.find(url)
        if (matchResult != null) {
            playlistId = matchResult.groupValues[1]
            fetchPlaylistTracks()
            Toast.makeText(this, "Playlist ID updated", Toast.LENGTH_SHORT).show()
            // Clear the text in urlEditText
            urlEditText.text.clear()
            // Optionally, change the color of sendUrlButton to indicate the URL has been sent
            sendUrlButton.setColorFilter(Color.GRAY)
        } else {
            Toast.makeText(this, "Invalid URL", Toast.LENGTH_SHORT).show()
        }
    }

    private fun flipCard(toBack: Boolean) {
        val duration = 250L

        // Animators for flipping out the current view
        val flipOutAnimator = AnimatorSet().apply {
            playSequentially(
                ObjectAnimator.ofFloat(if (toBack) showInfoButton else songInfoButton, "scaleX", 1f, 0f).setDuration(duration),
            )
        }

        // Animators for flipping in the new view
        val flipInAnimator = AnimatorSet().apply {
            playSequentially(
                ObjectAnimator.ofFloat(if (toBack) songInfoButton else showInfoButton, "scaleX", 0f, 1f).setDuration(duration)
            )
        }

        if (toBack) {
            // Showing song info
            flipOutAnimator.addListener(object : AnimatorListenerAdapter() {
                override fun onAnimationEnd(animation: Animator) {
                    showInfoButton.visibility = View.GONE
                    songInfoButton.visibility = View.VISIBLE
                    songInfoButton.scaleX = 0f
                    flipInAnimator.start()
                }
            })
            flipOutAnimator.start()
        } else {
            // Hiding song info
            flipOutAnimator.addListener(object : AnimatorListenerAdapter() {
                override fun onAnimationEnd(animation: Animator) {
                    songInfoButton.visibility = View.GONE
                    showInfoButton.visibility = View.VISIBLE
                    showInfoButton.scaleX = 0f
                    flipInAnimator.start()
                }
            })
            flipOutAnimator.start()
        }
    }

    private fun fetchPlaylistTracks() {
        val url = "https://api.spotify.com/v1/playlists/$playlistId/tracks"
        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer $accessToken")
            .build()

        client.newCall(request).enqueue(object : okhttp3.Callback {
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                Log.e(TAG, "Failed to fetch playlist tracks", e)
                runOnUiThread {
                    Toast.makeText(this@DuelActivity, "Failed to fetch playlist tracks", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: okhttp3.Call, response: okhttp3.Response) {
                if (!response.isSuccessful) {
                    Log.e(TAG, "Failed to fetch playlist tracks: ${response.code}")
                    runOnUiThread {
                        Toast.makeText(
                            this@DuelActivity,
                            "Failed to fetch playlist tracks",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                    return
                }

                val responseBody = response.body?.string()
                if (responseBody != null) {
                    try {
                        val jsonObject = JSONObject(responseBody)
                        val tracksArray = jsonObject.getJSONArray("items")
                        allTracks.clear()

                        for (i in 0 until tracksArray.length()) {
                            val trackObject = tracksArray.getJSONObject(i).getJSONObject("track")
                            val trackId = trackObject.getString("id")
                            val trackName = trackObject.getString("name")
                            val trackUri = trackObject.getString("uri")
                            //val artistName = trackObject.getJSONArray("artists").getJSONObject(0)
                                //.getString("name")
                            val artistsArray = trackObject.getJSONArray("artists")
                            val artists = mutableListOf<String>()

                            for (j in 0 until artistsArray.length()) {
                                artists.add(artistsArray.getJSONObject(j).getString("name"))
                            }

                            allTracks.add(TrackInfo(trackId, trackName, trackUri, artists))
                        }

                        runOnUiThread {
                            Toast.makeText(
                                this@DuelActivity,
                                "Playlist tracks loaded",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                    } catch (e: Exception) {
                        Log.e(TAG, "Error parsing playlist tracks", e)
                        runOnUiThread {
                            Toast.makeText(
                                this@DuelActivity,
                                "Error parsing playlist tracks",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                    }
                } else {
                    Log.e(TAG, "Response body is null")
                    runOnUiThread {
                        Toast.makeText(
                            this@DuelActivity,
                            "Response body is null",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                }
            }
        })
    }

    private fun updatePlayPauseButton() {
        spotifyAppRemote?.playerApi?.subscribeToPlayerState()?.setEventCallback { playerState ->
            if (playerState.isPaused) {
                playPauseButton.setImageResource(R.drawable.ic_play)  // Set to play icon if paused
            } else {
                playPauseButton.setImageResource(R.drawable.ic_pause)  // Set to pause icon if playing
            }
        }
    }

    private fun playNextSong() {
        if (songsPlayedInCurrentRound  >= 14) {
            nextSongButton.visibility = View.GONE
            finishGameButton.visibility = View.VISIBLE
        }

        if (songInfoButton.visibility == View.VISIBLE) {
            flipCard(toBack = false)
            startPlayingNextSong()
        } else {
            startPlayingNextSong()
        }
        updateSongCounter()
    }

    private fun updateSongCounter() {
        val totalSongs = 15 // Adjust if needed
        counterTextView.text = "$songsPlayedInCurrentRound/$totalSongs"
    }

    private fun updateSongInfo(artists: List<String>, song: String) {
        val artistNames = artists.joinToString(", ")
        songInfoButton.text = "Song: $song \n\nArtist: $artistNames"
    }

    private fun startNewGame() {
        songsPlayedInCurrentRound = 0
        playNextSong()
        newGameButton.visibility = View.GONE
        nextSongButton.visibility = View.VISIBLE
        counterTextView.visibility = View.VISIBLE
        resetButton.visibility = View.VISIBLE
        urlInputContainer.visibility = View.GONE
    }

    private fun finishGame() {
        Toast.makeText(this, "Game Finished", Toast.LENGTH_SHORT).show()
        newGameButton.visibility = View.VISIBLE
        nextSongButton.visibility = View.GONE
        finishGameButton.visibility = View.GONE
        songInfoButton.visibility = View.VISIBLE
        counterTextView.visibility = View.GONE
        urlInputContainer.visibility = View.VISIBLE
        showInfoButton.text = "Show information"
        spotifyAppRemote?.playerApi?.pause()
    }

    private fun startPlayingNextSong() {
        val availableTracks = allTracks.filterNot { playedSongs.contains(it.uri) }

        if (availableTracks.isEmpty()) {
            resetPlayedSongs()
            return
        }

        val randomTrack = availableTracks.random()
        spotifyAppRemote?.playerApi?.play(randomTrack.uri)
        playedSongs.add(randomTrack.uri)
        songsPlayedInCurrentRound++ // Increment the counter for the current round
        savePlayedSongs()
        updateSongInfo(randomTrack.artists, randomTrack.name)
        updateSongCounter()
    }

    private fun togglePlayPause() {
        spotifyAppRemote?.playerApi?.playerState?.setResultCallback { playerState ->
            if (playerState.isPaused) {
                spotifyAppRemote?.playerApi?.resume()
                playPauseButton.setImageResource(R.drawable.ic_pause)
            } else {
                spotifyAppRemote?.playerApi?.pause()
                playPauseButton.setImageResource(R.drawable.ic_play)
            }
        }
    }

    private fun savePlayedSongs() {
        val sharedPreferences = getSharedPreferences("DuelPlayedSongsPrefs", MODE_PRIVATE)
        val editor = sharedPreferences.edit()

        // Convert the list to a JSON string
        val gson = Gson()
        editor.putString("playedSongs", gson.toJson(playedSongs.toList()))

        editor.apply()
    }

    private fun loadPlayedSongs() {
        val sharedPreferences = getSharedPreferences("DuelPlayedSongsPrefs", MODE_PRIVATE)

        // Retrieve the JSON string and convert it back to a list
        val gson = Gson()
        val type = object : TypeToken<MutableList<String>>() {}.type

        playedSongs.clear()
        playedSongs.addAll(gson.fromJson(sharedPreferences.getString("playedSongs", "[]"), type))
    }

    private fun resetPlayedSongs() {
        playedSongs.clear()
        Toast.makeText(this, "All songs have been reset", Toast.LENGTH_LONG).show()
    }

    override fun onDestroy() {
        super.onDestroy()
        if (isBound) {
            unbindService(connection)
            isBound = false
        }
    }

    override fun onStart() {
        super.onStart()
        if (isBound) {
            spotifyService?.connectSpotify()
        }
    }

    override fun onStop() {
        super.onStop()
        savePlayedSongs()
        if (isBound) {
            spotifyService?.disconnectSpotify()
        }
    }
}