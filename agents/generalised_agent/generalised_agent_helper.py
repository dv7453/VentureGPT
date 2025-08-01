# agents/generalized_agent_helper.py

import logging
import json
import os
from groq import Groq  # Assuming Groq library provides a client named GroqClient


class GeneralizedAgentHelper:
    def __init__(self, llama_api_key_env_var='GENERALIZED_AGENT_API_KEY',
                 llama_endpoint='https://grqoclound.api/llama'):
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

    def aggregate_data(self, storage, idea_id):
        """
        Retrieves and aggregates data from all agents for the given idea_id.

        Args:
            storage (Storage): An instance of the Storage class.
            idea_id (str): The unique identifier for the startup idea.

        Returns:
            dict: A dictionary containing aggregated data from all agents.
        """
        try:
            data = storage.retrieve_outputs(idea_id)
            self.logger.info(f"Aggregated data for idea_id: {idea_id}")
            return data
        except Exception as e:
            self.logger.error(f"Error aggregating data: {e}")
            return {}
    def summarize_data_with_llama(self, aggregated_data):
        """
        Summarizes the aggregated data using Llama via Groq.
        """
        try:
            # Convert the aggregated_data dictionary to a formatted JSON string for inclusion in the prompt
            aggregated_data_json = json.dumps(aggregated_data, indent=4)
            prompt = (
                f"Generate a comprehensive and cohesive report based on the following aggregated data:\n\n '{aggregated_data_json}'\n\n The report should include sections for Legal Analysis, Economic Analysis, and Business Structure Analysis. Each section should be well-formatted in Markdown with appropriate headings and subheadings."
            )
            response = self.send_prompt_to_llama(prompt)
            if response:
                return response
            else:
                return "Unable to summarize data at this time."
        except Exception as e:
            self.logger.error(f"Error summarizing data with Llama: {e}")
            return "Unable to summarize data at this time."

    def format_report_with_llama(self, summary):
        """
        Optionally formats the summary into a final report using Llama via Groq.
        """
        try:
            prompt = (
                f"Format the following summary into a polished Markdown report:\n\n {summary}\n\n Ensure that the report has a clear structure, with appropriate headings, subheadings, and formatting."
            )
            response = self.send_prompt_to_llama(prompt, max_tokens=500)
            if response:
                return response
            else:
                return summary  # Fallback to the original summary if formatting fails
        except Exception as e:
            self.logger.error(f"Error formatting report with Llama: {e}")
            return summary  # Fallback to the original summary if formatting fails
