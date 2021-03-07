<template>
  <v-app-bar
      app
      color="primary"
      dark
  >
    <v-container>
      <v-row>
        <div class="d-flex align-center ml-6">
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
        <v-btn 
          class="mr-4"
          icon
          @click="$vuetify.theme.dark = !$vuetify.theme.dark"
        >
          <v-icon>mdi-brightness-6</v-icon>
        </v-btn>
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