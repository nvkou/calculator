<template>
    <v-app>
        <v-app-bar app color="primary" dark>
      <v-toolbar-title>calculator</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/">go home</v-btn>
      <v-btn color="secondary" @click="logout">Logout</v-btn>
    </v-app-bar>
    <v-card>
      <v-card-title class="text-h6">User Records Data Table</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="6">
            <v-select
            v-model="searchOperation"
            :items="operationOptions"
            label="Operation"
            @input="onPageChange"
            ></v-select>
          </v-col>
          <v-col cols="6">
            <v-text-field @keyup="onPageChange" v-model="searchOperationRespond" label="Operation Respond"></v-text-field>
          </v-col>
        </v-row>
        <v-data-table
          :headers="headers"
          :items="record"
          :search="search"
          :items-per-page="100"
          :footer-props="{ showFirstLastPage: true, itemsPerPageOptions: [10, 15] }"
          :page="current_page"
          @page-change="onPageChange"
        >
          <template v-slot:[`item.deleted`]="{ item }">
            <v-icon small v-if="item.deleted">mdi-close-circle</v-icon>
            <v-icon small v-else>mdi-check-circle</v-icon>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="deleteItem(item)">mdi-delete</v-icon>
          </template>
        </v-data-table>
        <v-dialog v-model="dialog" max-width="500">
          <v-card>
            <v-card-title class="headline">Delete Row</v-card-title>
            <v-card-text>Are you sure you want to delete this row?</v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" text @click="dialog = false">Cancel</v-btn>
              <v-btn color="primary" text @click="deleteRow">OK</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-card-text>
    </v-card>
</v-app>
  </template>
  
  
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {dispatchFetchUserRecords,dispatchDeleteRecord,dispatchLogOut} from '@/store/actions'



@Component
export default class DataTable extends Vue {
  searchOperation = '';
  searchOperationRespond = '';
  search= '';
  dialog = false;
  operationOptions=[
    {text: 'all', value: ''},
    { text: 'add', value: '1' },
      { text: 'sub', value: '2' },
      { text: 'mul', value: '3' },
      { text: 'div', value: '4' },
      { text: 'sqrt', value: '5' },
      { text: 'random', value: '6' },
      { text: 'misc', value: '7' }
  ];
  headers = [
    { text: 'ID', value: 'id' },
    { text: 'Update Time', value: 'updated_at' },
    { text: 'User Balance',value: 'user_balance'},
    //{ text: 'operation type', value: 'operation'},
    { text: 'Operation Result', value: 'operation_respond'},
    { text: 'Cost Amount', value: 'amount' },
    { text: 'Deleted', value: 'soft_delete' },
    { text: 'Actions', value: 'actions', sortable: false }
  ];
  record = [];
  current_page =1;
  page_size= 100;
  selected_item ={id: -1}
  mounted(){
    this.fetchRecord()
  }

  deleteItem(item: any): void {
    this.selected_item= item
    this.dialog = true;
  }
  onPageChange(){
    this.fetchRecord()
  }

  deleteRow(): void {
    const id = this.selected_item.id
    if(id < 1){
        this.dialog = false;
    this.selected_item={id: -1}
    } 
    dispatchDeleteRecord(this.$store,{id: id})
    this.dialog = false;
    this.selected_item={id: -1}
    this.fetchRecord()
  }
  logout(): void {
      dispatchLogOut(this.$store)
    }
  async fetchRecord(page: number =this.current_page,pageSize: number =this.page_size): Promise<void>{
    const pre_params ={
        page: page,
        limit: pageSize,
        operation: this.searchOperation,
        operation_respond: this.searchOperationRespond
    }
    let params = this.removeEmptyFields(pre_params)
    const remote = await dispatchFetchUserRecords(this.$store, params)
   this.record = remote?.data ?? []
  }

  removeEmptyFields(obj: {[key: string]: any}): {[key: string]: any} {
  return Object.fromEntries(
    Object.entries(obj)
      .filter(([_, v]) => v !== null && v !== undefined && v !== '')
  );
}
}

</script>
  