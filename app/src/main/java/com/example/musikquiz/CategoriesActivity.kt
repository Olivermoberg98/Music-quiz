// app/src/main/java/com/example/musikquiz/CategoriesActivity.kt
package com.example.musikquiz

import android.app.AlertDialog
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.ImageButton
import android.widget.TextView
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.spotify.android.appremote.api.ConnectionParams
import com.spotify.android.appremote.api.Connector
import com.spotify.android.appremote.api.SpotifyAppRemote
import com.spotify.protocol.client.Subscription
import com.spotify.protocol.types.PlayerState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import androidx.lifecycle.lifecycleScope
import org.apache.poi.ss.usermodel.WorkbookFactory
import java.io.InputStream

class CategoriesActivity : ComponentActivity() {

    private var spotifyAppRemote: SpotifyAppRemote? = null
    private var playerStateSubscription: Subscription<PlayerState>? = null

    private val categoryMappings = HashMap<String, Map<String, String>>()
    private val playedSongsMap = HashMap<String, MutableList<String>>()

    private lateinit var allCategories: List<Category>
    private lateinit var displayedCategories: MutableList<Category>
    private lateinit var adapter: CategoryAdapter

    private lateinit var answerTitleTextView: TextView
    private lateinit var playPauseButton: ImageButton
    private lateinit var resetButton: Button

    companion object {
        private const val CLIENT_ID = "fa6a760e4e794ecb8c642e8d3de00b50"
        private const val REDIRECT_URI = "musikquiz://callback"
        private const val TAG = "CategoriesActivity"
        private const val REQUIRED_CATEGORY_COUNT = 6
    }

    // The six backgrounds in the same order you had before
    private val categoryBgRes = listOf(
        R.drawable.categories_button_background_1,
        R.drawable.categories_button_background_2,
        R.drawable.categories_button_background_3,
        R.drawable.categories_button_background_4,
        R.drawable.categories_button_background_5,
        R.drawable.categories_button_background_6
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_categories)

        answerTitleTextView = findViewById(R.id.answerTitleTextView)
        playPauseButton = findViewById(R.id.play_pause_button)
        resetButton = findViewById(R.id.resetButton)

        playPauseButton.setOnClickListener { togglePlayPause() }
        resetButton.setOnClickListener { resetAllPlayedSongs() }

        // RecyclerView
        val recyclerView: RecyclerView = findViewById(R.id.categoriesRecyclerView)
        recyclerView.layoutManager = LinearLayoutManager(this)
        displayedCategories = mutableListOf()
        adapter = CategoryAdapter(mutableListOf(), { category -> onCategoryClicked(category) }, categoryBgRes)
        recyclerView.adapter = adapter

        val manageButton: Button = findViewById(R.id.manageCategoriesButton)
        manageButton.setOnClickListener { showManageCategoriesDialog() }

        // Load categories.json (IO thread)
        lifecycleScope.launch(Dispatchers.IO) {
            allCategories = loadCategoriesFromJson()

            if (allCategories.isEmpty()) {
                Log.e(TAG, "categories.json is empty or missing. Put categories.json in assets.")
                withContext(Dispatchers.Main) {
                    Toast.makeText(this@CategoriesActivity, "No categories found. Check assets/categories.json", Toast.LENGTH_LONG).show()
                }
                return@launch
            }

            if (allCategories.size < REQUIRED_CATEGORY_COUNT) {
                Log.w(TAG, "categories.json contains fewer than $REQUIRED_CATEGORY_COUNT items.")
                withContext(Dispatchers.Main) {
                    Toast.makeText(this@CategoriesActivity, "Need at least $REQUIRED_CATEGORY_COUNT categories in categories.json", Toast.LENGTH_LONG).show()
                }
            }

            // After loading categories, update displayed list on the main thread
            withContext(Dispatchers.Main) {
                if (allCategories.isEmpty()) {
                    Toast.makeText(this@CategoriesActivity, "categories.json is empty or missing", Toast.LENGTH_LONG).show()
                } else {
                    updateDisplayedCategoriesFromPrefs()
                }
            }


            // Load played songs (IO)
            loadPlayedSongsFromPrefs()
        }
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

