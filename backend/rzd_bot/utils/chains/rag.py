import os
from operator import itemgetter
from typing import List, Dict, Any

from openai import AsyncOpenAI

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStore
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable, RunnablePassthrough, RunnableLambda
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from rzd_bot.config.utils import get_settings
from rzd_bot.schemas import BranchEnum

COLLECTION_NAME = "rzd_base"
PERSIST_DIR = "./chroma_data"
MODEL_NAME = "Vikhrmodels/Vikhr-Nemo-12B-Instruct-R-21-09-24"
ID_KEY = "doc_id"
TOP_K = 15
MAX_SYMBOLS = 4000

ANSWER_SYSTEM_PROMPT = """\
Your task is to provide a clear, concise, and professional answer to \
the user's question only based on the provided information for the RZD platform. \
Give two answers to each question: one with a list of relevant document identifiers and the second \
with the answer to the question itself, using documents with these identifiers."""

ANSWER_HUMAN_PROMPT = """\
<attantion>
IMPORTANT: Your goal is to provide answers only within the scope of the RZD platform \
hosting platform and to provide accurate information to solve the user's problem. \
Use all relevant facts from the knowledge base. \
If there are no answers to the user's question in the found facts, say only "Я не знаю".
<attantion>
<input>
    <question>
        {question}
    </question>
    <user-profile>
        {user_profile}
    </user-profile>
</input>"""

SUMMARY_SYSTEM = """\
Reduce the length of your answer to the question by making it shorter, clearer, and more concise.

# Steps

1. Read the original answer carefully.
2. Identify the main points or ideas that need to be retained.
3. Paraphrase the answer by removing unnecessary information and simplifying the language to make it more concise.

# Output Format

Provide your answer in a short, clear text while preserving the main ideas of the original.

# Examples

**Original Answer:** "When we look at the diversity of nature, \
we can see a huge number of different colors of flowers, the size of which can vary, \
and fragrances that create a certain atmosphere. \
Since each flower has its own unique characteristics, \
it is difficult not to be amazed by their diversity."

**Paraphrased Answer:** "Nature is full of different flowers with unique fragrances and characteristics, \
each of which amazes with its variety.\""""

SUMMARY_HUMAN = """\
**Question:** {question}
**Original Answer:** {answer}
**Paraphrased Answer:**"""

settings = get_settings()


def get_embeddings_model() -> Embeddings:
    return HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large-instruct")


def get_vectorstore() -> VectorStore:
    embeddings_model = get_embeddings_model()
    return Chroma(
        embedding_function=embeddings_model,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIR
    )


def get_retriever() -> BaseRetriever:
    vectorstore = get_vectorstore()
    _retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
    return _retriever


def create_retriever_chain(_retriever: BaseRetriever) -> Runnable:
    async def ainvoke_retriever(_input):
        docs = await _retriever.vectorstore.asimilarity_search(
            _input['question'],
            filter=_input['filter'],
            k=TOP_K,
        )
        return docs

    def get_filter_param(_input: Dict[str, Any]):
        if branch := _input.get('branch', None):
            return {
                "$or": [
                    {
                        "branch": BranchEnum.ALL
                    },
                    {
                        "branch": branch,
                    }
                ]
            }

        elif docs_ids := _input.get('docs_ids', []):
            if len(docs_ids) == 1:
                return {"act_id": docs_ids[0]}

            param = {"$or": []}
            for doc_id in docs_ids:
                param["$or"].append({"act_id": doc_id})

            return param

    return {
        "question": itemgetter('question'),
        "filter": RunnableLambda(get_filter_param)
    } | RunnableLambda(ainvoke_retriever)


def format_docs_for_vikhr(docs: List[Document]) -> str:
    import json

    docs = [{
        "doc_id": index,
        "title": doc.metadata.get('top_level_section'),
        "content": doc.metadata.get('content')[:MAX_SYMBOLS]
    } for index, doc in enumerate(docs)]

    return json.dumps(docs, ensure_ascii=False)


async def create_chat_completions(_input: Dict[str, Any]) -> str:
    client = AsyncOpenAI(base_url=settings.LLM_URL, api_key=settings.LLM_API_KEY)
    question = _input['question']
    user_profile = _input['user_profile']
    docs = _input['context']
    relevant_indexes = _input.get('relevant_indexes')
    prompt = [
        {'role': 'system', 'content': ANSWER_SYSTEM_PROMPT},
        {'role': 'documents', 'content': docs},
        {'role': 'user', 'content': ANSWER_HUMAN_PROMPT.format(question=question, user_profile=user_profile)}
    ]

    if relevant_indexes:
        prompt.append({'role': 'assistant', 'content': relevant_indexes})

    res = (await client.chat.completions.create(
        model=MODEL_NAME,
        messages=prompt,
        temperature=0.25,
        max_tokens=2048
    )).choices[0].message.content
    return res


def format_answer(answer_data: Dict[str, Any]) -> Dict[str, Any]:
    import json

    docs = answer_data.get("docs", [])
    docs_relevant_indexes = answer_data.get('relevant_indexes')

    try:
        docs_relevant_indexes = json.loads(docs_relevant_indexes)
        docs = [docs[index] for index in docs_relevant_indexes["relevant_doc_ids"]]
    except BaseException:
        pass

    return {
        "answer": answer_data["answer"],
        "total_docs": len(docs),
        "docs": [{"content": doc.metadata.pop('content'), "metadata": doc.metadata} for doc in docs],
        "small_answer": answer_data["small_answer"],
    }


def create_base_chain(
        _model: BaseChatModel,
        _retriever: BaseRetriever
) -> Runnable:
    retriever_chain = create_retriever_chain(_retriever)

    context = (
        RunnablePassthrough.assign(
            docs=retriever_chain
        ).assign(context=lambda x: format_docs_for_vikhr(x["docs"]))
    )

    summarize_answer_prompt = ChatPromptTemplate.from_messages([
        ('system', SUMMARY_SYSTEM),
        ('human', SUMMARY_HUMAN),
    ])

    summarize_answer_chain = summarize_answer_prompt | _model | StrOutputParser()

    return context.assign(
        relevant_indexes=RunnableLambda(create_chat_completions)
    ).assign(answer=RunnableLambda(create_chat_completions)).assign(small_answer=summarize_answer_chain)


def create_chain_with_formated_output(_base_chain: Runnable) -> Runnable:
    return _base_chain.pick(["answer", "docs", "relevant_indexes", "small_answer"]) | format_answer


model = ChatOpenAI(
    model_name=MODEL_NAME,
    openai_api_base=settings.LLM_URL,
    openai_api_key=settings.LLM_API_KEY,
)
retriever = get_retriever()
base_chain = create_base_chain(model, retriever)
chain_with_formated_output = create_chain_with_formated_output(base_chain)
