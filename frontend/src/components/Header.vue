<template>
  <v-app-bar
      app
      color="#607d8b"
      dark
  >
    <v-container>
      <v-row>
        <div class="d-flex align-center">
          <h1>
            <router-link class="getlock-logo" to="/">GETLOCK</router-link>
          </h1>
        </div>
        <v-spacer></v-spacer>
        <v-btn 
          class="mr-4"
          icon
          v-if="isDevMode"
          @click="toggleDevPanel"
        >
          <v-icon>mdi-cog</v-icon>
        </v-btn>
        <v-icon>mdi-account-reactivate</v-icon>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
import Vue from 'vue'

export default {
  methods: {
    toggleDevPanel() {
      this.$store.commit('toggleDevPanel')
    }
  },
  computed: {
    isDevMode() {
      return Vue.config.devtools
    }
  }
}
</script>

<style scoped>
  .getlock-logo {
    text-decoration: none;
    color: white;
  }
</style>