    private fun onCategoryClicked(category: Category) {
        lifecycleScope.launch(Dispatchers.IO) {
            val mapping = categoryMappings[category.name] ?: run {
                val m = loadSongMappings(category.fileName, category.keyColumn, category.valueColumn)
                categoryMappings[category.name] = m
                m
            }

            val playedForCategory = playedSongsMap.getOrPut(category.name) { mutableListOf() }

            withContext(Dispatchers.Main) {
                if (mapping.isEmpty()) {
                    Toast.makeText(this@CategoriesActivity, "No songs available in this category file.", Toast.LENGTH_SHORT).show()
                } else {
                    playRandomTrack(mapping, playedForCategory)
                }
            }
        }
    }

    private fun playRandomTrack(map: Map<String, String>, playedSongs: MutableList<String>) {
        val availableSongs = map.keys.filterNot { playedSongs.contains(it) }
        if (availableSongs.isEmpty()) {
            Toast.makeText(this, "All songs in this category have been played. Resetting that category.", Toast.LENGTH_LONG).show()
            playedSongs.clear()
            return
        }

        val randomTrackUrl = availableSongs.randomOrNull()
        if (randomTrackUrl == null) {
            Toast.makeText(this, "No tracks available to play", Toast.LENGTH_LONG).show()
            return
        }

        val randomTrackUri = convertToSpotifyUri(randomTrackUrl)
        if (randomTrackUri == null) {
            Toast.makeText(this, "Invalid track URL in mapping: $randomTrackUrl", Toast.LENGTH_LONG).show()
            return
        }

        spotifyAppRemote?.let { remote ->
            remote.playerApi.play(randomTrackUri)

            playerStateSubscription?.cancel()
            playerStateSubscription = null

            playerStateSubscription = remote.playerApi.subscribeToPlayerState()
            playerStateSubscription?.setEventCallback { playerState ->
                val track = playerState.track
                if (track != null) {
                    val songUri = track.uri
                    val songUrl = convertToSpotifyUrl(songUri)
                    if (songUri == randomTrackUri && !playedSongs.contains(randomTrackUrl)) {
                        val answer = map[songUrl]
                        runOnUiThread {
                            answerTitleTextView.text = answer ?: ""
                            playedSongs.add(randomTrackUrl)
                        }
                    }
                }
            }
        } ?: run {
            Toast.makeText(this, "Failed to connect to Spotify.", Toast.LENGTH_LONG).show()
        }
    }

    private fun convertToSpotifyUri(link: String): String? {
        return when {
            link.startsWith("spotify:track:") -> link
            link.contains("open.spotify.com/track/") -> {
                val idPart = link.split("track/").last().split("?").firstOrNull()
                idPart?.let { "spotify:track:$it" }
            }
            link.startsWith("https://open.spotify.com/") -> {
                val uriPart = link.split("/").last().split("?").firstOrNull()
                uriPart?.let { "spotify:track:$it" }
            }
            else -> null
        }
    }

    private fun convertToSpotifyUrl(uri: String): String? {
        return when {
            uri.startsWith("spotify:track:") -> {
                val id = uri.split(":").lastOrNull()
                id?.let { "https://open.spotify.com/track/$it" }
            }
            uri.startsWith("https://open.spotify.com/") -> uri
            else -> null
        }
    }

    private fun resetAllPlayedSongs() {
        playedSongsMap.values.forEach { it.clear() }
        Toast.makeText(this, "Reset successful. All songs are available again for the enabled categories.", Toast.LENGTH_SHORT).show()
    }

    private fun savePlayedSongsToPrefs() {
        val sharedPreferences = getSharedPreferences("PlayedSongsPrefs", MODE_PRIVATE)
        val editor = sharedPreferences.edit()
        val gson = Gson()
        for ((categoryName, list) in playedSongsMap) {
            editor.putString("played_$categoryName", gson.toJson(list))
        }
        editor.apply()
    }

    private fun loadPlayedSongsFromPrefs() {
        val sharedPreferences = getSharedPreferences("PlayedSongsPrefs", MODE_PRIVATE)
        val gson = Gson()
        val type = object : TypeToken<MutableList<String>>() {}.type

        for (cat in allCategories) {
            val json = sharedPreferences.getString("played_${cat.name}", "[]")
            val list: MutableList<String> = gson.fromJson(json, type)
            playedSongsMap[cat.name] = list
        }
    }

    override fun onStop() {
        super.onStop()
        savePlayedSongsToPrefs()
        saveEnabledCategoriesToPrefs()
        SpotifyAppRemote.disconnect(spotifyAppRemote)
    }

