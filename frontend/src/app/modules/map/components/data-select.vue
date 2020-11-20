<template>
  <div>
    <div class="container">
      <!-- Level One -->
      <div class="option category">
        <label>{{ labels.category }}:</label>
        <multiselect
          :value="selected.category"
          :options="options.category"
          :multiple="false"
          :taggable="true"
          :allow-empty="false"
          :showLabels="false"
          @tag="addTag"
          @input="commit_category"
        ></multiselect>
      </div>
      <div class="option subcategory">
        <label>{{ labels.subcategory }}:</label>
        <multiselect
          :value="selected.subcategory"
          :options="options.subcategory"
          :multiple="false"
          :taggable="true"
          :allow-empty="false"
          :showLabels="false"
          @tag="addTag"
          @input="commit_subcategory"
        ></multiselect>
      </div>
      <div class="option metric">
        <label>{{ labels.metric }}:</label>
        <multiselect
          :value="selected.metric"
          :options="options.metric"
          :multiple="true"
          :taggable="true"
          :allow-empty="false"
          :close-on-select="false"
          :clear-on-select="false"
          :preserve-search="true"
          :showLabels="false"
          @tag="addTag"
          @input="commit_metric"
        >
          <template slot="selection" slot-scope="{ values, search, isOpen }">
            <span
              class="multiselect__single"
              v-if="values.length &amp;&amp; !isOpen"
            >{{ values.length }} option(s) selected</span>
          </template>
        </multiselect>
      </div>

      <!-- Level Two -->
      <div class="option state">
        <label>{{ labels.dropdown1 }}:</label>
        <multiselect
          :value="selected.dropdown1"
          :options="options.dropdown1"
          :multiple="false"
          :taggable="true"
          :allow-empty="false"
          :showLabels="false"
          @tag="addTag"
          @input="commit_dropdown1"
        ></multiselect>
      </div>
      <div class="option region">
        <label>{{ labels.dropdown2 }}:</label>
        <multiselect
          :value="selected.dropdown2"
          :options="options.dropdown2"
          :multiple="false"
          :taggable="true"
          :allow-empty="false"
          :showLabels="false"
          @tag="addTag"
          @input="commit_dropdown2"
        ></multiselect>
      </div>
      <div class="option gender">
        <label>{{ labels.dropdown3 }}:</label>
        <multiselect
          :value="selected.dropdown3"
          :options="options.dropdown3"
          :multiple="false"
          :taggable="true"
          :allow-empty="false"
          :showLabels="false"
          @tag="addTag"
          @input="commit_dropdown3"
        ></multiselect>
      </div>
      <div class="option thematic">
        <label>{{ labels.dropdown4 }}:</label>
        <multiselect
          :value="selected.dropdown4"
          :options="options.dropdown4"
          :multiple="false"
          :taggable="true"
          :allow-empty="false"
          :showLabels="false"
          @tag="addTag"
          @input="commit_dropdown4"
        ></multiselect>
      </div>
      <div class="option compared year">
        <label>{{ labels.dropdown6 }}:</label>
        <multiselect :value="selected.dropdown6"
                     :options="options.dropdown6"
                     :multiple="false"
                     :taggable="true"
                     :allow-empty="false"
                     :showLabels="false"
                     @tag="addTag"
                     @input="commit_dropdown6"></multiselect>
      </div>
      <div class="option year">
        <label>{{ labels.dropdown5 }}:</label>
        <multiselect
          :value="selected.dropdown5"
          :options="options.dropdown5"
          :multiple="false"
          :taggable="true"
          :allow-empty="false"
          :showLabels="false"
          @tag="addTag"
          @input="commit_dropdown5"
        ></multiselect>
      </div>
    </div>
    <!-- Button -->
    <div class="row buttonContainer">
      <!-- <div class="flex xs12"> -->
      <va-button class="mapButton" @click="create_terria_layer">MAP</va-button>
      <!-- </div> -->
    </div>
  </div>
