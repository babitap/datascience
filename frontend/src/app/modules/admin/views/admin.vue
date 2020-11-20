<template>
    <div class=admin>
        <modals-container />
        <div class="row row-equal outer-container" v-if="canSendSpecialUserInvite">
            <SuperUserManagement
                :openEditReportModal="openEditReportModal"
                :removeReport="removeReport"
            />
        </div>
        <div class="row row-equal outer-container">
            <div class="flex xs12 dropdown-container">
                <p class="flex xs12 group-title">Group Selection</p>
                    <div class="dropdown">
                        <SearchDropdown
                            :options="industryOptions"
                            v-on:selected="industrySelected"
                            name="industry"
                            label="Industry"
                            placeholder="Please select an industry">
                        </SearchDropdown>
                    </div>
                    <div class="dropdown">
                        <SearchDropdown
                            :options="this.filteredAdminEntityList"
                            v-on:selected="entitySelected"
                            name="school"
                            label="School"
                            placeholder="Please select an school">
                        </SearchDropdown>
                    </div>
                    <div class="dropdown">
                        <SearchDropdown
                            :options="this.adminGroupList"
                            v-on:selected="groupSelected"
                            name="group"
                            label="Group"
                            placeholder="Please select a group">
                        </SearchDropdown>
                    </div>
                </div>
            </div>
        <div class="row row-equal">
            <admin-usergroup 
                :userGroupData="adminUserGroupJsonData" 
                :selected_user_group="selected_user_group"
                @add_user_to_usergroup="add_user_to_usergroup"
                @remove_user_from_usergroup="remove_user_from_usergroup"
                @add_permission_to_usergroup="add_permission_to_usergroup"
                @remove_permission_from_usergroup="remove_permission_from_usergroup"
                @openEditGroupModal="openEditGroupModal"
                @remove_usergroup="remove_usergroup"
                @invite_user="inviteUser"
            ></admin-usergroup>
        </div>
    </div>
</template>

<script>
import AdminTree from '../components/admin-tree'
import AdminUsergroup from '../components/admin-usergroup'
import SearchDropdown from '../../shared/SearchDropdown'
import { mapState, mapActions } from "vuex";

import AddGroupModal from "../components/add-group-modal";
import InviteUserModal from "../components/invite-user-modal"
import SuperUserManagement from "../components/super-user-management"
import EditReportModal from "../components/edit-report-modal"

