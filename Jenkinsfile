pipeline {
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = 'rugged-sentry-454806-a8'
        GCLOUD_PATH = 'var/jenkins_home/google-cloud-sdk/bin'
    }

    stages {
        stage('Cloning Github repo to Jenkins')
        {
            steps{
                script {
                    echo 'Cloning Github repo to Jenkins....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Github_Token', url: 'https://github.com/Coderified/E-2-E-MLOPS-Project.git']])
                }
            }
        }
        stage('Setting up Virt Env and install dependencies')
        {
            steps{
                script {
                    echo 'Setting up Virt Env and install dependencies'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
        stage('Building & Pushing Docker img to GCR')
        {
            steps{
                withCredentials([file(credentialsId:'GCP-Key',variable:'GOOGLE_APPLICATION_CREDENTIALS')]){
                        script{
                            echo 'Building & Pushing Docker img to GCR........'
                            sh'''
                            export PATH=$PATH:$(GCLOUD_PATH)
                            
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                            gcloud config set project ${GCP_PROJECT}

                            gcloud auth configure-docker --quiet

                          
                            docker build -t gcr.io/${GCP_PROJECT}/ml-project-latest .

                            
                            docker push gcr.io/${GCP_PROJECT}/ml-project-latest   


                            '''
                        }

                }
            }
        }
        stage('Deploy to Google Cloud Run'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploy to Google Cloud Run.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}


                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ml-project \
                            --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated
                            
                        '''
                    }
                }
            }
        }
    }
}