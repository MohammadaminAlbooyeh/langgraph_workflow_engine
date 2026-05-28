"""ETL data pipeline workflow"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Data Pipeline",
    description="Extract, transform, load pipeline",
    type="data_pipeline",
    nodes=[
        Node(id="extract", type=NodeType.INPUT, name="Extract Data"),
        Node(id="clean", type=NodeType.TRANSFORMER, name="Clean Data",
             config=NodeConfig(custom_attributes={"transformation": "clean"})),
        Node(id="validate", type=NodeType.VALIDATOR, name="Validate Data"),
        Node(id="transform", type=NodeType.TRANSFORMER, name="Transform Data",
             config=NodeConfig(custom_attributes={"transformation": "normalize"})),
        Node(id="load", type=NodeType.OUTPUT, name="Load Data"),
    ],
    edges=[
        Edge(id="e1", source_id="extract", target_id="clean"),
        Edge(id="e2", source_id="clean", target_id="validate"),
        Edge(id="e3", source_id="validate", target_id="transform"),
        Edge(id="e4", source_id="transform", target_id="load"),
    ],
)
