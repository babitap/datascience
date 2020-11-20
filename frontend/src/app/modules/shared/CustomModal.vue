<template>
  <div class="example-modal-content">
    <va-card style="overflow-x: auto;">
      <h1>This is a custom component</h1>
      <p>{{ text }}</p>
      <button class="btn" @click="closeByEvent">Close this using events</button>
    </va-card>
  </div>
</template>

<script>
export default {
  name: 'custom-modal',
  props: ['text'], 
  methods: {

        closeByEvent() {
          this.$emit('close');
        },
  }

}
</script>