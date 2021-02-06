import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    dark: true,
    themes: {
      light: {
        primary: '#607d8b',
        secondary: '#009688',
        accent: '#4caf50',
        error: '#03a9f4',
        warning: '#2196f3',
        info: '#3f51b5',
        success: '#673ab7',
        footer: '#757575'
      },
      dark: {
        primary: '#2f4c59',
        secondary: '#009688',
        accent: '#4caf50',
        error: '#03a9f4',
        warning: '#2196f3',
        info: '#3f51b5',
        success: '#673ab7',
        footer: '#424242'
      },
    },
  },
});
