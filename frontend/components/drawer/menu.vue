<template>
  <q-drawer
      side="right"
      v-model="drawerRight"
      bordered
      :width="200"
      :breakpoint="500"
  >
    <q-btn flat @click="drawerRight = !drawerRight" round dense icon="arrow_back" size="20px" />
    <q-list>
      <template v-for="(menuItem, index) in menuList" :key="index">
        <q-item clickable v-ripple>
          <q-item-section>
            <nuxt-link
                :to="menuItem.link"
                class="tw-text-black hover:tw-text-[#ef3025] tw-cursor-pointer tw-transition-all"
            >
              {{menuItem.label}}
            </nuxt-link>
          </q-item-section>
        </q-item>
      </template>
    </q-list>
  </q-drawer>
</template>

<script setup lang="ts">
const props = defineProps({
  drawerRight: {
    type: Boolean,
    default: () => false
  }
})
watch(() => props.drawerRight,() => {
  drawerRight.value = true
})
const drawerRight = ref(false);

const menuList = [
  {
    label: 'Чат',
    link: '/',
  },
  {
    label: 'База знаний',
    link: '/base',
  },
  {
    label: 'Профиль',
    link: '/profile',
  },
];
</script>

<style scoped>

</style>
