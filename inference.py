from mongofetcher import MongoFetcher
from haystack.nodes import PromptNode, PromptTemplate, AnswerParser
from haystack.pipelines import Pipeline


def infer(prompt, anthropic_api_key='', mongo_db_password=''):
    prompt_text = f"""
    You are an expert UK tax advisor. Your goal is to give tax advice to users in the UK. You should maintain a friendly customer service tone. 
    Here are some important rules for the interaction:
    <rules>
        - If you do not know the answer, say "Sorry, I don't have enough information to answer that."
        - If you are unsure how to respond, say “Sorry, I didn’t understand that. Could you add some more details to the question?”
        - If you are asked advice to evade tax, say "Sorry, I  give tax advice. Do you have a tax question today I can help you with?"
        - If someone asks something irrelevant, say, “Sorry, I  give tax advice. Do you have a tax question today I can help you with?”
        - If someone asks something harmful or inappropriate, say " Sorry, I give tax advice. Do you have a tax question today I can help you with?"
    </rules>
    Keeping this in mind answer the following question <question>{prompt}</question>. 
    <documents>{{join(documents, delimiter=new_line, pattern='---'+new_line+'$content'+new_line+'URL: $url', str_replace={{new_line: ' ', '[': '(', ']': ')'}})}}</documents>
    The user may ask you questions about information from these documents, you should always aim to answer truthfully from the documents when possible. 
    Should you find the answer to the question in them, mention the link to the relevant article in your answer.
    """
    fetcher = MongoFetcher(mongo_db_password)
    prompt_node = PromptNode(
        model_name_or_path="claude-2",
        default_prompt_template=PromptTemplate(prompt_text),
        api_key=anthropic_api_key,
        max_length=768,
        model_kwargs={"stream": False},
    )

    pipe = Pipeline()
    pipe.add_node(component=fetcher, name="fetcher", inputs=["Query"])
    pipe.add_node(component=prompt_node, name="prompt_node", inputs=["fetcher"])
    return pipe.run(params={}, debug=True)['results'][0]
