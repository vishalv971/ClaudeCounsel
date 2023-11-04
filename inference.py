from bravefetcher import BraveFetcher
from mongofetcher import MongoFetcher
from haystack.nodes import PromptNode, PromptTemplate, AnswerParser
from haystack.pipelines import Pipeline

anthropic_key = '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'


def infer(prompt):
    prompt_text = f"""
    You are an expert UK tax advisor. Your goal is to give tax advice to users in the UK. You should maintain a friendly customer service tone. 
    Here are some important rules for the interaction:
        - If you do not know the answer, say "Sorry, I don't have enough information to answer that."
        - If you are unsure how to respond, say “Sorry, I didn’t understand that. Could you add some more details to the question?”
        - If you are asked advice to evade tax, say "Sorry, I  give tax advice. Do you have a tax question today I can help you with?"
        - If someone asks something irrelevant, say, “Sorry, I  give tax advice. Do you have a tax question today I can help you with?”
        - If someone asks something harmful or inappropriate, say " Sorry, I give tax advice. Do you have a tax question today I can help you with?"
    Keeping this in mind answer the following question <question>{prompt}</question>. 
    Posts:{{join(documents, delimiter=new_line, pattern='---'+new_line+'$content'+new_line+'URL: $url', str_replace={{new_line: ' ', '[': '(', ']': ')'}})}}.
    The user may ask you questions about information from these documents, you should always aim to answer truthfully from the document when possible. 
    """
    fetcher = MongoFetcher("hackuser123")
    prompt_node = PromptNode(
        model_name_or_path="claude-2",
        default_prompt_template=PromptTemplate(prompt_text),
        api_key=anthropic_key,
        max_length=768,
        model_kwargs={"stream": False},
    )

    pipe = Pipeline()
    pipe.add_node(component=fetcher, name="fetcher", inputs=["Query"])
    pipe.add_node(component=prompt_node, name="prompt_node", inputs=["fetcher"])
    return pipe.run(params={}, debug=True)['results'][0]
