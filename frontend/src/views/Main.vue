<template>
  <v-main>
    <v-container>
      <v-row>
        <WelcomeAlert/>
      </v-row>
      <v-row>
        <v-col v-if="$store.state.locks.length !== 0">
          <Session 
            v-for="lock in sortByActivity" 
            :key="lock.uuid"
            :lock="lock"
          />
        </v-col>
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
    fetchData(setLoader) {
      this.$store.dispatch('fetchData', setLoader);
    },
    resendReq() {
      setTimeout(() => {
        this.fetchData(false);
        this.resendReq()
      }, 5000)
    }
  },
  computed: {
    sortByTtl() {
      const locks = this.$store.state.locks;
      return locks.sort((a, b) => {
        return a.ttl - b.ttl;
      })
    },
    sortByActivity() {
      const sortedByTtl = this.sortByTtl;
      return sortedByTtl.sort((a, b) => {
        return a.expired - b.expired;
      })
    },
  },
  mounted() {
    this.fetchData(true);
    this.resendReq();
  }
}
</script>
