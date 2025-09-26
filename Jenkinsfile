pipeline{
    agent any
    environment{
        DOCKER_HUB_REPO = "tysonbaretto/ai-budy"
        DOCKER_HUB_CREDENTIALS_ID = "dockerhub-token"
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }
    stages{
        stage("Checkout GitHub"){
            steps {
                echo 'Checking out code from GitHub...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/tysonbarreto/AIOps_Groq_Quiz_Buddy.git']])
            }
        }

        stage("Build docker image"){
            steps {
                script {
                    echo "Building Docker Image..."
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:${IMAGE_TAG}")
                }
            }
        }

        stage("Push image to dockerHub"){
            steps {
                script {
                    echo "Pushing Image to DockerHub..."
                    docker.withRegistry("https://registry.hub.docker.com", "${DOCKER_HUB_CREDENTIALS_ID}"){
                    dockerImage.push("${IMAGE_TAG}")
                    }
                }
            }
        }

        stage("Update deployment manifest with latest image"){
            steps {
                script {
                    echo "Pushing Image to DockerHub..."
                    sh '''
                    sed -i "s|image: tysonbaretto/ai-budy/ai-quiz-budy:.*|image: tysonbaretto/ai-budy/ai-quiz-budy:${IMAGE_TAG}|" manifests/deployment.yaml
                    cat manifests/deployment.yaml
                    '''
                }
            }
        }

        stage("Commit the updated manifest deployment yaml file"){
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId:"github-token", usernameVariable: "GIT_USER", passwordVariable: "GIT_PASS")]){
                    echo "Commiting the updated manifest..."
                    sh '''
                    git config user.name "tysonbarreto"
                    git config user.email "tysonbarretto1991@gmail.com"
                    git add manifests/deployment.yaml
                    git commit -m "manifests/deployment.yaml updated image tag to ${IMAGE_TAG}" || echo "No changes to commit"
                    git push https://${GIT_USER}:${GIT_PASS}@github.com/tysonbarreto/AIOps_Groq_Quiz_Buddy.git HEAD:main
                    '''
                }
            }
        }
    }

        stage("Setup kubectl and argocd cli inside Jenkins"){
            steps {
                script {
                    sh '''
                    echo 'installing Kubectl & ArgoCD cli...'
                    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                    chmod +x kubectl
                    mv kubectl /usr/local/bin/kubectl
                    curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
                    chmod +x /usr/local/bin/argocd
                    '''
                }
            }
        }

        stage('Apply Kubernetes & Sync App with Argo CD'){
            steps {
                script {
                    kubeconfig(credentialsId: 'kubeconfig', serverUrl: 'https://192.168.49.2:8443'){
                        sh '''
                        argocd login 34.60.75.28:31704 --username admin --password $(kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d) --insecure
                        argocd app sync ai-quiz-budy
                        '''
                }
            }
        }
    }
}
}