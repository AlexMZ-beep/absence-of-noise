<template>
  <div class="tw-my-6 tw-mx-4" style="width: 350px">
    <div class="tw-flex tw-items-center tw-justify-between tw-mb-3">
      <h2 class="tw-text-xl ">История обращений</h2>
      <q-btn flat @click="drawerHistory = !drawerHistory" round dense icon="menu" />
    </div>
    <q-btn class="tw-mb-10" no-caps color="secondary" outline @click="newChat">Новый чат</q-btn>

    <q-card
      v-for="chat in chats"
      :key="chat.data.data.content"
      dark
      class="tw-mb-6 hover:tw-bg-primary cursor-pointer"
      :class="{ 'tw-bg-primary': chat.conversation_id === chatID }"
      @click="toChat(chat.conversation_id)"
    >
      <q-card-section>
        <div class="tw-text-sm tw-truncate">{{chat.data.data.content}}</div>
      </q-card-section>
    </q-card>
  </div>
</template>
<script setup>
import { getChats } from '~/shared/api/index.js';

const drawerHistory = useState('drawerHistory');

const chats = useState('chats', () => []);
const chatID = useState('chatID');

function toChat(conversation_id) {
  console.log(conversation_id);
  chatID.value = conversation_id;
}
function newChat() {
  chatID.value = null;
}
chats.value = await getChats();

console.log(chats);
</script>
