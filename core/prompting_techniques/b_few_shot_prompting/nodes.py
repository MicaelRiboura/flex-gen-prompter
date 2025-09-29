from core.prompting_techniques.base_node import BaseNode
from core.prompting_techniques.b_few_shot_prompting.state import FewShotPromptingState
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

class FewShotAnswerNode(BaseNode):

    def __init__(self, model, examples):
        super().__init__(model)
        self.examples = examples

    def invoke(self, state) -> FewShotPromptingState:
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{prompt}"),
                ("ai", "{answer}"),
            ]
        )

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=self.examples,
        )

        final_prompt = ChatPromptTemplate.from_messages(
            [
                few_shot_prompt,
                ("human", "{prompt}"),
            ]
        )

        chain = final_prompt | self.llm | StrOutputParser()
        result = chain.invoke({"prompt": state['prompt']})
        
        return { "answer": result }
        