<template>
  <div class="dropdown" v-if="options">
       <form autocomplete="off">
           <label class="flex xs12 dropdown-label" for="confuseChrome">{{label}}</label>
    <!-- Dropdown Input -->
    <input
      class="dropdown-input flex xs12"
      @focus="showOptions()"
      @blur="exit()"
      @keyup="keyMonitor"
      v-model="searchFilter"
      :disabled="disabled"
      :placeholder="placeholder"
      autocomplete="chrome-off"
    />

    <!-- Dropdown Menu -->
    <div class="dropdown-content" v-show="optionsShown">
      <div
        class="dropdown-item"
        @mousedown="selectOption(option)"
        v-for="(option, index) in filteredOptions"
        :key="index"
      >{{ option.name || option.id || '-' }}</div>
    </div>
       </form>
  </div>
</template>

<script>
export default {
  name: "SearchDropdown",
  props: {
    name: {
      type: String,
      required: false,
      default: "dropdown",
      note: "Input name"
    },
    label: {
      type: String,
      required: false,
      default: "label",
      note: "Label for dropdown"
    },
    options: {
      type: Array,
      required: true,
      default: () => [],
      note: "Options of dropdown. An array of options with id and name"
    },
    placeholder: {
      type: String,
      required: false,
      default: "Please select an option",
      note: "Placeholder of dropdown"
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
      note: "Disable the dropdown"
    }
  },
  data() {
    return {
      selected: {},
      optionsShown: false,
      searchFilter: ""
    };
  },
  mounted() {
      this.prepopulate();
  },
  computed: {
    filteredOptions() {
      const filtered = [];
      const regOption = new RegExp(this.searchFilter, "ig");
      for (const option of this.options) {
        if (this.searchFilter.length < 1 || option.name.match(regOption)) {
          filtered.push(option);
        }
      }
      return filtered;
    }
  },
  methods: {
    selectOption(option) {
      this.selected = option;
      this.optionsShown = false;
      this.searchFilter = this.selected.name;
      this.$emit("selected", this.selected);
    },
    showOptions() {
      if (!this.disabled) {
        this.searchFilter = "";
        this.optionsShown = true;
      }
    },
    exit() {
      if (!this.selected.id) {
        this.selected = {};
        this.searchFilter = "";
      } else {
        this.searchFilter = this.selected.name;
      }
      this.$emit("selected", this.selected);
      this.optionsShown = false;
    },
    // Selecting when pressing Enter
    keyMonitor: function(event) {
      if (event.key === "Enter" && this.filteredOptions[0])
        this.selectOption(this.filteredOptions[0]);
    },
    prepopulate(){
        if(this.options.length == 1){
            this.selected = this.options[0];
            this.searchFilter = this.selected.name;
        }
        this.$emit("selected", this.selected);
    }
  },
  watch: {
    searchFilter() {
      if (this.filteredOptions.length === 0) {
        this.selected = {};
      }
      this.$emit("filter", this.searchFilter);
    },
    options: function(newVal, oldVal) {
        if(newVal){
            const optionLength = newVal.length;
            if(optionLength === 0){
                this.searchFilter = '';
            }
            else if(optionLength === 1){ //Logic to re-select
                this.selected = this.options[0];
                this.searchFilter = this.selected.name;
                this.$emit("selected", this.selected);
            }
            else if(optionLength - oldVal.length === 1 ) { //Logic for newly added item
                const additionItem = newVal.filter(el => !oldVal.some(oel => el.id === oel.id))
                if(additionItem.length === 1){
                    this.selected = additionItem[0];
                    this.searchFilter = this.selected.name;
                    this.$emit("selected", this.selected);
                }
            }
            else{
                if(this.selected.id){
                    const selectedItem = this.options.find(el => el.id === this.selected.id);
                this.searchFilter = selectedItem.name;
                }
            }
        }
    }
  }
};
</script>

<style lang="scss" scoped>
.dropdown {
  position: relative;
  display: block;
  margin: auto;

  .dropdown-input {
    background: #ffffff;
    cursor: pointer;
    border: 1px solid #e7ecf5;
    border-radius: 3px;
    color: #333333;
    display: block;
    font-size: 1em;
    padding: 6px;
    min-width: 250px;
    max-width: 250px;
    margin-top: 1rem;

    &:hover {
      background: #f8f8fa;
    }
  }

  .dropdown-content {
    position: absolute;
    background-color: #ffffff;
    min-width: 248px;
    max-width: 248px;
    max-height: 248px;
    border: 1px solid #e7ecf5;
    box-shadow: 0 -8px 34px 0 rgba(0, 0, 0, 0.05);
    overflow: auto;
    z-index: 1;

    .dropdown-item {
      font-size: 1em;
      line-height: 1em;
      padding: 8px;
      text-decoration: none;
      display: block;
      cursor: pointer;

      &:hover {
        background-color: #e7ecf5;
      }
    }
  }

  .dropdown:hover .dropdowncontent {
    display: block;
  }

  .dropdown-label {
    padding-left: 0.25rem;
  }
}
</style>