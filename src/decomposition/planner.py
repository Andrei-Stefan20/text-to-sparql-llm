from langchain.prompts import PromptTemplate

class QueryDecomposer:
    def __init__(self, llm):
        self.llm = llm
        
    def create_plan(self, user_question):
        template = """
        You are a Knowledge Graph expert. Your task is to decompose a complex natural language question into a sequence of simple sub-tasks that can be solved with single SPARQL queries or filtering operations.
        
        User Question: {question}
        
        Plan (numbered list):
        """
        
        prompt = PromptTemplate(template=template, input_variables=["question"])
        response = self.llm.invoke(prompt.format(question=user_question))
        
        steps = self._parse_steps(response)
        return steps

    def _parse_steps(self, text):
        return [line.strip() for line in text.split('\n') if line.strip() and line[0].isdigit()]