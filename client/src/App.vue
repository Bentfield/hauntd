<template>
  <div id="app">
    <b-navbar spaced wrapper-class="container">
      <template slot="brand">
          <b-navbar-item tag="router-link" :to="{ path: '/' }">
              <img
                  src="./assets/logo.png"
                  alt="Hauntd CS411 Database Project"
              >
          </b-navbar-item>
      </template>
      <template slot="start">
        <b-navbar-item tag="router-link" :to="{ name: 'home' }">
          Home
        </b-navbar-item>
      </template>

      <template slot="end">
        <b-navbar-item tag="div">
          <div class="buttons">
            <a href="#" @click="signOut" v-if="isLoggedIn">Sign out</a>
            <g-signin-button
              v-if="!isLoggedIn"
              :params="googleSignInParams"
              @success="onSignInSuccess"
              @error="onSignInError">
              Sign in with Google
            </g-signin-button>
          </div>
        </b-navbar-item>
      </template>
    </b-navbar>
    <router-view/>
  </div>
</template>

<style lang="scss">
// Import Bulma's core
@import "~bulma/sass/utilities/_all";

// Set your colors
// $primary: #43aa8b;
$primary: #db504a;
$primary-invert: findColorInvert($primary);
$twitter: #4099FF;
$twitter-invert: findColorInvert($twitter);
$dark: #fff;

// Setup $colors to use as bulma classes (e.g. 'is-twitter')
$colors: (
    "white": ($white, $black),
    "black": ($black, $white),
    "light": ($light, $light-invert),
    "dark": ($dark, $dark-invert),
    "primary": ($primary, $primary-invert),
    "info": ($info, $info-invert),
    "success": ($success, $success-invert),
    "warning": ($warning, $warning-invert),
    "danger": ($danger, $danger-invert),
    "twitter": ($twitter, $twitter-invert)
);

// Links
$link: $primary;
$link-invert: $primary-invert;
$link-focus-border: $primary;

// Import Bulma and Buefy styles
@import "~bulma";
@import "~buefy/src/scss/buefy";

html, body {
    background-color: #3b3355;
    margin: 0;
    height: 100%;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #fff;
}

.g-signin-button {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 3px;
  background-color: #3c82f7;
  color: #fff;
  box-shadow: 0 3px 0 #0f69ff;
  cursor: pointer;
  margin-left: 10px;
}
</style>

<script lang="ts">
import GSignInButton from 'vue-google-signin-button';
import { Vue, Component } from 'vue-property-decorator';
import AppModule from '@/store/modules/app';

Vue.use(GSignInButton);

@Component
export default class App extends Vue {
  data() {
    return {
      googleSignInParams: {
        client_id: '406470965278-g9duphf6roh47jvu380q5orrojbs8jld.apps.googleusercontent.com',
      },
    };
  }

  mounted() {
    const token = localStorage.getItem('idToken');
    const email = localStorage.getItem('email');
    if (token !== null && email !== null) {
      const user = {
        token,
        email,
      };
      AppModule.SignIn(user);
    }
  }

  onSignInSuccess(googleUser: any) {
    const idToken = googleUser.getAuthResponse().id_token;
    const email = googleUser.getBasicProfile().getEmail();
    const user = {
      token: idToken,
      email,
    };
    AppModule.SignIn(user);
  }

  onSignInError() {}

  signOut() {
    AppModule.SignOut();
  }

  get isLoggedIn() {
    return AppModule.loggedIn;
  }
}
</script>
