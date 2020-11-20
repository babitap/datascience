<template>
  <aside
    class="app-sidebar"
    :class="computedClass"
    :style="computedStyle"
  >
    <ul class="app-sidebar__menu">
      <template v-for="(item, key) in items">
        <app-sidebar-link-group
          :key="key"
          :minimized="minimized"
          :icon="item.meta && item.meta.iconClass"
          v-if="item.children"
          :title="item.displayName"
          :children="item.children"
          :active-by-default="hasActiveByDefault(item)"
        >
          <app-sidebar-link
            v-for="(subMenuItem, key) in item.children"
            :key="key"
            :to="{ name: subMenuItem.name , params: subMenuItem.params }"
            :title="subMenuItem.displayName"
          />
        </app-sidebar-link-group>
        <app-sidebar-link
          v-else
          :key="key"
          :minimized="minimized"
          :active-by-default="item.name === $route.name"
          :icon="item.meta && item.meta.iconClass"
          :to="{ name: item.name }"
          :title="item.displayName"
        />
      </template>
    </ul>
  </aside>
</template>

<script>
import { educationMenuItems, defaultMenuItems, downloadMenuItems } from '@/app/shared/menu-items'
import AppSidebarLink from './components/app-sidebar-link'
import AppSidebarLinkGroup from './components/app-sidebar-link-group'
import { ColorThemeMixin } from '@/services/vuestic-ui'
import { mapState, mapActions } from "vuex";
//import VaIconMenu from '@/iconset/VaIconMenu'

export default {
  name: 'app-sidebar',
  inject: ['contextConfig'],
  components: {
    AppSidebarLink,
    AppSidebarLinkGroup,
  },
  mixins: [ColorThemeMixin],
  props: {
    minimized: {
      type: Boolean,
      required: true,
    },
    color: {
      type: String,
      default: 'secondary',
    },
  },
  data () {
    return {
      items: defaultMenuItems.routes,
    }
  },
  computed: {
      ...mapState({
      selectedEntity: state => state.user.selectedEntity,
      entityLookUpList: state => state.user.entityLookUpList,
      availableReports: state => state.report.availableReports

    }),
    computedClass () {
      return {
        'app-sidebar--minimized': this.minimized,
      }
    },
    computedStyle () {
      return {
        backgroundColor: this.contextConfig.invertedColor ? this.$themes.dark2 : this.colorComputed,
      }
    },
  },
  watch: {
      selectedEntity(newValue){
          if(newValue) {
            this.items = this.getDefaultMenu(newValue.industry_name)

            // dummy code for westpac
            if ( ["key research", "altra motion"].includes(this.selectedEntity.entity_name.toLowerCase())) {
              console.log("vo day ko")
              var i;
              for (i = 0; i < this.items.length; i++) {
                if (this.items[i].name === "dashboard" && this.items[i].displayName === "Dashboard") {
                  this.items[i].displayName = "Home";
                  break;
                }
              };
            } else {
              console.log(this.selectedEntity.entity_name.toLowerCase())
              var i;
              for (i = 0; i < this.items.length; i++) {
                if (this.items[i].name === "dashboard" && this.items[i].displayName === "Home") {
                  this.items[i].displayName = "Dashboard";
                  break;
                }
              };
            }


            this.getReportList(newValue.id)


          }
      },
      availableReports(newValue){
          this.convertToMenuItem()
      }
  },
  methods: {
      ...mapActions({
            getReportList: "report/getReportList",
        }),
    hasActiveByDefault (item) {
      return item.children.some(child => child.name === this.$route.name)
    },
    convertToMenuItem(){
        const categories = Object.keys(this.availableReports);
        let reports = []
        categories.forEach(c => {
            let cate = {name: 'report', displayName: `${c} Report`, meta: {iconClass: 'vuestic-iconset vuestic-iconset-files'}}
            cate.children = []
            this.availableReports[c].forEach(r => {
                let report = {name: 'report', displayName: `${r.name}`, params: {codename: `${r.codename}`}, meta: {iconClass: 'vuestic-iconset vuestic-iconset-files'}}
                cate.children.push(report)
            })
            reports.push(cate)
        })
        this.items = [...this.getDefaultMenu(this.selectedEntity.industry_name),
                      ...reports,
                      ...this.getSpecialMenu(this.selectedEntity.industry_name, this.selectedEntity.industry_id)]
    }
    ,
    getDefaultMenu(industryName){
        let menu = defaultMenuItems.routes

        if(industryName){
            switch (industryName.toLowerCase()) {
                case 'education':
                {
                  menu = [...menu, ...educationMenuItems.routes];
                  break;
                }
            }
        }
        return menu
    }
    ,
    getSpecialMenu(industryName, industryId){
        let menu = []

        if(industryName){
            switch (industryName.toLowerCase()) {
                case 'education':
                {
                    switch( industryId ){
                      case 48004:  // display the download page for 'The Cathedral School of St Anne and St James'
                      {
                        menu = [...menu,
                         ...downloadMenuItems.routes
                        ];
                        break;
                      }
                      default:
                      {
                        menu = [...menu];
                        break;
                      }
                    }
                }
            }
        }
        return menu
    }
  }
}

</script>

<style lang="scss">
.app-sidebar {
  overflow: auto;
  display: flex;
  max-height: 100%;
  flex: 0 0 16rem;

  @include media-breakpoint-down(sm) {
    flex: 0 0 100%;
  }

  &--minimized {
    flex: 0 0 3.25rem;
  }

  &__menu {
    margin-bottom: 0;
    padding-top: 2.5625rem;
    padding-bottom: 2.5rem;
    list-style: none;
    padding-left: 0;
    width: 100%;
  }
}
</style>
