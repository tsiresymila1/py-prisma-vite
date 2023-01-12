<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
  sockets: {
    connect: function () {
      console.log('Socket to notification channel connected')
    },
  },
});
</script>
<template>
  <router-view></router-view>
</template>
