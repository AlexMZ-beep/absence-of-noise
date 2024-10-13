<template>
  <q-dialog v-model="open">
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6">Добавление документа</div>
      </q-card-section>
      <q-form
        @submit.prevent="responseCreate"
        class="q-gutter-md"
      >
        <q-card-section class="q-pt-none tw-flex tw-flex-col tw-gap-y-5">
          <q-input outlined dense v-model="name" autofocus label="Название документа" @keyup.enter="open = false" />
          <q-file
            v-model="files"
            label="Выберите документ"
            outlined
            dense
            accept=".pdf"
          >
            <template v-slot:prepend>
              <q-icon name="attach_file" />
            </template>
          </q-file>
          <q-select
            dense
            outlined
            v-model="branch"
            :options="branches"
            label="Предприятие"
          />
        </q-card-section>

        <q-card-actions align="right" class="text-primary tw-flex tw-gap-x-5">
          <q-btn no-caps flat label="Отмена" v-close-popup @click="reset" />
          <q-btn no-caps color="primary" label="Добавить" @click.prevent="responseCreate" />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-dialog>
</template>
<script setup>
import { createDocument } from '~/components/api-service/index.js';

const props = defineProps({
  openOut: {
    type: Boolean,
    default: false,
  },
});
const branches = [
  'ALL', 'A', 'B', 'C',
];
const $q = useQuasar();
const branch = ref('');
const files = ref(null);
const emits = defineEmits(['create']);
watch(() => props.openOut, () => {
  openDialog();
});
const open = ref(false);
const name = ref('');
const loadingDocument = ref(false);
async function responseCreate() {
  $q.loading.show();
  try {
    console.log($q);
    const id = await createDocument({ title: name.value, branch: branch.value, file: files.value });
    $q.notify({ color: 'positive', message: 'Документ успешно добавлен' });
    createConfirm(id);
  } catch (error) {
    console.error(error);
    $q.notify({ color: 'negative', message: error.value.data.detail || error.value.message });
  } finally {
    $q.loading.hide();
  }
}

function reset() {
  name.value = '';
  branch.value = '';
  files.value = null;
}
function createConfirm(id) {
  emits('create', { name: name.value, branch: branch.value, id });
  open.value = false;
}
function openDialog() {
  open.value = true;
}
</script>
