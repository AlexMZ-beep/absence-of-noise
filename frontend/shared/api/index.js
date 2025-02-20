import { useBaseFetch } from '../../composables/useBaseFetch.js';

export async function getChat(conversation_id) {
  const { data, error } = await useBaseFetch(`/conversations/111/${conversation_id}`, {
    method: 'GET',
  });
  if (error.value) {
    return [{
      type: 'human',
      content: 'ХУЙ',
    }, {
      type: 'ai',
      content: 'Очень смешно годон, запускаю анигиляцию системы',
    }];
  }
  return data.value.data.map((msg) => ({
    type: msg.type,
    content: msg.data.content,
  }));
}
export async function getChats() {
  const { data, error } = await useBaseFetch('/conversations/111/', {
    method: 'GET',
  });

  if (error.value) {
    return [{
      conversation_id: 1112,
      data: {
        data: {
          content: 'Здравствуйте блаблаблаблаблаблаблабла блаблаблаблаблаблаблаблаблаблаблабла',
        },
      },
    }];
  }
  return data.value;
}
