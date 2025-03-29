pipeline {
    agent any

    environment{
        VENV_DIR = 'venv'
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
    }
    stages {
        stage('Setting up Virt Env and install dependencies')
        {
            steps{
                script {
                    echo 'Setting up Virt Env and install dependencies'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install -upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}