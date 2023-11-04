from bravefetcher import BraveFetcher
from mongofetcher import MongoFetcher
from haystack.nodes import PromptNode, PromptTemplate, AnswerParser
from haystack.pipelines import Pipeline

anthropic_key = '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'


def infer(prompt):
    prompt_text = f"""
    You are an expert UK tax advisor. Keeping this in mind answer the following question <question>{prompt}</question>. 
    Posts:{{join(documents, delimiter=new_line, pattern='---'+new_line+'$content'+new_line+'URL: $url', str_replace={{new_line: ' ', '[': '(', ']': ')'}})}}.
    If you do not know the answer, You are given a list of gov.uk articles and their urls to aid you. Should you find the answer to the question in them, mention the link to the relevant article in your answer. If you still do not know the answer say "unicorn!".
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
