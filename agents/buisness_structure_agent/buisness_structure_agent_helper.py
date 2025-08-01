# agents/business_structure_agent_helper.py

import logging
import json
from groq import Groq  # Assuming Groq library provides a client named GroqClient


class BusinessStructureAgentHelper:
    def __init__(self, llama_api_key, llama_endpoint='https://grqoclound.api/llama'):
        self.logger = logging.getLogger(__name__)
        self.llama_endpoint = llama_endpoint
        self.client = Groq(api_key=self.llama_api_key)

    def send_prompt_to_llama(self, prompt, max_tokens=500, temperature=0.7):
            """
            Sends a prompt to the Llama model via GroqClient and retrieves the response.
            """
            try:
                # Wrapping the prompt in a list of dictionaries as required by Groq's API
                messages = [{"role": "user", "content": prompt}]
                completion = self.client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=1,
                    stream=True
                )

                # Collecting the streamed response
                response_text = ""
                for chunk in completion:
                    response_text += chunk.choices[0].delta.content or ""

                return response_text.strip()

            except Exception as e:
                self.logger.error(f"Error sending prompt to Llama via Groq: {e}")
                return None
    def propose_business_models(self, industry, business_model_type):
        """
        Proposes suitable business models based on the industry and specified type using Llama via Groq.
        """
        prompt = (
            f"Propose suitable business models for a startup in the {industry} industry using a {business_model_type} model. Provide the models as a JSON array of strings. Return only the json object nothing else"
        )

        response = self.send_prompt_to_llama(prompt)
        return response
        # if response:
        #     try:
        #         models = json.loads(response)
        #         return models
        #     except json.JSONDecodeError as e:
        #         self.logger.error(f"Error decoding JSON response: {e}")
        #         return ["Unable to propose business models at this time."]
        # else:
        #     return ["Unable to propose business models at this time."]

    def map_organizational_structure(self, company_size):
        """
        Maps an organizational structure based on the company's size using Llama via Groq.
        """
        prompt = (
            f"Map an organizational structure for a company of size '{company_size}'. Provide the structure as a JSON object where keys are roles and values are their responsibilities. Return only the json object nothing else"
        )
        response = self.send_prompt_to_llama(prompt)
        return response
        # if response:
        #     try:
        #         structure = json.loads(response)
        #         return structure
        #     except json.JSONDecodeError as e:
        #         self.logger.error(f"Error decoding JSON response: {e}")
        #         return {"Error": "Unable to map organizational structure at this time."}
        # else:
        #     return {"Error": "Unable to map organizational structure at this time."}

    def plan_scalability(self, business_model, current_structure):
        """
        Plans scalability strategies based on the business model and current organizational structure using Llama via Groq.
        """
        # Convert the current_structure dictionary to a formatted JSON string for inclusion in the prompt
        current_structure_json = json.dumps(current_structure, indent=4)
        prompt = (
            f"Plan scalability strategies for a business using the '{business_model}' model and the following organizational structure:\n\n '{current_structure_json}' \n\n Provide the scalability plan as a detailed paragraph."
        )
        response = self.send_prompt_to_llama(prompt, max_tokens=300)
        return response
        # if response:
        #     return response
        # else:
        #     return "Unable to plan scalability at this time."
