<template>
<v-main>
    <v-container>
      <v-alert
        type="info"
        dense
        text
      >
        Main component
      </v-alert>
      <v-btn
        @click="fetchData"
      >
        fetch
      </v-btn>
    </v-container>
  </v-main>
</template>

<script>
import Axios from 'axios';

export default {
  name: 'Main',
  methods: {
    fetchData() {
      Axios.get('https://getlock.tech/v1/locks')
      .then(response => {
        console.log(response)
      })
      .catch(err => {
        console.log(err)
      })
    }
  }
}
</script>
