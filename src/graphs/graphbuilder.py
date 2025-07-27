from langgraph.graph import START, END, StateGraph
from src.llms.groqllm import GroqLLM
from src.states.blog_state import BlogState
from src.nodes.blog_node import BlogNode


class GraphBuilder:
    def __init__(self, llm):
        self.llm=llm
        self.graph=StateGraph(BlogState)
    
    def build_topic_graph(self):
        """
        Build a graph to generate blog based on the topic
        """
        blog_node=BlogNode(self.llm)
        self.graph.add_node("title_creation",blog_node.title_creation)
        self.graph.add_node("content_generation",blog_node.content_generation)

        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation","content_generation")
        self.graph.add_edge("content_generation",END)
        
        return self.graph

    def build_lang_graph(self):
        """
        Build a graph to generate blog based on the topic and in the language provided
        """
        print("IN build_lang_graph")
        blog_node=BlogNode(self.llm)

        self.graph.add_node("title_creation",blog_node.title_creation)
        self.graph.add_node("content_generation",blog_node.content_generation)

        self.graph.add_node("hindi_translation",lambda state:blog_node.translation({**state,"current_language":"hindi"}))

        self.graph.add_node("arabic_translation",lambda state:blog_node.translation({**state,"current_language":"arabic"}))

        self.graph.add_node("route", blog_node.route_decision)

        print("IN build_lang_graph")

        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation","content_generation")
        self.graph.add_edge("content_generation","route")

        self.graph.add_conditional_edges(
            "route",
            lambda state: state["next"],
            {"hindi": "hindi_translation", "arabic": "arabic_translation"}
        )

        self.graph.add_edge("hindi_translation",END)
        self.graph.add_edge("arabic_translation",END)
        
        return self.graph

    def setup_graph(self, usecase):
        if usecase=="Topic":
            self.build_topic_graph()
        if usecase=="Topic with Translation":
            self.build_lang_graph()

        return self.graph.compile()
    


llm=GroqLLM().get_llm()

## get the graph
graph_builder=GraphBuilder(llm)
graph=graph_builder.build_topic_graph().compile()