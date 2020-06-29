import '@babel/polyfill';
// Import Component hooks before component definitions
import './component-hooks';
import Vue from 'vue';
import './plugins/vuetify';
// import './plugins/buefy';
import './plugins/vee-validate';
import App from './App.vue';
import router from './router';
import store from '@/store';
import firebase from 'firebase';
import './registerServiceWorker';
import 'vuetify/dist/vuetify.min.css';
// import 'buefy/dist/buefy.css';

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');

// Your web app's Firebase configuration
var firebaseConfig = {
  apiKey: "AIzaSyBKZZBM1s6lR4rxyqFDNdVKpEiFm3xAxS4",
  authDomain: "ticker-ap.firebaseapp.com",
  databaseURL: "https://ticker-ap.firebaseio.com",
  projectId: "ticker-ap",
  storageBucket: "ticker-ap.appspot.com",
  messagingSenderId: "293053175762",
  appId: "1:293053175762:web:9c1cbedb5b759a47115a0b",
  measurementId: "G-2PNH015NNH"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
