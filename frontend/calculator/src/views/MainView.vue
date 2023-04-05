<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>calculator</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-chip color="warning" text-color="white" class="mr-4">{{ balance }} Point</v-chip>
      <v-btn color="primary" @click="goRecords">Check User Records</v-btn>
      <v-btn color="secondary" @click="logout">Logout</v-btn>
    </v-app-bar>

    <v-container>
      <v-row align="center" justify="center">
        <v-col cols="6">
          <v-text-field v-model="input1" :rules="validateInput" label="First Number"></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field v-model="input2" :rules="validateInput" label="Second Number"></v-text-field>
        </v-col>
      </v-row>

      <v-row align="center" justify="center">
        <v-col cols="6">
          <v-select v-model="operator" :items="operators" label="Operation"></v-select>
        </v-col>
        <v-col cols="6">
          <v-btn color="primary" @click="calculate">Go!</v-btn>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-textarea v-model="result" label="Remote result" readonly></v-textarea>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>
  
<script lang="ts">
import Vue from 'vue';
import { dispatchCalculateRemote, dispatchLogOut } from '@/store/actions';
import { readIsLoggedIn } from '@/store/getters';
import store from '@/store';
import axios from 'axios';

export default Vue.extend({
  data() {
    return {
      balance: 'N/A',
      input1: '',
      input2: '',
      operator: 'add',
        operators:[{ text: 'Add', value: 'add' },
            { text: 'Subtract', value: 'sub' },
            { text: 'Multiply', value: 'mul' },
            { text: 'Divide', value: 'div' },
            { text: 'Square Root', value: 'sqrt' },
            { text: 'Random String', value: 'random' }],
      result: '',
        validateInput:[
            (value: string) => /^([-+])?\d+(\.\d+)?$/g.test(value) || `Please input a number (can be with sign and decimal)`
        ]
    };
  },
  methods: {
   async calculate(): Promise<void> {
      let num1 = this.input1;
      let num2 = this.input2;
      let res: string | null = null;
      let endpoint = ""
      switch (this.operator) {
        case 'add':
          endpoint ='/add';
          break;
        case 'sub':
          endpoint = '/sub';
          break;
        case 'mul':
          endpoint ='/mul';
          break;
        case 'div':
          endpoint = '/div';
          break;
        case 'sqrt':
          endpoint = '/sqrt'
          break;
        case 'random':
          endpoint = '/random';
          break;
      }
      this.refresh()
      try{
       const response = await dispatchCalculateRemote(this.$store,{operation: endpoint, a: num1, b: num2});
        console.log(response);
        if(response){
          this.result = response.toString()
        }
      }catch(error: any){
        console.error(error)
      }
    },
    logout(): void {
      dispatchLogOut(this.$store)
    },
    created(): void{
      if(!readIsLoggedIn(this.$store)){
        this.$router.push('/login')
      }
    },
    refresh(): void{
        //todo 
    },
    goRecords(): void{
      this.$router.push('/records')
    }
  }
});
</script>
  
