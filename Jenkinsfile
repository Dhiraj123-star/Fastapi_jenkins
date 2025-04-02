pipeline {
    agent any

    environment {
        IMAGE_NAME = "dhiraj918106/fastapi_jenkins"  // Your Docker Hub repository
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[url: 'https://github.com/Dhiraj123-star/Fastapi_jenkins.git']]
                    ])
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker Image..."
                    docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'docker-hub-credentials', variable: 'DOCKERHUB_PASSWORD')]) {
                    sh '''
                        echo "Logging in to Docker Hub..."
                        echo $DOCKERHUB_PASSWORD | docker login -u dhiraj918106 --password-stdin
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                    echo "Pushing Docker Image to Docker Hub..."
                    docker push $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                    echo "Pulling latest image and starting container..."
                    docker-compose pull
                    docker-compose up -d
                '''
            }
        }
    }

    post {
        failure {
            echo "❌ Build failed! Check logs for details."
        }
        success {
            echo "✅ Deployment successful! FastAPI is running."
        }
    }
}
