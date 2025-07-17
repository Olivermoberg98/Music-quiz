package com.example.musikquiz

import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.ImageButton
import android.widget.TextView
import android.widget.Toast
import androidx.activity.ComponentActivity
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.spotify.android.appremote.api.ConnectionParams
import com.spotify.android.appremote.api.Connector
import com.spotify.android.appremote.api.SpotifyAppRemote
import com.spotify.protocol.client.Subscription
import com.spotify.protocol.types.PlayerState
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.apache.poi.ss.usermodel.WorkbookFactory
import java.io.InputStream
import kotlin.random.Random
import kotlinx.coroutines.*

class CategoriesActivity : ComponentActivity() {

    private var spotifyAppRemote: SpotifyAppRemote? = null
    private var accessToken: String? = null
    private var playerStateSubscription: Subscription<PlayerState>? = null

    private val songToMovieMap = HashMap<String, String>()
    private val songToCountryMap = HashMap<String, String>()
    private val songToEuroMap = HashMap<String, String>()
    private val songToArtistMapCat3 = HashMap<String, String>()
    private val songToArtistMapCat4 = HashMap<String, String>()
    private val songToArtistMapCat5 = HashMap<String, String>()
    private val songToArtistMapCat6 = HashMap<String, String>()

    private val playedMovieSongs = mutableListOf<String>()
    private val playedCountrySongs = mutableListOf<String>()
    private val playedEuroSongs = mutableListOf<String>()
    private val playedTwoThousandSongs = mutableListOf<String>()
    private val playedRockSongs = mutableListOf<String>()
    private val playedMelloSongs = mutableListOf<String>()
    private val played80s90sSongs = mutableListOf<String>()

    private lateinit var answerTitleTextView: TextView
    private lateinit var playPauseButton: ImageButton

    companion object {
        private const val CLIENT_ID = "fa6a760e4e794ecb8c642e8d3de00b50"
        private const val REDIRECT_URI = "musikquiz://callback"
        private const val TAG = "CategoriesActivity"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_categories)

        playPauseButton = findViewById(R.id.play_pause_button)
        playPauseButton.setOnClickListener {
            togglePlayPause()
        }

        accessToken = intent.getStringExtra("ACCESS_TOKEN")

        answerTitleTextView = findViewById(R.id.answerTitleTextView)

        loadPlayedSongs()

        // Load mappings concurrently
        CoroutineScope(Dispatchers.IO).launch {
            val movieMappingDeferred = async { loadSongMappings("hitster_data_rock_v0.xlsx", 3, 0) }
            val countryMappingDeferred = async { loadSongMappings("hitster_data_countries_v1.xlsx", 3, 2) }
            val euroMappingDeferred = async { loadSongMappings("hitster_data_eurovision_v0.xlsx", 3, 2) }
            val twoThousandMappingDeferred = async { loadSongMappings("hitster_data_2000_v0.xlsx", 3, 0) }
            val rockMappingDeferred = async { loadSongMappings("hitster_data_melodifestivalen_v0.xlsx", 3, 0) }
            val rapMappingDeferred = async { loadSongMappings("hitster_data_70s_v0.xlsx", 3, 0) }
            val popMappingDeferred = async { loadSongMappings("hitster_data_80s90s_v0.xlsx", 3, 0) }

            songToMovieMap.putAll(movieMappingDeferred.await())
            songToCountryMap.putAll(countryMappingDeferred.await())
            songToEuroMap.putAll(euroMappingDeferred.await())
            songToArtistMapCat3.putAll(twoThousandMappingDeferred.await())
            songToArtistMapCat4.putAll(rockMappingDeferred.await())
            songToArtistMapCat5.putAll(rapMappingDeferred.await())
            songToArtistMapCat6.putAll(popMappingDeferred.await())

            // Now that maps are loaded, you can update the UI or do other operations as needed
            withContext(Dispatchers.Main) {
                verifyLoadedData()
            }
        }

        val countryButton: Button = findViewById(R.id.countryButton)
        val euroButton: Button = findViewById(R.id.eurovisionButton)
        val movieButton: Button = findViewById(R.id.movieButton)
        val cat3Button: Button = findViewById(R.id.cat3Button)
        val cat4Button: Button = findViewById(R.id.cat4Button)
        val cat5Button: Button = findViewById(R.id.cat5Button)
        val cat6Button: Button = findViewById(R.id.cat6Button)
        val resetButton: Button = findViewById(R.id.resetButton)

