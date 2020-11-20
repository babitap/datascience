import { httpClient } from '@/app/shared/services/http-client'

export const mapState = {
  namespaced: true,
  state: {
    regionLevelOneData_left: {
      'options':null,
      'labels':null,
      'selections':null
    }, 
    regionLevelTwoData_left: {
      'options':null,
      'labels':null,
      'selections':null
    },
    regionLevelOneData_right: {
      'options':null,
      'labels':null,
      'selections':null
    }, 
    regionLevelTwoData_right: {
      'options':null,
      'labels':null,
      'selections':null
    },
    markerLevelOneData: {
      'options':null,
      'labels':null,
      'selections':null
    }, 
    markerLevelTwoData: {
      'options':null,
      'labels':null,
      'selections':null
    },
    terriaLayer: null,
    entityTerriaLayer: null,
    removeTerriaLayer: null,
  },
  mutations: {
    setRegionLevelOneData_left(state, data){
        state.regionLevelOneData_left = Object.assign({}, data)
    },
    setRegionLevelTwoData_left(state, data){
        state.regionLevelTwoData_left = Object.assign({}, data)
    },
    setRegionLevelOneData_right(state, data){
        state.regionLevelOneData_right = Object.assign({}, data)
    },
    setRegionLevelTwoData_right(state, data){
        state.regionLevelTwoData_right = Object.assign({}, data)
    },
    setMarkerLevelOneData(state, data){
        state.markerLevelOneData = Object.assign({}, data)
    },
    setMarkerLevelTwoData(state, data){
        state.markerLevelTwoData = Object.assign({}, data)
    },
    setTerriaLayer(state, data){
        state.terriaLayer = Object.assign({}, data)
    },
    setEntityTerriaLayer(state, data){
        state.entityTerriaLayer = Object.assign({}, data)
    },
    setRemoveTerriaLayer(state, data){
        state.removeTerriaLayer = Object.assign({}, data)
    },
  },
  actions: {

    async getLevelOneData(context, params) {


      

      //Call level one api
      const url = '/map/categories/' + params['type'] + '/' + params['school_id']
      const levelOne = await httpClient.get(url);

      //console.log("level 1 data from api")
      //console.log(url)

      if( levelOne["data"] !== null & levelOne["data"] !== undefined ){

          if( "data" in levelOne["data"] ){

            var options = levelOne["data"]['data']
            var labels = levelOne["data"]['labels']

            //Set selection defaults
            var selections = {}
            selections['category'] = [ Object.keys(options)[0] ]
            selections['subcategory'] = [ Object.keys(options[selections['category']])[0] ]
            selections['metric'] = [ options[selections['category']][selections['subcategory']][0] ]

            //Commit all
            var full_data={
              'options':options,
              'labels':labels,
              'selections':selections
            }
            //console.log('map-data.js - LEVEL ONE',params.type,params.split,full_data)
            if (params['type']=='region'){
              context.commit(params.split=='LEFT' ? 'setRegionLevelOneData_left' : 'setRegionLevelOneData_right', full_data)
            }
            else if (params['type']=='marker'){
              context.commit('setMarkerLevelOneData', full_data)
            }

          }          
      }     
    },

    async getLevelTwoData(context, params) {

      //Api call
      var query=_.omit(params,'school_id','type','split')
      var queryString = Object.keys(query).reduce(
        function(a,k){
          query[k].forEach(item => a.push(k+'='+encodeURIComponent(item))); 
          return a;
        },[]).join('&')
      //var queryString = Object.keys(query).map(key => key + '=' + encodeURIComponent(query[key])).join('&')
      const url = '/map/filters/' + params['type'] + '/' + params['school_id'] + '?' + queryString;
      const levelTwo = await httpClient.get( url );

      //console.log("levelTwo data from api")
      //console.log(url)
      //console.log(levelTwo)

      //Check response
      if( levelTwo["data"] !== null & levelTwo["data"] !== undefined ){

        var options = levelTwo["data"]["data"]
        var labels = levelTwo["data"]['labels']

        //Set selection defaults          
        var selections = {}
        selections['dropdown1'] = [ Object.keys(options)[0] ]
        selections['dropdown2'] = [ Object.keys(options[selections['dropdown1']])[0] ]
        selections['dropdown3'] = [ Object.keys(options[selections['dropdown1']][selections['dropdown2']])[0] ]
        selections['dropdown4'] = [Object.keys(options[selections['dropdown1']][selections['dropdown2']][selections['dropdown3']])[0]]

        var len = options[selections['dropdown1']][selections['dropdown2']][selections['dropdown3']][selections['dropdown4']].length
        selections['dropdown5'] = [options[selections['dropdown1']][selections['dropdown2']][selections['dropdown3']][selections['dropdown4']][len-1]]

        selections['dropdown6'] = [options[selections['dropdown1']][selections['dropdown2']][selections['dropdown3']][selections['dropdown4']][0]]

        //console.log("selection dropdown1")
        //console.log(options[selections['dropdown1']][selections['dropdown2']][selections['dropdown3']][selections['dropdown4']].length)
                    
        //Commit all
        var full_data={
          'options':options,
          'labels':labels,
          'selections':selections
        }
        //console.log('map-data.js - LEVEL TWO',params.type,params.split,full_data)
        if (params['type']=='region'){
          context.commit(params.split=='LEFT' ? 'setRegionLevelTwoData_left' : 'setRegionLevelTwoData_right', full_data)
        }
        else if (params['type']=='marker'){
          context.commit('setMarkerLevelTwoData', full_data)
        }
      } 
    },

    async reassignLevelOneData(context, params) {

        //Reassign data on submit
        var full_data={
          'options':params['options'],
          'labels':params['labels'],
          'selections':params['selections']
        }
        //console.log('Reassign - LEVEL ONE',params.type,params.split,full_data)
        if (params['type']=='region'){
          context.commit(params.split=='LEFT' ? 'setRegionLevelOneData_left' : 'setRegionLevelOneData_right', full_data)
        }
        else if (params['type']=='marker'){
          context.commit('setMarkerLevelOneData', full_data)
        }
    },

    async reassignLevelTwoData(context, params) {

        //Reassign data on submit
        var full_data={
          'options':params['options'],
          'labels':params['labels'],
          'selections':params['selections']
        }
        //console.log('Reassign - LEVEL TWO',params.type,params.split,full_data)
        if (params['type']=='region'){
          context.commit(params.split=='LEFT' ? 'setRegionLevelTwoData_left' : 'setRegionLevelTwoData_right', full_data)
        }
        else if (params['type']=='marker'){
          context.commit('setMarkerLevelTwoData', full_data)
        }
    },

    async getTerriaLayer(context, params) {

      //Api call
      const url = '/map/terria/' + params['params']['type'] + '/' + params['params']['school_id'];
      const body = {
          "params": params['query'],
          "format": params['format']
      };
      const terriaLayer = await httpClient.post( url, body );
      //console.log("params query")
      //console.log(params['query'])

      //Check response
      if( terriaLayer["data"] !== null & terriaLayer["data"] !== undefined ){
          context.commit('setTerriaLayer', terriaLayer["data"])
      } 
    },

    // get school location
    async getEntityTerriaLayer(context, params) {

      //console.log("undefined")
      //console.log(params['params']['school_id'])

      //Api call
      const url = '/map/terria/item/' + params['params']['school_id'];
      const body = {
          "params": null,
          "format": params['format']
      };
      var terriaLayer = null;
      if (params['params']['school_id'] !== null & params['params']['school_id'] !== undefined)
          terriaLayer = await httpClient.post(url, body);

      //Check response
      if( terriaLayer["data"] !== null & terriaLayer["data"] !== undefined ){
          context.commit('setEntityTerriaLayer', terriaLayer["data"])
      } 
    },

    async getRemoveTerriaLayer(context, params) {

      //Api call
      const url = '/map/terria/remove/' + params['params']['school_id'];
      const terriaLayer = await httpClient.post( url, params );

      //Check response
      if( terriaLayer["data"] !== null & terriaLayer["data"] !== undefined ){
          context.commit('setRemoveTerriaLayer', terriaLayer["data"])
      } 
    },

  },

}
