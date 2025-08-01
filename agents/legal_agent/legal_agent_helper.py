# agents/legal_agent_helper.py

import logging
import json
import os
from groq import Groq  # Assuming Groq library provides a client named GroqClient


class LegalAgentHelper:
    def __init__(self, llama_api_key_env_var='LEGAL_AGENT_API_KEY', llama_endpoint='https://grqoclound.api/llama'):
        self.logger = logging.getLogger(__name__)
        self.llama_endpoint = llama_endpoint

        if not self.llama_api_key:
            self.logger.error(f"Environment variable {llama_api_key_env_var} not set.")
            raise ValueError(f"Environment variable {llama_api_key_env_var} not set.")

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
    def fetch_regulations(self, industry):
        """
        Fetches relevant regulations based on the startup's industry using Llama via Groq.
        """
        prompt = (
            f"Provide a detailed overview of the regulations applicable to the {industry} industry. Include data protection laws, licensing requirements, compliance standards, and any other relevant regulations. Format the response as a JSON object with the following keys: 'data_protection_laws', 'licensing_requirements', 'compliance_standards', 'other_regulations'. Return only the json object nothing else"
        )
        response = self.send_prompt_to_llama(prompt)
        return response
        # if response:
        #     try:
        #         regulations = json.loads(response)
        #         return regulations
        #     except json.JSONDecodeError as e:
        #         self.logger.error(f"Error decoding JSON response: {e}")
        #         return {
        #             "data_protection_laws": "Unable to fetch data protection laws at this time.",
        #             "licensing_requirements": "Unable to fetch licensing requirements at this time.",
        #             "compliance_standards": "Unable to fetch compliance standards at this time.",
        #             "other_regulations": ["Unable to fetch other regulations at this time."]
        #         }
        # else:
        #     return {
        #         "data_protection_laws": "Unable to fetch data protection laws at this time.",
        #         "licensing_requirements": "Unable to fetch licensing requirements at this time.",
        #         "compliance_standards": "Unable to fetch compliance standards at this time.",
        #         "other_regulations": ["Unable to fetch other regulations at this time."]
        #     }

    def generate_compliance_checklist(self, regulations):
        """
        Generates a compliance checklist based on the provided regulations using Llama via Groq.
        """
        try:
            # Convert the regulations dictionary to a formatted JSON string for inclusion in the prompt
            regulations_json = json.dumps(regulations, indent=4)
            prompt = (
                f"Based on the following regulations, generate a detailed compliance checklist for a startup in the industry.\n\n '{regulations_json}' \n\n Provide the checklist as a JSON array of strings. Return only the json object nothing else"
            )
            response = self.send_prompt_to_llama(prompt)
            if response:
                try:
                    checklist = json.loads(response)
                    return checklist
                except json.JSONDecodeError as e:
                    self.logger.error(f"Error decoding JSON response: {e}")
                    return ["Unable to generate compliance checklist at this time."]
            else:
                return ["Unable to generate compliance checklist at this time."]
        except Exception as e:
            self.logger.error(f"Error generating compliance checklist with Llama: {e}")
            return ["Unable to generate compliance checklist at this time."]

    def assess_legal_risks(self, business_model):
        """
        Assesses potential legal risks associated with the business model using Llama via Groq.
        """
        prompt = (
            f"Assess the potential legal risks associated with the '{business_model}' business model. Consider aspects such as data privacy, intellectual property, contractual obligations, and regulatory compliance.Format the response as a JSON array of strings. Return only the json object nothing else"
        )
        response = self.send_prompt_to_llama(prompt)
        return response
        # if response:
        #     try:
        #         risks = json.loads(response)
        #         return risks
        #     except json.JSONDecodeError as e:
        #         self.logger.error(f"Error decoding JSON response: {e}")
        #         return ["Unable to assess legal risks at this time."]
        # else:
        #     return ["Unable to assess legal risks at this time."]
