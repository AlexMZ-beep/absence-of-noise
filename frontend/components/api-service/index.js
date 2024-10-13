export async function getDocuments() {
  const { data, error } = await useBaseFetch('/documents', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // return [{
  //     id: 0,
  //     title: 'Коллективный договор',
  //     branch: 'Главное предприятие',
  // },
  //     {
  //         id: 1,
  //         title: 'Уголовные дела заколюченных',
  //         branch: 'ТрансСиб',
  //     }
  // ];
  return data.value;
}

export async function createDocument({ title, branch, file }) {
  const formData = new FormData();
  formData.append('title', title);
  formData.append('branch', branch);
  formData.append('file', file, file.name);

  const { data, error } = await useBaseFetch('/docs', {
    method: 'POST',

    body: formData,
  });
  console.log(error);
  if (error) {
    throw error;
  }
  return data;
}
