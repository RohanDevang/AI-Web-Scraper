from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Define the prompt template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    "5. **Human Readable Format:** Ensure that the extracted information is presented in a clear and human-readable format."
)

# Instantiate the ChatGroq model
model = ChatGroq(
    temperature=0.7,
    groq_api_key='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',
    model_name="llama-3.1-70b-versatile"
)

def parse_with_groq(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
            print(f"Parsed batch: {i} of {len(dom_chunks)}")
            parsed_results.append(response.content)
        except Exception as e:
            print(f"Error parsing chunk {i}: {e}")
            parsed_results.append("")  # Append an empty string or handle as needed

    return "\n".join(parsed_results)
