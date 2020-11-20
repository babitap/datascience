import { httpClient } from '@/app/shared/services/http-client'
import { loadingService } from '@/app/shared/services/loading-service'

export const reportState = {
  namespaced: true,
  state: {
    availableReports:{},
    reportInfo:{
        accessToken: '',
        embedUrl: '',
        tokenExpiry: ''
    }
  },
  mutations: {
    setReportInfo(state, data){
        state.reportInfo = data
    },
    setAvailableReports(state, data) {
        state.availableReports = data
    }
  },
  actions: {
    async getReportList(context, entityId){
      const url = `/pbi/reportList/${entityId}`
      //loadingService.showLoading(true);

      return await httpClient.get(url)
        .then(res => {
            const data = res.data;
            let result = {'success': true, 'errorMessage': ''};

            if(!data.message){
                context.commit('setAvailableReports', data.reports)
            }
            else{
                result.success = false;
                result.errorMessage = 'Error retrieve report list';
            }
            return result;
        })
        .catch(err => {       
            console.log(err);    
            throw err; // reject
        })
        .finally(() =>{
            //loadingService.showLoading(false);
        })
    },

    async getReportEmbedInfo(context, params) {
      //call report API
      const url = `/pbi/reportEmbedInfo/${params.codename}`
      loadingService.showLoading(true);

      return await httpClient.get(url)
        .then(res => {
            const data = res.data;
            let result = {'success': true, 'errorMessage': ''};

            if(!data.message){
                context.commit('setReportInfo', data)
            }
            else{
                result.success = false;
                result.errorMessage = 'Error retrieve report information';
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

}
