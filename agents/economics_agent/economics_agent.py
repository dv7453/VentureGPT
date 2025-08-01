# agents/economics_agent.py

import yaml
import logging
from .economics_agent_helper import EconomicsAgentHelper


class EconomicsAgent:
    def __init__(self, config_path='config/config.yaml'):
        # Load configuration
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        # Extract API key for Groq (assuming it's stored here)
        llama_api_key = config['agents']['economics_agent']['llama_api_key']

        # Initialize helper functions
        self.helper = EconomicsAgentHelper(llama_api_key_env_var='ECONOMICS_AGENT_API_KEY')

        # Setup logging
        self.logger = logging.getLogger(__name__)

    def process(self, input_data):
        """
        Processes the input data to perform economic analysis.
        """
        try:
            self.logger.info("Starting economic analysis.")

            # Extract relevant information from input_data
            # Ensure that input_data contains 'industry' and 'business_model'
            industry = input_data.get('industry', 'General')
            business_model = input_data.get('business_model', 'Standard')  # e.g., Subscription, Freemium

            # Fetch market data
            market_data = self.helper.fetch_market_data(industry)
            # Generate financial projections
            financial_projections = self.helper.generate_financial_projections(business_model)

            # Conduct competitive analysis
            competitive_analysis = self.helper.conduct_competitive_analysis(industry)

            # Compile the analysis
            analysis = {
                "market_data": market_data,
                "financial_projections": financial_projections,
                "competitive_analysis": competitive_analysis
            }


            # Format the analysis into a readable string
            formatted_analysis = self.format_analysis(analysis)

            self.logger.info("Economic analysis completed successfully.")
            return analysis
        except Exception as e:
            self.logger.error(f"Error during economic analysis: {e}")
            return "An error occurred during economic analysis."

    def format_analysis(self, analysis):
        """
        Formats the analysis dictionary into a readable string.
        """
        try:
            formatted = "**Market Data:**\n"

            # Format market size
            market_size = analysis['market_data'].get('market_size', {})
            formatted += f"Market Size (Global): {market_size.get('value', 'N/A')}\n"
            if 'segmentation' in market_size:
                formatted += "Segmentation:\n"
                for segment, value in market_size['segmentation'].items():
                    formatted += f"  - {segment.capitalize()}: {value}\n"

            # Format growth rate
            growth_rate = analysis['market_data'].get('growth_rate', {})
            formatted += f"Growth Rate (Global): {growth_rate.get('value', 'N/A')}\n"
            if 'segmentation' in growth_rate:
                formatted += "Segmentation:\n"
                for segment, value in growth_rate['segmentation'].items():
                    formatted += f"  - {segment.capitalize()}: {value}\n"

            # Format key trends
            formatted += "Key Trends:\n"
            for trend in analysis['market_data'].get('key_trends', []):
                formatted += f"  - {trend}\n"

            # Format major players
            formatted += "Major Players:\n"
            for player in analysis['market_data'].get('major_players', []):
                formatted += f"  - {player}\n"

            # # Format financial projections
            formatted += "\n**Financial Projections:**\n"
            formatted += f"\n{analysis['financial_projections']} \n"
            # for year, projections in analysis['financial_projections'].items():
            #     formatted += f"{year}:\n"
            #     for key, value in projections.items():
            #         formatted += f"  - {key}: {value}\n"

            # Format competitive analysis
            formatted += "\n**Competitive Analysis:**\n"
            formatted += f"\n{analysis['competitive_analysis']} \n"
            # for competitor in analysis['competitive_analysis']:
            #     formatted += f"- **{competitor.get('Name', 'N/A')}**\n"
            #     formatted += f"  - Market Share: {competitor.get('Market Share', 'N/A')}\n"
            #     formatted += "  - Strengths:\n"
            #     for strength in competitor.get('Strengths', []):
            #         formatted += f"    - {strength}\n"
            #     formatted += "  - Weaknesses:\n"
            #     for weakness in competitor.get('Weaknesses', []):
            #         formatted += f"    - {weakness}\n"
            #
            # return formatted.strip()

        except Exception as e:
            self.logger.error(f"Error formatting analysis: {e}")
            return "Unable to format economic analysis at this time."
