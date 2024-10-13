<template>
  <q-dialog v-model="open">
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6">Добавление документа</div>
      </q-card-section>
      <q-form
        @submit.prevent="createUser"
        class="q-gutter-md"
      >
        <q-card-section class="q-pt-none tw-flex tw-flex-col tw-gap-y-5">
          <q-input outlined dense v-model="name" autofocus label="ФИО" @keyup.enter="open = false" />
          <q-input outlined dense v-model="experience" autofocus label="Стаж" @keyup.enter="open = false" />
          <q-select
            dense
            outlined
            v-model="branch"
            :options="branches"
            label="Предприятие"
          />
          <q-input outlined dense v-model="characteristic" autofocus label="Личные характеристики" @keyup.enter="open = false" />

        </q-card-section>

        <q-card-actions align="right" class="text-primary tw-flex tw-gap-x-5">
          <q-btn no-caps flat label="Отмена" v-close-popup @click="reset" />
          <q-btn no-caps color="primary" label="Добавить" @click.prevent="createUser" v-close-popup />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-dialog>
</template>
<script setup>
const props = defineProps({
  openOut: {
    type: Boolean,
    default: false,
  },
});
const branches = [
  'ALL', 'A', 'B', 'C',
];
const branch = ref('');
const experience = ref('');
const characteristic = ref('');
const emits = defineEmits(['create']);
watch(() => props.openOut, () => {
  openDialog();
});
const open = ref(false);
const name = ref('');

function createUser() {
  emits('create', {
    name: name.value,
    enterprise: branch.value,
    id: Date.now(),
    characteristic: characteristic.value,
    experience: experience.value,
  });
}

function reset() {
  name.value = '';
}

function openDialog() {
  open.value = true;
}
</script>
