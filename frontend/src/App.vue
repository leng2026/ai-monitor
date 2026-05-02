<template>
  <div class="container">
    <h1>品牌监测区</h1>
    <input v-model="brand" type="text" placeholder="输入品牌名（如：瑞幸）" />
    <button @click="monitor">查询</button>
    <div v-if="monitorData && !monitorData.error" class="monitor-result">
      <p><strong>品牌：</strong>{{ monitorData.brand }}</p>
      <p><strong>热度：</strong>{{ monitorData.status }}</p>
      <p><strong>平台提及：</strong></p>
      <ul>
        <li v-for="(mentioned, platform) in monitorData.platforms" :key="platform">
          {{ platform }}：{{ mentioned ? '🔥 提及' : '⚪ 未提及' }}
        </li>
      </ul>
      <p><strong>总结：</strong>{{ monitorData.summary }}</p>
    </div>
    <div v-if="monitorData && monitorData.error" style="color:red;">
      {{ monitorData.error }}
    </div>

    <h1>内容生成区</h1>
    <textarea v-model="prompt" rows="10" placeholder="输入提示词"></textarea>
    <button @click="generate">生成</button>
    <div v-if="content" class="generated-content">{{ content }}</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      brand: '',
      monitorData: null,
      prompt: '',
      content: ''
    }
  },
  methods: {
    async monitor() {
      try {
        const res = await axios.post('http://localhost:8000/monitor', { brand: this.brand })
        this.monitorData = res.data
      } catch (e) {
        this.monitorData = { error: e.message }
      }
    },
    async generate() {
      try {
        const res = await axios.post('http://localhost:8000/generate', { prompt: this.prompt })
        this.content = res.data?.content || res.data?.error || JSON.stringify(res.data)
      } catch (e) {
        this.content = '请求失败: ' + e.message
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
input, textarea {
  display: block;
  width: 100%;
  margin: 8px 0;
  padding: 8px;
  font-size: 16px;
}
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
.monitor-result {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
  margin-top: 15px;
}
.generated-content {
  background: #f0f9ff;
  padding: 15px;
  border-radius: 8px;
  margin-top: 15px;
  white-space: pre-wrap;
}
</style>
