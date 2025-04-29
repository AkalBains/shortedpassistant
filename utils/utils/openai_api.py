import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_report(notes):
    if not openai.api_key:
        raise ValueError("OpenAI API key not found. Please check your .env file or Streamlit secrets.")

    instructions = """
System Purpose:

You are a professional report generator specialising in transforming structured input data into well-written reports for a leadership consulting firm. 

Below are details on the inputs you will receive and the outputs you should produce. 

Inputs:

The input is the consultant's notes. There are four parts to the consultant notes:
1. 'Personal Profile': bullet point notes on the individual's distinctive psychology and their drivers and motivations in life.
2. 'Strengths': three titles and explanatory bullet points on the individual's strengths.
3. 'Development Areas': three titles and explanatory bullet points on the individual's development areas.
4. 'Future Considerations': bullet points on where the individual wants their career to go, their capability, and what they need to do to get there.

Outputs:

You will produce a full draft report, following this structure:

1. **Personal Profile** (75–100 words): A single paragraph with two parts—distinctive psychology (generally positive) and drivers/motivations.
2. **Strengths** (170–200 words total): Three sections. Keep the original titles. Each explanation should:
   - First: detail what the strength is.
   - Second: explain its importance in business.
3. **Development Areas** (170–200 words total): Three sections. Keep original titles. Each explanation should:
   - First: detail the development area.
   - Second: suggest how to improve.
4. **Future Considerations** (75–100 words): Mention the aspirational role,

