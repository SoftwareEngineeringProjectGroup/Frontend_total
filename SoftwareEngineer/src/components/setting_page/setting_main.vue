<template>
  <div class="setting-page">
    <div class="avatar-wrapper" @click="triggerAvatarInput">
      <div v-if="form.avatar" class="avatar-container">
        <img :src="form.avatar" class="avatar" alt="no"/>
      </div>
      <div v-else class="avatar-placeholder">
        <span>上传头像</span>
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
      <el-form-item label="性别">
        <el-radio-group v-model="form.gender">
          <el-radio :value="'male'">男</el-radio>
          <el-radio :value="'female'">女</el-radio>
          <el-radio :value="'other'">其他</el-radio>
        </el-radio-group>
      </el-form-item>

      <!-- 个人 Prompt -->
      <el-form-item label="个人 Prompt" style="font-size: 20px" size="large">
        <el-input
            v-model="form.prompt"
            type="textarea"
            placeholder="请输入您的个人提示语"

        ></el-input>
      </el-form-item>

      <!-- 特殊 API -->
      <el-form-item label="特殊 AP">
        <el-input v-model="form.apiUrl" placeholder="请输入 AP 地址"></el-input>
      </el-form-item>

      <!-- 本地/联网 开关 -->
      <el-form-item label="联网">
        <el-switch
            v-model="form.isOnline"
            active-text="联网"
            inactive-text="本地"
            active-color="#13ce66"
            inactive-color="#ff4949"
        ></el-switch>
      </el-form-item>

    </el-form>

    <el-button type="success" @click="handleButton" class="action-btn">
      {{ isEditing ? '保存设置' : '编辑' }}
    </el-button>
  </div>
</template>

<script setup>
import {ref} from 'vue';
import {
  ElForm,
  ElFormItem,
  ElInput,
  ElButton,
  ElSwitch,
  ElRadioGroup,
  ElRadio,
} from 'element-plus';

const form = ref({
  avatar: '',
  gender: 'male',
  prompt: '鸡你太美',
  isOnline: true,
  apiUrl: 'app',
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
};

const handleSave = () => {
  console.log('保存设置:', form.value);
  isEditing.value = false;
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
  justify-content: center; /* 垂直居中 */
  align-items: center; /* 水平居中 */
  padding: 10px; /* 加入一些内边距，防止内容靠边显示 */
}

.settings-form {
  width: 480px;
  margin: 0 auto;
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
  margin-bottom: 20px;
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