<template>
    <q-card>
      <q-card-section>
        <div class="text-h6 title hover:tw-text-primary tw-transition-all tw-cursor-pointer">{{ name }}</div>
        <div class="text-subtitle2">by John Doe</div>
      </q-card-section>
      <q-card-section class="q-pt-none tw-flex tw-items-center tw-justify-between">
        <p>
          Количество документов: {{ numberDocs }}
        </p>
        <q-icon class="tw-cursor-pointer" name="settings" size="24px">
          <q-menu auto-close>
            <q-list style="min-width: 100px">
              <q-item clickable v-close-popup @click="edit">
                <q-item-section>Редактировать</q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup @click="remove">
                <q-item-section>Удалить</q-item-section>
              </q-item>

            </q-list>
          </q-menu>
        </q-icon>
      </q-card-section>
    </q-card>
</template>

<script setup>
const props = defineProps({
  id: {
    type: Number,
    default: () => 0
  },
  name: {
    type: String,
    default: () => 'Default name'
  },
  numberDocs: {
    type: Number,
    default: () => 0
  }
})
const emits = defineEmits(['edit', 'remove'])
function edit() {
  emits('edit', props.id)
}
function remove() {
  emits("remove", props.id)
}
</script>

<style scoped>
.title{
  font-family: RussianRail;
}
</style>
