<template>
<div>
    <p class="display-7" style="color: #5f6e78;">{{path_string}}  </p>
    <br >
</div>
</template>

<script>
export default {
  data() {
    return {
      items: [], 
      path_string: null,
    }
  },

  watch: {
    '$route' () {
      const vm = this;

      vm.updateBreadcrumbs();
    }
  },

  mounted() {
    const vm = this;

    vm.updateBreadcrumbs();
  },

  methods: {
    updateBreadcrumbs() {
      const vm = this;
      vm.items = vm.$route.meta.breadcrumb;
      vm.path_string = null
      if(vm.items){
          for(var i=0; i<vm.items.length; i++){
            if( ! vm.path_string ){
                vm.path_string = vm.items[i].name
            }
            else{
                vm.path_string = vm.path_string + ' / ' + vm.items[i].name
            }
          }
      }
    }
  }
}
</script>