<template>
  <v-app>
    <Header/>
    <v-slide-x-transition appear mode="out-in">
      <router-view></router-view>
    </v-slide-x-transition>
    <Footer/>
  </v-app>
</template>

<script>
import Header from './components/Header';
import Footer from './components/Footer';

export default {
  name: 'App',

  components: {
    Header,
    Footer
  },

  data: () => ({
    //
  }),
};
</script>
