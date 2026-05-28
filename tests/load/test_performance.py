from locust import HttpUser, task, between


class WorkflowEngineUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def health_check(self):
        self.client.get("/api/v1/health")

    @task
    def list_workflows(self):
        self.client.get("/api/v1/workflows")

    @task(2)
    def create_workflow(self):
        self.client.post("/api/v1/workflows", json={
            "name": "Load Test Workflow",
            "type": "custom",
        })

    @task
    def get_metrics(self):
        self.client.get("/api/v1/monitoring/summary")

    @task
    def list_tools(self):
        self.client.get("/api/v1/tools")
