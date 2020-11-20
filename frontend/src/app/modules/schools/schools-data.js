import { httpClient } from '@/app/shared/services/http-client'
import { loadingService } from '@/app/shared/services/loading-service'

export const schoolsState = {
  namespaced: true,
  state: {
    selectedSchool: {},
    schools: [],
    selectedEntity: {}
  },
  mutations: {
    setSchools (state, data) {
      if (data && data.length > 0) {
        state.schools = data
      }
    },
    updateSelectedSchool (state, data) {
      state.selectedSchool = data
    },
    setSelectedEntity(state, data){
        state.selectedEntity = data
    }
  },
  actions: {
    async getSchools (context) {           
      const url = `schools`;
      loadingService.showLoading(true);
      const body = {
        query: `
          query{
            acaraSchoolMasters{
              acaraId
              schoolName
              suburb
              state
              postcode
              schoolType
              schoolSector
            }
          }
        `,         
      };      
  
      const returnedJson = await httpClient.post( url, body )
      .then(res=>{     
        const data=res.data; 
        if(data.data != null & data.data !=undefined)
        {  
          if(data.data.acaraSchoolMasters != null & data.data.acaraSchoolMasters !=undefined)
          {   
            context.commit('setSchools', data.data.acaraSchoolMasters) 
          }             
        }
        else
        {
          console.log("returnedJson[\"data\"][\"data\"] is undefined ")
          console.log( data )
        }
      }) 
      .catch(err => {       
       console.log(err);    
       throw err; 
      })
      .finally(() =>{
        loadingService.showLoading(false);
      })
     },    
    
    async getSelectedSchool(context, userID){
      const url = `schools`;
      loadingService.showLoading(true);
      const body = {
        query: `
          query($userID:Int!){
            acaraUserSelectedSchoolQuery{
            selectedSchool(userId:$userID){
              acaraId
              schoolName
              suburb
              state
              postcode
              schoolType
              schoolSector
              } 
            }
          }
        `, 
        variables:{'userID': userID }        
      };  

      const returnedJson = await httpClient.post( url, body )
      .then(res=>{     
        const data=res.data;    
  
        if(data.data != null & data.data !=undefined)
        {  
          if(data.data.acaraUserSelectedSchoolQuery != null & data.data.acaraUserSelectedSchoolQuery !=undefined)
          {
            if(data.data.acaraUserSelectedSchoolQuery.selectedSchool != null & data.data.acaraUserSelectedSchoolQuery.selectedSchool !=undefined)   
            {           
              context.commit('updateSelectedSchool', data.data.acaraUserSelectedSchoolQuery.selectedSchool)       
            }
          }             
        }
        else
        {
          console.log("returnedJson[\"data\"][\"data\"] is undefined ")
          console.log( data )
        }
      }) 
      .catch(err => {       
       console.log(err);    
       throw err; 
      })
      .finally(() =>{
        loadingService.showLoading(false);
      })
     }
    },
    setSelectedSchool (context, school) {
      context.commit('updateSelectedSchool', school)
    },
    switchSchool (context, school) {
      context.commit('updateSelectedSchool', school)
    },
    setSelectedEntity(context, entity){
        context.commit('setSelectedEntity', entity)
    }  
}
