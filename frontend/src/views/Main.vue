<template>
  <v-main>
    <v-container>
      <v-row>
        <WelcomeAlert/>
      </v-row>
      <v-row>
        <Session v-if="$store.state.locks.length !== 0" />
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import Session from '../components/Session';
import WelcomeAlert from '../components/WelcomeAlert';

export default {
  name: 'Main',
  components: {
    Session,
    WelcomeAlert,
  },
  methods: {
    fetchData() {
      this.$store.dispatch('fetchData');
    }
  },
  mounted() {
    this.fetchData();
  }
}
</script>
