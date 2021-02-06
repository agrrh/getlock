<template>
  <v-slide-x-transition 
    appear 
    mode="out-in" 
  >
    <v-navigation-drawer 
      v-if="$store.state.devPanelVisible"
      fixed
      mini-variant
      mini-variant-width="64"
    >
      <v-list-item class="px-2 py-1">
        <v-list-item-avatar>
          <v-icon>mdi-cog</v-icon>
        </v-list-item-avatar>
      </v-list-item>

      <v-divider></v-divider>
      <v-list dense>
        <DevPanelBtn
          :btnMethod="putLock"
          iconMdi="mdi-lock-open-plus"
        >
        Add session
        </DevPanelBtn>
        <DevPanelBtn
          :btnMethod="generateId"
          iconMdi="mdi-account-reactivate"
        >
        Generate ID
        </DevPanelBtn>
      </v-list>
    </v-navigation-drawer>
  </v-slide-x-transition>
</template>

<script>
import Axios from 'axios'
import DevPanelBtn from './DevPanelBtn'

export default {
  components: {
    DevPanelBtn
  },
  methods: {
    generateId() {
      Axios.get('https://www.uuidgenerator.net/api/version4')
      .then(response => {
        this.$store.commit('updateSessionId', response.data);
      })
      .catch(err => {
        console.log(err);
      })
    },
    getId() {
      const id = new Promise((resolve) => {
        const data = Axios.get('https://www.uuidgenerator.net/api/version4');
        resolve(data);
      })
      return id;
    },
    async putLock() {
      await this.getId()
      .then(response => {
        Axios.put(`https://getlock.tech/v2/~test/${response.data}`,
          {},
          {
            headers: {
              'X-Getlock-Auth': 'test'
            }
          }
        )
      })
      .then(response => {
        console.log(response);
        this.$store.dispatch('fetchData');
      })
      .catch(err => {
        console.log(err)
      })
    }
  },
}
</script>