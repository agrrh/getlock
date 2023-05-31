<template>
  <v-col class="mt-8">
    <h1 style="font-size: 40px">
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
      <p class="welcome-alert-text mb-0 mt-2"> {{ quantityMessage }}</p>
      <p class="welcome-alert-text" v-if="!sessionsCount">
        You can check out quick guide below in order to add some,
        or visit <a class="welcome-alert__link" href="https://getlock.agrrh.com/">getlock.agrrh.com</a> for more examples and info.
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
  font-size: 16px;
}

.loader-wrp {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.loader-wrp__text {
  margin-bottom: 0;
}

.welcome-alert__link {
  color: #009688;
}
</style>
