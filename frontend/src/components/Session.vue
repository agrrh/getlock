<template>
  <v-col>
    <v-slide-x-transition 
      appear 
      mode="out-in" 
      v-for="lock in $store.state.locks" 
      :key="lock.uuid"
    >
      <v-card class="mb-4 py-4 px-6">
        <span class="font-weight-bold">
          Session:
        </span> 
        {{ lock }}
        <p style="color: #009688" class="font-weight-bold mb-3">
          In progress
        </p>
        <v-progress-linear
          color="#3f51b5"
          buffer-value="0"
          stream
        ></v-progress-linear>
      </v-card>
    </v-slide-x-transition>
  </v-col>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Session',
  computed: {
    ...mapGetters([
      'getLocks'
    ])
  }
}
</script>