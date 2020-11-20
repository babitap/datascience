<template>
  <div class="schoolList">
    <modals-container />
    <va-card :title="'List of entities'">
      <template slot="actions" v-if="canCreateEntity">
        <va-button small @click="createEntity()">CREATE ENTITY</va-button>
      </template>
      <div class="row align--center">
        <div class="flex xs12 md6">
          <va-input
            :value="term"
            :placeholder="'Search by name'"
            @input="search"
            removable
          >
            <va-icon name="fa fa-search" slot="prepend" />
          </va-input>
        </div>

        <div class="flex xs12 md3 offset--md3">
          <va-select
            v-model="perPage"
            :label="'Per page'"
            :options="perPageOptions"
            noClear
          />
        </div>
      </div>

      <va-data-table
        :fields="fields"
        :data="filteredData"
        :per-page="parseInt(perPage)"
      >
        <template slot="actions" slot-scope="props">
          <va-button small @click="selectEntity(props.rowData)">
            SELECT
          </va-button>
        </template>
      </va-data-table>
    </va-card>
  </div>
</template>

<script>
import { debounce } from 'lodash'
import { mapState, mapActions } from 'vuex'
import CreateEntityModal from "../components/create-entity-modal"

export default {
  name: 'app-entity-list',
  components: {
    CreateEntityModal
  },
  data () {
    return {
      term: null,
      perPage: '10',
      perPageOptions: ['4', '6', '10', '20'],
    }
  },
  async created () {
    // if(  this.schools.length == 0 ){
    //   await this.getSchools();
    // }
  },
  computed: {
    ...mapState({
      entities: state => state.user.entityLookUpList,
      canCreateEntity: state => state.user.isSuperUser
    }),
    fields () {
      return [
        {
          name: 'industry_id',
          title: 'Id',
          sortField: 'industry_id',
          width: '15%',
        },
        {
          name: 'entity_name',
          title: 'Name',
          sortField: 'entity_name',
          width: '50%',
        }, 
        {
          name: 'industry_name',
          title: 'Type',
          sortField: 'industry_name',
          width: '30%',
        },
        {
          name: '__slot:actions',
          dataClass: 'text-right',
        }
      ]
    },
    filteredData () {
      if (!this.term || this.term.length < 1) {
        return this.entities
      }

      return this.entities.filter(item => {
        return item.entity_name.toLowerCase().includes(this.term.toLowerCase())
      })
    },
  },
  methods: {
    ...mapActions({
      getSchools: 'schools/getSchools',
      switchEntity: 'user/updateSelectedEntity',
    }),
    search: debounce(function (term) {
      this.term = term
    }, 400),
    selectEntity (entity) {
      this.switchEntity(entity)
      this.$router.push({ name: 'dashboard' })
    },
    createEntity(){
      this.$modal.show(CreateEntityModal, 
                {
                    title: 'Create Entity',
                }, 
                {
                    isAutoHeight: true, 
                    resizable: false,
                    adaptive: true,
                    draggable: true,
                    root: this.$root
                },
            )
    }
  },
}
</script>

<style lang="scss">
label.va-select {
  background: green !important;
}
</style>
