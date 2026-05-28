"""Benchmark workflow execution performance."""
import asyncio
import time
from backend.services.workflow_service import WorkflowService
from backend.services.execution_service import ExecutionService


async def benchmark():
    wf_svc = WorkflowService()
    ex_svc = ExecutionService()

    wf = await wf_svc.create({
        "name": "Benchmark",
        "nodes": [{"id": "n1", "type": "input", "name": "Input"}, {"id": "n2", "type": "output", "name": "Output"}],
        "edges": [{"id": "e1", "source_id": "n1", "target_id": "n2"}],
    })

    iterations = 100
    start = time.time()
    for _ in range(iterations):
        ex = await ex_svc.create(wf.id, {})
        await ex_svc.start(ex.id, wf.nodes, wf.edges)

    elapsed = time.time() - start
    print(f"Executed {iterations} workflows in {elapsed:.2f}s")
    print(f"Average: {(elapsed / iterations) * 1000:.1f}ms per execution")


if __name__ == "__main__":
    asyncio.run(benchmark())