</template>
<script>
import Multiselect from "vue-multiselect";

export default {
  components: {
    Multiselect
  },
  props: {
    data_select: Object
  },
  data() {
    return {
      options: {
        category: [],
        subcategory: [],
        metric: [],
        dropdown1: [],
        dropdown2: [],
        dropdown3: [],
        dropdown4: [],
        dropdown5: [],
        dropdown6: []
      },
      labels: {
        category: "",
        subcategory: "",
        metric: "",
        dropdown1: "",
        dropdown2: "",
        dropdown3: "",
        dropdown4: "",
        dropdown5: "",
        dropdown6: ""
      },
      selected: {
        category: [],
        subcategory: [],
        metric: [],
        dropdown1: [],
        dropdown2: [],
        dropdown3: [],
        dropdown4: [],
        dropdown5: [],
        dropdown6: []
      }
    };
  },
  watch: {
    data_select: {
      handler(new_value, old_value) {
        //console.log('new data select :' + JSON.stringify(new_value))
		    //console.log('new data select :' + JSON.stringify(new_value.level_one_selected.subcategory))
        if (new_value) {
          this.selected = {
            category: new_value.level_one_selected
              ? new_value.level_one_selected.category
              : [],
            subcategory: new_value.level_one_selected
              ? new_value.level_one_selected.subcategory
              : [],
            metric: new_value.level_one_selected
              ? new_value.level_one_selected.metric
              : [],
            dropdown1: new_value.level_two_selected
              ? new_value.level_two_selected.dropdown1
              : [],
            dropdown2: new_value.level_two_selected
              ? new_value.level_two_selected.dropdown2
              : [],
            dropdown3: new_value.level_two_selected
              ? new_value.level_two_selected.dropdown3
              : [],
            dropdown4: new_value.level_two_selected
              ? new_value.level_two_selected.dropdown4
              : [],
            dropdown5: new_value.level_two_selected
              ? new_value.level_two_selected.dropdown5
              : [],
            dropdown6: new_value.level_two_selected
              ? new_value.level_two_selected.dropdown6
              : []
          };
		  // this part will asign label name for the drop down
          this.labels = {
            category: new_value.level_one_selected
              ? new_value.level_one_labels.category
              : "",
            subcategory: new_value.level_one_selected
              ? new_value.level_one_labels.subcategory
              : "",
            metric: new_value.level_one_selected
              ? new_value.level_one_labels.metric
              : "",
            dropdown1: new_value.level_two_selected
              ? new_value.level_two_labels.dropdown1
              : "",
            dropdown2: new_value.level_two_selected
              ? new_value.level_two_labels.dropdown2
              : "",
            dropdown3: new_value.level_two_selected
              ? new_value.level_two_labels.dropdown3
              : "",
            dropdown4: new_value.level_two_selected
              ? new_value.level_two_labels.dropdown4
              : "",
            dropdown5: new_value.level_two_selected
              ? "End Year"
              : "",
            dropdown6: new_value.level_two_selected
              ? "Start Year"
              : ""
          };
			// this part will asign all options (values) for the drop down
          this.options = {
            category: new_value.level_one_options
              ? this.get_default_options("category", this.selected, new_value)
              : [],
            subcategory: new_value.level_one_options
              ? this.get_default_options(
                  "subcategory",
                  this.selected,
                  new_value
                )
              : [],
            metric: new_value.level_one_options
              ? this.get_default_options("metric", this.selected, new_value)
              : [],
            dropdown1: new_value.level_two_options
              ? this.get_default_options("dropdown1", this.selected, new_value)
              : [],
            dropdown2: new_value.level_two_options
              ? this.get_default_options("dropdown2", this.selected, new_value)
              : [],
            dropdown3: new_value.level_two_options
              ? this.get_default_options("dropdown3", this.selected, new_value)
              : [],
            dropdown4: new_value.level_two_options
              ? this.get_default_options("dropdown4", this.selected, new_value)
              : [],
            dropdown5: new_value.level_two_options
              ? this.get_default_options("dropdown5", this.selected, new_value)
              : [],
            dropdown6: new_value.level_two_options
              ? this.get_default_options("dropdown6", this.selected, new_value)
              : []
          };
        } else {
          this.selected = {
            category: [],
            subcategory: [],
            metric: [],
            dropdown1: [],
            dropdown2: [],
            dropdown3: [],
            dropdown4: [],
            dropdown5: [],
            dropdown6: []
          };
          this.labels = {
            category: "",
            subcategory: "",
            metric: "",
            dropdown1: "",
            dropdown2: "",
            dropdown3: "",
            dropdown4: "",
            dropdown5: "",
            dropdown6: ""
          };
          this.options = {
            category: [],
            subcategory: [],
            metric: [],
            dropdown1: [],
            dropdown2: [],
            dropdown3: [],
            dropdown4: [],
            dropdown5: [],
            dropdown6: []
          };
        }
      },
      deep: true
    }
  },

  methods: {
    addTag(newTag) {
      const tag = {
        name: newTag,
        code: newTag.substring(0, 2) + Math.floor(Math.random() * 10000000)
      };
      this.options.push(tag);
      this.value.push(tag);
    },

    // for getting all options for each field when a field is changed
    get_default_options(key, selected, data_select) {
      //Returns default options

      //Ensure valid key
      if (
        (data_select.level_one_options === null) |
        (data_select.level_one_options === undefined)
      ) {
        return [];
      }
      if (
        (data_select.level_two_options === null) |
        (data_select.level_two_options === undefined)
      ) {
        return [];
      }

      //Check case
      var output = "";
      if (key === "category") {
        output = Object.keys(data_select.level_one_options).sort();
      } else if (key === "subcategory") {
        output = Object.keys(
          data_select.level_one_options[selected["category"][0]]
        ).sort();
      } else if (key === "metric") {
        output = Object.assign(
          [],
          data_select.level_one_options[selected["category"][0]][
            selected["subcategory"][0]
          ]
        ).sort();
      } else if (key === "dropdown1") {
        output = Object.keys(data_select.level_two_options).sort();
      } else if (key === "dropdown2") {
        output = Object.keys(
          data_select.level_two_options[selected["dropdown1"][0]]
        ).sort();
      } else if (key === "dropdown3") {
        output = Object.keys(
          data_select.level_two_options[selected["dropdown1"][0]][
            selected["dropdown2"][0]
          ]
        ).sort();
      } else if (key === "dropdown4") {
        output = Object.keys(
          data_select.level_two_options[selected["dropdown1"][0]][
            selected["dropdown2"][0]
          ][selected["dropdown3"][0]]
        ).sort();
      } else if (key === "dropdown5") {
        output = Object.assign(
          [],
          data_select.level_two_options[selected["dropdown1"][0]][
            selected["dropdown2"][0]
          ][selected["dropdown3"][0]][selected["dropdown4"][0]]
        ).sort();
		  }else if (key === "dropdown6") {
		    output = Object.assign(
		      [],
		      data_select.level_two_options[selected["dropdown1"][0]][
		        selected["dropdown2"][0]
		      ][selected["dropdown3"][0]][selected["dropdown4"][0]]
		    ).sort();
      }

      return output;
    },

    /*--------------This commit for setting selected values when any dropdown field is changed---------------------------------------*/
    //Level one commits
    emit_level_one_change(new_data, field) {
      /* Emit changes of filters to level one component */

      var params = {
        type: this.data_select.type,
        split: this.data_select.split
      };
      //console.log('emit_level_one_change()', params, new_data )
      this.$emit("update_level_one_selections", params, new_data);
    },
    commit_category(new_value) {
      /* Commits change to category and alters default of subcategory and metric */
      //Take original
      var new_data = JSON.parse(JSON.stringify(this.selected));

      //console.log("commit_category")
      //console.log(new_data)
      //console.log(this.data_select)

      //Change
      new_data["category"] = _.isArray(new_value) ? new_value : [new_value];
      new_data["subcategory"] = [
        this.get_default_options("subcategory", new_data, this.data_select)[0]
      ];
      new_data["metric"] = [
        this.get_default_options("metric", new_data, this.data_select)[0]
      ];

      //Commit data
      this.emit_level_one_change(new_data, "category");
    },
    commit_subcategory(new_value) {
      /* Commits change to subcategory and alters default of metric */

      //Take original
      var new_data = JSON.parse(JSON.stringify(this.selected));

      //Change
      new_data["subcategory"] = _.isArray(new_value) ? new_value : [new_value];
      new_data["metric"] = [
        this.get_default_options("metric", new_data, this.data_select)[0]
      ];

      //Commit data
      this.emit_level_one_change(new_data, "subcategory");
    },
    commit_metric(new_value) {
      /* Commits change to metric */
      //Take original
      var new_data = JSON.parse(JSON.stringify(this.selected));

      //Change
      new_data["metric"] = _.isArray(new_value) ? new_value : [new_value];

      this.emit_level_one_change(new_data, "metric");
    },

    /*--------------------------------------------------------------------*/
    //Level two commits
    emit_level_two_change(new_data, field) {
      /* Emit changes of filters to level two component */

      var params = {
        type: this.data_select.type,
        split: this.data_select.split
      };

      //console.log('emit_level_two_change()', params, new_data )
      this.$emit("update_level_two_selections", params, new_data);
    },
    commit_dropdown1(new_value) {
      /* Commits change to dropdown1 */

      //Take original
      var new_data = JSON.parse(JSON.stringify(this.selected));

      //Change
      new_data["dropdown1"] = _.isArray(new_value) ? new_value : [new_value];
      new_data["dropdown2"] = this.get_default_options(
        "dropdown2",
        new_data,
        this.data_select
      ).includes(new_data["dropdown2"][0])
        ? new_data["dropdown2"]
        : [
            this.get_default_options("dropdown2", new_data, this.data_select)[0]
          ];

      //console.log("drop2 after change1")
      //console.log(new_data["dropdown2"])

      new_data["dropdown3"] = this.get_default_options(
        "dropdown3",
        new_data,
        this.data_select
      ).includes(new_data["dropdown3"][0])
        ? new_data["dropdown3"]
        : [
            this.get_default_options("dropdown3", new_data, this.data_select)[0]
          ];
      new_data["dropdown4"] = this.get_default_options(
        "dropdown4",
        new_data,
        this.data_select
      ).includes(new_data["dropdown4"][0])
        ? new_data["dropdown4"]
        : [
            this.get_default_options("dropdown4", new_data, this.data_select)[0]
          ];
      new_data["dropdown5"] = this.get_default_options(
        "dropdown5",
        new_data,
        this.data_select
      ).includes(new_data["dropdown5"][0])
        ? new_data["dropdown5"]
        : [
            this.get_default_options("dropdown5", new_data, this.data_select)[0]
          ];

      this.emit_level_two_change(new_data, "dropdown1");
    },
    commit_dropdown2(new_value) {
      /* Commits change to dropdown2 */

      //Take original
      var new_data = JSON.parse(JSON.stringify(this.selected));

      //Change
      new_data["dropdown2"] = _.isArray(new_value) ? new_value : [new_value];
      new_data["dropdown3"] = this.get_default_options(
        "dropdown3",
        new_data,
        this.data_select
      ).includes(new_data["dropdown3"][0])
        ? new_data["dropdown3"]
        : [
            this.get_default_options("dropdown3", new_data, this.data_select)[0]
          ];
      new_data["dropdown4"] = this.get_default_options(
        "dropdown4",
        new_data,
        this.data_select
      ).includes(new_data["dropdown4"][0])
        ? new_data["dropdown4"]
        : [
            this.get_default_options("dropdown4", new_data, this.data_select)[0]
          ];
      new_data["dropdown5"] = this.get_default_options(
        "dropdown5",
        new_data,
        this.data_select
      ).includes(new_data["dropdown5"][0])
        ? new_data["dropdown5"]
        : [
            this.get_default_options("dropdown5", new_data, this.data_select)[0]
          ];

      this.emit_level_two_change(new_data, "dropdown2");
    },
    commit_dropdown3(new_value) {
      /* Commits change to dropdown3 */

      //Take original
      var new_data = JSON.parse(JSON.stringify(this.selected));

      //Change
      new_data["dropdown3"] = _.isArray(new_value) ? new_value : [new_value];
      new_data["dropdown4"] = this.get_default_options(
        "dropdown4",
        new_data,
        this.data_select
      ).includes(new_data["dropdown4"][0])
        ? new_data["dropdown4"]
        : [
            this.get_default_options("dropdown4", new_data, this.data_select)[0]
          ];
      new_data["dropdown5"] = this.get_default_options(
        "dropdown5",
        new_data,
        this.data_select
      ).includes(new_data["dropdown5"][0])
        ? new_data["dropdown5"]
        : [
            this.get_default_options("dropdown5", new_data, this.data_select)[0]
          ];

      this.emit_level_two_change(new_data, "dropdown3");
    },
    commit_dropdown4(new_value) {
      /* Commits change to dropdown4 */

      //Take original
      var new_data = JSON.parse(JSON.stringify(this.selected));

      //Change
      new_data["dropdown4"] = _.isArray(new_value) ? new_value : [new_value];
      new_data["dropdown5"] = this.get_default_options(
        "dropdown5",
        new_data,
        this.data_select
      ).includes(new_data["dropdown5"][0])
        ? new_data["dropdown5"]
        : [
            this.get_default_options("dropdown5", new_data, this.data_select)[0]
          ];

      this.emit_level_two_change(new_data, "dropdown4");
    },
    commit_dropdown5(new_value) {
      /* Commits change to dropdown5 */

      //Take original
      var new_data = JSON.parse(JSON.stringify(this.selected));

	    //console.log("newdata for dropdown5")
      //console.log(new_data)
      //Change
      new_data["dropdown5"] = _.isArray(new_value) ? new_value : [new_value];

      this.emit_level_two_change(new_data, "dropdown5");
    },
	  commit_dropdown6(new_value) {
        /* Commits change to dropdown5 */

        //Take original
        var new_data = JSON.parse(JSON.stringify(this.selected));
        //console.log("newdata for dropdown6")
        //console.log(new_data)
        //Change
        new_data["dropdown6"] = _.isArray(new_value) ? new_value : [new_value];

        this.emit_level_two_change(new_data, "dropdown6");
     },

    /*--------------------------------------------------------------------*/
    //Create terria layer
    create_terria_layer() {
      /* Emit selected options to create terria layer */

      var params = {
        type: this.data_select.type,
        split: this.data_select.split
      };

      console.log("create_terria_layer()", this.selected);
      this.$emit("create_terria_layer", params, this.selected);
    }
  }
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}

.option {
  padding: 5px;
  width: 235px;
  max-width: 100%;

  &.state {
    width: 120px;
  }

  &.region {
    width: 120px;
  }

  &.gender {
    width: 115px;
  }

  &.thematic {
    width: 145px;
  }

  &.year {
    width: 115px;
  }

  &.subcategory {
    width: 260px;
  }
}

.buttonContainer {
  margin-top: 5rem !important;
  margin-bottom: 1rem !important;
  display: flex;
  justify-content: center;

  & > button {
    width: 300px;
  }
}
</style>

