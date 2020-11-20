<template>
  <div class="flex xs12">
    <!--
  <modals-container />
    -->
    <v-dialog
      @before-opened="dialogEvent('before-open')"
      @before-closed="dialogEvent('before-close')"
      @opened="dialogEvent('opened')"
      @closed="dialogEvent('closed')"
    />
      <div class="flexi container">
        <div class="flex xs12">
            <p class="group-title">Group Detail</p>
            <va-button
            class="alignright admin-usergroup__button"
            @click="addGroupOnClicked"
          >NEW</va-button>
        </div>
        <div class="flex xs12 flexi">
            <div v-if="usergroupDataJson.profile.value === 0" class="profile-div">
                <p class="profile-text">Please select school and group first</p>
            </div>
            <div v-if="usergroupDataJson.profile.value !== 0" class="profile-div">
                <label class="profile-label" for="groupName">Name</label>
                <p class="profile-text">{{usergroupDataJson.profile.label}}</p>
            </div>
            <div v-if="usergroupDataJson.profile.value !== 0" class="profile-div">
                <label class="profile-label" for="groupDescription">Description</label>
                <p class="profile-text">{{usergroupDataJson.profile.description}}</p>
            </div>
            <div class="edit-button">
                <va-button
                    v-if="usergroupDataJson.profile.value !== 0"
                    class="alignright admin-usergroup__button"
                    @click="click_remove_group( usergroupDataJson.profile.value, usergroupDataJson.profile.label )"
                >DELETE</va-button>
                <va-button
                    v-if="usergroupDataJson.profile.value !== 0"
                    class="alignright admin-usergroup__button"
                    @click="click_edit_group"
                >EDIT</va-button>
            </div>
        </div>
      </div>
      <div v-if="usergroupDataJson.profile.value !== 0" class="flexi container">
          <div class="flex xs12">
              <p class="group-title">User Management</p>
          </div>
          <div class="flex xs5">
          <va-card style="overflow-x: auto;">
            <!-- selected users -->
            <va-tree-root class="flex xs12">
              <va-tree-category isOpen label="Selected users" icon="ion ion-md-people">
                <va-tree-node
                  :highlighted="selected_user.value===selected.selected_user_value"
                  v-for="selected_user in usergroupDataJson.selected_users"
                  :label="selected_user.label"
                  :key="selected_user.value"
                  icon="ion ion-md-person"
                >
                  <a @click="click_selected_user(selected_user.value)">{{ selected_user.label }}</a>
                </va-tree-node>
              </va-tree-category>
            </va-tree-root>
          </va-card>
        </div>
        <div class="flex xs2 arrow-container">
          <va-button
              class="arrow-button admin-usergroup__button"
              v-if="selected.selected_user_value!==null"
              @click="click_user_transfer_button"
            >&#62;</va-button>
            <va-button
              class="arrow-button admin-usergroup__button"
              v-if="selected.available_user_value!==null"
              @click="click_user_transfer_button"
            >&#60;</va-button>
        </div>
        <div class="flex xs5">
          <va-card style="overflow-x: auto;">
            <!-- available users -->
            <va-tree-root class="flex xs12">
              <va-tree-category isOpen label="Available users" icon="ion ion-md-people">
                <va-tree-node
                  :highlighted="available_user.value===selected.available_user_value"
                  v-for="available_user in this.getAvailableUsers"
                  :label="available_user.label"
                  :key="available_user.value"
                  icon="ion ion-md-person"
                >
                  <a @click="click_available_user(available_user.value)">{{ available_user.label }}</a>
                </va-tree-node>
                <va-tree-node class="invite-user" icon="ion ion-md-person">
                  <a @click="click_add_user( )">+ User</a>
                </va-tree-node>
              </va-tree-category>
            </va-tree-root>
          </va-card>
        </div>
      </div>
      <div v-if="usergroupDataJson.profile.value !== 0" class="flexi container">
          <div class="flex xs12">
              <p class="group-title">Permission Management</p>
          </div>
          <div class="flex xs5">
          <va-card style="overflow-x: auto;">
            <!-- selected permissions -->
            <va-tree-root class="flex xs12">
              <va-tree-category isOpen label="Selected permissions" icon="ion ion-md-people">
                <va-tree-node
                  :highlighted="selected_permission.value===selected.selected_permission_value"
                  v-for="selected_permission in usergroupDataJson.selected_permissions"
                  :label="selected_permission.label"
                  :key="selected_permission.value"
                  icon="ion ion-md-key"
                >
                  <a
                    @click="click_selected_permission(selected_permission.value)"
                  >{{ selected_permission.label }}</a>
                </va-tree-node>
              </va-tree-category>
            </va-tree-root>
          </va-card>
        </div>
        <div class="flex xs2 arrow-container">
            <va-button
              class="arrow-button admin-usergroup__button"
              v-if="selected.selected_permission_value!==null"
              @click="click_permission_transfer_button"
            >&#62;</va-button>
            <va-button
              class="arrow-button admin-usergroup__button"
              v-if="selected.available_permission_value!==null"
              @click="click_permission_transfer_button"
            >&#60;</va-button>
        </div>
        <div class="flex xs5">
          <va-card style="overflow-x: auto;">
            <!-- available permissions -->
            <va-tree-root class="flex xs12">
              <va-tree-category isOpen label="Available permissions" icon="ion ion-md-people">
                <va-tree-node
                  :highlighted="available_permission.value===selected.available_permission_value"
                  v-for="available_permission in this.getAvailablePermissions"
                  :label="available_permission.label"
                  :key="available_permission.value"
                  icon="ion ion-md-key"
                >
                  <a
                    @click="click_available_permission(available_permission.value)"
                  >{{ available_permission.label }}</a>
                </va-tree-node>
              </va-tree-category>
            </va-tree-root>
          </va-card>
        </div>
      </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "admin-usergroup",
  components: {
  },
  props: {
    selected_user_group: Object,
    userGroupData: Object
  },
  data: function() {
    return {
      selected: {
        selected_user_value: null,
        available_user_value: null,
        selected_permission_value: null,
        available_permission_value: null
      },
      usergroupDataJson: {
        profile: {
          value: 0,
          label: "",
          description: ""
        },
        selected_users: [],
        available_users: [],
        selected_permissions: [],
        available_permissions: []
      }
    };
  },

  watch: {
    userGroupData(new_value) {
      if (new_value !== null) {
        this.usergroupDataJson = new_value;
      } else {
        this.usergroupDataJson = this.resetUserGroupData();
      }
    }
  },
  computed: {
    getAvailableUsers() {
      if (
        this.usergroupDataJson &&
        this.usergroupDataJson.available_users &&
        this.usergroupDataJson.selected_users
      ) {
        return this.usergroupDataJson.available_users.filter(
          el =>
            !this.usergroupDataJson.selected_users.some(
              su => su.value === el.value
            )
        );
      }
      return [];
    },
    getAvailablePermissions() {
      if (
        this.usergroupDataJson &&
        this.usergroupDataJson.available_permissions &&
        this.usergroupDataJson.selected_permissions
      ) {
        return this.usergroupDataJson.available_permissions.filter(
          el =>
            !this.usergroupDataJson.selected_permissions.some(
              su => su.value === el.value
            )
        );
      }
      return [];
    }
  },
  methods: {
    ...mapActions({
      loadAdminTreeJsonData: "admin/getAdminTreeJsonData",
      addNewUserGroup: "admin/addNewUserGroup",
      editUserGroup: "admin/editUserGroup",
      invitNewUser: "admin/invitNewUser",
      loadAdminUserGroupJsonData: "admin/getAdminUserGroupJsonData"
    }),
    click_selected_user: function(user_value) {
      this.selected.selected_user_value = user_value;
      this.selected.available_user_value = null;
    },
    click_available_user: function(user_value) {
      this.selected.selected_user_value = null;
      this.selected.available_user_value = user_value;
    },
    click_selected_permission: function(permission_value) {
      this.selected.selected_permission_value = permission_value;
      this.selected.available_permission_value = null;
    },
    click_available_permission: function(permission_value) {
      this.selected.selected_permission_value = null;
      this.selected.available_permission_value = permission_value;
    },
    click_user_transfer_button: function() {
      var param = {
        usergroup_id: this.usergroupDataJson.profile.value
      };
      if (
        this.selected.available_user_value !== null &&
        this.selected.selected_user_value == null
      ) {
        param["user_id"] = this.selected.available_user_value;
        this.$emit("add_user_to_usergroup", param);
      } else if (
        this.selected.available_user_value == null &&
        this.selected.selected_user_value !== null
      ) {
        param["user_id"] = this.selected.selected_user_value;
        this.$emit("remove_user_from_usergroup", param);
      }
    },
    click_permission_transfer_button: function() {
      var param = {
        usergroup_id: this.usergroupDataJson.profile.value
      };
      if (
        this.selected.available_permission_value !== null &&
        this.selected.selected_permission_value == null
      ) {
        param["permission_id"] = this.selected.available_permission_value;
        this.$emit("add_permission_to_usergroup", param);
      } else if (
        this.selected.available_permission_value == null &&
        this.selected.selected_permission_value !== null
      ) {
        param["permission_id"] = this.selected.selected_permission_value;
        this.$emit("remove_permission_from_usergroup", param);
      }
    },
    click_edit_group: function(
      usergoup_value,
      usergroup_label,
      usergroup_description
    ) {
      this.$emit("openEditGroupModal", {profile:this.usergroupDataJson.profile, operation:'Edit'});
    },
    click_remove_group: function(usergroup_value, usergroup_label) {
      this.$modal.show("dialog", {
        title: "Alert!",
        text: "Are you sure to delete " + usergroup_label + " ?",
        buttons: [
          {
            title: "Yes, Delete",
            handler: () => {
              // user is now sure to delete
              var param = {};
              (param["industry_id"] = this.selected_user_group.industry_value),
              (param["entity_id"] = this.selected_user_group.entity_value),
              (param["usergroup_id"] = this.selected_user_group.user_group_value),
              this.$emit("remove_usergroup", param);
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
    click_add_user: function() {
        this.$emit("invite_user");
      // invit a new user to join
      //this.invitNewUser(param)
    },
    dialogEvent(eventName) {
      console.log("Dialog event: " + eventName);
    },
    resetUserGroupData() {
      return {
        profile: {
          value: 0,
          label: "",
          description: ""
        },
        selected_users: [],
        available_users: [],
        selected_permissions: [],
        available_permissions: []
      };
    },
    addGroupOnClicked(){
        this.$emit("openEditGroupModal", {profile:null, operation:'New'});
    }
  }
};
</script>

<style lang="scss">
.admin-usergroup {
  &__button {
    width: 100px;
    margin: 0 0 0 1rem !important;
    font-weight: bold;
  }
}
</style>

<style scoped>
.flexi {
  display: flex;
  flex-wrap: wrap;
}

.container {
  border: none;
  border-radius: 0.375rem;
  background: white;
  margin-bottom: 0.75rem;
}

.group-title {
  float: left;
  font-weight: 600;
}

.alignright {
  float: right;
}

.profile-div {
  width: 33%;
  padding: 0.75rem;
}

.profile-div ~ .profile-div {
  width: 67%;
}

.profile-label {
  text-decoration: underline;
}

.profile-text {
  margin-top: 0.75rem;
}

.edit-button {
  margin-top: 0.75rem;
}

.arrow-container {
  text-align: center;
}

.arrow-button {
  display: inline-block;
}

.invite-user {
  cursor: pointer;
}
</style>