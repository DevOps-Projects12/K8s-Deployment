pipeline {

  environment {
    dockerimagename = "siri2025/employee1"
    dockerImage = ""
  }

  agent any

  stages {

   stage('Checkout Source') {
  steps {
         git branch: 'feature/devops-test',
        credentialsId: 'github-creds',
        url: 'https://github.com/DevOps-Projects12/K8s-Deployment.git'
  }
}

    stage('Build image') {
      steps{
        script {
          dockerImage = docker.build dockerimagename
        }
      }
    }

    stage('Pushing Image') {
      environment {
               registryCredential = 'dockerhublogin'
           }
      steps{
        script {
          docker.withRegistry( 'https://registry.hub.docker.com', registryCredential ) {
            dockerImage.push("latest")
          }
        }
      }
    }

    stage('Deploying App to Kubernetes') {
      steps {
        script {
          kubernetesDeploy(configs: "deploymentservice.yml", kubeconfigId: "kubernetes")
        }
      }
    }

  }

}
