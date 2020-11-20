<template>
<div class="row">

    <!-- 

   ###############################################
   ###############################################
   ###############################################

             All of this is in developent

   ###############################################
   ###############################################
   ###############################################

    -->


    <!-- Show map selection -->
    <l-map ref="map"
      class='flex xs6' 
      :zoom="zoom"
      :center="center"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      @update:bounds="boundsUpdated">
        <l-tile-layer 
            :url="url"
            :maxZoom="maxZoom"
            :attribution="attribution"
        >
        </l-tile-layer>
        <l-geo-json
            :geojson="geojson"
            :options="options"
            :options-style="styleFunction"
        />
        <l-circle-marker
            v-for="marker in markers" 
            :lat-lng="marker.coord"
            :radius="defaultMarkerStyle.radius"
            :color="defaultMarkerStyle.color"
            @click="clickMarker"
        />
    </l-map>

    <!-- Show info -->
    <div class='flex xs6' id='map-data'>

        <va-card class="row h-25" id='map-card' style="overflow-x: auto;">
          <div id='hover-info'><label>Hover over a region</label></div>
        </va-card>

        <div class="row" id='chosen-regions-hidden' @change='addRegion($event)' hidden>
        </div>
        
        <div class="row" style="height: 600px; max-height: 100%;" id='chosen-cards'>

          <div class='flex xs12' style="overflow: hidden;"> 
            <div style="overflow-y: scroll;">
              <va-button class="mb-2" @click="addGroupNode()">Add group</va-button>
              <vue-tree-list
                @click="onClick"
                @delete-node="onDel"
                :model="selection_treeview"
                default-tree-node-name="new node"
                default-leaf-node-name="new leaf"
                v-bind:default-expanded="false">
                <span class="icon" slot="addTreeNodeIcon">📂</span>
                <span class="icon" slot="addLeafNodeIcon">＋</span>
                <span class="icon" slot="editNodeIcon">📃</span>
                <span class="icon" slot="delNodeIcon">✂️</span>
                <span class="icon" slot="leafNodeIcon">🍃</span>
                <span class="icon" slot="treeNodeIcon">🌲</span>
              </vue-tree-list>
            </div>
          </div>

          <!-- Selected regions -->
          <va-card class='flex xs6' style="height: 100%; overflow-x: auto;">
          
            <label>Regions:</label>

            <!-- Toggle regions -->
            <va-toggle class="mb-2" v-model="select_regions">Create new region group</va-toggle>
            <div v-if="select_regions" class="flex row align--center">
              <va-input v-model="new_group_label" placeholder="Name of group" class="mb-0"/>
              <va-button class="mb-2" @click="addRegionGroup()">
                Add region(s) to group
              </va-button>
            </div>

            <!-- Treeview regions -->
            <va-tree-root>
              <va-tree-category v-for="group in groups" :label="group.label">
                <va-tree-node v-for="region in group.regions" :key="region.id">
                  <div class="flex row align--center">
                  {{ region.name }}
                  <va-checkbox v-if="select_regions" slot="checkbox" v-model="region.selected"/>
                  <va-icon
                      name="ion ion-md-close"
                      color="info"
                      class="ml-2 pa-1 shrink"
                      style="cursor: pointer;"
                      @click.native="removeRegionFromGroup(region,group)"
                    />
                  </div>
                </va-tree-node>
                <va-icon
                    name="ion ion-md-close"
                    color="info"
                    slot="checkbox"
                    style="cursor: pointer;"
                    @click.native="removeGroup(group)"
                  />
                
              </va-tree-category>

              <va-tree-node v-for="region in regions" :key="region.id">
                <div class="flex row align--center">
                {{ region.name }}
                <va-checkbox v-if="select_regions" slot="checkbox" v-model="region.selected"/>
                <va-icon
                    name="ion ion-md-close"
                    color="info"
                    class="ml-2 pa-1 shrink"
                    style="cursor: pointer;"
                    @click.native="removeRegion(region)"
                  />
                </div>
              </va-tree-node>
            </va-tree-root>

          </va-card>

        </div>

    </div>

