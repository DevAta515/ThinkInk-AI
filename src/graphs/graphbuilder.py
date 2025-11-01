from langgraph.graph import START, END, StateGraph
from src.llms.groqllm import GroqLLM
from src.states.blog_state import BlogState
from src.nodes.blog_node import BlogNode
from typing import List, Optional



class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)
    
    def build_topic_graph(self):
        """Build a graph to generate blog based on the topic only"""
        blog_node = BlogNode(self.llm)
        
        self.graph.add_node("title_creation", blog_node.title_creation)
        self.graph.add_node("content_generation", blog_node.content_generation)

        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)
        
        return self.graph

    def build_dynamic_lang_graph(self):
        """
        Build a graph that can handle ANY language with one dynamic translation node
        """
        blog_node = BlogNode(self.llm)

        # Core nodes
        self.graph.add_node("title_creation", blog_node.title_creation)
        self.graph.add_node("content_generation", blog_node.content_generation)
        self.graph.add_node("dynamic_translation", blog_node.dynamic_translation)

        # Graph flow
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")

        # Conditional edge after content generation
        self.graph.add_conditional_edges(
            "content_generation",
            blog_node.route_decision,
            {
                "translate": "dynamic_translation",
                "end": END
            }
        )

        # Translation goes to END
        self.graph.add_edge("dynamic_translation", END)
        
        return self.graph

    def setup_graph(self, usecase: str):
        # Reset graph for new build
        self.graph = StateGraph(BlogState)
        
        if usecase == "Topic":
            # print("USECASE: Topic only")
            self.build_topic_graph()
        elif usecase == "Topic with Translation":
            # print("USECASE: Topic with Dynamic Translation")
            self.build_dynamic_lang_graph()
        else:
            raise ValueError(f"Unknown usecase: {usecase}")

        return self.graph.compile()
    

llm = GroqLLM().get_llm()
graph_builder = GraphBuilder(llm)
graph = graph_builder.setup_graph(usecase="Topic with Translation")