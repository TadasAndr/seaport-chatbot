from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

class LLM:
    def __init__(self, vector_store):
        self.chat_histories = {}
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4-turbo",
            streaming=True
        )
        self.setup_chain()

    def get_chat_history(self, session_id: str):
        if session_id not in self.chat_histories:
            self.chat_histories[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        return self.chat_histories[session_id]

    def setup_chain(self):
        prompt_template = """You are an helpful assistant that is an expert of charges and rules at Klaipėda State seaport.
            You only answer in lithuanian.
            If you don't know the answer, say you don't know.
            The user does not know about document's existence so do not refer to it directly.
            Do not repeat the question back.


        {context}

        Question: {question}
        Answer:"""

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(),
            memory=memory,
            combine_docs_chain_kwargs={"prompt": prompt}
        )

    def ask(self, question, session_id, stream_handler=None):
        callbacks = [stream_handler] if stream_handler else None
        response = self.chain({"question": question}, callbacks=callbacks)
        return response['answer']