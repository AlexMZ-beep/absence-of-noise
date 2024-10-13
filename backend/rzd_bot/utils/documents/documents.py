import os
import re
import tempfile
from typing import List, Dict
from uuid import uuid4

import redis
from langchain_community.document_loaders import PDFMinerLoader
from langchain_core.documents import Document

from rzd_bot.config import get_settings
from rzd_bot.utils.chains import get_vectorstore

settings = get_settings()


def get_redis_client() -> redis.Redis:
    return redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def delete_document(doc_id: str) -> bool:
    """
    Удаление всех строк с данным `id` из базы ChromaDB.

    :param doc_id: Идентификатор документа для удаления.
    :return: True, если удаление прошло успешно, False иначе.
    """
    store = get_vectorstore()

    where_clause = {"act_id": doc_id}
    store._collection.delete(where=where_clause)

    redis_client = get_redis_client()
    redis_key = f"document:{doc_id}"
    redis_client.delete(redis_key)

    return True


def get_documents() -> List[Dict[str, str]]:
    """
    Получение списка уникальных документов (id и title).

    :return: Список документов с уникальными `id` и `title`.
    """
    documents = []

    redis_client = get_redis_client()
    pattern = "document:*"

    for key in redis_client.scan_iter(match=pattern, count=100):
        doc = redis_client.json().get(key)
        if doc:
            documents.append(doc)

    return documents


def extract_sections(pdf_path: str) -> List[Dict[str, str]]:
    """
    Извлечение секций из PDF-файла.

    :param pdf_path: Путь к PDF-файлу.
    :return: Список секций с содержимым и метаданными.
    """
    loader = PDFMinerLoader(pdf_path)
    docs = loader.load()
    text = docs[0].page_content

    top_level_sections = re.split(r'\n(?=Раздел \d+\.)', text)

    all_sections = []

    for top_section in top_level_sections:

        top_match = re.match(r'(Раздел \d+\..+?)(?=\n\d+\.\d+\.|\Z)', top_section, re.DOTALL)
        if top_match:
            top_section_name = top_match.group(1).strip()

            subsections = re.split(r'\n(?=\d+\.\d+\.)', top_section)

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
    try:
        sections = extract_sections(tmp_file_path)
    finally:
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

    document_info = {
        "id": act_id,
        "title": title,
        "branch": branch,
    }

    redis_client = get_redis_client()

    redis_key = f"document:{act_id}"

    redis_client.json().set(redis_key, '$', document_info)

    return document_info
