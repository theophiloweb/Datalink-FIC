import google.generativeai as genai
from dotenv import load_dotenv
import os

class IAInteraction:
    """
    Classe para interagir com o modelo de linguagem grande (LLM) do Google AI.
    """

    def __init__(self, api_key_env_var="API_STUDIO_IA", model_name="gemini-1.5-pro-latest"):
        """
        Construtor da classe.

        Args:
            api_key_env_var (str, optional): Nome da variável de ambiente que contém a chave de API. Padrão é "API_STUDIO_IA".
            model_name (str, optional): Nome do modelo LLM a ser usado. Padrão é "gemini-1.5-pro-latest".
        """
        load_dotenv()
        genai.configure(api_key=os.getenv(api_key_env_var))

        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        self.model = genai.GenerativeModel(model_name=model_name,
                                          generation_config=self.generation_config,
                                          safety_settings=self.safety_settings)
        self.convo = None

    def start_chat(self, history=None):
        """
        Inicia uma nova conversa com o modelo LLM.

        Args:
            history (list, optional): Histórico da conversa anterior, se houver. Padrão é None.

        Returns:
            None
        """
        self.convo = self.model.start_chat(history=history)

    def send_message(self, message):
        """
        Envia uma mensagem para o modelo LLM e obtém a resposta.

        Args:
            message (str): A mensagem a ser enviada para o modelo.

        Returns:
            str: A resposta do modelo LLM.
        """
        self.convo.send_message(message)
        return self.convo.last.text