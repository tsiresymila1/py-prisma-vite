<template>
  <button
    @click="redirect"
    :="$attrs"
    :class="to === $route.fullPath ? 'bg-[var(--app-second-color)' : ''"
    class="flex my-1 text-gray-300 pl-8 py-4 hover:text-gray-300 cursor-pointer hover:bg-[var(--app-second-color)] mx-4 rounded-lg focus:bg-[var(--app-second-color)]"
  >
    <span class="mr-4">
      <slot name="icon"></slot>
    </span>
    <div class="font-bold text-[18px]">{{ $props.label }}</div>
  </button>
</template>
<script lang="ts" setup>
interface SidenavActionProps extends ButtonHTMLAttributes {
  label: string;
  to: string;
}
defineProps<SidenavActionProps>();
</script>
<script lang="ts">
import { ButtonHTMLAttributes, defineComponent } from "vue";

export default defineComponent({
  methods: {
    redirect: function () {
      this.$router.push(this.to);
    },
  },
  mounted() {
    console.log(
      "test",
      this.to,
      this.$route.fullPath,
      this.to === this.$route.fullPath
    );
  },
});
</script>
