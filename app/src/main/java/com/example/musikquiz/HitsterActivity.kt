package com.example.musikquiz

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.activity.ComponentActivity
import com.google.zxing.integration.android.IntentIntegrator
import com.google.zxing.integration.android.IntentResult
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.spotify.android.appremote.api.ConnectionParams
import com.spotify.android.appremote.api.Connector
import com.spotify.android.appremote.api.SpotifyAppRemote
import com.spotify.protocol.client.Subscription
import com.spotify.protocol.types.PlayerState
//import kotlinx.android.synthetic.main.activity_hitster.*

class HitsterActivity : ComponentActivity() {

    private var spotifyAppRemote: SpotifyAppRemote? = null
    private var playerStateSubscription: Subscription<PlayerState>? = null

    companion object {
        private const val CLIENT_ID = "YOUR_CLIENT_ID"
        private const val REDIRECT_URI = "YOUR_REDIRECT_URI"
        private const val TAG = "HitsterActivity"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_hitster)

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
                    openSpotify(result.contents)
                } else {
                    Toast.makeText(this, "Not a valid Spotify link", Toast.LENGTH_SHORT).show()
                }
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data)
        }
    }

    private fun openSpotify(uri: String) {
        val intent = Intent(Intent.ACTION_VIEW).apply {
            data = Uri.parse(uri)
            `package` = "com.spotify.music"
            // Set flags to clear any existing task and start a new one
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            putExtra(Intent.EXTRA_REFERRER, Uri.parse("android-app://${packageName}"))
        }
        if (intent.resolveActivity(packageManager) != null) {
            startActivity(intent)
        } else {
            Toast.makeText(this, "Spotify app not installed", Toast.LENGTH_SHORT).show()
        }
    }
}
