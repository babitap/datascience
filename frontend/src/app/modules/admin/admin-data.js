import { httpClient } from '@/app/shared/services/http-client'
import { loadingService } from '@/app/shared/services/loading-service'
import { Store } from 'vuex';

export const adminState = {
  namespaced: true,
  state: {
    adminTreeJsonData: null, 
    adminUserGroupJsonData: null, 
    adminEntityList: null,
    adminGroupList: null,
    adminReportList: null
  },
  mutations: {

    setAdminTreeData(state, data){
        state.adminTreeJsonData = data; 
    },
    setAdminUserGroupJsonData(state, data){
        state.adminUserGroupJsonData = data 
    },
    setAdminEntityList(state, data){
      state.adminEntityList = data;
    },
    setAdminGroupList(state, data){
        state.adminGroupList = data;
    },
    updateAdminEntityList(state, data){
        state.adminEntityList.entities = data;
    },
    setAdminReportList(state, data){
        state.adminReportList = data;
    }
  },
  actions: {
    async getAdminTreeJsonData (context) {

      const url = `/admintree`;
      const adminTreeJson = await httpClient.get( url ); 
      if( adminTreeJson['data'] ){
        context.commit('setAdminTreeData', adminTreeJson['data'])
      }
      
    },
    async getAdminUserGroupJsonData(context, param){

        if(this.state.admin.adminUserGroupJsonData != null)
        {
            context.commit('setAdminUserGroupJsonData', null);
        }
        
        var industry_id = param['industry_id']
        var entity_id = param['entity_id']
        var usergroup_id = param['usergroup_id']
        const url = `/admingroup/${entity_id}?group_id=${usergroup_id}`;
        const adminUserGroupJson = await httpClient.get( url ); 
        if( adminUserGroupJson['data'] ){
          context.commit('setAdminUserGroupJsonData', adminUserGroupJson['data'])
        } 
    },

    async addUserToUserGroup( context, param ){
        var industry_id = param['industry_id']
        var entity_id = param['entity_id']
        var usergroup_id = param['usergroup_id']
        var user_id = param['user_id']

        const url = `/usergroups?industry_id=${industry_id}&entity_id=${entity_id}&entitygroup_id=${usergroup_id}&username=${user_id}`

        const addUserToUserGroupResponse = await httpClient.post( url  )
        // check response from post request 

        if(addUserToUserGroupResponse.data){
            let updatedState = this.state.admin.adminUserGroupJsonData;
            updatedState.selected_users = addUserToUserGroupResponse.data.selected_users;
            context.commit('setAdminUserGroupJsonData', updatedState);
        }
    },

    async removeUserToUserGroup( context, param ){
        var industry_id = param['industry_id']
        var entity_id = param['entity_id']
        var usergroup_id = param['usergroup_id']
        var user_id = param['user_id']

        const url = `/usergroups?industry_id=${industry_id}&entity_id=${entity_id}&entitygroup_id=${usergroup_id}&username=${user_id}`

        const removeUserFromUserGroupResponse = await httpClient.delete( url  )
        // check response from post request 

        if(removeUserFromUserGroupResponse.data){
            let updatedState = this.state.admin.adminUserGroupJsonData;
            updatedState.selected_users = removeUserFromUserGroupResponse.data.selected_users;
            context.commit('setAdminUserGroupJsonData', updatedState);
        }
    },    

    async addPermissionToUserGroup( context, param ){
        var industry_id = param['industry_id']
        var entity_id = param['entity_id']
        var usergroup_id = param['usergroup_id']
        var permission_id = param['permission_id']

        const url = `/permissions?industry_id=${industry_id}&entity_id=${entity_id}&entitygroup_id=${usergroup_id}&permission_id=${permission_id}`

        const addPermissionToUserGroupResponse = await httpClient.post( url  )
        // check response from post request 

        if(addPermissionToUserGroupResponse.data){
            let updatedState = this.state.admin.adminUserGroupJsonData;
            updatedState.selected_permissions = addPermissionToUserGroupResponse.data.selected_permissions;
            context.commit('setAdminUserGroupJsonData', updatedState);
        }
    },

    async removePermissionFromUserGroup( context, param ){
        var industry_id = param['industry_id']
        var entity_id = param['entity_id']
        var usergroup_id = param['usergroup_id']
        var permission_id = param['permission_id']

        const url = `/permissions?industry_id=${industry_id}&entity_id=${entity_id}&entitygroup_id=${usergroup_id}&permission_id=${permission_id}`

        const removePermissionFromUserGroupResponse = await httpClient.delete( url  )
        // check response from post request 

        if(removePermissionFromUserGroupResponse.data){
            let updatedState = this.state.admin.adminUserGroupJsonData;
            updatedState.selected_permissions = removePermissionFromUserGroupResponse.data.selected_permissions;
            context.commit('setAdminUserGroupJsonData', updatedState);
        }
    },    
    async addNewUserGroup( context, param ){
        var industry_id = param['industry_id']
        var entity_id = param['entity_id']
        var usergroup_name = param['usergroup_name']
        var usergroup_description = param['usergroup_description']

        const url = `/groups?entity_id=${entity_id}&name=${usergroup_name}&description=${usergroup_description}`
        const addUserGroupReponse = await httpClient.post(url)
        
        if( addUserGroupReponse['data'] ){
            context.commit('setAdminGroupList', addUserGroupReponse['data']);
        }
    },
    async editUserGroup( context, param ){
        var industry_id = param['industry_id']
        var entity_id = param['entity_id']

        var usergroup_id = param['usergroup_id']
        var usergroup_name = param['usergroup_name']
        var usergroup_description = param['usergroup_description']
        // 'entitygroup_id','name','description'
        const url = `/groups?entity_id=${entity_id}&entitygroup_id=${usergroup_id}&name=${usergroup_name}&description=${usergroup_description}`;
        const editUserGroupReponse = await httpClient.patch(url)


        if( editUserGroupReponse['data'] ){
            context.commit('setAdminGroupList', editUserGroupReponse['data'])

            let updatedState = this.state.admin.adminUserGroupJsonData;
            if(updatedState.profile.value){
                const groupInfo = this.state.admin.adminGroupList.groups.find(el => el.id === updatedState.profile.value);
                if(groupInfo){
                    updatedState.profile.label = groupInfo.name;
                    updatedState.profile.description = groupInfo.description;
                    context.commit('setAdminUserGroupJsonData', updatedState);
                }
            }
        }
    },
    async deleteUserGroup( context, param ){
        var industry_id = param['industry_id']
        var entity_id = param['entity_id']
        var usergroup_id = param['usergroup_id']

        // 'entitygroup_id','name','description'
        const url = `/groups?entity_id=${entity_id}&entitygroup_id=${usergroup_id}`
        const deleteUserGroupReponse = await httpClient.delete(url)

        if( deleteUserGroupReponse['data'] ){
            context.commit('setAdminGroupList', deleteUserGroupReponse['data']);
        }
    },  
    
    async invitNewUser( context, param ){
        const url = `/users`;
        loadingService.showLoading(true);

        return await httpClient.post(url, param)
            .then(res => {
                const data = res.data;
                let result = {'success': true, 'errorMessage': ''};

                if(!data.message){
                    if(data.special_user && data.special_user === true){
                        //it was invite special user request
                    }
                    else{
                        let updatedState = this.state.admin.adminUserGroupJsonData;
                        updatedState.available_users = data.available_users;
                        context.commit('setAdminUserGroupJsonData', updatedState);
                    }
                }
                else{
                    result.success = false;
                    result.errorMessage = 'Error sending invite user request';
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
    },    
    async getAdminEntityList (context, param) {

        const entityId = param.entityId;

        const url = `/adminEntityList?entity_id=${entityId}`;

        return await httpClient.get(url)
            .then(res => {
                const data = res.data;
                let result = {'success': true, 'errorMessage': ''};

                if(!data.message){
                    context.commit('setAdminEntityList', data);
                    return result;
                }
                else{
                    result.success = false;
                    result.errorMessage = 'Error retrieve entity list';
                }
                return result;
            })
            .catch(err => {       
                console.log(err);    
                throw err; // reject
            })
    },
    async getAdminGroupList (context, param) {

        const entityId = param.entityId;

        const url = `/adminGroupList?entity_id=${entityId}`;
        const groupList = await httpClient.get( url ); 
        if( groupList['data'] ){
            context.commit('setAdminGroupList', groupList['data'])
        }
    },  
    async getAdminReportList (context, param) {
        const url = `/adminReportList?entity_id=${param.entityId}`;

        return await httpClient.get(url)
            .then(res => {
                const data = res.data;
                let result = {'success': true, 'errorMessage': ''};

                if(!data.message){
                    context.commit('setAdminReportList', data);
                    return result;
                }
                else{
                    result.success = false;
                    result.errorMessage = 'Error retrieve admin report list';
                }
                return result;
            })
            .catch(err => {       
                console.log(err);    
                throw err; // reject
            })
    },
    async addNewReport( context, param ){
        const url = `/reports`;
        loadingService.showLoading(true);

        return await httpClient.post(url, param)
            .then(res => {
                const data = res.data;
                let result = {'success': true, 'errorMessage': ''};

                if(!data.message){
                    const newReport = data.report;
                    if(newReport && this.state.admin.adminReportList){
                        let currentReports = [...this.state.admin.adminReportList.reports]
                        let report = currentReports.find(r => r.id === newReport.id)
                        if(report){
                            //shouldn't happen
                            report = newReport
                        }
                        else{
                            currentReports.push(newReport)
                        }
                        context.commit('setAdminReportList', {...this.state.admin.adminReportList, ...{reports:currentReports}})
                    }
                }
                else{
                    result.success = false;
                    result.errorMessage = 'Error create new report';
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
    }, 
    async updateReport( context, param ){
        const url = `/reports`;
        loadingService.showLoading(true);

        return await httpClient.patch(url, param)
            .then(res => {
                const data = res.data;
                let result = {'success': true, 'errorMessage': ''};

                if(!data.message){
                    const newReport = data.report;
                    if(newReport && this.state.admin.adminReportList){
                        let currentReports = [...this.state.admin.adminReportList.reports]
                        const reportIndex = currentReports.findIndex(r => r.id === newReport.id)
                        
                        if(reportIndex !== -1){
                            currentReports[reportIndex] = {...currentReports[reportIndex],...newReport}
                            context.commit('setAdminReportList', {...this.state.admin.adminReportList, ...{reports:currentReports}})
                        }
                    }
                }
                else{
                    result.success = false;
                    result.errorMessage = 'Error update report';
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
    },  
    async deleteReport( context, param ){
      const url = `/reports`;
      loadingService.showLoading(true);
      
      return await httpClient.patch(url, param)
        .then(res => {
            const data = res.data;
            let result = {'success': true, 'errorMessage': ''};

            if(!data.message){
                const deletedReport = data.report;
                if(deletedReport && this.state.admin.adminReportList){
                    let currentReports = [...this.state.admin.adminReportList.reports]
                    const reportIndex = currentReports.findIndex(r => r.id === deletedReport.id)
                    
                    if(reportIndex !== -1){
                      currentReports.splice(reportIndex, 1)
                      context.commit('setAdminReportList', {...this.state.admin.adminReportList, ...{reports:currentReports}})
                    }
                }
            }
            else{
                result.success = false;
                result.errorMessage = 'Error delete report';
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
    },  
    clearAdminGroupList(context) {
        context.commit('setAdminGroupList', []);
    },
    clearAdminUserGroupJsonData(context){
        context.commit('setAdminUserGroupJsonData', null);
    },
    updateAdminEntityList(context, param){
        context.commit('updateAdminEntityList', param)
    }
  },
}
