"""Load testing for the LangGraph Workflow Engine."""
import asyncio
import time
import statistics
from httpx import AsyncClient, ASGITransport
from backend.main import app


class LoadTestResults:
    def __init__(self, name: str):
        self.name = name
        self.times = []
        self.errors = 0
        self.total_requests = 0

    def add_result(self, elapsed: float):
        self.times.append(elapsed)
        self.total_requests += 1

    def add_error(self):
        self.errors += 1
        self.total_requests += 1

    def print_summary(self):
        if not self.times:
            print(f"\n{self.name}: NO SUCCESSFUL REQUESTS")
            print(f"  Total Requests: {self.total_requests}")
            print(f"  Errors: {self.errors}")
            return

        success_rate = ((self.total_requests - self.errors) / self.total_requests) * 100
        avg_time = statistics.mean(self.times)
        min_time = min(self.times)
        max_time = max(self.times)
        median_time = statistics.median(self.times)

        print(f"\n{self.name}")
        print(f"  Total Requests: {self.total_requests}")
        print(f"  Successful: {len(self.times)}")
        print(f"  Errors: {self.errors}")
        print(f"  Success Rate: {success_rate:.1f}%")
        print(f"  Average Time: {avg_time*1000:.2f}ms")
        print(f"  Median Time: {median_time*1000:.2f}ms")
        print(f"  Min Time: {min_time*1000:.2f}ms")
        print(f"  Max Time: {max_time*1000:.2f}ms")
        if len(self.times) > 1:
            std_dev = statistics.stdev(self.times)
            print(f"  Std Dev: {std_dev*1000:.2f}ms")


async def test_health_endpoint(client: AsyncClient, results: LoadTestResults, num_requests: int = 100):
    """Load test the health endpoint."""
    for _ in range(num_requests):
        try:
            start = time.perf_counter()
            response = await client.get("/api/v1/health")
            elapsed = time.perf_counter() - start

            if response.status_code == 200:
                results.add_result(elapsed)
            else:
                results.add_error()
        except Exception as e:
            print(f"Error: {e}")
            results.add_error()


async def test_create_workflow(client: AsyncClient, results: LoadTestResults, num_requests: int = 50):
    """Load test workflow creation."""
    workflow_template = {
        "name": "Load Test Workflow",
        "description": "Workflow for load testing",
        "type": "custom",
        "nodes": [
            {"id": "n1", "type": "INPUT", "name": "Input", "config": {}},
            {"id": "n2", "type": "OUTPUT", "name": "Output", "config": {}},
        ],
        "edges": [
            {"id": "e1", "source_id": "n1", "target_id": "n2", "type": "DIRECT"},
        ],
    }

    for i in range(num_requests):
        try:
            workflow = workflow_template.copy()
            workflow["name"] = f"Workflow {i}"

            start = time.perf_counter()
            response = await client.post("/api/v1/workflows", json=workflow)
            elapsed = time.perf_counter() - start

            if response.status_code == 201:
                results.add_result(elapsed)
            else:
                results.add_error()
        except Exception as e:
            print(f"Error: {e}")
            results.add_error()


async def test_list_workflows(client: AsyncClient, results: LoadTestResults, num_requests: int = 100):
    """Load test listing workflows."""
    for _ in range(num_requests):
        try:
            start = time.perf_counter()
            response = await client.get("/api/v1/workflows")
            elapsed = time.perf_counter() - start

            if response.status_code == 200:
                results.add_result(elapsed)
            else:
                results.add_error()
        except Exception as e:
            print(f"Error: {e}")
            results.add_error()


async def test_create_execution(client: AsyncClient, workflow_id: str, results: LoadTestResults, num_requests: int = 50):
    """Load test execution creation."""
    execution_template = {
        "workflow_id": workflow_id,
        "inputs": {"data": "test"},
    }

    for _ in range(num_requests):
        try:
            start = time.perf_counter()
            response = await client.post("/api/v1/executions", json=execution_template)
            elapsed = time.perf_counter() - start

            if response.status_code == 201:
                results.add_result(elapsed)
            else:
                results.add_error()
        except Exception as e:
            print(f"Error: {e}")
            results.add_error()


async def main():
    """Run all load tests."""
    print("=" * 60)
    print("LangGraph Workflow Engine - Load Testing")
    print("=" * 60)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Test 1: Health endpoint
        health_results = LoadTestResults("Health Endpoint")
        print("\nRunning health endpoint tests...")
        await test_health_endpoint(client, health_results, 100)
        health_results.print_summary()

        # Test 2: List workflows
        list_results = LoadTestResults("List Workflows")
        print("Running list workflows tests...")
        await test_list_workflows(client, list_results, 50)
        list_results.print_summary()

        # Test 3: Create workflow
        create_wf_results = LoadTestResults("Create Workflow")
        print("Running create workflow tests...")
        await test_create_workflow(client, create_wf_results, 30)
        create_wf_results.print_summary()

        # Get a workflow for execution tests
        print("Creating test workflow for execution tests...")
        response = await client.post(
            "/api/v1/workflows",
            json={
                "name": "Test Workflow for Execution",
                "nodes": [
                    {"id": "n1", "type": "INPUT", "name": "Input", "config": {}},
                    {"id": "n2", "type": "OUTPUT", "name": "Output", "config": {}},
                ],
                "edges": [{"id": "e1", "source_id": "n1", "target_id": "n2", "type": "DIRECT"}],
            }
        )

        if response.status_code == 201:
            workflow_id = response.json()["id"]

            # Test 4: Create execution
            create_exec_results = LoadTestResults("Create Execution")
            print("Running create execution tests...")
            await test_create_execution(client, workflow_id, create_exec_results, 30)
            create_exec_results.print_summary()

        # Print summary
        print("\n" + "=" * 60)
        print("Load Testing Summary")
        print("=" * 60)
        total_requests = (
            health_results.total_requests
            + list_results.total_requests
            + create_wf_results.total_requests
            + (create_exec_results.total_requests if 'create_exec_results' in locals() else 0)
        )
        total_errors = (
            health_results.errors
            + list_results.errors
            + create_wf_results.errors
            + (create_exec_results.errors if 'create_exec_results' in locals() else 0)
        )

        overall_success = ((total_requests - total_errors) / total_requests * 100) if total_requests > 0 else 0
        print(f"\nTotal Requests: {total_requests}")
        print(f"Total Errors: {total_errors}")
        print(f"Overall Success Rate: {overall_success:.1f}%")

        if total_errors == 0:
            print("\n✓ All tests passed! System is performing well under load.")
        else:
            print(f"\n⚠ {total_errors} errors detected. Review logs for details.")


if __name__ == "__main__":
    asyncio.run(main())
