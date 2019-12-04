import * as VueGoogleMaps from 'vue2-google-maps';
import Vue from 'vue';
import Buefy from 'buefy';
import axios from 'axios';
import VueAxios from 'vue-axios';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import App from './App.vue';
import router from './router';
import store from './store';

library.add(fas);

Vue.component('vue-fontawesome', FontAwesomeIcon);

Vue.config.productionTip = false;

Vue.use(VueAxios, axios);

Vue.use(VueGoogleMaps, {
  load: { key: 'AIzaSyDtwvbSXPyMkXpHFaAgtYYzbac_gOY2ZTI' },
});

Vue.use(Buefy, {
  defaultIconComponent: 'vue-fontawesome',
  defaultIconPack: 'fas',
});

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');
