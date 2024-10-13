<template>
  <q-card
    class="tw-bg-primary"
  >
    <q-card-section>
      <div class="tw-text-xl tw-truncate tw-text-sky-50">Выберите тему обращения</div>
    </q-card-section>
    <q-card-section>
      <q-select
        rounded
        class="tw-text-primary tw-bg-secondary tw-mb-3"
        filled
        option-label="title"
        option-value="id"
        v-model="choosedTicket"
        :options="tickets"
        label="Тема обращения"
        dense
      />
      <q-input
        label="Краткое описание обращения"
        filled
        dense
        class="tw-text-primary tw-bg-secondary tw-mb-3"
      />
      <q-input
        v-model="message"
        filled
        label="Текст обращения"
        class="tw-text-primary tw-bg-secondary"
        type="textarea"
      />
    </q-card-section>
    <q-card-section>
      <q-btn rounded no-caps color="secondary" text-color="primary">Отправить обращение</q-btn>

    </q-card-section>
  </q-card>
</template>

<script setup>
const message = useState('message');
const choosedTicket = useState('choosedTicket');
const tickets = [{
  id: 1,
  title: 'Помощь по фунуционалу',
}];
</script>
