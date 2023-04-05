<template>
    <v-main>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>{{appName}}</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>
                <v-form @keyup.enter="submit">
                  <v-text-field @keyup.enter="submit" v-model="email"  name="Email" label="Email" type="text"></v-text-field>
                  <v-text-field @keyup.enter="submit" v-model="username"  name="username" label="username" type="text"></v-text-field>
                  <v-text-field @keyup.enter="submit" v-model="password" name="password" label="Password" id="password" type="password"></v-text-field>
                </v-form>
                <div v-if="loginError">
                  <v-alert :value="loginError" transition="fade-transition" type="error">
                    Incorrect email or password
                  </v-alert>
                </div>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click.prevent="submit">Login</v-btn>
                <v-btn @click="register" >Register</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-main>
  </template>
  
  <script lang="ts">
  import { Component, Vue } from 'vue-property-decorator';
  import { api } from '@/api';
  import { appName } from '@/env';
  import { readLoginError } from '@/store/getters';
  import { dispatchLogIn } from '@/store/actions';
  import { dispatchRegisterUser } from '@/store/actions'
  
  @Component
  export default class Login extends Vue {
    public email = '';
    public password = '';
    public username ='';
    public appName = appName;
  
  
    public get loginError() {
      return readLoginError(this.$store);
    }
  
    public submit() {
      dispatchLogIn(this.$store, {username: this.username, password: this.password, email: this.email});
    }

    public register(){
        dispatchRegisterUser(this.$store,{username: this.username, password: this.password, email: this.email})
    }
  }
  </script>
  
  <style>
  </style>
  