from src.states.blog_state import BlogState, Blog
from langchain_core.messages import SystemMessage, HumanMessage

class BlogNode:
    """
    A class to represent the blog node.
    """

    def __init__(self, llm):
        self.llm=llm

    def title_creation(self, state:BlogState):
        """
        create the title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt="""
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly

                   """
            
            sytem_message=prompt.format(topic=state["topic"])
            print(sytem_message)
            response=self.llm.invoke(sytem_message)
            print(response)
            return {"blog":{"title":response.content}}
        
    def content_generation(self, state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}
    
    def translation(self,state:BlogState):
        """
        Translate the content to the specified language.
        """
        translation_prompt="""
        Translate the following content into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.

        ORIGINAL CONTENT:
        {blog_content}

        """
        print("HERE    ", state["curr_lang"])
        print(state)
        blog_content=state["blog"]["content"]
        messages=[
            HumanMessage(translation_prompt.format(current_language=state["curr_lang"], blog_content=blog_content))
        ]
        try:
            transaltion_content = self.llm.with_structured_output(Blog).invoke(messages)
            print("ANSWER     ", transaltion_content)
            return {"blog": {"content": transaltion_content}}
        except Exception as e:
            ValueError(f"Error here {e}")


    def route(self, state:BlogState):
        return {"current_language":state['curr_lang']}
    
    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation function.
        """
        if state["curr_lang"] == "hindi":
            return "hindi"
        elif state["curr_lang"] == "arabic": 
            return "arabic"
        else:
            return state['curr_lang']

        # return {"next": state["curr_lang"]}
