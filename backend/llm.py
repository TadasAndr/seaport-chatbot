from langchain.chains import RetrievalQA
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
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4-turbo",
            streaming=True
        )
        self.setup_chain()

    def setup_chain(self):
        prompt_template = """You are a helpful assistant that is an expert on charges and rules at Klaipėda State seaport.
            You only answer in Lithuanian.
            If you don't know the answer, say you don't know.
            The user does not know about document's existence so do not refer to it directly.

        Context: {context}

        Question: {question}
        Answer:"""

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(),
            return_source_documents=False,
            chain_type_kwargs={"prompt": prompt}
        )

    def ask(self, question, session_id, stream_handler=None):
        callbacks = [stream_handler] if stream_handler else None
        response = self.chain({"query": question}, callbacks=callbacks)
        return response['result']