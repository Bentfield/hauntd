<template>
    <b-navbar spaced wrapper-class="container">
      <template slot="brand">
          <b-navbar-item tag="router-link" :to="{ path: '/' }">
              <img
                  src="../assets/logo.png"
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
            <a href="#" @click="signOut" v-if="loggedIn">Sign out</a>
            <g-signin-button
              v-if="!loggedIn"
              :params="googleSignInParams"
              @success="onSignInSuccess"
              @error="onSignInError">
              Sign in with Google
            </g-signin-button>
          </div>
        </b-navbar-item>
      </template>
    </b-navbar>
</template>

<style>
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
import { Vue, Component, Prop } from 'vue-property-decorator';
import AppModule from '@/store/modules/app';
import * as json from '../../credentials_dev.json';

Vue.use(GSignInButton);

@Component
export default class NavBar extends Vue {
  public loggedIn : Boolean = false;

  data() {
    return {
      googleSignInParams: {
        client_id: json.web.client_id,
      },
    };
  }

  onSignInSuccess(googleUser: any) {
    const idToken = googleUser.getAuthResponse().id_token;
    AppModule.SignIn(idToken);
    this.loggedIn = true;
  }

  onSignInError() {}

  signOut() {
    AppModule.SignOut();
    this.loggedIn = false;
  }
}
</script>
