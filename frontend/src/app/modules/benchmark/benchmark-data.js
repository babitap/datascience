import { httpClient } from '@/app/shared/services/http-client'

export const benchmarkState = {
  namespaced: true,
  state: {
    benchmarkStructureData:   null,
    benchmarkChartsData:      null, 
    benchmarkSchoolFilterOptionsData:null, 
    benchmarkSchoolFilterValuesData: null, 
    benchmarkComparableSchools: null, 
  },
  mutations: {
    setBenchmarkStructureData(state, data){
        state.benchmarkStructureData = data
    },
    setBenchmarkChartsData(state, data){
        state.benchmarkChartsData = data
    }, 
    setBenchmarkSchoolFilterOptionsData(state, data){
        state.benchmarkSchoolFilterOptionsData = data 
    },
    setBenchmarkSchoolFilterValuesData(state, data){
      state.benchmarkSchoolFilterValuesData = data 
    },    
    setBenchmarkComparableSchoolsData(state, data){
      state.benchmarkComparableSchools = data 
    },    
  },
  actions: {
    async getBenchmarkStructureData (context,schoolId) {
      const url = `benchmark`;    
      const body = {
        query: `
        query{
            acaraBenchmarkQuery{
              datasets{
                label
                value
                metrics{
                  label
                  value
                  model
                  field
                  subMetrics{
                    label
                    value
                    field
                  }
                }
              }
            }
          }
        `, 
        variables:{ }
      }; 
      const benchmarkStructureData = await httpClient.post( url,body ); 
      if( benchmarkStructureData["data"]["data"]["acaraBenchmarkQuery"]['datasets'] !== null ){
        context.commit('setBenchmarkStructureData', benchmarkStructureData["data"]["data"]["acaraBenchmarkQuery"]['datasets'])
      } 
    },

    async getBenchmarkChartsData(context, param ) {
        var school_id = param['school_id']
        var comparable_school_ids = param['comparable_school_ids']
        var model = param['model']
        var metric_field = param['metric_field']
        var submetrics_fields = param['submetrics_fields']

        // convert comparable_school_ids to readable string 
        var comparable_school_ids_string = "[" + comparable_school_ids.join(",") + "]"
        // convert submetrics_fields to readable string 
        var submetrics_fields_string = "[]"
        if( submetrics_fields | submetrics_fields.length==0 ){
            submetrics_fields_string = "[]"
        }
        else{
            submetrics_fields_string  = "[\"" +  submetrics_fields.join("\",\"") + "\"]"
        }        

        const url = `benchmark`;
        const body = {
            query: `
                query($id:Int!, $comparableIds:[Int!], $model:String!, $metricField:String!, $submetricsFields:[String!]){
                    acaraBenchmarkQuery{
                    charts(id:$id, comparableIds:$comparableIds, model:$model, metricField:$metricField, submetricsFields:$submetricsFields){
                        position{
                        id
                        value
                        focused 
                        }
                        trend{
                        id
                        focused
                        lineData{
                            calendarYear
                            value
                        }
                        }
                    }
                    }
                }
                `, 
            variables:`
            { 
                "id": ${school_id}, 
                "comparableIds":${comparable_school_ids_string}, 
                "model" : "${model}", 
                "metricField":"${metric_field}", 
                "submetricsFields": ${submetrics_fields_string}
            }
            `
        };  

        const benchmarkChartData = await httpClient.post( url, body ); 
          if( benchmarkChartData["data"]["data"] !== null & benchmarkChartData["data"]["data"] !== undefined ){            
            if( "acaraBenchmarkQuery" in benchmarkChartData["data"]["data"] ){
              if( "charts" in benchmarkChartData["data"]["data"]["acaraBenchmarkQuery"] ){            
                context.commit('setBenchmarkChartsData', benchmarkChartData["data"]["data"]["acaraBenchmarkQuery"]["charts"])
              }
              else{
                console.log("charts object does not exist in benchmarkChartData[\"data\"][\"data\"][\"acaraBenchmarkQuery\"]")
                console.log(benchmarkChartData["data"]["data"]["acaraBenchmarkQuery"])
              }
            }
            else{
              console.log("acaraBenchmarkQuery object does not exist in benchmarkChartData[\"data\"][\"data\"]")
              console.log(benchmarkChartData["data"]["data"])
            }            
        }
        else{
          console.log("benchmarkChartData[\"data\"][\"data\"] is undefined ")
          console.log( benchmarkChartData )
        }
    }, 

    async getBenchmarkSchoolFilterData(context, param ) {
      var school_id = param['school_id']
      const url = `benchmark`;
      const body = {
          query: `
          query($id:Int!){
            acaraBenchmarkQuery{
              filterOptions{
                schoolSectorOptions{
                  value
                  label
                }
                schoolTypeOptions{
                  value
                  label 
                }
                geolocationOptions{
                  value
                  label 
                }
                stateOptions{
                  value
                  label 
                }
                schoolGenderOptions{
                  value
                  label 
                }
              }
              filterDefaultValues(id:$id){
                  schoolSectorDefaultOption{
                    value
                    label 
                  }
                  schoolTypeDefaultOption{
                    value
                    label 
                  }
                  stateDefaultOption{
                    value
                    label 
                  }
                  geolocationDefaultOption{
                    value
                    label 
                  }
                  schoolGenderDefaultOption{
                    value
                    label 
                  }
                	enrolmentRangeStartValue
                	enrolmentRangeEndValue
                	distanceKmValue
                }
              }
            }
          
              `, 
          variables:`
          { 
              "id": ${school_id}
          }
          `
      }; 

      const benchmarkSchoolFilterData = await httpClient.post( url, body );
      if( benchmarkSchoolFilterData["data"]["data"] !== null & benchmarkSchoolFilterData["data"]["data"] !== undefined ){
          if( "acaraBenchmarkQuery" in benchmarkSchoolFilterData["data"]["data"] ){
            if( "filterOptions" in benchmarkSchoolFilterData["data"]["data"]["acaraBenchmarkQuery"] ){
              context.commit('setBenchmarkSchoolFilterOptionsData', benchmarkSchoolFilterData["data"]["data"]["acaraBenchmarkQuery"]["filterOptions"])
              context.commit('setBenchmarkSchoolFilterValuesData', benchmarkSchoolFilterData["data"]["data"]["acaraBenchmarkQuery"]["filterDefaultValues"])
            }
            else{
              console.log("filters object does not exist in benchmarkSchoolFilterData[\"data\"][\"data\"][\"acaraBenchmarkQuery\"]")
              console.log(benchmarkSchoolFilterData["data"]["data"]["acaraBenchmarkQuery"])
            }
          }
          else{
            console.log("acaraBenchmarkQuery object does not exist in benchmarkSchoolFilterData[\"data\"][\"data\"]")
            console.log(benchmarkSchoolFilterData["data"]["data"])
          }          
      }
      else{
        console.log("benchmarkSchoolFilterData[\"data\"][\"data\"] is undefined ")
        console.log( benchmarkSchoolFilterData )
      }    
  },

  async getBenchmarkComparableSchoolsData(context, param ) {
    var school_id = param['school_id']

    var school_sector_str = "[]"
    if( param['school_sector'] | param['school_sector'].length==0 ){
      school_sector_str = "[]"
    }
    else{
      school_sector_str  = "[\"" +  param['school_sector'].join("\",\"") + "\"]"
    }    

    var school_type_str = "[]"
    if( param['school_type'] | param['school_type'].length==0 ){
      school_type_str = "[]"
    }
    else{
      school_type_str  = "[\"" +  param['school_type'].join("\",\"") + "\"]"
    }    

    var school_state_str = "[]"
    if( param['school_state'] | param['school_state'].length==0 ){
      school_state_str = "[]"
    }
    else{
      school_state_str  = "[\"" +  param['school_state'].join("\",\"") + "\"]"
    }    

    var school_gender_str = "[]"
    if( param['school_gender'] | param['school_gender'].length==0 ){
      school_gender_str = "[]"
    }
    else{
      school_gender_str  = "[\"" +  param['school_gender'].join("\",\"") + "\"]"
    }    

    var school_geolocation_str = "[]"
    if( param['school_geolocation'] | param['school_geolocation'].length==0 ){
      school_geolocation_str = "[]"
    }
    else{
      school_geolocation_str  = "[\"" +  param['school_geolocation'].join("\",\"") + "\"]"
    }    

    var enrolment_start_value = param['enrolment_start_value'] 
    var enrolment_end_value = param['enrolment_end_value'] 
    var distance_km = param['distance_km'] 

    const url = `benchmark`;
    const body = {
        query: `
            query($id:Int!, 
              $schoolSector:[String!],
              $schoolType:[String!],
              $SchoolGender: [String!],
              $schoolGeolocation:[String!],
              $schoolState:[String!],
              $enrolmentStartValue:Int!,
              $enrolmentEndValue:Int!,
              $distanceKm:Int!
            ){
              acaraBenchmarkQuery{
                comparableSchools(id:$id, schoolSector:$schoolSector,
                  schoolType:$schoolType, schoolGender:$SchoolGender,
                  schoolGeolocation:$schoolGeolocation,
                  schoolState:$schoolState,
                  enrolmentStartValue:$enrolmentStartValue,
                  enrolmentEndValue:$enrolmentEndValue,
                  distanceKm:$distanceKm ,
                ){
                  id
                }
              }
            }
            `, 
        variables:`
        { 
            "id": ${school_id}, 
            "schoolSector": ${school_sector_str},
            "schoolType": ${school_type_str},
            "SchoolGender": ${school_gender_str},
            "schoolGeolocation": ${school_geolocation_str},
            "schoolState": ${school_state_str},
            "enrolmentStartValue": ${enrolment_start_value},
            "enrolmentEndValue": ${enrolment_end_value},
            "distanceKm": ${distance_km}
        }
        `
    }; 

    const benchmarkComparableSchoolsData = await httpClient.post( url, body ); 
    if( benchmarkComparableSchoolsData["data"]["data"] !== null & benchmarkComparableSchoolsData["data"]["data"] !== undefined ){
        if( "acaraBenchmarkQuery" in benchmarkComparableSchoolsData["data"]["data"] ){
          if( "comparableSchools" in benchmarkComparableSchoolsData["data"]["data"]["acaraBenchmarkQuery"] ){
            context.commit('setBenchmarkComparableSchoolsData', benchmarkComparableSchoolsData["data"]["data"]["acaraBenchmarkQuery"]["comparableSchools"])            
          }
          else{
            console.log("filters object does not exist in benchmarkComparableSchoolsData[\"data\"][\"data\"][\"acaraBenchmarkQuery\"]")
            console.log(benchmarkComparableSchoolsData["data"]["data"]["acaraBenchmarkQuery"])
          }
        }
        else{
          console.log("acaraBenchmarkQuery object does not exist in benchmarkComparableSchoolsData[\"data\"][\"data\"]")
          console.log(benchmarkComparableSchoolsData["data"]["data"])
        }        
    }
    else{
      console.log("benchmarkComparableSchoolsData[\"data\"][\"data\"] is undefined ")
      console.log( benchmarkComparableSchoolsData )
    }

  },
  }
}
