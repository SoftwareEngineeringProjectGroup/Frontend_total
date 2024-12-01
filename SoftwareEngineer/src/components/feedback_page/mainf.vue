
<template>
  <div class="feedback-form">
    <div class="form-container">
      <!-- 如果反馈未提交，显示表单 -->
      <div v-if="!feedbackSent">
        <h1 class="title">Send Us Your Feedback</h1>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="name">Your Name</label>
            <input
                v-model="feedback.name"
                type="text"
                id="name"
                placeholder="Enter your name"
                required
            />
          </div>

          <div class="form-group">
            <label for="email">Your Email</label>
            <input
                v-model="feedback.email"
                type="email"
                id="email"
                placeholder="Enter your email"
                required
                ref="emailInput"
                @input="validateEmail"
            />
          </div>

          <div class="form-group">
            <label for="message">Feedback Message</label>
            <textarea
                v-model="feedback.message"
                id="message"
                placeholder="Enter your feedback"
                rows="5"
                required
            ></textarea>
          </div>

          <button type="submit" :disabled="isSubmitting" class="submit-btn">
            Submit Feedback
          </button>
        </form>
      </div>

      <!-- 如果反馈已提交，显示感谢信息和笑脸 -->
      <div v-if="feedbackSent" class="thank-you">
        <div class="smiley">&#128578;</div>
        <p class="thank-you-message">Thank you for your feedback!</p>
      </div>

      <!-- 显示提交失败时的错误 -->
      <div v-if="error" class="error">
        <p>{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const feedback = ref({
  name: '',
  email: '',
  message: ''
})

const isSubmitting = ref(false)
const feedbackSent = ref(false)
const error = ref(false)
const errorMessage = ref('')

const emailInput = ref(null)

const handleSubmit = async () => {
  if (!feedback.value.name || !feedback.value.email || !feedback.value.message) {
    return
  }

  isSubmitting.value = true
  error.value = false
  errorMessage.value = ''

  // try {
  //   const response = await sendFeedback(feedback.value)
  //   if (response.status === 200) {
  //     feedbackSent.value = true
  //   } else {
  //     throw new Error('Failed to submit feedback')
  //   }
  // } catch (err) {
  //   error.value = true
  //   errorMessage.value = err.message || 'An error occurred. Please try again.'
  // } finally {
  //   isSubmitting.value = false
  // }
  setTimeout(()=>{feedbackSent.value = true},2000);

}

const sendFeedback = (feedbackData) => {
  return axios.post('/api/feedback', feedbackData) // 这里的 '/api/feedback' 替换成你的服务器地址
}

const validateEmail = () => {
  const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/
  if (!emailPattern.test(feedback.value.email)) {
    emailInput.value.setCustomValidity("Please enter a valid email address.")
  } else {
    emailInput.value.setCustomValidity("")
  }
}
</script>

<style scoped>
/* 使用渐变背景和更现代的布局 */
.feedback-form {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-container {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

.title {
  text-align: center;
  color: #333;
  font-size: 2rem;
  margin-bottom: 20px;
  font-family: 'Roboto', sans-serif;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-size: 1.1rem;
  margin-bottom: 8px;
  color: #555;
  font-family: 'Roboto', sans-serif;
}

input, textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  font-family: 'Roboto', sans-serif;
  box-sizing: border-box;
  transition: border-color 0.3s ease-in-out;
}

input:focus, textarea:focus {
  border-color: #ff6f61;
  outline: none;
}

textarea {
  resize: vertical;
}

.submit-btn {
  background-color: #ff6f61;
  color: white;
  font-size: 1.1rem;
  padding: 15px;
  border: none;
  border-radius: 8px;
  width: 100%;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.submit-btn:hover {
  background-color: #e65a4e;
}

.confirmation, .error {
  text-align: center;
  font-size: 1.1rem;
  margin-top: 20px;
  font-family: 'Roboto', sans-serif;
}

.confirmation {
  color: #4caf50;
}

.error {
  color: #ff4e50;
}

/* 感谢信息的样式 */
.thank-you {
  text-align: center;
  font-size: 1.5rem;
  color: #4caf50;
  font-family: 'Roboto', sans-serif;
}

.smiley {
  font-size: 5rem;
}

.thank-you-message {
  margin-top: 10px;
  font-size: 1.2rem;
}
</style>
