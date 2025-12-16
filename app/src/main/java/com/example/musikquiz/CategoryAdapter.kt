// app/src/main/java/com/example/musikquiz/CategoryAdapter.kt
package com.example.musikquiz

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import androidx.recyclerview.widget.RecyclerView

class CategoryAdapter(
    private var categories: MutableList<Category>,
    private val onCategoryClick: (Category) -> Unit,
    private val bgRes: List<Int>
) : RecyclerView.Adapter<CategoryAdapter.CategoryViewHolder>() {

    inner class CategoryViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val button: Button = view.findViewById(R.id.categoryButton)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CategoryViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_category, parent, false)
        return CategoryViewHolder(view)
    }

    override fun onBindViewHolder(holder: CategoryViewHolder, position: Int) {
        val category = categories[position]
        holder.button.text = category.name

        // Set one of the six backgrounds to resemble TP look (cycle if > 6)
        if (bgRes.isNotEmpty()) {
            val resId = bgRes[position % bgRes.size]
            holder.button.setBackgroundResource(resId)
        }

        holder.button.setOnClickListener { onCategoryClick(category) }
    }

    override fun getItemCount(): Int = categories.size

    fun replaceAll(newList: List<Category>) {
        // Replace with a *new* list so we don’t mutate the one owned by the activity
        categories = newList.toMutableList()
        notifyDataSetChanged()
    }
}
