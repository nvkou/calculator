import axios from 'axios';
import { apiUrl } from '@/env';
import { IUserProfile, IUserProfileUpdate, IUserProfileCreate } from './interfaces';
import { dispatchFetchUserRecords } from './store/actions';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string, email: string) {
    const data ={
        username: username,
        password: password,
        email: email
    }

    return axios.post(`${apiUrl}/login`, data);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/user`, authHeaders(token));
  },
  async registerUser(username: string, password: string, email: string){
    const data={
        username: username,
        password: password,
        email: email
    
    }
    return axios.post(`${apiUrl}/register`,data);
  },
  async getCalculateResult(operation: string, a: string, b: string, token: string ){
      return axios.get(`${apiUrl}${operation}?a=${a}&b=${b}`, authHeaders(token))
  },
  async fetchUserRecords(params: object, token: string){
    const url = `${apiUrl}/user_records`;
    return  axios.get(url,{params: params, headers:{Authorization: `Bearer ${token}`}})
  },
  async deleteUserRecord(record_id: number, token: string){
    return axios.delete(`${apiUrl}/user_records/${record_id}`,authHeaders(token))
  }
};
