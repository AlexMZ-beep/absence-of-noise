<template>
  <q-dialog v-model="open">
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6 tw-font-bold">{{ question }}</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <p
          class="tw-p-1"
          v-html="text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')" />
      </q-card-section>
      <q-card-section>
        <div class="tw-text-lg tw-font-bold tw-mb-2">Источники информации</div>
        <div v-for="doc in docs" :key="doc.act_name" class="tw-flex tw-flex-col tw-gap-4 tw-mb-2">
          <div class="tw-text-base">
            Документ {{ doc.act_name }}
          </div>
          <div v-for="section in doc.sections" :key=" section.top_level_section">
            {{ section.top_level_section }}
            <q-expansion-item
              v-for="section_number in section.section_numbers"
              :key="section_number"
              :label="`Пункт ${section_number.section_number}`"
            >
              <q-card>
                <q-card-section>
                  {{section_number.content}}
                </q-card-section>
              </q-card>
            </q-expansion-item>
            <q-separator />
          </div>
        </div>
      </q-card-section>
      <q-card-actions align="right" class="text-primary tw-flex tw-gap-x-5">
        <q-btn no-caps flat label="Закрыть" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>
<script setup>
const props = defineProps({
  openOut: {
    type: Boolean,
    default: false,
  },
  docs: {
    type: Array,
    default: () => [],
  },
  text: {
    type: String,
    default: '',
  },
  question: {
    type: String,
    default: '',
  },
});

watch(() => props.openOut, () => {
  openDialog();
});
const open = ref(false);
function openDialog() {
  open.value = true;
}
</script>
