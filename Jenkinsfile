pipeline {
    agent any

    environment {
        GHCR_IMAGE = 'ghcr.io/ce-sdpx-ceseejai/simple-api:latest'
        REPO_URL = 'https://github.com/CE-SDPX-CESeejai/simple-api.git'
        ROBOT_REPO_URL = 'https://github.com/CE-SDPX-CESeejai/simple-api-robot.git'
        GHCR_USERNAME = 'ce-sdpx-ceseejai'
        GHCR_TOKEN = credentials('GHCR_PAT')
    }

    stages {
        stage('Verify Repository Checkout') {
            steps {
                script {
                    echo 'Checking if repository was checked out correctly...'
                    sh '''
                    ls -la
                    if [ ! -f "app.py" ]; then
                        echo "ERROR: Expected files not found in workspace!"
                        exit 1
                    fi
                    '''
                }
            }
        }

        stage('Build Docker Image with Dependencies') {
            agent { label 'test' }
            steps {
                script {
                    echo 'Building Docker image with dependencies...'
                    sh 'docker build -t $GHCR_IMAGE .'
                }
            }
        }

        stage('Run Container on Test VM') {
            agent { label 'test' }
            steps {
                script {
                    echo 'Stopping any existing container...'
                    sh 'docker stop simple-api-test || true'
                    sh 'docker rm simple-api-test || true'

                    echo 'Running container on test environment...'
                    sh 'docker run -d --name simple-api-test -p 5000:5000 $GHCR_IMAGE'
                    sleep(5)
                }
            }
        }

        stage('Clone simple-api-robot Repository') {
            agent { label 'test' }
            steps {
                script {
                    echo 'Cloning simple-api-robot repository...'
                    withCredentials([usernamePassword(credentialsId: 'GITHUB_CREDENTIALS', usernameVariable: 'GITHUB_USERNAME', passwordVariable: 'GITHUB_PAT')]) {
                        sh '''
                        rm -rf simple-api-robot
                        git clone https://${GITHUB_USERNAME}:${GITHUB_PAT}@github.com/CE-SDPX-CESeejai/simple-api-robot.git
                        if [ ! -d "simple-api-robot" ]; then
                            echo "ERROR: Cloning failed, directory does not exist!"
                            exit 1
                        fi
                        '''
                    }
                }
            }
        }

        stage('Run Robot Framework Tests on Test VM') {
            agent { label 'test' }
            steps {
                script {
                    echo 'Running Robot Framework tests inside Docker container...'
                    sh '''
                    if [ ! -d "simple-api-robot" ]; then
                        echo "ERROR: simple-api-robot directory not found!"
                        exit 1
                    fi

                    # Copy tests into container
                    docker cp simple-api-robot simple-api-test:/app/simple-api-robot

                    # Run tests inside container
                    docker exec simple-api-test robot /app/simple-api-robot/tests
                    '''
                }
            }
        }

        stage('Push Image to GitHub Container Registry') {
            agent { label 'test' }
            steps {
                script {
                    echo 'Logging into GitHub Container Registry...'
                    sh 'echo $GHCR_TOKEN | docker login ghcr.io -u $GHCR_USERNAME --password-stdin'

                    echo 'Pushing image to GitHub Container Registry...'
                    sh 'docker push $GHCR_IMAGE'
                }
            }
        }

        stage('Deploy on Pre-production VM') {
            agent { label 'preprod' }
            steps {
                script {
                    echo 'Logging into GitHub Container Registry...'
                    sh 'echo $GHCR_TOKEN | docker login ghcr.io -u $GHCR_USERNAME --password-stdin'

                    echo 'Pulling image from GitHub Container Registry...'
                    sh 'docker pull $GHCR_IMAGE'

                    echo 'Stopping existing container (if any)...'
                    sh 'docker stop simple-api-preprod || true'
                    sh 'docker rm simple-api-preprod || true'

                    echo 'Running new container in pre-production...'
                    sh 'docker run -d --restart unless-stopped --name simple-api-preprod -p 5000:5000 $GHCR_IMAGE'
                }
            }
        }
    }

    post {
        always {
            script {
                echo 'Cleaning up test environment...'
                sh 'docker stop simple-api-test || true'
                sh 'docker rm simple-api-test || true'
            }
        }
    }
}
