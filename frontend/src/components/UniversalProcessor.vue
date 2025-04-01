// frontend/src/components/UniversalProcessor.vue
<template>
  <div class="processor">
    <div class="input-section">
      <select v-model="requestType">
        <option value="text_to_video">نص إلى فيديو</option>
        <option value="document_analysis">تحليل المستندات</option>
        <option value="file_conversion">تحويل الملفات</option>
        <!-- جميع أنواع الخدمات الأخرى -->
      </select>
      
      <textarea v-if="inputType === 'text'" v-model="inputText"></textarea>
      <input v-else type="file" @change="handleFileUpload">
      
      <button @click="submitTask">معالجة</button>
    </div>
    
    <div class="result-section" v-if="result">
      <video v-if="resultType === 'video'" :src="result" controls></video>
      <pre v-else-if="resultType === 'text'">{{ result }}</pre>
      <a v-else :href="result" download>تحميل الملف الناتج</a>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      requestType: 'text_to_video',
      inputText: '',
      inputFile: null,
      result: null,
      resultType: null
    }
  },
  computed: {
    inputType() {
      // تحديد نوع الإدخال بناءً على نوع الطلب
      return ['text_to_video', 'text_analysis'].includes(this.requestType) 
        ? 'text' 
        : 'file'
    }
  },
  methods: {
    async submitTask() {
      const formData = new FormData()
      if (this.inputType === 'file') {
        formData.append('input_data', this.inputFile)
      } else {
        formData.append('input_data', this.inputText)
      }
      
      const response = await this.$axios.post('/api/process', {
        request_type: this.requestType,
        input_data: this.inputType === 'text' ? this.inputText : formData,
        params: {}
      })
      
      this.pollTaskResult(response.data.task_id)
    },
    async pollTaskResult(taskId) {
      const checkStatus = async () => {
        const response = await this.$axios.get(`/api/task/${taskId}`)
        if (response.data.status === 'COMPLETED') {
          this.result = response.data.result
          this.determineResultType()
        } else if (response.data.status !== 'FAILED') {
          setTimeout(checkStatus, 1000)
        }
      }
      await checkStatus()
    },
    determineResultType() {
      // تحديد نوع النتيجة لعرضها بشكل صحيح
      if (typeof this.result === 'string') {
        if (this.result.startsWith('http')) {
          this.resultType = 'file'
        } else {
          this.resultType = 'text'
        }
      } else if (this.result instanceof Blob) {
        this.resultType = this.requestType.includes('video') ? 'video' : 'file'
      }
    }
  }
}
</script>