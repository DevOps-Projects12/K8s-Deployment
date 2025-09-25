# K8s-Deployment

**Short summary:**
Flask-based Employee Management REST API. Containerized with Docker (siri2025/employee1) and deployed to Kubernetes (Minikube) via deployment.yaml and service.yaml. This README shows exactly how to run and verify the project locally, push the image to DockerHub, and deploy to Minikube.

**Prerequisites:**

- Windows machine with Docker Desktop 
- Minikube installed
- kubectl installed and configured to talk to your Minikube cluster.
- Docker Hub account
- Git 
- Python (only for local run, optional if you test only via Docker).


**1) Run locally (quick smoke test)**

Install dependencies:
cmd: pip install -r requirements.txt

Start the app:
cmd: python app.py

Test endpoints (in a new terminal):

curl http://127.0.0.1:5000/employees
curl -X POST http://127.0.0.1:5000/employees -H "Content-Type: application/json" -d "{\"name\":\"Siri\",\"role\":\"DevOps Engineer\"}"


Expected: JSON responses; POST returns newly created employee.

**2) Build & run with Docker (local container)**

Build the Docker image (tagged for DockerHub):
docker build -t siri2025/employee1:latest .

Run the container mapping port 5000:
docker run -d --name employee1 -p 5000:5000 siri2025/employee1:latest

Verify container & logs:
docker ps
docker logs -f employee1


Test from host:
curl http://localhost:5000/employees

Tip: If you built using a different local image name (e.g., employee1:latest) tag it first:
docker tag employee1:latest siri2025/employee1:latest

**3) Push image to DockerHub**

Login:
docker login -u <username>


Push:
docker push siri2025/employee1:latest
Verify image on DockerHub: https://hub.docker.com/r/siri2025/employee1

**4) Kubernetes deployment (Minikube)**

Files used: k8s/deployment.yaml and k8s/service.yaml (NodePort)

Point kubectl to your cluster (if using Minikube):

minikube start
minikube status
kubectl config current-context   # ensure it points to minikube

Apply manifests:
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

Check resources:
kubectl get pods -o wide
kubectl get svc


View logs / debug pods:
kubectl logs <pod-name>
kubectl describe pod <pod-name>

**5) Accessing service on Minikube (Windows notes)**

minikube service employee-api-service
This command prints and opens a URL (e.g., http://127.0.0.1:60419 or http://192.168.49.2:30001). Keep the terminal open if it uses a tunnel.

If service type is NodePort, you can also use:
minikube ip           # returns minikube VM IP (e.g., 192.168.49.2)
then in browser
http://<minikube-ip>:30001/employees

Note: On Docker driver/Windows, direct node IP access may not work; prefer minikube service or tunnel.

**6) CI/CD Pipeline with Jenkins**

After successfully containerizing and deploying the Employee Management application locally, I integrated a Jenkins pipeline to automate the complete workflow.

**7) Commands to redeploy / update image**

Rebuild and push new image:

docker build -t siri2025/employee1:v1.1 .

docker push siri2025/employee1:v1.1

Update Deployment to use new image and roll:
kubectl set image deployment/employee-api-deployment employee-api=siri2025/employee1:v1.1
kubectl rollout status deployment/employee-api-deployment


To rollback:
kubectl rollout undo deployment/employee-api-deployment

**8) Cleanup commands**

**delete k8s resources**

kubectl delete -f k8s/service.yaml

kubectl delete -f k8s/deployment.yaml

**stop minikube**

minikube stop

**stop and remove docker container and image locally**

docker stop employee1

docker rm employee1

docker rmi siri2025/employee1:latest


**9) Common troubleshooting (short)**

1) curl: Failed to connect — ensure the app process or container is running. Check docker ps or python app.py terminal.
2) Docker errors / named pipe on Windows — start Docker Desktop and wait until it says “Docker is running.”
3) Minikube NodePort not accessible — use minikube service or run minikube tunnel (for LoadBalancer).
4) Image push denied — ensure docker login succeeded and you tagged image as siri2025/employee1:tag.
5) Pod CrashLoopBackOff — kubectl logs <pod> and kubectl describe pod <pod> to see exception. Likely missing env, incorrect image tag, or port misconfiguration.
