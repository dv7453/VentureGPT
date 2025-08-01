# agents/economics_agent_helper.py

import logging
import json
import os
from groq import Groq  # Assuming Groq library provides a client named GroqClient


class EconomicsAgentHelper:
    def __init__(self, llama_api_key_env_var='ECONOMICS_AGENT_API_KEY', llama_endpoint='https://grqoclound.api/llama'):
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
    def fetch_market_data(self, industry):
        """
        Fetches relevant market data based on the startup's industry using Llama via Groq.
        """
        prompt = (
            f"Provide a detailed overview of the market for the {industry} industry. Include current market size, projected growth rates, key trends, and major players. Format the response as a JSON object with the following keys: 'market_size', 'growth_rate', 'key_trends', 'major_players'. Return only the json object nothing else"
        )
        response = self.send_prompt_to_llama(prompt)
        return response
        # if response:
        #     try:
        #         market_data = json.loads(response)
        #         return market_data
        #     except json.JSONDecodeError as e:
        #         self.logger.error(f"Error decoding JSON response: {e}")
        #         return {
        #             "market_size": "Unable to fetch market size at this time.",
        #             "growth_rate": "Unable to fetch growth rate at this time.",
        #             "key_trends": ["Unable to fetch key trends at this time."],
        #             "major_players": ["Unable to fetch major players at this time."]
        #         }
        # else:
        #     return {
        #         "market_size": "Unable to fetch market size at this time.",
        #         "growth_rate": "Unable to fetch growth rate at this time.",
        #         "key_trends": ["Unable to fetch key trends at this time."],
        #         "major_players": ["Unable to fetch major players at this time."]
        #     }

    def generate_financial_projections(self, business_model):
        """
        Generates financial projections based on the provided business model using Llama via Groq.
        """
        prompt = (
            f"Generate a three-year financial projection for a startup using the '{business_model}' business model. Include projected revenues, expenses, and profits for each year. Format the response as a JSON object with years as keys and sub-keys 'Revenue', 'Expenses', and 'Profit'. Return only the json object nothing else. i repeat return only the json object nothing else",
        )
        response = self.send_prompt_to_llama(prompt)
        return response
        # if response:
        #     try:
        #         projections = json.loads(response)
        #         return projections
        #     except json.JSONDecodeError as e:
        #         self.logger.error(f"Error decoding JSON response: {e}")
        #         return {"Error": "Unable to generate financial projections at this time."}
        # else:
        #     return {"Error": "Unable to generate financial projections at this time."}

    def conduct_competitive_analysis(self, industry):
        """
        Conducts a competitive analysis within the given industry using Llama via Groq.
        """
        prompt = (
            f"Conduct a competitive analysis for the {industry} industry. Identify 3 key competitors, their market shares, strengths, and weaknesses. Format the response as a JSON array of objects, each containing 'Name', 'Market Share', 'Strengths', and 'Weaknesses'. Return only the json object nothing else"
        )

        response = self.send_prompt_to_llama(prompt)
        return response

        # if response:
        #     try:
        #         competitors = json.loads(response)
        #         return competitors
        #     except json.JSONDecodeError as e:
        #         self.logger.error(f"Error decoding JSON response: {e}")
        #         return [{"Error": "Unable to conduct competitive analysis at this time."}]
        # else:
        #     return [{"Error": "Unable to conduct competitive analysis at this time."}]
