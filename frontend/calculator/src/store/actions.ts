import { api } from '@/api';
import router from '@/router';
import { getLocalToken, removeLocalToken, saveLocalToken } from '@/utils';
import { AxiosError } from 'axios';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { State } from './state';
import {
    commitAddNotification,
    commitRemoveNotification,
    commitSetLoggedIn,
    commitSetLogInError,
    commitSetToken,
    commitSetUserProfile,
} from './mutations';
import { AppNotification, MainState } from './state';

type MainContext = ActionContext<MainState, State>;

export const actions = {
    async actionLogIn(context: MainContext, payload: { username: string; password: string, email: string }) {
        try {
            const response = await api.logInGetToken(payload.username, payload.password, payload.email);
            const token = response.data.token;
            console.log(token)
            if (token) {
                saveLocalToken(token);
                commitSetToken(context, token);
                commitSetLoggedIn(context, true);
                commitSetLogInError(context, false);
                await dispatchGetUserProfile(context);
                await dispatchRouteLoggedIn(context);
                commitAddNotification(context, { content: 'Logged in', color: 'success' });
            } else {
                await dispatchLogOut(context);
            }
        } catch (err) {
            commitSetLogInError(context, true);
            await dispatchLogOut(context);
        }
    },
    async actionLogout(context: MainContext){
        await dispatchLogOut(context)
        dispatchRouteLogOut
    },
    async actionRegisterUser(context: MainContext, payload:{username: string; password: string; email: string}){
        try{
            const response = await api.registerUser(payload.username,payload.password,payload.email);
            const result = response.data
        }catch(error:any){
            await dispatchCheckApiError(context,error)
        }
    },
    async actionGetUserProfile(context: MainContext) {
        try {
            const response = await api.getMe(context.state.token);
            if (response.data) {
                commitSetUserProfile(context, response.data);
            }
        } catch (error: any) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCheckLoggedIn(context: MainContext) {
        if (!context.state.isLoggedIn) {
            let token = context.state.token;
            if (!token) {
                const localToken = getLocalToken();
                if (localToken) {
                    commitSetToken(context, localToken);
                    token = localToken;
                }
            }
            if (token) {
                try {
                    const response = await api.getMe(token);
                    commitSetLoggedIn(context, true);
                    commitSetUserProfile(context, response.data);
                } catch (error) {
                    await dispatchRemoveLogIn(context);
                }
            } else {
                await dispatchRemoveLogIn(context);
            }
        }
    },
    async actionRemoveLogIn(context: MainContext) {
        removeLocalToken();
        commitSetToken(context, '');
        commitSetLoggedIn(context, false);
    },
    async actionLogOut(context: MainContext) {
        await dispatchRemoveLogIn(context);
        await dispatchRouteLogOut(context);
    },
    async actionUserLogOut(context: MainContext) {
        await dispatchLogOut(context);
        commitAddNotification(context, { content: 'Logged out', color: 'success' });
    },
    actionRouteLogOut(context: MainContext) {
        if (router.currentRoute.path !== '/login') {
            router.push('/login');
        }
    },
    async actionCheckApiError(context: MainContext, payload: AxiosError) {
        if (payload.response!.status === 401) {
            await dispatchLogOut(context);
        }
    },
    actionRouteLoggedIn(context: MainContext) {
        if (router.currentRoute.path === '/login' || router.currentRoute.path === '/') {
            router.push('/');
        }
    },
    async removeNotification(context: MainContext, payload: { notification: AppNotification, timeout: number }) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                commitRemoveNotification(context, payload.notification);
                resolve(true);
            }, payload.timeout);
        });
    },
    async calculateRemote(context: MainContext, payload: {operation: string, a: string, b: string}){
        const loading = {content: 'Requesting remote calcaulation', showProgress: true};
        try{
            commitAddNotification(context, loading)
           let token = context.state.token || getLocalToken()
           token ||= ''
        const remoteResult = await api.getCalculateResult(payload.operation, payload.a, payload.b, token);
        commitRemoveNotification(context,loading);
        let result = "error"
        if(remoteResult.status === 200){
            if(Array.isArray(remoteResult.data)){
                result = remoteResult.data.join(',') as string
            }else{
                result = (remoteResult.data.result) as string
            }
            
        }
        return result;
        }catch(error){
            commitRemoveNotification(context, loading)
            commitAddNotification(context,{color:'error', content: 'remote request faild'})
            console.error(error)
        } 
    },
    async fetchUserRecords(context: MainContext, payload: object){
        const loading ={content: 'loading data', showProgress: true}
        let token = context.state.token || getLocalToken();
           token ||= ''
        try{
            commitRemoveNotification(context,loading);
            return api.fetchUserRecords(payload, token)            
            
        }catch(error: any){
            commitRemoveNotification(context,loading)
            commitAddNotification(context,{color: 'error', content:'error on loading data'})
        }
    },

    async softdeleteRecord(context: MainContext,payload:{id: number}){
        const loading ={content: 'requesting', showProgress: true}
        let token = context.state.token || getLocalToken();
           token ||= ''
        try{
            commitRemoveNotification(context,loading);
            return api.deleteUserRecord(payload.id,token);

        }catch(error: any){
            commitRemoveNotification(context,loading)
            commitAddNotification(context,{color: 'error', content:'error on process request'})
        }

    }
};

const { dispatch } = getStoreAccessors<MainState | any, State>('');

export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);
export const dispatchCheckLoggedIn = dispatch(actions.actionCheckLoggedIn);
export const dispatchGetUserProfile = dispatch(actions.actionGetUserProfile);
export const dispatchRegisterUser = dispatch(actions.actionRegisterUser)
export const dispatchLogIn = dispatch(actions.actionLogIn);
export const dispatchLogOut = dispatch(actions.actionLogOut);
export const dispatchUserLogOut = dispatch(actions.actionUserLogOut);
export const dispatchRemoveLogIn = dispatch(actions.actionRemoveLogIn);
export const dispatchRouteLoggedIn = dispatch(actions.actionRouteLoggedIn);
export const dispatchRouteLogOut = dispatch(actions.actionRouteLogOut);
export const dispatchRemoveNotification = dispatch(actions.removeNotification);
export const dispatchCalculateRemote = dispatch(actions.calculateRemote);
export const dispatchFetchUserRecords = dispatch(actions.fetchUserRecords);
export const dispatchDeleteRecord = dispatch(actions.softdeleteRecord);