</div>
</template>

<script>
import { LMap, LTileLayer, LCircleMarker, LGeoJson, LFeatureGroup } from 'vue2-leaflet';
import { httpClient } from '@/app/shared/services/http-client'
import * as turf from '@turf/turf'
import { VueTreeList, Tree, TreeNode } from 'vue-tree-list'

export default {
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
    LCircleMarker,
    VueTreeList
  },
  data () {
    return {
      //Base map
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 10,
      maxZoom: 25,
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
      center: [-34.927853, 138.610565],
      bounds: null,

      //Leaflet
      loading: false,
      geojson: null,
      defaultRegionStyle:{
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
      },
      markers: null,
      turf_markers: null,
      defaultMarkerStyle: {
        radius: 6,
        color: 'red'
      },

      //Select regions
      select_regions:false,
      new_group_label:'',
      group_id:0,
      groups: [],
      region_id:0,
      regions: [],

      selection_treeview: new Tree([])

    }
  },
  computed: {
    options() {
      return {
        onEachFeature: this.onEachFeatureFunction
      };
    },
    styleFunction() {
        return (feature) => {
            return {
                ...this.defaultRegionStyle,
                ...{fillColor: this.getColor(parseFloat(feature.properties.Feature))}
            };
        };
    },
    onEachFeatureFunction() {
      return (feature, layer) => {            
        layer.on({
            mouseover: this.highlightFeature,
            mouseout: this.resetHighlight,
            click: this.clickRegion
        });
      };
    }
  },
  async created() {
    //Load geojson data
    this.loading = true;
    var url = '/map/geojson/SA/SA2'
    var data = await httpClient.get( url );
    this.geojson = data['data'];
    this.loading = false;

    //Load marker data
    this.loading = true;
    url = '/map/marker/SA'
    data = await httpClient.get( url );
    this.markers = data['data']['data'].map(function (p) {
      return {
        'lat':p.Latitude,
        'lng':p.Longitude,
        'coord':L.latLng([p.Latitude,p.Longitude]),
        'name':p.name,
        'code':p.code
      }
    })
    this.loading = false;
  },
  methods: {
    findLayersFromType(layer_type){
      var layers=[]
      this.$refs.map.mapObject.eachLayer( function(layer) {
          if(layer instanceof layer_type){
              layers.push(layer);
          }
          else if(layer_type == L.geoJSON){
            if('feature' in layer){
              layers.push(layer);
            }
          }
      });
      return layers 
    },
    findMarkersFromRegion(rgn_layer){
        //Change inner markers
        var output = []
        var latlng = null
        var markerLayers = this.findLayersFromType(L.CircleMarker)

        //Loop all markers
        for (var i=0; i<markerLayers.length; i++){
          latlng = markerLayers[i].getLatLng()
          latlng=turf.point([latlng.lng,latlng.lat])

          //Check if marker in geojson layer
          if(turf.inside(latlng, rgn_layer.feature)){
              output.push(markerLayers[i])
          }
        }
        return output
    },
    findRegionFromMarker(mrkr_layer){
        //Change inner markers
        var latlng = mrkr_layer.getLatLng()
        latlng=turf.point([latlng.lng,latlng.lat])
        var rgnLayers = this.findLayersFromType(L.geoJSON)

        //Loop all markers
        for (var i=0; i<rgnLayers.length; i++){
          //Check if marker in geojson layer
          if(turf.inside(latlng, rgnLayers[i].feature)){
              return [rgnLayers[i]]
          }
        }
    },






    addRegionGroup (){
      //Collect selected regions
      var rgns = []
      for (var i=0; i<this.groups.length; i++){
        rgns = rgns.concat(this.groups[i].regions.filter(obj => obj.selected === true))
      }
      rgns = rgns.concat(this.regions.filter(obj => obj.selected === true))
      //Delete selected regions
      for (var i=0; i<this.groups.length; i++){
        this.groups[i].regions = this.groups[i].regions.filter(obj => obj.selected === false)
        //Remove group if empty
        if (this.groups[i].regions.length==0){ this.removeGroup(this.groups[i]) }
      }
      this.regions = this.regions.filter(obj => obj.selected === false)
      //Add new group
      this.group_id+=1
      this.groups.push({
          id: this.group_id,
          label:this.new_group_label,
          selected:false,
          regions: rgns,
          schools: []
        },
        )
      //Turn off toggle
      this.select_regions=false
      this.new_group_label=''
    },
    removeRegion(region) {
      this.regions = this.regions.filter(regionToFilter => regionToFilter !== region)
      //Reset map layer style for removed layer
      this.resetDefaultStyle(region.layer,'region')
    },
    removeGroup(group){
      //Get index of group
      var index = this.groups.indexOf(group)
      //Remove regions first
      this.groups[index].regions.forEach(rgn => this.resetDefaultStyle(rgn.layer,'region'))
      //Remove group
      this.groups.splice(index, 1)
    },
    removeRegionFromGroup(region,group) {
      //Get group
      var grp = this.groups.filter(obj => {return obj.id === group.id})[0]
      //Modify group (remove region)
      var rgns = grp.regions.filter(regionToFilter => regionToFilter !== region)
      //Replace regions in group
      if (rgns.length==0){
        this.removeGroup(grp)
      }
      else{
        this.groups[this.groups.indexOf(grp)].regions = rgns
      }
      //Add region to regions list
      this.region_id+=1
      this.regions.push({
        'id':this.region_id,
        'name':region.name,
        'selected':false,
        'layer':region.layer
      })
    },


    //leaflet functions
    zoomUpdated (zoom) {
      this.zoom = zoom;
    },
    centerUpdated (center) {
      this.center = center;
    },
    boundsUpdated (bounds) {
      this.bounds = bounds;
    },
    getColor(val) {
            
        //Find percent relative to min/max
        //if (val<min) {val=min;} 
        //else if (val>max) {val=max;}
        var perc = 0.5//(val-min)/(max-min);

        //Set HSL
        var s=70;//saturation
        var l=50;//lightness

        var color_min=0;//red
        var color_max=60;//yellow
        var h = perc*(color_max-color_min)

        return "hsl("+h+","+s+"%,"+l+"%)"
    },
    highlightFeature(e) {

        //Highlight only when not clicked
        var layer = e.target;
        var click = layer.options['click'];
        if (!click){
            layer.setStyle({
                weight: 5,
                color: '#666',
                dashArray: '',
                fillOpacity: 0.9
            });

            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) { layer.bringToFront();}
        }

        //Change Pane
        this.updateInfoPane(layer.feature.properties['SA2_NAME16']);
    },
    resetHighlight(e) {

        //Reset highlight only when not clicked
        var layer = e.target;
        var click = layer.options['click']==undefined ? false : layer.options['click']
        if (!click){
            layer.setStyle(this.defaultRegionStyle);
        }
        this.updateInfoPane();
    },
    updateInfoPane(name){
        document.getElementById('hover-info').innerHTML = (name ? '<label><b>' 
                + name + '</b></label>' : '<label>Hover over a region</label>');
    },
    clickRegion(e) {

        //Get layer and click
        var layer = e.target;
        var click = layer.options['click']==undefined ? false : layer.options['click']

        //Set region style
        this.setRegionStyle(layer,!click)

        //Set marker style related to selected marker
        var markers = this.findMarkersFromRegion(layer)
        markers.forEach(m => this.setMarkerStyle(m,!click))

        //Change list
        this.changeHidden(e,markers);
    },
    setRegionStyle(layer, click){

        if( click ){
          //Turn on
          layer.options['click']=true
          layer.setStyle({
            weight: 5,
            color: '#000',
            dashArray: '',
            fillOpacity: 1.0
          });
        }
        else{
          //Turn off 
          layer.options['click']=false
          layer.setStyle(
            this.defaultRegionStyle
          );
        }        
    },
    clickMarker(e) {

        //Get layer and click
        var layer = e.target;
        var click = layer.options['click']==undefined ? false : layer.options['click']

        //Set marker style 
        this.setMarkerStyle(layer,!click)

        //Set region style related to selected marker
        this.findRegionFromMarker(layer).forEach(r => this.setRegionStyle(r,!click))

        //Change list
        //this.changeHidden(e);
    },
    setMarkerStyle(layer, click){

        if( click ){
          //Turn on
          layer.options['click']=true
          layer.setStyle({
            radius: 6,
            color: 'blue'
          });
        }
        else{
          //Turn off 
          layer.options['click']=false
          layer.setStyle(
            this.defaultMarkerStyle
          );
        }
    },

    //List functions
    changeHidden(e,markers) {

        //elect hidden element
        const hidden_elem = document.getElementById('chosen-regions-hidden')

        //Get region to add
        var code = e.target.feature.properties['SA2_MAIN16']

        //Change elem
        hidden_elem.innerHTML = code;

        //Trigger change event
        var event = new CustomEvent("change", {detail: {...e,...markers}})
        hidden_elem.dispatchEvent(event);
    },
    /*addRegion(e){
        
        //Get hidden input then clear element
        var input = document.getElementById('chosen-regions-hidden').innerHTML;
        document.getElementById('chosen-regions-hidden').innerHTML = '';

        //Get layer data
        var layer = e.detail.target

        //Remove from selected list if already there
        var filterForInputRegion = this.regions.filter(obj => obj.name === input)
        if (filterForInputRegion.length !== 0){  
          //Remove
          this.regions.splice( this.regions.indexOf(filterForInputRegion[0]), 1 )
        }
        //Add to selected list if not already there
        else {
          this.region_id+=1
          this.regions.push({
            'id':this.region_id,
            'name':input,
            'selected':false,
            'layer':layer
          })
        }
    },*/
    searchForRegion(r){
      //need to search for region within all region selected in treeview
      //for child in this.selection_treeview.children:

    },
    addRegion(e){
        
        //Get hidden input then clear element
        var input = document.getElementById('chosen-regions-hidden').innerHTML;
        document.getElementById('chosen-regions-hidden').innerHTML = '';

        //Get layer data
        console.log(e)
        var layer = e.detail.target
        var markers = e.detail.target

        //Remove from selected list if already there
        this.searchForRegion(input)
        var filterForInputRegion = this.regions.filter(obj => obj.name === input)
        if (filterForInputRegion.length !== 0){  
          //Remove
          this.regions.splice( this.regions.indexOf(filterForInputRegion[0]), 1 )
        }
        //Add to selected list if not already there
        else {
          //Create region node
          var node = new TreeNode({ 
            name: input,
            type: 'region',
            isLeaf: false,
            addTreeNodeDisabled: true,
            addLeafNodeDisabled: true,
            editNodeDisabled: true,
            dragDisabled: false, 
          })
          //Add marker nodes as children
          if (!this.selection_treeview.children) this.selection_treeview.children = []
          this.selection_treeview.addChildren(node)
        }
    },
    addGroupNode(){
      var node = new TreeNode({ 
        name: 'New Group',
        type: 'group',
        isLeaf: false,
        addTreeNodeDisabled: true,
        addLeafNodeDisabled: true,
        editNodeDisabled: false,
        dragDisabled: true, 
      })
      if (!this.selection_treeview.children) this.selection_treeview.children = []
      this.selection_treeview.addChildren(node)
    },


    //-------------------------------------
    onDel (node) {
      console.log(node)
      node.remove()
    },
    onClick (params) {
      console.log(params)
    },

  }
}
</script>

<style lang="scss">
@import "~leaflet/dist/leaflet.css";
</style>
<style lang="less" rel="stylesheet/less">
  .vtl {
    .vtl-drag-disabled {
      background-color: #d0cfcf;

      &:hover {
        background-color: #d0cfcf;
      }
    }

    .vtl-disabled {
      background-color: #d0cfcf;
    }
  }
</style>
<style lang="less" rel="stylesheet/less" scoped>
  .icon {
    &:hover {
      cursor: pointer;
    }
  }
</style>
