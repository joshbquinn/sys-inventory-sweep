stage('Test') {
    parallel linux: {
        node('ubuntu') {
            try {
                stage('SCM checkout') {
                    checkout scm
                }
                stage('Set Environment') {
                    echo "-=- preparing project environment -=-"
                    // Get Python dependencies
                    echo "Set up virtual env and pip install nose and other app dependencies"
                }
                stage('Tests') {
                    echo 'nosetests test/*'
                }
                stage('Run Script') {
                    sh 'python src/system_inventory.py'

                }
                stage('Archival') {
                    archiveArtifacts 'Inventory_store/*/*.json'
                }
                stage('Deploy') {
                    sh 'echo pacage up distribution of app'
                }
            }catch(err) {
                notify("Error ${err}")
                currentBuild.result == 'Failure'

            }
            finally {
                echo 'junit **/target/*.xml'
            }
        }
    },
            windows: {
                node('windows') {
                    try {
                        stage('SCM checkout') {
                            checkout scm
                        }
                        stage('Set Environment') {
                            // Get Python dependencies
                            bat "echo Set up virutal env and pip install nose and other app dependencies"
                        }
                        stage('Tests') {
                            echo 'nosetests test/*'
                        }
                        stage('Run Script') {
                            bat 'python src/system_inventory.py'

                        }
                        stage('Archival') {
                            archiveArtifacts 'Inventory_store/*/*.json'
                        }
                        stage('Deploy') {
                            bat 'echo package up distribution of app'
                        }
                    }catch(err) {
                        notify("Error ${err}")
                        currentBuild.result == 'Failure'

                    }
                    finally {
                        echo 'junit **/target/*.xml'
                    }
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