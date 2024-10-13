<template>
  <q-layout view="hHh LpR fFf" class="h-full shadow-2 rounded-borders">
    <q-header elevated class="tw-bg-white">
      <q-toolbar>
        <q-toolbar-title class="tw-text-black tw-flex tw-items-center tw-h-[72px]">
          <q-img height="72px" width="121px" src="/rzd_icon.png" class="tw-mr-5" />
          <div class="laptop:tw-block tw-hidden">
            Поддержка сотрудников компании
          </div>
        </q-toolbar-title>
        <div class="tw-gap-x-20 tw-hidden tw-items-center tw-text-base tw-mr-5 tablet:tw-flex">
          <div
            v-for="menuItem in menuList"
            @click="menuItem.func()"
            class="tw-text-black hover:tw-text-[#ef3025] tw-cursor-pointer tw-transition-all"
          >
            {{ menuItem.label }}
          </div>
        </div>
        <div class="tw-hidden">
          <q-btn color="dark" flat @click="drawerMobileMenu = !drawerMobileMenu" round dense icon="menu" />
        </div>
      </q-toolbar>
    </q-header>
    <q-drawer
      v-model="layout"
      show-if-above
      :width="400"
      :breakpoint="500"
      bordered
      :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-3'"
    >
      <q-scroll-area class="fit">
        <div class="tw-text-center tw-my-5 tw-text-2xl">
          Панель администратора <br>(для демонстрации)
        </div>
        <q-list>
          <template v-for="(document, index) in documents" :key="index">
            <q-item clickable v-ripple @click="selectDocument(document)">
              <q-item-section avatar>
                <q-checkbox v-model="document.checked" val="orange" color="primary" size="md" />
              </q-item-section>
              <q-item-section class="tw-flex tw-flex-col tw-gap-y-2">
                <div>
                  Документ: {{ document.title }}
                </div>
                <div>
                  Предприятие: {{ document.branch }}
                </div>
              </q-item-section>
            </q-item>
            <q-separator />
          </template>
          <q-item clickable @click="isAddNewDocument = !isAddNewDocument">
            <q-item-section>
              + Добавить документ
            </q-item-section>
          </q-item>
        </q-list>
        <q-separator class="tw-my-10" />
        <q-list v-if="!!chatHistory">
          <div class="tw-text-center tw-my-5 tw-text-2xl">
            История чатов
          </div>
          <template v-for="item in chatHistory" :key="item.id">
            <q-item @click="chooseChat(item)" :active="item.id === idChat" clickable v-ripple>

              <q-item-section class="tw-flex tw-flex-col tw-gap-y-2">
                {{ item.chat.find((el) => el.question).question }}
                <div>
                  от {{ item.profile?.name || 'Аноним' }}
                </div>
              </q-item-section>
            </q-item>
            <q-separator />
          </template>
        </q-list>
      </q-scroll-area>
    </q-drawer>
    <drawer-menu :drawer-right="drawerMobileMenu" />
    <q-page-container>
      <q-page padding>
        <slot />
      </q-page>
    </q-page-container>
    <q-drawer
      v-model="layout"
      show-if-above
      :width="400"
      :breakpoint="500"
      side="right"
    >
      <q-scroll-area class="fit">
        <div class="tw-my-5 tw-text-2xl">
          Профили пользователей
        </div>
        <div class="tw-mr-10">
          <template v-for="(profile, index) in profiles" :key="index">
            <q-card
              @click="chooseProfile(profile)"
              class="hover:tw-shadow-xl tw-cursor-pointer tw-mb-5 tw-p-5 tw-border-2"
              clickable
              :class="{ 'tw-border-[#ef3025]': profile.name === choosedProfile.name }"
              v-ripple>
              <q-item-section avatar>
                <q-icon name="account_circle" size="48px" />
              </q-item-section>
              <q-item-section class="tw-flex tw-flex-col tw-gap-y-2">
                <div class="tw-font-bold">
                  {{ profile.name }}
                </div>
                <div>
                  Предприятие: {{ profile.enterprise }}
                </div>
                <div>
                  Стаж: {{ profile.experience }}
                </div>
                <div>
                  Личные характеристики: {{ profile.characteristic }}
                </div>
              </q-item-section>
            </q-card>
          </template>
          <q-item-section>
            <q-btn color="primary" @click="isAddNewUser = !isAddNewUser">
              + Добавить пользователя
            </q-btn>
          </q-item-section>
        </div>
      </q-scroll-area>
    </q-drawer>
    <modal-new-base :open-out="isAddNewDocument" @create="createDocument" />
    <modal-new-profile :open-out="isAddNewUser" @create="createProfile" />
  </q-layout>
