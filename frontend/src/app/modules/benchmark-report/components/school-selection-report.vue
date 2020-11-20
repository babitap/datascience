<template>
  <div class="container filter">
    <div class="selectionContainer">
      <!-- select School Sector  -->
      <div class="option schoolSector">
        <label>School Sector:</label>
        <multiselect :value="selected_values.schoolSectorDefaultOption"
                     tag-placeholder="Add this as new tag"
                     placeholder="Search or add a tag"
                     label="label"
                     track-by="value"
                     :options="school_sector_options"
                     :multiple="true"
                     :taggable="true"
                     :showLabels="false"
                     @tag="addTag"
                     @input="commit_school_sector" />
      </div>
      <!-- select School Type  -->
      <div class="option schoolType">
        <label>School Type:</label>
        <multiselect :value="selected_values.schoolTypeDefaultOption"
                     tag-placeholder="Add this as new tag"
                     placeholder="Search or add a tag"
                     label="label"
                     track-by="value"
                     :options="school_type_options"
                     :multiple="true"
                     :taggable="true"
                     :showLabels="false"
                     @tag="addTag"
                     @input="commit_school_type" />
      </div>

      <!-- select States  -->
      <div class="option state">
        <label>State:</label>
        <multiselect :value="selected_values.stateDefaultOption"
                     tag-placeholder="Add this as new tag"
                     placeholder="Search or add a tag"
                     label="label"
                     track-by="value"
                     :options="school_state_options"
                     :multiple="true"
                     :taggable="true"
                     :showLabels="false"
                     @tag="addTag"
                     @input="commit_school_state" />
      </div>
      <!-- select Geolocation  -->
      <!-- @input is short hand of v-on:input which handles events users change the option -->
      <div class="option geolocation">
        <label>Geolocation:</label>
        <multiselect :value="selected_values.geolocationDefaultOption"
                     tag-placeholder="Add this as new tag"
                     placeholder="Search or add a tag"
                     label="label"
                     track-by="value"
                     :options="school_geolocation_options"
                     :multiple="true"
                     :taggable="true"
                     :showLabels="false"
                     @tag="addTag"
                     @input="commit_school_geolocation" />
      </div>
      <!-- select Year  -->
      <div class="option year">
        <label>Year:</label>
        <multiselect :value="selected_values.YearValue"
                     tag-placeholder="Add this as new tag"
                     placeholder="Search or add a tag"
                     label="label"
                     track-by="value"
                     :options="school_year_options"
                     :multiple="false"
                     :taggable="true"
                     :showLabels="false"
                     @tag="addTag"
                     @input="commit_school_year" />
      </div>
      <!-- select Genders  -->
      <div class="option genders">
        <label>Gender:</label>
        <multiselect :value="selected_values.schoolGenderDefaultOption"
                     tag-placeholder="Add this as new tag"
                     placeholder="Search or add a tag"
                     label="label"
                     track-by="value"
                     :options="school_gender_options"
                     :multiple="false"
                     :taggable="true"
                     :showLabels="false"
                     @tag="addTag"
                     @input="commit_school_gender" />
      </div>

      <!-- Enrolment Range Inputs  -->
      <div class="option enrolmentRange">
        <label>Enrolment Range:</label>
        <div class="container input-container">
          <input type="number" :value="selected_values.enrolmentRangeStartValue" @change="commit_enrolment_range_start_value">
          <span> - </span>
          <input type="number" :value="selected_values.enrolmentRangeEndValue" @change="commit_enrolment_range_end_value">
        </div>
      </div>
      <!-- Distance inputs  -->
      <div class="option distance">
        <label>Distance within (km):</label>
        <div class="container  input-container">
          <input class="distanceInput" type="number" :value="selected_values.distanceKmValue" @change="commit_distance_km">
        </div>
      </div>
    </div>
     <!-- Button -->
    <div class="buttonContainer">
      <va-button @click="updateBenchmark">BENCHMARK</va-button>
    </div>
  </div>
