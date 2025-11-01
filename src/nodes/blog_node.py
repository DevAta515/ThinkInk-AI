from src.states.blog_state import BlogState, Blog
from langchain_core.messages import SystemMessage, HumanMessage
from typing import List, Dict, Any

class BlogNode:
    """
    A class to represent the blog node with dynamic multi-language support.
    """

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        """
        Create the title for the blog
        """
        if "topic" in state and state["topic"]:
            prompt = """
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly
                   """
            
            system_message = prompt.format(topic=state["topic"])
            # print(system_message)
            response = self.llm.invoke(system_message)
            # print(response)
            return {"blog": {"title": response.content}}
        
    def content_generation(self, state: BlogState):
        """
        Generate blog content
        """
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}
    
    def dynamic_translation(self, state: BlogState):
        """
        Dynamic translation that works with ANY language from state
        """
        translation_prompt = """
        Translate the following content into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.

        ORIGINAL CONTENT:
        {blog_content}
        """
        # print(f"Translating to: {state['curr_lang']}")
        blog_content = state["blog"]["content"]
        messages = [
            HumanMessage(translation_prompt.format(
                current_language=state["curr_lang"], 
                blog_content=blog_content
            ))
        ]
        try:
            translation_content = self.llm.with_structured_output(Blog).invoke(messages)
            # print("Translated content:", translation_content)
            return {"blog": {"content": translation_content}}
        except Exception as e:
            print(ValueError(f"Error in translation: {e}"))
            return {"blog": {"content": state["blog"]["content"]}}

    def route_decision(self, state: BlogState):
        """
        Simple route decision - always go to translation if language is specified
        """
        current_lang = state.get("curr_lang", "").strip().lower()
        
        if current_lang and current_lang != "english":
            return "translate"
        else:
            return "end"