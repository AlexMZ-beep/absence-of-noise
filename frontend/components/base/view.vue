<template>
  <div>
    <div class="tw-text-xl tw-mb-10 tw-flex tw-items-center tw-justify-between">
      <h1 class="tw-text-primary tw-text-2xl header-name">
        <span class="tw-bg-[#ef3025] tw-text-white tw-p-1">ДОКУМЕНТЫ</span> ДЛЯ ОТВЕТОВ АССИСТЕНТА
      </h1>
      <q-btn
      no-caps
      color="primary"
      @click="createDocumentsBase"
      >+ Создать базу документов</q-btn>
    </div>
    <base-card-list>
      <base-card
          v-for="item in documentBases"
          :key="item.id"
          :id="item.id"
          :name="item.name"
          :numberDocs="item.numberDocs"
          @edit="editDocumentBase"
          @remove="removeDocumentBase"
      />
    </base-card-list>
    <modal-new-base :open="isNewDialog" @create="createConfirmDocumentsBase"/>
  </div>
</template>
<script setup>
const documentBases = ref([
  {
    id: 1,
    name: 'Поддержка сотрудников РЖД',
    numberDocs: 10
  },
  {
    id: 2,
    name: 'Поддержка сотрудников РЖД',
    numberDocs: 10
  },
  {
    id: 3,
    name: 'Поддержка сотрудников РЖД',
    numberDocs: 10
  }, {
    id: 4,
    name: 'Поддержка сотрудников РЖД',
    numberDocs: 10
  },
  {
    id: 5,
    name: 'Поддержка сотрудников РЖД',
    numberDocs: 10
  },
  {
    id: 6,
    name: 'Поддержка сотрудников РЖД',
    numberDocs: 10
  }, {
    id: 7,
    name: 'Поддержка сотрудников РЖД',
    numberDocs: 10
  },
  {
    id: 8, name: 'Поддержка сотрудников РЖД',
    numberDocs: 10
  },
  {
    id: 9,
    name: 'Поддержка сотрудников РЖД',
    numberDocs: 10
  }, {
    id: 11,
    name: 'Поддержка сотрудников РЖД',
    numberDocs: 10
  },
  {
    id: 12,
    name: 'Поддержка сотрудников РЖД',
    numberDocs: 10
  },
  {
    id: 13,
    name: 'Поддержка сотрудников РЖД',
    numberDocs: 10
  }
])
const router = useRouter()
const isNewDialog = ref(false)
const isDeleteDialog = ref(false)
const removeDocumentBase = (id) => {
  documentBases.value = documentBases.value.filter((doc) => doc.id !== id)
}
const editDocumentBase = (id) => {
  router.push(`/base/${id}`)
}
const createDocumentsBase = () => {
  isNewDialog.value = !isNewDialog.value
}
const useNewDocumentBase = useState('newDocumentBase')

const createConfirmDocumentsBase = (name) => {
  useNewDocumentBase.value.name = name
  router.push('/base/create')
}
</script>
<style scoped>
.header-name{
  font-family: RussianRail;
}
</style>
