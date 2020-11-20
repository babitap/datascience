<template>
  <div>
    <!-- 
    <LeafletMap style='height: 600px;'>
    </LeafletMap>
    -->
    <div class="selectionContainer">
      <va-accordion>
        <va-collapse>
          <span slot="header">Configuration</span>
          <div slot="body">
            <div>
              <!------------------------------------------------>
              <!-- Select colour -->
              <p class="display-6">Select Colour:</p>
              <!-- select option -->
              <va-select
                v-model="formatSelect.colour"
                textBy="description"
                :options="formatOptions.colour"
              />

              <!-- show option -->
              <div v-if="formatSelect.colour.description=='Single'">
                <va-advanced-color-picker v-model="formatSelect.colour.value" />
              </div>
              <div v-if="formatSelect.colour.description=='Colour Map'">
                <va-select
                  v-model="formatSelect.colour.value"
                  textBy="description"
                  :options="colourMap"
                />
              </div>
              <!------------------------------------------------>
              <!-- Select scale -->
              <p class="display-6">Select Scale:</p>

              <!-- select option -->
              <va-select
                v-model="formatSelect.scale"
                textBy="description"
                :options="formatOptions.scale"
              />

              <!-- show option -->
              <div v-if="formatSelect.scale.id==1 | formatSelect.scale.id==2">
                <p class="display-7"># of bins:</p>
                <va-input
                  v-model="formatSelect.scale.value"
                  type="number"
                  min="1"
                  placeholder="Number of bins"
                />
              </div>
              <div v-if="formatSelect.scale.id==3">
                <p class="display-7">Min/max value:</p>
                <va-slider
                  range
                  v-model="formatSelect.scale.value"
                  min="10"
                  max="1000"
                  value-visible
                />
              </div>

              <!------------------------------------------------>
              <!-- Select size or opacity -->
              <div v-if="selectedTabIndex==0">
                <p class="display-6">Select Opacity:</p>
                <va-input
                  v-model="formatSelect.opacity.value"
                  type="number"
                  min="0"
                  max="1"
                  placeholder="Input Opacity"
                />
              </div>
              <div v-if="selectedTabIndex==1">
                <p class="display-6">Select Size:</p>
                <va-input
                  v-model="formatSelect.size.value"
                  type="number"
                  min="1"
                  placeholder="Input Size"
                />
              </div>
            </div>
          </div>
        </va-collapse>
        <va-collapse :isOpenDefault="true">
          <span slot="header">Layer Selection</span>
          <div slot="body">
            <div class="">
              <va-tabs grow v-model="selectedTabIndex">
                <va-tab v-for="title in tabOptions" :key="title">{{title}}</va-tab>
              </va-tabs>
            </div>
            <div class="">
              <div v-show="selectedTabIndex === 0"  class="regionContainer">
                <div class="region">
                  <div class="singleRegionContainer">
                    <h5>Left region</h5>
                    <DataSelection
                      id="left-region-select"
                      :data_select="left_region_select"
                      @create_terria_layer="createTerriaLayer"
                      @update_level_one_selections="set_new_level_one_selections"
                      @update_level_two_selections="set_new_level_two_selections"
                    ></DataSelection>
                  </div>
                </div>
                <div class="region">
                  <div class="singleRegionContainer">
                    <h5>Right region</h5>
                    <DataSelection
                      id="right-region-select"
                      :data_select="right_region_select"
                      @create_terria_layer="createTerriaLayer"
                      @update_level_one_selections="set_new_level_one_selections"
                      @update_level_two_selections="set_new_level_two_selections"
                    ></DataSelection>
                  </div>
                </div>
              </div>
              <div v-show="selectedTabIndex === 1"  class="regionContainer">
                <div class="region">
                  <div class="singleRegionContainer">
                    <h5>Markers</h5>
                    <DataSelection
                      id="marker-select"
                      :data_select="marker_select"
                      @create_terria_layer="createTerriaLayer"
                      @update_level_one_selections="set_new_level_one_selections"
                      @update_level_two_selections="set_new_level_two_selections"
                    ></DataSelection>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </va-collapse>
        <!-- va-collapse items -->
      </va-accordion>
    </div>

    <div class="row map">
      <div class="flex xs12" style="float: left;" id="terria-map">
        <iframe
          id="embedded-terria-map"
          frameborder="0"
          src="https://findex-map.azurewebsites.net/"
          style="height: 800px; width: 100%;"
          @load="mapEntityTerriaLayer"
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script>
import DataSelection from "../components/data-select";
import LeafletMap from "../components/leaflet-select";
import { mapState, mapActions } from "vuex";

