<template>
  <v-col class="text-center mt-12">
    <h1 style="font-size: 56px">
      Welcome, test!
    </h1>
    <p class="welcome-alert-text mb-0 mt-4"> {{ quantityMessage }}</p>
    <p class="welcome-alert-text" v-if="!sessionsCount">
      You can check out 
      <a style="color: #009688">the official API guide</a>
      in order to add some.
    </p>
  </v-col>
</template>

<script>
export default {
  name: 'WelcomeAlert',
  computed: {
    quantityMessage() {
      switch (this.sessionsCount) {
        case 0:
            return 'There are currently no active sessions'
        case 1: 
            return 'There is currently 1 active session'
        default:
            return `There are currently ${this.sessionsCount} active sessions`
      }
    },
    sessionsCount() {
      return this.$store.state.locks.length;
    }
  },
}
</script>

<style scoped>
.welcome-alert-text {
  font-size: 18px;
}
</style>