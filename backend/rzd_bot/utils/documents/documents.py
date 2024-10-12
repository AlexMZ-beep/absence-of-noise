import os
import re
import tempfile
from typing import List, Dict
from uuid import uuid4

from langchain_core.documents import Document
from pypdf import PdfReader

from rzd_bot.utils.chains import get_vectorstore


def delete_document(doc_id: str) -> bool:
    """
    Удаление всех строк с данным `id` из базы ChromaDB.

    :param doc_id: Идентификатор документа для удаления.
    :return: True, если удаление прошло успешно, False иначе.
    """
    store = get_vectorstore()

    where_clause = {"act_id": doc_id}
    store._collection.delete(where=where_clause)
    return True


def get_documents() -> List[Dict[str, str]]:
    """
    Получение списка уникальных документов (id и title).

    :return: Список документов с уникальными `id` и `title`.
    """
    store = get_vectorstore()
    all_entries = store.get(
        where={},
        include=["metadatas"],
        limit=None
    )
    metadatas = all_entries.get('metadatas', [])
    unique_docs = {}

    for meta in metadatas:
        doc_id = meta.get('act_id')
        title = meta.get('act_name')
        if doc_id is not None and title is not None:
            unique_key = (doc_id, title)
            unique_docs[unique_key] = {"id": doc_id, "title": title, "branch": meta.get('branch')}

    documents = list(unique_docs.values())
    return documents


def extract_sections(pdf_path: str) -> List[Dict[str, str]]:
    """
    Извлечение секций из PDF-файла.

    :param pdf_path: Путь к PDF-файлу.
    :return: Список секций с содержимым и метаданными.
    """
    reader = PdfReader(pdf_path)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    # Разделяем текст на верхнеуровневые разделы
    top_level_sections = re.split(r'\n(?=Раздел \d+\.)', text)

    # Список для хранения всех секций
    all_sections = []

    # Обрабатываем каждый верхнеуровневый раздел
    for top_section in top_level_sections:
        # Ищем название верхнеуровневого раздела
        top_match = re.match(r'(Раздел \d+\..+?)(?=\n\d+\.\d+\.|\Z)', top_section, re.DOTALL)
        if top_match:
            top_section_name = top_match.group(1).strip()

            # Разделяем текст на подсекции
            subsections = re.split(r'\n(?=\d+\.\d+\.)', top_section)

            # Обрабатываем каждую подсекцию
            for subsection in subsections[1:]:  # Пропускаем первый элемент
                match = re.match(r'(\d+\.\d+\.)', subsection)
                if match:
                    section_number = match.group(1)
                    section_content = subsection[len(section_number):].strip()
                    all_sections.append({
                        'content': section_content,
                        'top_level_section': top_section_name,
                        'section_number': section_number,
                    })

    return all_sections


def upload_document(document: bytes, title: str, branch: str) -> Dict[str, str]:
    """
    Загрузка документа в ChromaDB.

    :param document: Содержимое PDF файла в байтах.
    :param branch: Филиал к которому относиться документ
    :param title: Название документа.
    :return: Словарь с `id` и `title` загруженного документа.
    """
    store = get_vectorstore()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(document)
        tmp_file_path = tmp_file.name

    sections = extract_sections(tmp_file_path)
    os.remove(tmp_file_path)
    if not sections:
        raise ValueError("PDF не содержит валидных секций.")

    act_id = str(uuid4())
    docs = [
            Document(
                page_content=section['top_level_section'] + '\n' + section['content'],
                metadata={
                    "content": section['content'],
                    "act_id": act_id,
                    "top_level_section": section['top_level_section'],
                    "section_number": section['section_number'],
                    "act_name": title,
                    "branch": branch,
                }
            )
            for section in sections
        ]

    store.add_documents(documents=docs)
    return {
        "id": docs[0].metadata['act_id'],  # Все секции имеют одинаковый `act_id`
        "title": title
    }
