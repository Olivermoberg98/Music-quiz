package com.example.musikquiz

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.activity.ComponentActivity
import com.google.zxing.integration.android.IntentIntegrator
import com.google.zxing.integration.android.IntentResult

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val hitsterButton: Button = findViewById(R.id.hitsterButton)
        val categoriesButton: Button = findViewById(R.id.categoriesButton)
        val tpButton: Button = findViewById(R.id.tpButton)

        hitsterButton.setOnClickListener {
            val intent = Intent(this, HitsterActivity::class.java)
            startActivity(intent)
        }

        categoriesButton.setOnClickListener {
            val intent = Intent(this, CategoriesActivity::class.java)
            startActivity(intent)
        }

        tpButton.setOnClickListener {
            val intent = Intent(this, TPActivity::class.java)
            startActivity(intent)
        }
    }
}
