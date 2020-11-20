<template>
  <div class="container">
    <va-button class="alignright" small @click="createReport()">CREATE REPORT</va-button>
    <va-data-table
      class="reportTable"
      :fields="fields"
      :data="reports"
    >
      <template slot="actions" slot-scope="props">
        <va-button small @click="update(props.rowData)">
          UPDATE
        </va-button>
        <va-button small @click="remove(props.rowData)">
          DELETE
        </va-button>
      </template>
    </va-data-table>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
  name: "report-management",
  components:{
  },
  props: {
    
  },
  data() {
    return {
    };
  },
  computed:{
    ...mapState({
      reports: state => state.admin.adminReportList ? state.admin.adminReportList.reports : [],
      selectedEntity: state => state.user.selectedEntity
    }),
    fields () {
      return [
        {
          name: 'name',
          title: 'Display name',
          sortField: 'name',
          width: '15%',
        },
        {
          name: 'workspace_id',
          title: 'Workspace Id',
          sortField: 'workspace_id',
          width: '20%',
        }, 
        {
          name: 'report_id',
          title: 'Report Id',
          sortField: 'report_id',
          width: '20%',
        },
        {
          name: 'permission__name',
          title: 'Permission',
          sortField: 'permission_id',
          width: '15%',
        },
        {
          name: 'category__name',
          title: 'Category',
          sortField: 'category_id',
          width: '15%',
        },
        {
          name: '__slot:actions',
          dataClass: 'text-right',
        }
      ]
    },
  },
  methods:{
    ...mapActions({
      getAdminReportList: 'admin/getAdminReportList',
    }),
    update(report){
      console.log('update report: ' + JSON.stringify(report))
      this.$emit("openEditReportModal", {report:report, operation:'Edit'});
    },
    remove(report){
      this.$modal.show("dialog", {
        title: "Alert!",
        text: "Are you sure to delete " + report.name + " ?",
        buttons: [
          {
            title: "Yes, Delete",
            handler: () => {
              // user is now sure to delete
              var param = {
                id: report.id,
                name: report.name,
                workspaceId: report.workspace_id,
                reportId: report.report_id,
                entityId: this.selectedEntity ? this.selectedEntity.id : 0,
                permissionId: report.permission_id,
                categoryId: report.category_id,
                isActive: 0
              };
              this.$emit("removeReport", param);
              this.$modal.hide("dialog");
            }
          },
          {
            title: "Close",
            default: true
          }
        ]
      });
    },
    createReport(){
      this.$emit("openEditReportModal", {operation:'New'});
      console.log('create report')
    }
  },
  mounted(){
    if(this.selectedEntity){
      this.getAdminReportList({entityId: this.selectedEntity.id})
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  padding: 0.75rem;
  padding-top: 1rem;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-end;

  & .reportTable {
    width: 100%;
  }
}

.alignright {
  float: right;
}

</style>