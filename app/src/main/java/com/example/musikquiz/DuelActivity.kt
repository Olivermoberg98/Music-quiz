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
import com.spotify.android.appremote.api.ConnectionParams
import com.spotify.android.appremote.api.Connector
import com.spotify.android.appremote.api.SpotifyAppRemote
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.io.IOException
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.ServiceConnection
import android.os.IBinder
import android.view.Gravity
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.RelativeLayout
import android.widget.Spinner
import androidx.constraintlayout.widget.ConstraintLayout
import androidx.core.content.ContextCompat
import androidx.core.content.res.ResourcesCompat


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

    private lateinit var teamInputContainer: LinearLayout
    private lateinit var teamDisplayContainer: LinearLayout
    private lateinit var songCountContainer: RelativeLayout


    private lateinit var playlistId: String
    private var accessToken: String? = null
    private var songsPlayedInCurrentRound = 0

    private val playedSongs = mutableSetOf<String>()
    private var allTracks = mutableListOf<TrackInfo>()
    private val teamNames = mutableListOf<String>()
    private val teamScores = mutableMapOf<String, Int>()
    private val teamNameMap = mutableMapOf<EditText, Int>()
    private var teamCounter = 0

    private lateinit var songCountSpinner: Spinner
    private var totalSongs = 15

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
        songCountContainer = findViewById(R.id.songCountContainer)

        urlEditText = findViewById(R.id.urlEditText)
        sendUrlButton = findViewById(R.id.sendUrlButton)
        urlInputContainer = findViewById(R.id.urlInputContainer)

        teamInputContainer = findViewById(R.id.teamInputContainer)
        teamDisplayContainer = findViewById(R.id.teamDisplayContainer)

        findViewById<ImageButton>(R.id.addTeamButton).setOnClickListener {
            addTeamInput()
        }

        findViewById<ImageButton>(R.id.removeTeamButton).setOnClickListener {
            removeTeamInput()
        }

        songCountSpinner = findViewById(R.id.songCountSpinner)

        val songCounts = (1..30).toList()
        val spinnerAdapter = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_item,
            songCounts
        ).apply {
            setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        }

        songCountSpinner.adapter = spinnerAdapter
        songCountSpinner.setSelection(songCounts.indexOf(15)) // default

        songCountSpinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(
                parent: AdapterView<*>,
                view: View?,
                position: Int,
                id: Long
            ) {
                totalSongs = songCounts[position]
                updateSongCounter()
            }

            override fun onNothingSelected(parent: AdapterView<*>) {}
        }

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

        addTeamInput()
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
            urlEditText.text.clear()
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
        if (songsPlayedInCurrentRound >= totalSongs - 1) {
            nextSongButton.visibility = View.GONE
            finishGameButton.visibility = View.VISIBLE

            val teamDisplayContainer = findViewById<LinearLayout>(R.id.teamDisplayContainer)
            val layoutParams = teamDisplayContainer.layoutParams as ConstraintLayout.LayoutParams

            // Update the layout parameters to position below finishGameButton
            layoutParams.topToBottom = finishGameButton.id
            teamDisplayContainer.layoutParams = layoutParams

            teamDisplayContainer.visibility = View.VISIBLE

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
        songCountContainer.visibility = View.GONE
        displayTeams()
    }

    private fun finishGame() {
        showWinnerDialog()
    }

    private fun resetGameState() {
        newGameButton.visibility = View.VISIBLE
        nextSongButton.visibility = View.GONE
        finishGameButton.visibility = View.GONE
        songInfoButton.visibility = View.VISIBLE
        counterTextView.visibility = View.GONE
        urlInputContainer.visibility = View.VISIBLE
        showInfoButton.text = "Show information"
        spotifyAppRemote?.playerApi?.pause()
        teamInputContainer.visibility = View.VISIBLE
        resetButton.visibility = View.GONE
        teamDisplayContainer.visibility = View.GONE
        songCountSpinner.visibility = View.VISIBLE

        // Reset team scores for next game
        teamScores.clear()
        teamNames.forEach { teamScores[it] = 0 }
    }

    private fun showWinnerDialog() {
        // Sort teams by score in descending order
        val sortedTeams = teamScores.entries.sortedByDescending { it.value }

        // Create dialog
        val dialog = android.app.AlertDialog.Builder(this)

        // Create custom view for the dialog
        val dialogView = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(48, 48, 48, 48)
            gravity = Gravity.CENTER
        }

        // Title
        val titleText = TextView(this).apply {
            text = "🏆 Game Results 🏆"
            textSize = 28f
            setTextColor(Color.parseColor("#C8A2C8")) // Lavender color
            typeface = ResourcesCompat.getFont(this@DuelActivity, R.font.trajanbold)
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 32)
        }
        dialogView.addView(titleText)

        // Display top 3 teams
        val teamsToShow = minOf(3, sortedTeams.size)
        for (i in 0 until teamsToShow) {
            val team = sortedTeams[i]
            val medal = when(i) {
                0 -> "🥇"
                1 -> "🥈"
                2 -> "🥉"
                else -> ""
            }

            val teamResultText = TextView(this).apply {
                text = "$medal ${team.key}: ${team.value} points"
                textSize = 22f
                setTextColor(Color.BLACK)
                typeface = ResourcesCompat.getFont(this@DuelActivity, R.font.trajanbold)
                gravity = Gravity.CENTER
                setPadding(0, 16, 0, 16)
            }
            dialogView.addView(teamResultText)
        }

        dialog.setView(dialogView)
        dialog.setPositiveButton("Close") { dialogInterface, _ ->
            dialogInterface.dismiss()
            resetGameState()
        }

        dialog.setCancelable(false) // Prevent dismissing by clicking outside
        dialog.show()
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

    private fun addTeamInput() {
        val teamIndex = teamCounter  // Get the current index based on teamCounter

        val teamInputLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            background = ContextCompat.getDrawable(this@DuelActivity, R.drawable.rounded_button)
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(0, 16, 0, 14)
            }
            setPadding(0, 16, 16, 16)
        }

        val teamNumber = TextView(this).apply {
            text = teamCounter.toString()
            textSize = 18f
            setTextColor(ContextCompat.getColor(this@DuelActivity, android.R.color.black))
            gravity = Gravity.CENTER_VERTICAL
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(16, 0, 16, 0)
            }
        }

        val teamNameInput = EditText(this).apply {
            hint = "Enter team name"
            layoutParams = LinearLayout.LayoutParams(
                0,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                weight = 1f
            }

            // Set a TextWatcher to handle team name updates
            addTextChangedListener(object : TextWatcher {
                override fun afterTextChanged(s: Editable?) {
                    val teamName = s.toString().trim()
                    if (teamName.isNotEmpty()) {
                        // Update or add team name in the list
                        teamNames[teamIndex] = teamName
                    }
                }

                override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
                override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            })

            // Track the EditText with its team index
            teamNameMap[this] = teamIndex
        }

        teamInputLayout.addView(teamNumber)
        teamInputLayout.addView(teamNameInput)
        teamInputContainer.addView(teamInputLayout)

        // Increment the team counter

        teamCounter++

        // Initialize the teamNames list with empty names if needed
        while (teamNames.size < teamCounter) {
            teamNames.add("")
        }
    }

    private fun removeTeamInput() {
        val teamCount = teamInputContainer.childCount
        if (teamCount > 2) {
            // Remove the last added team input
            val lastTeamInput = teamInputContainer.getChildAt(teamCount - 1)
            teamInputContainer.removeView(lastTeamInput)

            // Decrement the team counter
            teamCounter--

            // Remove the corresponding team name from the list
            if (teamCounter >= 0 && teamCounter < teamNames.size) {
                teamNames.removeAt(teamCounter)
            }
        } else {
            Toast.makeText(this, "At least one team is required", Toast.LENGTH_SHORT).show()
        }
    }

    private fun displayTeams() {
        // Hide the team input container and show the team display container
        teamInputContainer.visibility = View.GONE
        teamDisplayContainer.visibility = View.VISIBLE

        // Clear the team display container
        teamDisplayContainer.removeAllViews()

        // Add team display layouts for each team
        for (i in teamNames.indices) {
            addTeamDisplay(i)
        }
    }

    private fun addTeamDisplay(index: Int) {
        val teamName = teamNames.getOrNull(index) ?: return

        val teamDisplayLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(30, 30, 0, 8)
            }
        }

        val teamNameTextView = TextView(this).apply {
            id = View.generateViewId()
            text = teamName
            textSize = 24f
            setTextColor(ContextCompat.getColor(this@DuelActivity, android.R.color.white))
            typeface = ResourcesCompat.getFont(this@DuelActivity, R.font.trajanbold)
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(0, 0, 20, 0)
            }
        }

        val teamScoreTextView = TextView(this).apply {
            id = View.generateViewId()
            text = teamScores.getOrDefault(teamName, 0).toString()
            textSize = 24f
            setTextColor(ContextCompat.getColor(this@DuelActivity, android.R.color.white))
            typeface = ResourcesCompat.getFont(this@DuelActivity, R.font.trajanbold)
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(0, 0, 12, 0)
            }
        }

        val buttonContainer = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                gravity = Gravity.END
                setMargins(0, 0, 30, 0) // Margin to the right wall
            }
            setBackgroundColor(Color.TRANSPARENT)
        }

        val buttonLayoutParams = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.WRAP_CONTENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        ).apply {
            width = 108 // Adjust the width as needed
            height = 108 // Adjust the height as needed
        }

        val incrementButton = ImageButton(this).apply {
            layoutParams = buttonLayoutParams
            setImageResource(R.drawable.ic_increment)
            contentDescription = "Increment Points"
            setOnClickListener {
                val currentScore = teamScores[teamName] ?: 0
                teamScores[teamName] = currentScore + 1
                teamScoreTextView.text = teamScores[teamName].toString()
            }
        }

        val decrementButton = ImageButton(this).apply {
            layoutParams = buttonLayoutParams
            setImageResource(R.drawable.ic_decrement)
            contentDescription = "Decrement Points"
            setOnClickListener {
                val currentScore = teamScores[teamName] ?: 0
                if (currentScore > 0) {
                    teamScores[teamName] = currentScore - 1
                    teamScoreTextView.text = teamScores[teamName].toString()
                }
            }
        }

        buttonContainer.addView(incrementButton)
        buttonContainer.addView(decrementButton)

        teamDisplayLayout.addView(teamNameTextView)
        teamDisplayLayout.addView(teamScoreTextView)
        teamDisplayLayout.addView(buttonContainer)

        teamDisplayContainer.addView(teamDisplayLayout)
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