    private fun loadCategoriesFromJson(): List<Category> {
        return try {
            val input: InputStream = assets.open("categories.json")
            val json = input.bufferedReader().use { it.readText() }
            val gson = Gson()
            val type = object : TypeToken<List<Category>>() {}.type
            gson.fromJson(json, type)
        } catch (e: Exception) {
            Log.e(TAG, "Failed to load categories.json", e)
            emptyList()
        }
    }

    private fun saveEnabledCategoriesToPrefs() {
        val sharedPreferences = getSharedPreferences("CategoriesPrefs", MODE_PRIVATE)
        val editor = sharedPreferences.edit()
        val enabledSet = displayedCategories.map { it.name }.toSet()
        editor.putStringSet("enabled_categories", enabledSet)
        editor.apply()
    }

    private fun getEnabledCategoriesFromPrefs(): Set<String> {
        val sharedPreferences = getSharedPreferences("CategoriesPrefs", MODE_PRIVATE)
        val set = sharedPreferences.getStringSet("enabled_categories", null)

        return if (set != null && set.isNotEmpty()) {
            set
        } else {
            // Default: first 6 or fewer
            val default = allCategories.take(REQUIRED_CATEGORY_COUNT).map { it.name }.toSet()
            Log.d(TAG, "Defaulting enabled categories: $default")
            default
        }
    }


    private fun updateDisplayedCategoriesFromPrefs() {
        val enabled = getEnabledCategoriesFromPrefs()
        Log.d(TAG, "Enabled categories: $enabled")
        displayedCategories.clear()
        displayedCategories.addAll(allCategories.filter { enabled.contains(it.name) })
        adapter.replaceAll(displayedCategories)

        if (displayedCategories.isEmpty()) {
            Toast.makeText(this, "No categories are enabled. Use Manage categories to enable 6 categories.", Toast.LENGTH_LONG).show()
        }
    }


    private fun showManageCategoriesDialog() {
        if (allCategories.isEmpty()) {
            Toast.makeText(this, "No categories defined.", Toast.LENGTH_SHORT).show()
            return
        }

        val names = allCategories.map { it.name }.toTypedArray()
        val enabledSet = getEnabledCategoriesFromPrefs()
        val checked = BooleanArray(names.size) { index -> enabledSet.contains(names[index]) }

        val builder = AlertDialog.Builder(this)
            .setTitle("Select exactly $REQUIRED_CATEGORY_COUNT categories")

        builder.setMultiChoiceItems(names, checked) { _, which, isChecked ->
            checked[which] = isChecked
        }

        builder.setNegativeButton("Cancel", null)

        // Create dialog so we can override positive click (prevent dismiss if not exactly 6)
        val dialog = builder.create()
        dialog.setButton(AlertDialog.BUTTON_POSITIVE, "Save") { _, _ -> /* noop - replaced below */ }
        dialog.show()

        // override positive button click
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
            val newEnabled = names.filterIndexed { index, _ -> checked[index] }.toSet()
            if (newEnabled.size != REQUIRED_CATEGORY_COUNT) {
                Toast.makeText(this, "Please select exactly $REQUIRED_CATEGORY_COUNT categories (selected: ${newEnabled.size})", Toast.LENGTH_SHORT).show()
            } else {
                val prefs = getSharedPreferences("CategoriesPrefs", MODE_PRIVATE)
                prefs.edit().putStringSet("enabled_categories", newEnabled).apply()
                updateDisplayedCategoriesFromPrefs()
                dialog.dismiss()
            }
        }
    }

    private suspend fun loadSongMappings(fileName: String, keyColumn: Int, valueColumn: Int): Map<String, String> {
        val map = HashMap<String, String>()
        try {
            val inputStream: InputStream = assets.open(fileName)
            val workbook = WorkbookFactory.create(inputStream)
            val sheet = workbook.getSheetAt(0)
            for (row in sheet) {
                if (row.rowNum == 0) continue
                val key = row.getCell(keyColumn)?.stringCellValue?.trim()
                val value = row.getCell(valueColumn)?.stringCellValue?.trim()
                if (key != null && value != null) {
                    map[key] = value
                }
            }
            workbook.close()
        } catch (e: Exception) {
            Log.e(TAG, "Error loading Excel file: $fileName", e)
        }
        return map
    }

    private fun updatePlayPauseButton() {
        spotifyAppRemote?.playerApi?.subscribeToPlayerState()?.setEventCallback { playerState ->
            if (playerState.isPaused) {
                playPauseButton.setImageResource(R.drawable.ic_play)
            } else {
                playPauseButton.setImageResource(R.drawable.ic_pause)
            }
        }
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
}