export default {
  name: "map_component",
  components: {
    DataSelection,
    LeafletMap,
  },
  data() {
    return {
      //Needed for terriajs configuration
      left_region_layer_count: -1, // Must start -1
      right_region_layer_count: -1, // Must start -1
      marker_layer_count: 0, // Must start 0

      //Structure for tabs
      selectedDataSetIndex: 0,
      // mapStructureData: [{
      //     'value':'Left Region',
      //     'label':'Left Region',
      //     'data_select':null
      // },
      // {
      //     'value':'Right Region',
      //     'label':'Right Region',
      //     'data_select':null
      // },
      // {
      //     'value':'Markers',
      //     'label':'Markers',
      //     'data_select':null
      // }],
      leftRegionSelect: 0,
      rightRegionSelect: 1,
      markerSelect: 2,
      selectedTabIndex: 0,
      tabOptions: ["Region", "Markers"],

      //   mapStructureData: [
      //     {
      //       value: "Left Region",
      //       label: "Left Region",
      //       data_select: null
      //     },
      //     {
      //       value: "Right Region",
      //       label: "Right Region",
      //       data_select: null
      //     },
      //     {
      //       value: "Markers",
      //       label: "Markers",
      //       data_select: null
      //     }
      //   ],

      //Structure for selects
      left_region_select: {
        type: "region",
        split: "LEFT",
        level_one_options: null,
        level_one_selected: null,
        level_two_options: null,
        level_two_labels: null,
        level_two_selected: null
      },
      right_region_select: {
        type: "region",
        split: "RIGHT",
        level_one_options: null,
        level_one_selected: null,
        level_two_options: null,
        level_two_labels: null,
        level_two_selected: null
      },
      marker_select: {
        type: "marker",
        split: null,
        level_one_options: null,
        level_one_selected: null,
        level_two_options: null,
        level_two_labels: null,
        level_two_selected: null
      },
      //Format strcture
      colourMap: ["red-white-hsl(240,50%,50%)", "green-orange"],
      formatSelect: {
        colour: {
          id: 1,
          description: "Colour Map",
          value: "red-white-hsl(240,50%,50%)"
        },
        scale: {
          id: 1,
          description: "Quantile",
          value: 10
        },
        opacity: {
          id: 1,
          description: "opacity",
          value: 1
        },
        size: {
          id: 1,
          description: "size",
          value: 3
        }
      },
      formatOptions: {
        colour: [
          {
            id: 1,
            description: "Colour Map",
            value: "red-white-hsl(240,50%,50%)"
          },
          {
            id: 2,
            description: "Single",
            value: "#ffd50a"
          }
        ],
        scale: [
          {
            id: 1,
            description: "Auto",
            value: 10
          },
          {
            id: 2,
            description: "Quantile",
            value: 10
          },
          {
            id: 3,
            description: "Min/Max",
            value: [20, 80]
          }
        ]
      }
    };
  },
  computed: {
    ...mapState({
      selectedEntity: state => state.user.selectedEntity,
      regionLevelOneData_left: state => state.map.regionLevelOneData_left,
      regionLevelTwoData_left: state => state.map.regionLevelTwoData_left,
      regionLevelOneData_right: state => state.map.regionLevelOneData_right,
      regionLevelTwoData_right: state => state.map.regionLevelTwoData_right,
      markerLevelOneData: state => state.map.markerLevelOneData,
      markerLevelTwoData: state => state.map.markerLevelTwoData,
      terriaLayer: state => state.map.terriaLayer,
      entityTerriaLayer: state => state.map.entityTerriaLayer,
      removeTerriaLayer: state => state.map.removeTerriaLayer
    }),
    focused_school_id: function() {
      if (this.selectedEntity !== null) {
        return this.selectedEntity.industry_id;
      } else {
        return null;
      }
    }
  },

  async created() {
    //Load region data
    await this.orch_load_level_data();
  },

  watch: {
     //selectedTabIndex: function(new_value, old_value) {
    //   console.log("watch selectedDataSetIndex", new_value, old_value);

    //   //Save old_value data
    //   if (old_value === 0) {
    //     this.mapStructureData[0].data_select = Object.assign(
    //       {},
    //       this.left_region_select
    //     );
    //   } else if (old_value === 1) {
    //     this.mapStructureData[1].data_select = Object.assign(
    //       {},
    //       this.right_region_select
    //     );
    //   } else if (old_value === 2) {
    //     this.mapStructureData[2].data_select = Object.assign(
    //       {},
    //       this.marker_select
    //     );
    //   }

      //Assign new_value data
    //   if (new_value === 0) {
    //       //this.leftRegionSelect += 1
    //       //this.rightRegionSelect += 1
    //     //this.reassign_data_select({ type: "region", split: "LEFT" });
    //     //this.reassign_data_select({ type: "region", split: "RIGHT" });
    //   } else if (new_value === 1) {
    //       //this.markerSelect += 1
    //     //this.reassign_data_select({ type: "marker", split: null });
    //   }
    // },
    focused_school_id: function() {
      if (this.focused_school_id) {
        this.orch_load_level_data();
        this.mapEntityTerriaLayer();
      }
    },
    regionLevelOneData_left: function() {
      this.left_region_select = {
        type: "region",
        split: "LEFT",
        level_one_options: this.regionLevelOneData_left.options,
        level_one_labels: this.regionLevelOneData_left.labels,
        level_one_selected: this.regionLevelOneData_left.selections,
        level_two_options: this.regionLevelTwoData_left.options,
        level_two_labels: this.regionLevelTwoData_left.labels,
        level_two_selected: this.regionLevelTwoData_left.selections
      };
    },
    regionLevelTwoData_left: function() {
      this.left_region_select = {
        type: "region",
        split: "LEFT",
        level_one_options: this.regionLevelOneData_left.options,
        level_one_labels: this.regionLevelOneData_left.labels,
        level_one_selected: this.regionLevelOneData_left.selections,
        level_two_options: this.regionLevelTwoData_left.options,
        level_two_labels: this.regionLevelTwoData_left.labels,
        level_two_selected: this.regionLevelTwoData_left.selections
      };
    },
    regionLevelOneData_right: function() {
      this.right_region_select = {
        type: "region",
        split: "RIGHT",
        level_one_options: this.regionLevelOneData_right.options,
        level_one_labels: this.regionLevelOneData_right.labels,
        level_one_selected: this.regionLevelOneData_right.selections,
        level_two_options: this.regionLevelTwoData_right.options,
        level_two_labels: this.regionLevelTwoData_right.labels,
        level_two_selected: this.regionLevelTwoData_right.selections
      };
    },
    regionLevelTwoData_right: function() {
      this.right_region_select = {
        type: "region",
        split: "RIGHT",
        level_one_options: this.regionLevelOneData_right.options,
        level_one_labels: this.regionLevelOneData_right.labels,
        level_one_selected: this.regionLevelOneData_right.selections,
        level_two_options: this.regionLevelTwoData_right.options,
        level_two_labels: this.regionLevelTwoData_right.labels,
        level_two_selected: this.regionLevelTwoData_right.selections
      };
    },
    markerLevelOneData: function() {
      this.marker_select = {
        type: "marker",
        split: null,
        level_one_options: this.markerLevelOneData.options,
        level_one_labels: this.markerLevelOneData.labels,
        level_one_selected: this.markerLevelOneData.selections,
        level_two_options: this.markerLevelTwoData.options,
        level_two_labels: this.markerLevelTwoData.labels,
        level_two_selected: this.markerLevelTwoData.selections
      };
    },
    markerLevelTwoData: function() {
      this.marker_select = {
        type: "marker",
        split: null,
        level_one_options: this.markerLevelOneData.options,
        level_one_labels: this.markerLevelOneData.labels,
        level_one_selected: this.markerLevelOneData.selections,
        level_two_options: this.markerLevelTwoData.options,
        level_two_labels: this.markerLevelTwoData.labels,
        level_two_selected: this.markerLevelTwoData.selections
      };
    }
  },

  methods: {
    ...mapActions({
      loadLevelOneData: "map/getLevelOneData",
      loadLevelTwoData: "map/getLevelTwoData",
      reassignLevelOneData: "map/reassignLevelOneData",
      reassignLevelTwoData: "map/reassignLevelTwoData",
      loadTerriaLayer: "map/getTerriaLayer",
      loadEntityTerriaLayer: "map/getEntityTerriaLayer",
      loadRemoveTerriaLayer: "map/getRemoveTerriaLayer"
    }),

    /*--------------------------------------------------------------------*/
    async orch_load_level_data() {
      if (this.focused_school_id) {
        var params = {
          school_id: this.focused_school_id
        };
        //Load region data
        this.load_level_data({
          ...params,
          ...{ type: "region", split: "LEFT" }
        });
        this.load_level_data({
          ...params,
          ...{ type: "region", split: "RIGHT" }
        });
        this.load_level_data({ ...params, ...{ type: "marker", split: null } });
      }
    },
    async load_level_data(params) {
      //Load level one
      await this.loadLevelOneData(params);

      //Then load level two
      if (params["type"] == "region") {
        if (params.split == "LEFT") {
          await this.load_level_two_data(
            params,
            this.regionLevelOneData_left.selections
          );
          //Save initial data load
          //   this.mapStructureData[0].data_select = Object.assign(
          //     {},
          //     this.left_region_select
          // );
        } else if (params.split == "RIGHT") {
          await this.load_level_two_data(
            params,
            this.regionLevelOneData_right.selections
          );
          //Save initial data load
          //   this.mapStructureData[1].data_select = Object.assign(
          //     {},
          //     this.right_region_select
          //   );
        }
      } else if (params["type"] == "marker") {
        await this.load_level_two_data(
          params,
          this.markerLevelOneData.selections
        );
        //Save initial data load
        // this.mapStructureData[2].data_select = Object.assign(
        //   {},
        //   this.marker_select
        // );
      }
    },
    async load_level_two_data(params, selections) {
      if (
        this.focused_school_id &&
        "category" in selections &&
        "subcategory" in selections &&
        "metric" in selections
      ) {
        await this.loadLevelTwoData({ ...params, ...selections });
      }
    },

    /*--------------------------------------------------------------------*/
    async set_new_level_one_selections(params, new_selections) {
      //Get level two data based on new level one selections
      await this.load_level_two_data(
        { ...{ school_id: this.focused_school_id }, ...params },
        new_selections
      );

      //Check type
      if (params["type"] == "region") {
        //Check split side
        if (params["split"] == "LEFT") {
          this.left_region_select = Object.assign({}, this.left_region_select, {
            level_one_selected: new_selections
          });
        } else if (params["split"] == "RIGHT") {
          this.right_region_select = Object.assign(
            {},
            this.right_region_select,
            { level_one_selected: new_selections }
          );
        }
      } else if (params["type"] == "marker") {
        this.marker_select = Object.assign({}, this.marker_select, {
          level_one_selected: new_selections
        });
      }
    },
    async set_new_level_two_selections(params, new_selections) {
      //Check type
      if (params["type"] == "region") {
        //Check split side
        if (params["split"] == "LEFT") {
          this.left_region_select = Object.assign({}, this.left_region_select, {
            level_two_selected: new_selections
          });
        } else if (params["split"] == "RIGHT") {
          this.right_region_select = Object.assign(
            {},
            this.right_region_select,
            { level_two_selected: new_selections }
          );
        }
      } else if (params["type"] == "marker") {
        this.marker_select = Object.assign({}, this.marker_select, {
          level_two_selected: new_selections
        });
      }
    },
    async reassign_data_select(params) {
      //Update data select
      if (params["type"] == "region") {
        if (params.split == "LEFT") {
          await this.reassignLevelOneData({
            ...params,
            ...{
              options: this.mapStructureData[0].data_select.level_one_options,
              labels: this.mapStructureData[0].data_select.level_one_labels,
              selections: this.mapStructureData[0].data_select
                .level_one_selected
            }
          });
          await this.reassignLevelTwoData({
            ...params,
            ...{
              options: this.mapStructureData[0].data_select.level_two_options,
              labels: this.mapStructureData[0].data_select.level_two_labels,
              selections: this.mapStructureData[0].data_select
                .level_two_selected
            }
          });
        } else if (params.split == "RIGHT") {
          await this.reassignLevelOneData({
            ...params,
            ...{
              options: this.mapStructureData[1].data_select.level_one_options,
              labels: this.mapStructureData[1].data_select.level_one_labels,
              selections: this.mapStructureData[1].data_select
                .level_one_selected
            }
          });
          await this.reassignLevelTwoData({
            ...params,
            ...{
              options: this.mapStructureData[1].data_select.level_two_options,
              labels: this.mapStructureData[1].data_select.level_two_labels,
              selections: this.mapStructureData[1].data_select
                .level_two_selected
            }
          });
        }
      } else if (params["type"] == "marker") {
        await this.reassignLevelOneData({
          ...params,
          ...{
            options: this.mapStructureData[2].data_select.level_one_options,
            labels: this.mapStructureData[2].data_select.level_one_labels,
            selections: this.mapStructureData[2].data_select.level_one_selected
          }
        });
        await this.reassignLevelTwoData({
          ...params,
          ...{
            options: this.mapStructureData[2].data_select.level_two_options,
            labels: this.mapStructureData[2].data_select.level_two_labels,
            selections: this.mapStructureData[2].data_select.level_two_selected
          }
        });
      }
    },

    /*--------------------------------------------------------------------*/
    async createTerriaLayer(params, selected) {
      //This functon creates layer on terriajs

      if (this.focused_school_id) {
        //Collect layer data to post in http body
        var format = await this.loadTerriaFormat(params);

        //Load region data with api call
        var terria_params = {
          params: {
            ...{ school_id: this.focused_school_id },
            ...params
          },
          query: selected,
          format: format
        };
        await this.loadTerriaLayer(terria_params);
        console.log(this.terriaLayer);

        //Send to iFrame
        this.sendTerriaIFrame(this.terriaLayer);
        console.log("Create", params["type"], "-", params["split"], "!!");
      }
    },
    async mapEntityTerriaLayer() {
      //This functon maps the current school selected onto terria
      var terria_params = {
        params: {
          school_id: this.focused_school_id
        },
        format: {
          camera: {
            north: -8,
            east: 158,
            south: -45,
            west: 109
          },
          id: 0 //Always have school marked at zero, if school changed, this should replace previous
        }
      };
      await this.loadEntityTerriaLayer(terria_params);

      //Send to iFrame
      this.sendTerriaIFrame(this.entityTerriaLayer);
      console.log("Item!!");
    },
    async removeLayer_fromTerria(id, layer_type, splitDirection) {
      //This functon removes layer from terriajs by specified index, layer_type and splitDirection
      //Sends no data to the existing layer
      console.log(id, splitDirection);
      var terria_params = {
        params: {
          school_id: this.focused_school_id,
          type: layer_type
        },
        format: {
          camera: {
            north: -8,
            east: 158,
            south: -45,
            west: 109
          },
          id: id,
          splitDirection: splitDirection
        }
      };
      await this.loadRemoveTerriaLayer(terria_params);

      //Send to iFrame
      this.sendTerriaIFrame(this.removeTerriaLayer);
      console.log("Remove!!");
    },
    async loadTerriaFormat(params) {
      //--------------------------
      //      Set layer info
      //--------------------------

      //Region layer
      if (params["type"] === "region") {
        //Left region
        if (params["split"] === "LEFT") {
          //Increase layer count
          this.left_region_layer_count += 1;
          const id = -2 * (this.left_region_layer_count + 1); //-2,-4,-6,-8 -- count will be first zero
          //Remove prior layer
          if (this.left_region_layer_count > 0) {
            await this.removeLayer_fromTerria(id + 2, "region", -1); //add 2 to get previous id
          }
          //Return new layer
          return {
            camera: {
              north: -8,
              east: 158,
              south: -45,
              west: 109
            },
            id: id,
            splitDirection: -1,
            name: "Left Region layer",
            regionTypeDimensionId: "sa2",
            formatSelect: this.formatSelect
            //'colorMap':'red-white-hsl(240,50%,50%)',
            //'colorBins':10,
          };
        }

        //Right region
        else if (params["split"] === "RIGHT") {
          //Increase layer count
          this.right_region_layer_count += 1;
          const id = -2 * this.right_region_layer_count - 1; //-1,-3,-5,-7 -- count will be first zero
          //Remove prior layer
          if (this.right_region_layer_count > 0) {
            await this.removeLayer_fromTerria(id + 2, "region", 1); //add 2 to get previous id
          }
          //Return new layer
          return {
            camera: {
              north: -8,
              east: 158,
              south: -45,
              west: 109
            },
            id: id,
            splitDirection: 1,
            name: "Right Region layer",
            regionTypeDimensionId: "sa2",
            formatSelect: this.formatSelect
            //'colorMap':'red-white-hsl(240,50%,50%)',
            //'colorBins':10,
          };
        }
      }

      //Marker layer
      else if (params["type"] === "marker") {
        this.marker_layer_count += 1;
        //Remove prior layer
        if (this.marker_layer_count > 1) {
          await this.removeLayer_fromTerria(
            this.marker_layer_count - 1,
            "marker",
            null
          );
        }
        return {
          camera: {
            north: -8,
            east: 158,
            south: -45,
            west: 109
          },
          id: this.marker_layer_count, //1,2,3,4 -- count will be first one
          name: "Marker layer", //"Marker layer: "+this.marker_layer_count,
          formatSelect: this.formatSelect
          /*'colorMap': 'red-white-hsl(240,50%,50%)',
                    'colorBins': 0,
                    'scale': 3,
                    'scaleByValue': true,*/
        };
      }

      //Item layer
      else if (params["type"] === "item") {
        //Might need to do this later....
        return {};
      }
    },
    sendTerriaIFrame(layer) {
      //Post layer to terria map iframe window
      const iframeWindow = document.getElementById("embedded-terria-map")
        .contentWindow;
      //if ( iframeWindow.readyState  == 'complete' ) { <--------- doesn't work from a different domain
      iframeWindow.postMessage(
        { initSources: [layer] },
        "https://findex-map.azurewebsites.net/"
      );
      //}
    }
  }
};
</script>
<style lang="scss" scoped>
.regionContainer {
  display: flex;
  justify-content: space-evenly;
  padding-bottom: 10vh; //This is add to the bottom to give more room for the container, otherwise some dropdown can not see all the options

  @include media-breakpoint-up(xs) {
    display: block;
  }

  @include media-breakpoint-up(md) {
    display: flex;
  }
}

.region {
  margin: 10px;
  background-color: white;
  border-radius: 5px;
}

.singleRegionContainer {
  padding: 15px;
}

.selectionContainer {
  display: block;
  justify-content: center;
}
</style>
