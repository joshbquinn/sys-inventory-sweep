pipeline {
    agent none
    stages {
        stage('Build') {
            agent any
            steps {
                checkout scm
            }
        }

        stage('Environment preparation') {

            echo "-=- preparing project environment -=-"
            // Get Python dependencies
            echo "Set up virutal env and pip install nose and other app dependencies"

        }
        stage('Run Script on Ubuntu') {
            agent {
                label 'ubuntu'
            }
            steps{
                sh 'python src/system_inventory.py'
                echo 'nosetests test/*'
            }

            post {
                always {
                    echo 'store the reports'
                }
            }
        }

        stage('Run Script on Windows') {
            agent {
                label 'windows'
            }
            steps{
                bat 'python src/system_inventory.py'
                echo 'nosetests test/*'
            }

            post {
                always {
                    echo 'store the reports'
                }
            }
        }

        stage('Archive')
        agent any
        steps{
            archiveArtifacts 'Inventory_store/*/*.json'
        }

        if ( currentBuild.result = 'Failure'){
            notify("Error ${err}")
        }
    }
}

def notify(status){
    emailext (
            to: "jbqjenkins@gmail.com",
            subject: "${status}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
            body: """<p>${status}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
        <p>Check console output at <a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a></p>""",
    )
}

//def checkOs(){
//    if (isUnix()) {
//        def uname = sh script: 'uname', returnStdout: true
//        if (uname.startsWith("Darwin")) {
//            return "Macos"
//        }
//
//        else {
//            return "Linux"
//        }
//    }
//    else {
//        return "Windows"
//    }
//}
