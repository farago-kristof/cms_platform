<template>
  <div class="article-card">
    <h2 class="title">{{ title }}</h2>
    <p class="summary">{{ summary }}</p>
    <a class="link" :href="link" target="_blank" rel="noopener noreferrer">Read more</a>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  summary: {
    type: String,
    required: false,
    default: ''
  },
  link: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
.article-card {
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 6px;
  max-width: 600px;
  margin: 1rem auto;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.title {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: #35495e;
}

.summary {
  font-size: 1rem;
  margin-bottom: 1rem;
  color: #555;
}

.link {
  color: #42b983;
  font-weight: 600;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}
</style>
