pipeline{
    agent any
    environment{
        DOCKER_HUB_REPO = "tysonbaretto/ai-quiz-budy"
        DOCKER_HUB_CREDENTIALS_ID = "dockerhub-token"
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }
    stages{
        stage("Checkout GitHub"){
            steps{
                echo 'Checking out code from GitHub...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/tysonbarreto/AIOps_Groq_Quiz_Buddy.git']])
            }
        }

        stage("Build docker image"){
            steps{
                script{
                    echo "Building Docker Image..."
                }
            }
        }

        stage("Push image to dockerHub"){
            steps{
                script{
                    echo "Pushing Image to DockerHub..."
                }
            }
        }

        stage("Update deployment manifest with latest image"){
            steps{
                script{
                    echo "Pushing Image to DockerHub..."
                }
            }
        }
    }
}