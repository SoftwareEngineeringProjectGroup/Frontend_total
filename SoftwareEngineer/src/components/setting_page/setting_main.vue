<template>
  <div class="setting-page">
    <div class="avatar-wrapper" @click="triggerAvatarInput">
      <div v-if="form.avatar" class="avatar-container">
        <img :src="form.avatar" class="avatar" alt="no"/>
      </div>
      <div v-else class="avatar-placeholder">
        <span>Upload</span>
      </div>
    </div>

    <!-- 隐藏的 file input 用于触发文件选择 -->
    <input
        ref="avatarInput"
        type="file"
        class="avatar-input"
        @change="handleAvatarChange"
        accept="image/*"
        style="display:none"
    />

    <el-form :model="form" label-width="140px" class="settings-form" :disabled="!isEditing" label-position="top"
             size="large">

      <!-- 性别 -->
      <el-form-item label="Gender">
        <el-radio-group v-model="form.gender">
          <el-radio :value="'male'">male</el-radio>
          <el-radio :value="'female'">female</el-radio>
          <el-radio :value="'other'">other</el-radio>
        </el-radio-group>
      </el-form-item>

      <!-- 个人 Prompt -->
      <el-form-item label="Personal prompt" style="font-size: 20px" size="large">
        <el-input
            v-model="form.prompt"
            type="textarea"
            placeholder="Please enter the prompt"

        ></el-input>
      </el-form-item>

      <!-- 特殊 API -->
      <el-form-item label="Extend">
        <el-input v-model="form.apiUrl" placeholder="Please enter the URL"></el-input>
      </el-form-item>

      <!-- 本地/联网 开关 -->
      <el-form-item label="Mode">
        <el-switch
            v-model="form.isShow"
            active-text="demo"
            inactive-text="local"
            active-color="#13ce66"
            inactive-color="#ff4949"
        ></el-switch>
      </el-form-item>

    </el-form>

    <el-button :type="buttonType" @click="handleButton" class="action-btn">
      {{ isEditing ? 'Save' : 'Edit' }}
    </el-button>
  </div>
</template>

<script setup>
import {onBeforeMount, ref} from 'vue';
import {
  ElForm,
  ElFormItem,
  ElInput,
  ElButton,
  ElSwitch,
  ElRadioGroup,
  ElRadio,
} from 'element-plus';
import {useStateStore} from "@/stores/stateStore";

const buttonType = ref("")

const form = ref({
  avatar: '',
  gender: 'male',
  prompt: '',
  isShow: true,
  apiUrl: '',
});

//初始化表格
const store = useStateStore()
onBeforeMount(() => {
  form.value.avatar = store.userImagePath;
  form.value.gender = store.gender;
  form.value.prompt = store.personalPrompt;
  if (store.baseUrl !== "http://10.252.130.135:8000" && store.baseUrl !== "http://127.0.0.1:8000") form.value.apiUrl = store.baseUrl;
  form.value.isShow = store.isShow;
});


const isEditing = ref(false);

const triggerAvatarInput = () => {
  const avatarInput = document.querySelector('.avatar-input');
  avatarInput.click();
};

const handleAvatarChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      form.value.avatar = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const handleEdit = () => {
  isEditing.value = true;
  buttonType.value = "success"
};

const handleSave = () => {
  console.log('保存设置:', form.value);
  store.setuserImagePath(form.value.avatar);
  store.setGender(form.value.gender)
  store.setPersonalPrompt(form.value.prompt)

  if (form.value.isShow) store.setbaseUrl("http://10.252.130.135:8000")
  else store.setbaseUrl("http://127.0.0.1:8000")

  if (form.value.apiUrl !== "") store.setbaseUrl(form.value.apiUrl);
  store.setIsShow(form.value.isShow)
  isEditing.value = false;
  buttonType.value = ""
};

const handleButton = () => {
  if (isEditing.value) handleSave();
  else handleEdit();
};
</script>

<style scoped>
.setting-page {
  width: 100%;
  height: 100vh;

  display: flex;
  flex-direction: column; /* 竖直排列 */
  justify-content: flex-start; /* 向上对齐 */
  align-items: center; /* 水平居中 */
  padding: 20px; /* 增加内边距，避免内容与顶部过于贴合 */
}

.settings-form {
  width: 480px;
  margin-top: 20px; /* 添加顶部外边距 */
  background-color: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 10px; /* 增加间距 */
  font-size: 18px; /* 调整整体字体大小 */
}

.avatar-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  position: relative;
  text-align: center;
  margin-bottom: 10px;
  margin-top: 40px;
}

.avatar-container, .avatar-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 3px solid #409EFF;
  background-color: #f0f2f5;
  overflow: hidden;
  transition: all 0.3s ease;
}

.avatar-container:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.avatar-placeholder span {
  color: #409EFF;
  font-weight: bold;
  font-size: 18px; /* 增加字体大小 */
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.el-form-item {
  margin-bottom: 25px; /* 增加表单项之间的间距 */
  font-size: 20px;
}

.el-input, .el-radio-group, .el-switch {
  border-radius: 8px;
}

.el-button {
  width: 480px;
  padding: 14px;
  border-radius: 8px;
  font-weight: bold;
  font-size: 18px; /* 增加按钮字体大小 */
  transition: background-color 0.3s ease;
  margin-top: 10px;
  height: 40px;
}

.el-button:focus {
  outline: none;
}

.el-switch .el-switch__core {
  border-radius: 30px;
}

.el-switch__label {
  font-size: 18px; /* 增加开关标签字体大小 */
}

h2 {
  text-align: center;
  color: #409EFF;
  margin-bottom: 20px;
}

.avatar-input {
  display: none;
}

</style>