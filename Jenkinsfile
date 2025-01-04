pipeline {
    agent any

    environment {
        ACTIVESTATE_CLI_CACHEDIR = "${WORKSPACE}/.cache"
        ACTIVESTATE_API_KEY = credentials('ACTIVESTATE_API_KEY')
        DOCKER_USERNAME = credentials('DOCKER_USERNAME')
        DOCKER_PASSWORD = credentials('DOCKER_PASSWORD')
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        AWS_REGION = 'us-east-1'
        ECR_REPO_URL = '778602549455.dkr.ecr.us-east-1.amazonaws.com/github-actions'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install State Tool') {
            steps {
                sh 'curl -q https://platform.activestate.com/dl/cli/install.sh | bash -s -n'
            }
        }
        stage('Activate ActiveState Runtime') {
            steps {
                sh '''
                    export PATH="$HOME/.local/ActiveState/StateTool/release/bin:$PATH"
                    state pull
                '''
            }
        }
        stage('Cache ActiveState CLI') {
            steps {
                script {
                    if (fileExists('activestate.yaml')) {
                        echo "ActiveState cache exists"
                    } else {
                        sh "mkdir -p ${env.ACTIVESTATE_CLI_CACHEDIR}"
                    }
                }
            }
        }
        stage('Test with Pytest') {
            steps {
                sh 'state run pytest'
            }
        }
        stage('Build & Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        sh '''
                        docker build -t hasnatabk/github-actions:latest .
                        docker tag hasnatabk/github-actions:latest hasnatabk/github-actions:v1
                        docker push hasnatabk/github-actions:latest
                        '''
                    }
                }
            }
        }
        stage('Build & Push to ECR') {
            steps {
                withAWS(credentials: 'aws-credentials', region: "${AWS_REGION}") {
                    sh '''
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO_URL}
                    docker tag hasnatabk/github-actions:latest ${ECR_REPO_URL}:latest
                    docker push ${ECR_REPO_URL}:latest
                    '''
                }
            }
        }
    }
}
