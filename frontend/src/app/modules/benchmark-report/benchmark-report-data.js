import { httpClient } from '@/app/shared/services/http-client'

export const benchmarkReportState = {
  namespaced: true,
  state: {

    benchmarkSchoolFilterOptionsData: null, 




    benchmarkStructureData: null,
    benchmarkChartsData:      null, 
    benchmarkSchoolFilterValuesData: null, 
    benchmarkComparableSchools: null, 
  },
  mutations: {
    setBenchmarkSchoolFilterOptionsData(state, data) {
      state.benchmarkSchoolFilterOptionsData = data
    },

    setBenchmarkSchoolFilterValuesData(state, data) {
      state.benchmarkSchoolFilterValuesData = data
    },    
    setBenchmarkChartsData(state, data) {
      state.benchmarkChartsData = data
    }, 

  },
  actions: {
    async getBenchmarkSchoolFilterData(context, param) {

      //console.log("load fitler getBenchmarkSchoolFilterData ")
      //console.log(param)

      var school_id = param['school_id']

      //thao test
      const url1 = '/benchmarkReport/filters/' + param['school_id']
      const levelOne = await httpClient.get(url1);


      //const benchmarkSchoolFilterData = await httpClient.post(url, body);
      const benchmarkSchoolFilterData = await httpClient.get(url1);
      if (benchmarkSchoolFilterData["data"] !== null & benchmarkSchoolFilterData["data"] !== undefined) {
        if ("acaraBenchmarkQuery" in benchmarkSchoolFilterData["data"]) {
          if ("filterOptions" in benchmarkSchoolFilterData["data"]["acaraBenchmarkQuery"]) {
            context.commit('setBenchmarkSchoolFilterOptionsData', benchmarkSchoolFilterData["data"]["acaraBenchmarkQuery"]["filterOptions"])
            context.commit('setBenchmarkSchoolFilterValuesData', benchmarkSchoolFilterData["data"]["acaraBenchmarkQuery"]["filterDefaultValues"])
            console.log("filterOptions")
            console.log(benchmarkSchoolFilterData["data"]["acaraBenchmarkQuery"]["filterOptions"])
            console.log("filterDefaultValues")
            console.log(benchmarkSchoolFilterData["data"]["acaraBenchmarkQuery"]["filterDefaultValues"])
          }
          else {
            console.log("filters object does not exist in benchmarkSchoolFilterData[\"data\"][\"acaraBenchmarkQuery\"]")
            console.log(benchmarkSchoolFilterData["data"]["data"]["acaraBenchmarkQuery"])
          }
        }
        else {
          console.log("acaraBenchmarkQuery object does not exist in benchmarkSchoolFilterData[\"data\"]")
          console.log(benchmarkSchoolFilterData["data"])
        }
      }
      else {
        console.log("benchmarkSchoolFilterData[\"data\"] is undefined ")
        console.log(benchmarkSchoolFilterData)
      }
    },

    async getBenchmarkReportChartsData(context, param) {
      var school_id = param['school_id']
      const url = '/benchmarkReport/benchmarkReportData';
      const body = {
        "params": param      };
      const benchmarkChartData = await httpClient.post(url, body);
      console.log("benchmarkChartData")
      console.log(benchmarkChartData["data"])

      if (benchmarkChartData["data"] !== null & benchmarkChartData["data"] !== undefined) {
         context.commit('setBenchmarkChartsData', benchmarkChartData["data"])
          
       
      }
      else {
        console.log("benchmarkChartData[\"data\"]is undefined ")
        console.log(benchmarkChartData)
      }
      
    }, 


  }
}