export default {
    name: "admin",
    components: {
        AdminTree,
        AdminUsergroup,
        SearchDropdown,
        AddGroupModal,
        InviteUserModal,
        SuperUserManagement,
        EditReportModal
    },
  data() {
    return {

        isOpen: false, 
        selected_user_group: {
            industry_value: 1,
            entity_value:   0,
            user_group_value: 0,
        }, 

        usergroupData: {
            profile: {
                value: 'group1',
                label: 'admin team',
            },
            selected_users:[
                {
                    value: 'fred.gu@findex.com.au',
                    label: 'fred.gu@findex.com.au',
                }
            ],
            available_users:[
                {
                    value: 'thao@findex.com.au',
                    label: 'thao@findex.com.au',
                },
                {
                    value: 'nathan.curiale@findex.com.au',
                    label: 'nathan.curiale@findex.com.au',
                },                
            ],
            selected_permissions:[
                {
                    value: 'permission1',
                    label: 'permission1',
                }, 
            ],
            available_permissions:[
                {
                    value: 'permission2',
                    label: 'permission2',
                },
                {
                    value: 'permission3',
                    label: 'permission3',
                },           
            ],
        },
        industryOptions:[{ id: 1, name: 'Education'}],
        filteredAdminEntityList: []
    }
  },
  computed: {
    ...mapState({
      adminTreeJsonData: state => state.admin.adminTreeJsonData,
      adminUserGroupJsonData: state => state.admin.adminUserGroupJsonData,
      adminEntityList: state => state.admin.adminEntityList ? state.admin.adminEntityList.entities : [],
      adminGroupList: state => state.admin.adminGroupList ? state.admin.adminGroupList.groups : [],
      selectedEntity: state => state.user.selectedEntity,
      canSendSpecialUserInvite: state => state.user.isSuperUser
    })
  },  
  created() {
      //start loading animation
    
    if( this.selectedEntity.id > 0 ){
        this.getAdminEntityList({'entityId': this.selectedEntity.id})
        this.filteredAdminEntityList = this.adminEntityList.filter(e => e.id === this.selectedEntity.id);
    }
    

  },
  watch:{
      adminTreeJsonData(new_value){
          if(new_value!==null && new_value!==undefined ){
            if( new_value['entities'].length>0 ){
                if( new_value['entities'][0]['user_groups'].length>0 ){
                    this.selected_user_group.industry_value = new_value['value']
                    this.selected_user_group.entity_value   = new_value['entities'][0]['value']
                    this.selected_user_group.user_group_value   = new_value['entities'][0]['user_groups'][0]['value']

                    var param={   'industry_id':  this.selected_user_group.industry_value,
                                'entity_id':    this.selected_user_group.entity_value,
                                'usergroup_id': this.selected_user_group.user_group_value
                        }
      
                    this.loadAdminUserGroupJsonData(param)
                }
            }
              
          }
      },
      selected_user_group(new_value){
          if( new_value!==null && new_value!==undefined && new_value.user_group_value!==null ){
              
              var param={   'industry_id':  new_value.industry_value,
                        'entity_id':new_value.entity_value,
                        'usergroup_id':new_value.user_group_value
                }
                this.loadAdminUserGroupJsonData(param)
          }
      },
      adminEntityList(new_value){
          if(new_value!==null && new_value!==undefined){
                this.filteredAdminEntityList = this.adminEntityList.filter(e => e.id === this.selectedEntity.id);
          }
      }
  },
  methods: 
  {
        ...mapActions({
            loadAdminTreeJsonData       : "admin/getAdminTreeJsonData",
            loadAdminUserGroupJsonData  : "admin/getAdminUserGroupJsonData",
            addUserToUserGroup          : "admin/addUserToUserGroup",
            removeUserToUserGroup       : "admin/removeUserToUserGroup",
            addPermissionToUserGroup    : "admin/addPermissionToUserGroup",
            removePermissionFromUserGroup: "admin/removePermissionFromUserGroup",
            getAdminEntityList          : "admin/getAdminEntityList",
            getAdminGroupList           : "admin/getAdminGroupList",
            clearAdminGroupList         : "admin/clearAdminGroupList",
            clearAdminUserGroupJsonData : "admin/clearAdminUserGroupJsonData",
            deleteUserGroup             : "admin/deleteUserGroup",
            deleteReport                : "admin/deleteReport",
            getReportList               : "report/getReportList"
        }), 
        update_user_group( input_param ){
            this.selected_user_group = input_param
        }, 
        add_user_to_usergroup( input_param ){
            var param = {}
            param['industry_id'] = this.selected_user_group.industry_value
            param['entity_id']   = this.selected_user_group.entity_value
            param['usergroup_id'] = input_param['usergroup_id']
            param['user_id'] = input_param['user_id']
            this.addUserToUserGroup( param )
        },
        remove_user_from_usergroup(input_param){
            var param = {}
            param['industry_id'] = this.selected_user_group.industry_value
            param['entity_id']   = this.selected_user_group.entity_value
            param['usergroup_id'] = input_param['usergroup_id']
            param['user_id'] = input_param['user_id']
            this.removeUserToUserGroup( param )
        },
        add_permission_to_usergroup(input_param){
            var param = {}
            param['industry_id'] = this.selected_user_group.industry_value
            param['entity_id']   = this.selected_user_group.entity_value
            param['usergroup_id'] = input_param['usergroup_id']
            param['permission_id'] = input_param['permission_id']
            this.addPermissionToUserGroup( param )            
        },
        remove_permission_from_usergroup(input_param){
            var param = {}
            param['industry_id'] = this.selected_user_group.industry_value
            param['entity_id']   = this.selected_user_group.entity_value
            param['usergroup_id'] = input_param['usergroup_id']
            param['permission_id'] = input_param['permission_id']
            this.removePermissionFromUserGroup( param )            
        }, 
        entitySelected(e){
            if(e && e.id){
                if (e.id !== this.selected_user_group.entity_value){
                    this.selected_user_group.entity_value = e.id;
                    this.getAdminGroupList({'entityId': this.selected_user_group.entity_value});
                    this.clearAdminGroupList();
                    this.clearAdminUserGroupJsonData();
                }
            }
        },
        groupSelected(e){
            if(e && e.id){
                if(e.id !== this.selected_user_group.user_group_value){
                    this.selected_user_group.user_group_value = e.id;
                    var param={   
                        'industry_id': 0,
                        'entity_id': this.selected_user_group.entity_value,
                        'usergroup_id':this.selected_user_group.user_group_value
                    }
                    this.loadAdminUserGroupJsonData(param)
                }
            }
        },
        industrySelected(e){
        },
        openEditGroupModal(modalInfo){
            let title = `${modalInfo.operation} User Group`;
            let groupId = 0;

            if(modalInfo.operation.toLowerCase() === 'edit'){
                title = `${title}: ${modalInfo.profile.label}`;
                groupId = this.selected_user_group.user_group_value;
            }
            
            this.$modal.show(AddGroupModal, 
                {
                    title: title,
                    industry_id: this.selected_user_group.industry_value, 
                    entity_id:   this.selected_user_group.entity_value, 
                    usergroup_id: groupId, 
                    usergroup_name: modalInfo.profile ? modalInfo.profile.label : '', 
                    usergroup_description: modalInfo.profile ? modalInfo.profile.description: '',
                }, 
                {
                    isAutoHeight: true, 
                    resizable: true,
                    adaptive: true,
                    draggable: true,
                    root: this.$root
                },
                        
            )
        },
        remove_usergroup(input_param){
            this.deleteUserGroup(input_param);
            this.clearAdminGroupList();
            this.clearAdminUserGroupJsonData();
        },
        inviteUser(){
            this.$modal.show(InviteUserModal, 
                {
                    title: 'Invite User',
                    options: this.adminEntityList,
                    selectedEntity: this.selected_user_group.entity_value
                }, 
                {
                    isAutoHeight: true, 
                    resizable: true,
                    adaptive: true,
                    draggable: true,
                    root: this.$root
                },
            )
        },
        openEditReportModal(modalInfo){
            let title = `${modalInfo.operation} Report`;

            if(modalInfo.operation.toLowerCase() === 'edit'){
                title = `${title}: ${modalInfo.report.name}`;
            }
            
            this.$modal.show(EditReportModal, 
                {
                    title: title,
                    propsId: modalInfo.report ? modalInfo.report.id : 0, 
                    propsName: modalInfo.report ? modalInfo.report.name : '', 
                    propsWorkspaceId: modalInfo.report ? modalInfo.report.workspace_id : '', 
                    propsReportId: modalInfo.report ? modalInfo.report.report_id : '', 
                    propsPermissionId: modalInfo.report ? modalInfo.report.permission_id: 0,
                    propsCategoryId: modalInfo.report ? modalInfo.report.category_id: 0
                }, 
                {
                    isAutoHeight: true, 
                    resizable: true,
                    adaptive: true,
                    draggable: true,
                    root: this.$root,
                    height: "auto"
                },
                        
            )
        },
        removeReport(param){
          this.deleteReport(param)
            .then(() => {
              if(this.selectedEntity){
                this.getReportList(this.selectedEntity.id)
              }
            })
        }
  }
}
</script>
<style scoped>
.dropdown-container {
  display: flex;
  flex-wrap: wrap;
  border: none;
  border-radius: 0.375rem;
  background: white;
}

.dropdown {
  margin: 5px;
}

.outer-container {
  margin-left: 0 !important;
  margin-right: 0 !important;
}

.row.row-equal.outer-container + .row.row-equal.outer-container {
  margin-top: 15px;
}

.group-title {
  float: left;
  font-weight: 600;
  padding: 0 !important;
}
</style>

