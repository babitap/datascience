import { httpClient } from '@/app/shared/services/http-client'
import { loadingService } from '@/app/shared/services/loading-service'
import store from '../../app-state';

function parseJwt (token) {
  var base64Url = token.split('.')[1]
  var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
  var jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
  }).join(''))

  return JSON.parse(jsonPayload)
};

function populateInitial (firstName, lastName) {
  let initial = ''

  if (firstName && lastName) {
    if (firstName !== '') {
      initial += firstName.charAt(0).toUpperCase()
    }
    if (lastName !== '') {
      initial += lastName.charAt(0).toUpperCase()
    }
  }
  return initial
}

export const userState = {
  namespaced: true,
  state: {
    authenticated: false,
    jwt: null,
    firstName: null,
    lastName: null,
    specialPermissionList: [],
    permissionList:{},
    isFindex: false,
    isFindexAll: false,
    isSuperUser: false,
    entityLookUpList: [],
    lastSelectedEntity: {},
    selectedEntity: {}
  },
  getters: {
    accessToken: (state) => state.jwt,
    getUserInitial: (state) => {
        return populateInitial(state.firstName, state.lastName)
    }
  },
  mutations: {
    setAuthenticated (state, token) {
      state.jwt = token.accessToken
      state.authenticated = true
    },
    clearAuthentication (state) {
      state.authenticated = false
      state.jwt = null
    },
    setUserAuthData (state, data) {
      state.authenticated = data.authenticated
      state.jwt = data.jwt
      state.firstName = data.firstName
      state.lastName = data.lastName
    },
    setUserData (state, data){
        state.specialPermissionList = data.specialPermissionList;
        state.permissionList = data.permissionList;
        state.entityLookUpList = data.entityLookUpList;
        state.isSuperUser = data.isSuperUser;
        state.isFindex = data.isFindex;
        state.isFindexAll = data.isFindexAll;
        state.lastSelectedEntity = data.lastSelectedEntity;
    },
    setSelectedEntity(state, data){
        state.selectedEntity = data
    },
    setLastSelectedEntity(state, data){
        state.lastSelectedEntity = data
    },
    setEntityLookUpList(state, data){
        state.entityLookUpList = data
    }
  },
  actions: {
    authenticate (context, token) {
      if(token){
        let userData = {}
        userData.firstName = token.idTokenClaims.given_name
        userData.lastName = token.idTokenClaims.family_name
        userData.jwt = token.accessToken
        userData.authenticated = true
        context.commit('setUserAuthData', userData);
        context.dispatch('retrieveUserDetail');
      }
      
      localStorage.setItem('user', JSON.stringify(context.state))
    },
    logout (context) {
      context.commit('clearAuthentication')
      localStorage.removeItem('user')
    },
    init (context) {
      const data = localStorage.getItem('user')
      if (data) {
        let userData = JSON.parse(data)
        if(userData.jwt){
          const tokenInfo = parseJwt(userData.jwt)
          userData.firstName = tokenInfo.given_name
          userData.lastName = tokenInfo.family_name
        }
        context.commit('setUserAuthData', userData);
        context.dispatch('retrieveUserDetail');
      }
    },
    async retrieveUserDetail( context){
        const url = `/users`;

        return await httpClient.get(url)
            .then(res => {
                const data = res.data;
                let result = {'success': true, 'errorMessage': ''};

                if(!data.message){
                    context.commit('setUserData', data);
                    //If user has last selected entity set, use it by default
                    if(data.lastSelectedEntity){
                        context.commit('setSelectedEntity', data.lastSelectedEntity)
                    }
                    else{ //Otherwise use first one from entity list
                        if(data.entityLookUpList && data.entityLookUpList.length > 0){
                            context.dispatch('updateSelectedEntity', data.entityLookUpList[0])
                        }
                    }
                }
                else{
                    result.success = false;
                    result.errorMessage = 'Error retrieve user detail';
                }
                return result;
            })
            .catch(err => {       
                console.log(err);    
                throw err; // reject
            })
    },
    async updateSelectedEntity(context, entity){
        if(entity){
            context.commit('setSelectedEntity', entity)
            //now update database
            await httpClient.patch(`/users`, {'last_selected_entity':entity.id})
            .then(res => {
                const data = res.data;
                let result = {'success': true, 'errorMessage': ''};

                if(!data.message){
                    if(data.lastSelectedEntity){
                        context.commit('setLastSelectedEntity', data.lastSelectedEntity);
                    }
                }
                else{
                    result.success = false;
                    result.errorMessage = 'Error update selected entity';
                }
                return result;
            })
            .catch(err => {       
                console.log(err);    
                throw err; // reject
            })
        }
    },
    async createEntity(context, params){
        if(params){
            loadingService.showLoading(true);
            return await httpClient.post(`/entities`, params)
            .then(res => {
                const data = res.data;
                let result = {'success': true, 'errorMessage': ''};

                if(!data.message){
                    const newEntity = data.entity;
                    if(newEntity){
                        const entityLookUpList = [...this.state.user.entityLookUpList]
                        const existed = entityLookUpList.find(e => e.id === newEntity.id)
                        if(existed){
                            //shouldn't happen
                            existed.entity_name = newEntity.entity_name
                            existed.industry_name = newEntity.industry_name
                        }
                        else{
                            entityLookUpList.push({id:newEntity.id, industry_name:newEntity.industry_name, entity_name:newEntity.entity_name, industry_id:newEntity.industry_id})
                        }
                        context.commit('setEntityLookUpList', entityLookUpList);
                    }
                }
                else{
                    result.success = false;
                    result.errorMessage = 'Error create entity';
                }
                return result;
            })
            .catch(err => {       
                console.log(err);    
                throw err; // reject
            })
            .finally(() =>{
                loadingService.showLoading(false);
            })
        }
    },
    async updateEntity(context, params){
        if(params){
            loadingService.showLoading(true);
            return await httpClient.patch(`/entities`, params)
            .then(res => {
                const data = res.data;
                let result = {'success': true, 'errorMessage': ''};

                if(!data.message){
                    const updatedEntity = data.entity;
                    if(updatedEntity){
                        let entityLookUpList = [...this.state.user.entityLookUpList]
                        let existed = entityLookUpList.find(e => e.id === updatedEntity.id)
                        if(existed){
                            existed.entity_name = updatedEntity.entity_name
                            existed.industry_name = updatedEntity.industry_name
                            context.commit('setEntityLookUpList', entityLookUpList);
                            context.commit('setSelectedEntity', existed);
                        }

                        let adminEntityList = [...this.state.admin.adminEntityList.entities]
                        let existedEntity = adminEntityList.find(e => e.id === updatedEntity.id)
                        if(existedEntity){
                            existedEntity.name = updatedEntity.entity_name
                            store.dispatch('admin/updateAdminEntityList', adminEntityList)
                        }
                    }
                }
                else{
                    result.success = false;
                    result.errorMessage = 'Error update entity';
                }
                return result;
            })
            .catch(err => {       
                console.log(err);    
                throw err; // reject
            })
            .finally(() =>{
                loadingService.showLoading(false);
            })
        }
    }
  },
}
