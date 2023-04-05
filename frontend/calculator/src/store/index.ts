import Vue from 'vue'
import Vuex, { StoreOptions } from 'vuex';
import { State } from './state';
import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';

Vue.use(Vuex)

 const defaultState ={
  isLoggedIn: null,
  token: '',
  logInError: false,
  userProfile: null,
  dashboardMiniDrawer: false,
  dashboardShowDrawer: true,
  notifications: [],
}

const mainState ={
  state: defaultState,
  mutations,
  actions,
  getters,
}

const storeOptions: StoreOptions<State> = {
  modules: {
    main: mainState
  },
};

export const store = new Vuex.Store<State>(storeOptions);

export default store;
