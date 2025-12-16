package com.example.musikquiz

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.ImageButton
import com.journeyapps.barcodescanner.BarcodeCallback
import com.journeyapps.barcodescanner.BarcodeResult
import com.journeyapps.barcodescanner.DecoratedBarcodeView

class ScannerActivity : Activity() {

    private lateinit var barcodeView: DecoratedBarcodeView
    private var isFlashOn = false
    private lateinit var flashButton: ImageButton

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.scanner_activity)

        barcodeView = findViewById(R.id.barcode_scanner)
        barcodeView.statusView?.visibility = View.GONE


        // Start scanning
        barcodeView.decodeContinuous(object : BarcodeCallback {
            override fun barcodeResult(result: BarcodeResult?) {
                result?.text?.let {
                    val data = Intent().apply { putExtra("SCAN_RESULT", it) }
                    setResult(Activity.RESULT_OK, data)
                    finish()
                }
            }
        })

        // Flash toggle
        flashButton = findViewById(R.id.flashButton)
        flashButton.setOnClickListener {
            toggleFlash()
        }

        // Close button
        val closeButton: ImageButton = findViewById(R.id.closeButton)
        closeButton.setOnClickListener {
            setResult(Activity.RESULT_CANCELED)
            finish()
        }
    }

    override fun onResume() {
        super.onResume()
        barcodeView.resume()
    }

    override fun onPause() {
        super.onPause()
        barcodeView.pause()
    }

    private fun toggleFlash() {
        isFlashOn = !isFlashOn

        if (isFlashOn) {
            flashButton.setImageResource(R.drawable.ic_flash_on)
            barcodeView.setTorchOn()
        } else {
            flashButton.setImageResource(R.drawable.ic_flash_off)
            barcodeView.setTorchOff()
        }
    }
}
