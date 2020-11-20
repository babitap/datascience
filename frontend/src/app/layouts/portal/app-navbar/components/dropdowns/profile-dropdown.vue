<template>
  <div class="profile-dropdown">
    <div class="profile-dropdown__content pl-4 pr-4 pt-2 pb-2">
      <a v-if="hasPermission() === true" @click="admin" class="profile-dropdown__item pt-1 pb-1 mt-2 mb-2">Admin</a>
      <a @click="signout" class="profile-dropdown__item pt-1 pb-1 mt-2 mb-2">Sign Out</a>
      <!-- <a @click="go_to_graphiql">GraphiQL</a> -->
    </div>
  </div>
</template>

<script>
import { permissionService } from '@/app/shared/services/permission-service';
import { authService } from "@/app/shared/services/auth-service";
import { mapActions } from "vuex";
import { config } from "@/app/config";
import store from "@/app/app-state";

export default {
  name: "profile-section",
  props: {
    options: {
      type: Array,
      default: () => [
        {
          name: "Logout",
          handler: "signout"
        }
      ]
    },
  },
  computed: {
    graphql_url: function() {
      const baseurl = config.api.baseUrl + "/graphql?access_token=";
      const access_token = store.getters["user/accessToken"];
      return baseurl + access_token;
    }
  },
  methods: {
    ...mapActions("user", ["logout"]),
    signout() {
      this.logout();
      authService.logout();
      this.$router.push({ name: "home" });
      this.$emit('closeMe')
    },
    admin() {
      this.$router.push({ name: "admin" }).catch(err => {});
      this.$emit('closeMe')
    },
    go_to_graphiql() {
      window.open(this.graphql_url, "_blank");
      this.$emit('closeMe')
    },
    hasPermission(){
        return permissionService.hasPermission('user_management');
    }
  }
};
</script>

<style lang="scss">
.profile-dropdown {
  cursor: pointer;
  position: absolute;
  top: 4rem;
  right: -1rem;

  &__anchor {
    color: $vue-green;
  }

  .va-dropdown-popper__anchor {
    display: flex;
    justify-content: flex-end;
  }

  &__content {
    background-color: $dropdown-background;
    box-shadow: $gray-box-shadow;
    border-radius: 0.5rem;
    width: 8rem;
  }

  &__item {
    display: block;
    color: $vue-darkest-blue;

    &:hover,
    &:active {
      color: #d43d27 !important;
    }
  }

  .va-dropdown__anchor {
    display: inline-block;
  }
}
</style>
