"""Data analysis pipeline workflow"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Data Analysis Pipeline",
    description="End-to-end data analysis workflow",
    nodes=[
        Node(id="load", type=NodeType.INPUT, name="Load Data"),
        Node(id="clean", type=NodeType.TRANSFORMER, name="Clean & Prepare",
             config=NodeConfig(custom_attributes={"transformation": "clean_data"})),
        Node(id="analyze", type=NodeType.AGENT, name="Data Analyst",
             config=NodeConfig(system_prompt="Analyze the data and identify patterns.")),
        Node(id="visualize", type=NodeType.CUSTOM, name="Generate Visualizations"),
        Node(id="report", type=NodeType.AGENT, name="Report Writer",
             config=NodeConfig(system_prompt="Write a comprehensive analysis report.")),
        Node(id="output", type=NodeType.OUTPUT, name="Analysis Report"),
    ],
    edges=[
        Edge(id="e1", source_id="load", target_id="clean"),
        Edge(id="e2", source_id="clean", target_id="analyze"),
        Edge(id="e3", source_id="analyze", target_id="visualize"),
        Edge(id="e4", source_id="visualize", target_id="report"),
        Edge(id="e5", source_id="report", target_id="output"),
    ],
)
