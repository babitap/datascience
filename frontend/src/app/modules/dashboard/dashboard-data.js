import { httpClient } from '@/app/shared/services/http-client'
import { loadingService } from '@/app/shared/services/loading-service'

export const dashboardState = {
  namespaced: true,
  state: {
    dashboardJsonData: null, 
  },
  mutations: {
    setDashboardData(state, data){
      state.dashboardJsonData = data; 
    }
  },
  actions: {
    async getDashboardJsonData (context, schoolId) {
      const url = `dashboard`;
      loadingService.showLoading(true);
      const body = {
        query: `
          query($id:Int!){
            acaraDashboardQuery{
              basicMetrics(id: $id){
                studentTeacherRatio
                studentNonTeacherRatio
                recurrentIncomePerStudent
              } 
              basicYearlyInfo(id:$id){
                calendarYear
                totalEnrolments
                fullTimeEquivalentEnrolments
                fullTimeEquivalentTeachingStaff
                fullTimeEquivalentNonTeachingStaff
              }
              finance(id:$id){
                calendarYear
                incomeTotalNetRecurrent
                incomeFeesChargesParent
                incomeAusRecurrent
                incomeStateRecurrent
                incomeOtherPrivate
              }
            }
          }
        `, 
        variables:{'id': schoolId }
      }; 
      
    const dashboardJson = await httpClient.post( url, body )
    .then(res=>{     
      const data=res.data;    

      if(data.data != null & data.data !=undefined)
      { 
            context.commit('setDashboardData', data.data)       
      }
      else
      {
        console.log("dashboardJson [\"data\"][\"data\"] is undefined ")
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
}
