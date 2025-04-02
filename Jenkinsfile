pipeline {
    agent any

    environment {
        IMAGE_NAME = "dhiraj918106/fastapi_jenkins"  // Your Docker Hub repository
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/Dhiraj123-star/Fastapi_jenkins.git'  // Updated GitHub repo
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'docker-hub-credentials', variable: 'DOCKERHUB_PASSWORD')]) {
                    sh 'echo $DOCKERHUB_PASSWORD | docker login -u dhiraj918106 --password-stdin'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh 'docker push $IMAGE_NAME:$IMAGE_TAG'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh 'docker-compose pull'
                sh 'docker-compose up -d'
            }
        }
    }
}
