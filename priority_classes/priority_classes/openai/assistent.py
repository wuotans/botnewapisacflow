import json
import logging
import os.path
from priority_classes.decorators.decorators import time_out
from openai import OpenAI
import openai
import copy

class RunningQueue(Exception):
    pass


class Assistent:

    def __init__(self,name_assistent,instructions,tools=None,model='gpt-3.5-turbo-1106',temperature:int=0,*args,**kwargs):
        self.client = OpenAI()
        self.responses = None
        self.message = None
        self.run = None
        self.assistant=None
        self.thread = None
        self.available_functions = None
        self.name = name_assistent
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.temperature = temperature
        self.assistant_id = self.get_assistent_config()['assistant_id']
        self.thread_id = None
        self.update_assistant()


    def create_assistent(self,*args,**kwargs):
        self.assistant = self.client.beta.assistants.create(
            name=self.name,
            instructions=self.instructions,
            tools=self.tools,
            model=self.model,
            temperature=self.temperature,
            **kwargs
        )
        return self

    def update_assistant(self,**kwargs):
        self.assistant = self.client.beta.assistants.update(
            assistant_id=self.assistant_id,
            name=self.name,
            instructions=self.instructions,
            tools=self.tools,
            model=self.model,
            temperature=self.temperature
        )
        return self
    def get_list_created_assistents(self):
        my_assistants = self.client.beta.assistants.list(
            order="desc",
        )
        return my_assistants.data

    def get_assistent_config(self):
        try:
            #logging.info(self.get_created_assistents()[-1].id)
            #self.assistant = 'asst_TOCoHFxLTFpldLwtzuJjA365'#self.get_created_assistents()[-1]
            if not os.path.exists('config/config_assistent.json'):
                self.assistant_id = self.create_assistent().assistant.id #'asst_TOCoHFxLTFpldLwtzuJjA365'#
                assistent_config_file={
                    'assistant_id':self.assistant_id
                }
                os.makedirs('config',exist_ok=True)
                with open('config/config_assistent.json','w',encoding='utf-8') as f:
                    f.write(json.dumps(assistent_config_file,ensure_ascii=False,indent=4))
            else:
                with open('config/config_assistent.json','r',encoding='utf-8') as f:
                    assistent_config_file = json.loads(f.read())
            logging.info(assistent_config_file)
            return assistent_config_file
        except Exception as e:
            logging.exception(e)

    def load_available_functions(self,available_functions):
        self.available_functions = available_functions
        return self


    def create_new_conversation(self):
        self.thread = self.client.beta.threads.create()
        self.thread_id = self.thread.id
        return self

    def use_existent_thread_id(self,thread_id):
        self.thread_id = thread_id
        return self

    def run_assistent(self):
        self.run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
            instructions=self.instructions,
            tools=self.tools,
        )
        return self

    def verify_expiration(self, expires_at):
        logging.info(expires_at)  # 1704832738
        # Timestamps
        now = hd.get_dummy() / 1000
        logging.info(now)
        if now < expires_at:
            return True
        return False

    @time_out(120, show_exception=True)
    def verify_run(self):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=self.run.id
        )
        status = [val for val in (run.completed_at, run.cancelled_at, run.failed_at) if val is not None]
        if run.required_action:
            if isinstance(self.verify_response_tools(run.required_action),Assistent):
                raise RunningQueue
            return False
        if len(status) > 0:
            return True
        else:
            raise RunningQueue



    def add_file_search_to_main_assistent(self,name_to_vector_store,list_of_files_path):
        self.tools.append({"type": "file_search"})
        self.update_assistant(tools=self.tools)
        # Create a vector store caled "Financial Statements"
        self.vector_store = self.client.beta.vector_stores.create(name=name_to_vector_store)

        # Ready the files for upload to OpenAI
        file_streams = [open(path, "rb") for path in list_of_files_path]

        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=self.vector_store.id, files=file_streams
        )

        # You can print the status and the file counts of the batch to see the result of this operation.
        logging.info(file_batch.status)
        logging.info(file_batch.file_counts)
        self.update_assistant(tool_resources={"file_search": {"vector_store_ids": [self.vector_store.id]}})
        return self

    def add_file_search_to_thread_assistent(self,name_to_vector_store,list_of_files_path):
        self.tools.append({"type": "file_search"})
        self.update_assistant(tools=self.tools)
        # Create a vector store caled "Financial Statements"
        self.vector_store_thread = self.client.beta.vector_stores.create(
            name=name_to_vector_store,
            expires_after={
                "anchor": "last_active_at",
                "days": 3
            }
        )
        # Ready the files for upload to OpenAI
        file_streams = [open(path, "rb") for path in list_of_files_path]

        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=self.vector_store_thread.id, files=file_streams
        )
        logging.info(file_batch.status)
        logging.info(file_batch.file_counts)

        self.update_thread(
            tool_resources={"file_search": {"vector_store_ids": [self.vector_store_thread.id]}}
        )

        # The thread now has a vector store with that file in its tool resources.
        logging.info(self.thread.tool_resources.file_search)
        return self

    def update_thread(self,**kwargs):
        # Update a thread
        self.thread = self.client.beta.threads.update(
            thread_id=self.thread_id,
            **kwargs
        )
        return self

    def add_user_message(self, msg):
        self.message = self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=msg
        )
        return self

    def show_responses(self):
        self.responses = self.client.beta.threads.messages.list(
            thread_id=self.thread_id
        )
        answer = self.responses.data[0].content[0].text.value
        logging.info(answer)
        return answer

    def test_assistent(self):
        logging.info('Sou seu assistente pessoal, em que posso ajudar?')
        while True:
            ask = input()
            self.add_user_message(ask)
            self.run_assistent()
            self.verify_run()
            self.show_responses()

    def submit_tools_response(self, tool_outputs):
        self.run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread_id,
            run_id=self.run.id,
            tool_outputs=tool_outputs
        )
        return self

    def verify_response_tools(self,response):
        tool_outputs = []
        try:
            for tool_call in response.submit_tool_outputs.tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                logging.info(function_args)
                function_response = function_to_call(
                    **function_args
                )
                function_response = function_response if function_response is not None else 'Erro na busca'
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": str(function_response),
                })
                #logging.info(tool_outputs)
            self.submit_tools_response(tool_outputs)
        except Exception as e:
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": f'ERRO: {str(e)}',
            })
            self.submit_tools_response(tool_outputs)
        return self


if __name__ == '__main__':
    instructions="""
    Você é um agente de suporte ao sistema ssw, responsavel por perguntar e responder duvidas dos usuarios  relacionadas ao sistema SSW
    quando solicitado a realizar consultas você deve perguntar qual o numero da nota fiscal ou CTRC  ou chave danfe afim de ativar uma API externa
    """
    ass = Assistent('Consultor SSW',instructions,model='gpt-4o')
    logging.info(ass.assistant_id)