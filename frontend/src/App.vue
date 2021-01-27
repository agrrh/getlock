<template>
  <v-app>
    <DevPanel/>
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
import DevPanel from './components/DevPanel';

export default {
  name: 'App',

  components: {
    Header,
    Footer,
    DevPanel
  },

  data: () => ({
    //
  }),
};
</script>

<style>
@media (min-width:1904px) {
    .container {
        max-width: 1185px !important;
    }
}
</style>