</template>
<script>
import Multiselect from "vue-multiselect";
import { AvailableColorThemes, ColorThemes } from '../../../layouts/portal/services/themes-config'
  export default {
  name:'SchoolSelectionReport',
  components: {
    Multiselect
    },
  // data get from parent
  props: {
    filter_options: Object,
    filtered_values: Object
    },
  // data by default (initial value) when loading the component
  data() {
    return {
      school_sector_options: [],
      school_type_options: [],
      school_gender_options: [],
      school_geolocation_options: [],
      school_state_options: [],
      school_year_options: [], 

      selected_values: {
        schoolSectorDefaultOption: [],
        schoolTypeDefaultOption: [],
        schoolGenderDefaultOption: [],
        YearValue: [],
        geolocationDefaultOption: [],
        stateDefaultOption: [],
        enrolmentRangeStartValue: null,
        enrolmentRangeEndValue: null,
        distanceKmValue: null
      }
    };
  },
  watch: {
    filter_options: function (new_value) {
      //console.log("new filter_optoins from prop");
      //console.log(new_value);
      if (new_value) {
        this.school_sector_options = new_value["schoolSectorOptions"];
        this.school_type_options = new_value["schoolTypeOptions"];
        this.school_gender_options = new_value["schoolGenderOptions"];
        this.school_year_options = new_value["calendarYearOptions"];
        this.school_state_options = new_value["stateOptions"];
        this.school_geolocation_options = new_value["geolocationOptions"];
      } else {
        this.school_sector_options = [];
        this.school_type_options = [];
        this.school_gender_options = [];
        this.school_year_options = [];
        this.school_state_options = [];
        this.school_geolocation_options = [];
      }
    },
    filtered_values: function(new_value) {
      if (new_value) {
        this.selected_values.schoolSectorDefaultOption =
          new_value["schoolSectorDefaultOption"];

        this.selected_values.schoolTypeDefaultOption =
          new_value["schoolTypeDefaultOption"];

        this.selected_values.schoolGenderDefaultOption =
          new_value["schoolGenderDefaultOption"];

        this.selected_values.YearValue =
          new_value["YearValue"];

        this.selected_values.stateDefaultOption =
          new_value["stateDefaultOption"];

        this.selected_values.geolocationDefaultOption =
          new_value["geolocationDefaultOption"];

        this.selected_values.enrolmentRangeStartValue =
          new_value["enrolmentRangeStartValue"];

        this.selected_values.enrolmentRangeEndValue =
          new_value["enrolmentRangeEndValue"];

        this.selected_values.distanceKmValue = new_value["distanceKmValue"];
      }
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

    commit_any_filter(new_value, field) {


      var new_data = JSON.parse(JSON.stringify(this.selected_values));
      new_data[field] = new_value;


      this.$emit("update_filter_value", new_data);
    },

    commit_school_sector(new_value) {
      this.commit_any_filter(new_value, "schoolSectorDefaultOption");
    },
    commit_school_type(new_value) {
      this.commit_any_filter(new_value, "schoolTypeDefaultOption");
    },
    commit_school_gender(new_value) {

      this.commit_any_filter(new_value, "schoolGenderDefaultOption");
    },
    commit_school_year(new_value) {

      this.commit_any_filter(new_value, "YearValue");
    },
    commit_school_state(new_value) {

      this.commit_any_filter(new_value, "stateDefaultOption");
    },
    commit_school_geolocation(new_value) {
      this.commit_any_filter(new_value, "geolocationDefaultOption");
    },
    commit_enrolment_range_start_value(event) {
      this.commit_any_filter(event.target.value, "enrolmentRangeStartValue");
    },
    commit_enrolment_range_end_value(event) {
      this.commit_any_filter(event.target.value, "enrolmentRangeEndValue");
    },
    commit_distance_km(event) {
      this.commit_any_filter(event.target.value, "distanceKmValue");
    },
    //emit to return this event to parent and let parent solve it using refresh_comparable_schools_data function
    updateBenchmark(){
      this.$emit("refresh_benchmark_data");
    }
  }
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss" scoped>
.selectionContainer {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  padding: 10px;
}

.filter {
  border: none;
  border-radius: 0.375rem;
  padding-right: 20px;
  background: white;
}

.input-container {
  padding: 0;
  justify-content: space-between;
  align-items: center;

  & input {
    height: 43px;
    min-height: 40px;
    width: 40%;
    max-width: 100%;
    border-radius: 5px;
    border: 1px solid #e8e8e8;
    color: #34495e;
    text-align: center;

    &.distanceInput {
      width: 100%;
    }
  }
}

.second-input {
  margin-left: 10px;
  margin-right: -1rem;
}

.option {
  padding: 5px;
  width: 190px;
  max-width: 100%;
}

.buttonContainer {
  padding: 10px;
  display: flex;
  justify-content: center;
}

</style>

<style lang="scss">
.option .multiselect__tag {
  background: #0eacbd;

  & .multiselect__tag-icon::after {
    color: white;
  }
}
</style>