        countryButton.setOnClickListener { playRandomTrack(songToCountryMap, playedCountrySongs) }
        euroButton.setOnClickListener { playRandomTrack(songToEuroMap, playedEuroSongs) }
        movieButton.setOnClickListener { playRandomTrack(songToMovieMap, playedMovieSongs) }
        cat3Button.setOnClickListener { playRandomTrack(songToArtistMapCat3, playedTwoThousandSongs) }
        cat4Button.setOnClickListener { playRandomTrack(songToArtistMapCat4, playedRockSongs) }
        cat5Button.setOnClickListener { playRandomTrack(songToArtistMapCat5, playedMelloSongs) }
        cat6Button.setOnClickListener { playRandomTrack(songToArtistMapCat6, played80s90sSongs) }
        resetButton.setOnClickListener { resetPlayedSongs() }
    }

    override fun onStart() {
        super.onStart()
        connectToSpotifyAppRemote()
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
            }

            override fun onFailure(throwable: Throwable) {
                Log.e(TAG, "Failed to connect to Spotify App Remote", throwable)
            }
        })
    }

    private fun convertToSpotifyUri(link: String): String? {
        return if (link.startsWith("https://open.spotify.com/")) {
            val uriPart = link.split("/").last().split("?").firstOrNull()
            uriPart?.let { "spotify:track:$it" }
        } else {
            // Assuming non-Spotify URLs should be handled or returned as is
            null
        }
    }

    private fun convertToSpotifyUrl(uri: String): String? {
        return if (uri.startsWith("spotify:track:")) {
            val uriPart = uri.split(":").lastOrNull()
            uriPart?.let { "https://open.spotify.com/track/$it" }
        } else {
            // Return null if the input is not a Spotify URI
            null
        }
    }

    private fun playRandomTrack(map: Map<String, String>, playedSongs: MutableList<String>) {
        // Filter out the played songs
        val availableSongs = map.keys.filterNot { playedSongs.contains(it) }

        if (availableSongs.isEmpty()) {
            Toast.makeText(this, "All songs have been played. This category will be reset", Toast.LENGTH_LONG).show()
            playedSongs.clear()
            return
        }

        // Select a random track URL from the available songs
        val randomTrackUrl = availableSongs.randomOrNull()
        if (randomTrackUrl != null) {
            val randomTrackUri = convertToSpotifyUri(randomTrackUrl)
            if (randomTrackUri != null) {
                // Play the selected track
                spotifyAppRemote?.let { remote ->
                    remote.playerApi.play(randomTrackUri)

                    // Cancel any previous subscription
                    playerStateSubscription?.cancel()
                    playerStateSubscription = null

                    // Subscribe to player state updates
                    playerStateSubscription = remote.playerApi.subscribeToPlayerState()
                    playerStateSubscription?.setEventCallback { playerState ->
                        val track = playerState.track
                        Log.d(TAG, "Player state updated: $playerState")

                        if (track != null ) {
                            val songUri = track.uri
                            val songUrl = convertToSpotifyUrl(songUri)
                            Log.d(TAG, "Requested URI: $randomTrackUri")
                            Log.d(TAG, "Actual Song URI: $songUri")

                            // Check if the track matches the one we played and hasn't been processed yet
                            if (songUri == randomTrackUri && !playedSongs.contains(randomTrackUrl)) {
                                val answer = map[songUrl]
                                runOnUiThread {
                                    answerTitleTextView.text = answer
                                    playedSongs.add(randomTrackUrl)
                                }
                            }
                        }
                    }
                } ?: run {
                    Toast.makeText(this@CategoriesActivity, "Failed to connect to Spotify.", Toast.LENGTH_LONG).show()
                }
            } else {
                Toast.makeText(this@CategoriesActivity, "Invalid track URI.", Toast.LENGTH_LONG).show()
            }
        } else {
            Toast.makeText(this@CategoriesActivity, "No tracks available to play", Toast.LENGTH_LONG).show()
        }
    }

    private fun savePlayedSongs() {
        val sharedPreferences = getSharedPreferences("PlayedSongsPrefs", MODE_PRIVATE)
        val editor = sharedPreferences.edit()

        // Convert the lists to JSON strings
        val gson = Gson()
        editor.putString("playedMovieSongs", gson.toJson(playedMovieSongs))
        editor.putString("playedEuroSongs", gson.toJson(playedEuroSongs))
        editor.putString("playedCountrySongs", gson.toJson(playedCountrySongs))
        editor.putString("playedTwoThousandSongs", gson.toJson(playedTwoThousandSongs))
        editor.putString("playedRockSongs", gson.toJson(playedRockSongs))
        editor.putString("playedMelloSongs", gson.toJson(playedMelloSongs))
        editor.putString("played80s90sSongs", gson.toJson(played80s90sSongs))

        editor.apply()
    }

    private fun loadPlayedSongs() {
        val sharedPreferences = getSharedPreferences("PlayedSongsPrefs", MODE_PRIVATE)

        // Retrieve the JSON strings and convert them back to lists
        val gson = Gson()
        val type = object : TypeToken<MutableList<String>>() {}.type

        playedMovieSongs.clear()
        playedMovieSongs.addAll(gson.fromJson(sharedPreferences.getString("playedMovieSongs", "[]"), type))

        playedEuroSongs.clear()
        playedEuroSongs.addAll(gson.fromJson(sharedPreferences.getString("playedEuroSongs", "[]"), type))

        playedCountrySongs.clear()
        playedCountrySongs.addAll(gson.fromJson(sharedPreferences.getString("playedCountrySongs", "[]"), type))

        playedTwoThousandSongs.clear()
        playedTwoThousandSongs.addAll(gson.fromJson(sharedPreferences.getString("playedTwoThousandSongs", "[]"), type))

        playedRockSongs.clear()
        playedRockSongs.addAll(gson.fromJson(sharedPreferences.getString("playedRockSongs", "[]"), type))

        playedMelloSongs.clear()
        playedMelloSongs.addAll(gson.fromJson(sharedPreferences.getString("playedMelloSongs", "[]"), type))

        played80s90sSongs.clear()
        played80s90sSongs.addAll(gson.fromJson(sharedPreferences.getString("played80s90sSongs", "[]"), type))
    }

    private suspend fun loadSongMappings(fileName: String, keyColumn: Int, valueColumn: Int): Map<String, String> {
        val map = HashMap<String, String>()
        try {
            // Open the Excel file from assets
            val inputStream: InputStream = assets.open(fileName)
            val workbook = WorkbookFactory.create(inputStream)
            val sheet = workbook.getSheetAt(0)

            // Iterate through all rows in the sheet
            for (row in sheet) {
                // Skip header row (assuming the first row is the header)
                if (row.rowNum == 0) continue

                // Get the cell values
                val key = row.getCell(keyColumn)?.stringCellValue?.trim()
                val value = row.getCell(valueColumn)?.stringCellValue?.trim()

                // Check if both values are not null
                if (key != null && value != null) {
                    map[key] = value
                }
            }
            // Close the workbook to free resources
            workbook.close()
        } catch (e: Exception) {
            Log.e(TAG, "Error loading Excel file: $fileName", e)
        }
        return map
    }

    private fun verifyLoadedData() {
        // Verify mappings
        val mappingsValid = songToMovieMap.isNotEmpty() &&
                songToCountryMap.isNotEmpty() &&
                songToEuroMap.isNotEmpty() &&
                songToArtistMapCat3.isNotEmpty() &&
                songToArtistMapCat4.isNotEmpty() &&
                songToArtistMapCat5.isNotEmpty() &&
                songToArtistMapCat6.isNotEmpty()

        if (mappingsValid) {
            Toast.makeText(this, "Mappings Loaded Successfully", Toast.LENGTH_SHORT).show()
        } else {
            Toast.makeText(this, "Failed to load some mappings", Toast.LENGTH_SHORT).show()
        }

        // Verify played songs
        val playedSongsLoaded =
                playedMovieSongs.isNotEmpty() ||
                playedCountrySongs.isNotEmpty() ||
                songToEuroMap.isNotEmpty() ||
                playedTwoThousandSongs.isNotEmpty() ||
                playedRockSongs.isNotEmpty() ||
                playedMelloSongs.isNotEmpty() ||
                played80s90sSongs.isNotEmpty()

        if (playedSongsLoaded) {
            Toast.makeText(this, "Played songs loaded", Toast.LENGTH_SHORT).show()
        } else {
            Toast.makeText(this, "No played songs found", Toast.LENGTH_SHORT).show()
        }
    }

    private fun resetPlayedSongs() {
        playedMovieSongs.clear()
        playedCountrySongs.clear()
        playedEuroSongs.clear()
        playedTwoThousandSongs.clear()
        playedRockSongs.clear()
        playedMelloSongs.clear()
        played80s90sSongs.clear()
        Toast.makeText(this, "Reset successful. All songs are available to play again.", Toast.LENGTH_SHORT).show()
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

    override fun onStop() {
        super.onStop()
        savePlayedSongs()
        SpotifyAppRemote.disconnect(spotifyAppRemote)
    }
}
