<template>
    <div class="password-prompt">
      <h2>Passwort eingeben</h2>
      <input
        type="password"
        v-model="password"
        placeholder="Passwort"
        @keyup.enter="checkPassword"
      />
      <button @click="checkPassword">OK</button>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </template>
  
  <script>

  export default {
    data() {
      return {
        password: '',
        error: ''
      };
    },
    methods: {
      checkPassword() {
        const correctPassword = 'lupine123'; // Replace with your desired password
        if (this.password === correctPassword) {
          this.$emit('password-correct');
        } else {
          this.error = 'Incorrect password. Please try again.';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .password-prompt {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }
  
  input {
    margin: 10px 0;
    padding: 8px;
    font-size: 16px;
  }
  
  button {
    padding: 8px 16px;
    font-size: 16px;
    cursor: pointer;
  }
  
  .error {
    color: red;
  }
  </style>