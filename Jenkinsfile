pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "dhiraj918106/fastapi_jenkins:latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/Dhiraj123-star/Fastapi_jenkins.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker Image..."
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'docker-hub-token', variable: 'DOCKERHUB_TOKEN')]) {
                    script {
                        echo "Logging in to Docker Hub..."
                        sh "echo \$DOCKERHUB_TOKEN | docker login -u dhiraj918106 --password-stdin"
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing Docker Image to Docker Hub..."
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }
    }

    post {
        success {
            echo "✅ Build and push completed successfully!"
        }
        failure {
            echo "❌ Build failed! Check logs for details."
        }
    }
}