</template>
<script setup>
import { getDocuments } from '~/components/api-service/index.js';

const isAddNewUser = ref(false);
const isAddNewDocument = ref(false);

const layout = ref(true);
// onMounted(() => {
//   if (window.screenMovie < 600) {
//     layout.value = false;
//   }
// });
const drawerMobileMenu = ref(false);
const choosedProfile = useState('choosedProfile', () => ({
  name: '',
  characteristic: '',
  experience: '',
  enterprise: '',
}));
const chatHistory = useState('chatHistory', () => []);
const chatTree = useState('chatTree');
const documents = useState('documents', () => []);

documents.value = await getDocuments();
documents.value = documents.value.map((el) => {
  if (el.branch === 'ALL') {
    return {
      ...el,
      checked: true,
    };
  }
  return {
    ...el,
    checked: false,
  };
});
const menuList = [
  {
    label: 'Новый чат',
    func: newChat,
  },

];
const profiles = ref([
  {
    name: 'Александр Михайлович Алексеев',
    characteristic: 'Инвалид 2 группы',
    experience: '15 лет',
    enterprise: 'ALL',
  },
  {
    name: 'Петр Оспович Иванов',
    characteristic: 'Молодой специалист',
    experience: '1 года',
    enterprise: 'C',
  },
  {
    name: 'Елизавета Максимовна Полковникова',
    characteristic: 'Многодетная мать',
    experience: '3 года',
    enterprise: 'ALL',
  },
]);

function createProfile({ name, characteristic, experience, enterprise }) {
  profiles.value.push({
    name,
    characteristic,
    experience,
    enterprise,
  });
}
const idChat = useState('idChat', () => null);

function saveChat(oldChatTree) {
  if (idChat.value) {
    chatHistory.value.find((el) => el.id === idChat.value).chat = oldChatTree;
  } else {
    chatHistory.value.push({
      id: Date.now(),
      chat: oldChatTree,
      profile: choosedProfile.value,
    });
  }
}

function newChat() {
  if (chatTree.value.length > 1) {
    saveChat(chatTree.value);
  }
  chatTree.value = [];
  idChat.value = null;
  choosedProfile.value = {
    name: '',
    characteristic: '',
    experience: '',
    enterprise: '',

  };
}

function createDocument({ id, name, branch }) {
  documents.value.push({
    title: name,
    id,
    branch,
    checked: false,
  });
}
const isDefaultBranch = useState('isDefaultBranch', () => true);

function selectDocument(item) {
  item.checked = !item.checked;
  isDefaultBranch.value = false;
}

function chooseChat(itemHistory) {
  if (chatTree.value.length > 1) {
    saveChat(chatTree.value);
  }
  chatTree.value = itemHistory.chat;
  idChat.value = itemHistory.id;
  choosedProfile.value = { ...itemHistory.profile };
  checkDocument(itemHistory.profile);
}
function chooseProfile(profile) {
  isDefaultBranch.value = true;
  if (chatTree.value.length > 1) {
    saveChat(chatTree.value);
  }
  chatTree.value = [];
  idChat.value = null;
  choosedProfile.value = { ...profile };
  checkDocument(profile);
}
function checkDocument(profile) {
  console.log(profile);
  documents.value.forEach((el) => {
    if (el.branch === profile.enterprise) {
      el.checked = true;
    } else if (el.branch !== 'ALL') {
      el.checked = false;
    }
  });
}
</script>
<style scoped>
.q-toolbar {
  padding: 0 12px 0 0;
}
</style>
