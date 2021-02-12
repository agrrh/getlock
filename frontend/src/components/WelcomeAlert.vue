<template>
  <v-col class="text-center mt-12">
    <h1 style="font-size: 56px">
      Welcome, user!
    </h1>
    <div v-if="isLoading" class="mt-4">
      <div class="welcome-alert-text loader-wrp font-weight-medium">
        <p class="loader-wrp__text">Loading list of sessions</p>
        <v-progress-circular
          class="ml-4"
          :size="16"
          :width="2"
          color="#009688"
          indeterminate
        ></v-progress-circular>
      </div>
    </div>
    <div v-else>
      <p class="welcome-alert-text mb-0 mt-4"> {{ quantityMessage }}</p>
      <p class="welcome-alert-text" v-if="!sessionsCount">
        You can check out 
        <a style="color: #009688">the official API guide</a>
        in order to add some.
      </p>
    </div>
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
    },
    isLoading() {
      return this.$store.state.listIsLoading
    }
  },
}
</script>

<style scoped>
.welcome-alert-text {
  font-size: 18px;
}

.loader-wrp {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loader-wrp__text {
  margin-bottom: 0;
}
</style>