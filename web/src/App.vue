<template>
  <div>
    <ArticleCard
      v-for="article in articles"
      :key="article.id"
      :title="article.title"
      :link="article.link"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ArticleCard from './components/ArticleCard.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
const articles = ref([])

onMounted(async () => {
  try {
    // Fetch IDs
    const idsResponse = await fetch(`${API_BASE_URL}/articles/gen_ai`)
    if (!idsResponse.ok) throw new Error('Failed to fetch article IDs')
    const responseJson = await idsResponse.json()
    const ids = responseJson.article_ids


    // Fetch each article by ID
    const detailResponses = await Promise.all(
      ids.map(id =>
        fetch(`${API_BASE_URL}/articles/${id}`).then(res => {
          if (!res.ok) throw new Error(`Failed to fetch article ${id}`)
          return res.json()
        })
      )
    )

    articles.value = detailResponses
  } catch (err) {
    console.error('Error fetching articles:', err)
  }
})
</script>
