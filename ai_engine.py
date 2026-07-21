from groq import Groq
from data_structures import AIRequest
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_answer(req: AIRequest) -> str:
    """
    Build a prompt from the student's question + PDF context,
    send it to Groq (LLaMA 3), and return the answer as a string.
    """

    prompt = f"""You are a helpful AI tutor.
Use ONLY the context below to answer the student's question.
If the answer is not in the context, say "I couldn't find that in the document."

Context:
{req.context[:3000]}

Question: {req.question}

Answer:"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful AI tutor who answers questions only from the provided context."},
                {"role": "user",   "content": prompt}
            ],
            max_tokens=512,
            temperature=0.5,
        )
        return response.choices[0].message.content

    except Exception as e:
        error_str = str(e)

        if '429' in error_str or 'rate_limit' in error_str.lower():
            return (
                "⚠️ **Rate Limit Hit!**\n\n"
                "😔 Too many requests — please wait a moment and try again.\n"
                "💡 Groq free tier allows ~30 requests/minute."
            )
        elif '401' in error_str or 'invalid_api_key' in error_str.lower():
            return (
                "🔑 **Invalid API Key!**\n\n"
                "Please check your GROQ_API_KEY in the .env file.\n"
                "Get a free key at console.groq.com"
            )
        else:
            return f"❌ **AI Error:** {error_str[:200]}"