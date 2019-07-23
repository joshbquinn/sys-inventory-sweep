node {
    parallel Linux: {
        node('ubuntu') {
            try {
                stage('SCM checkout') {
                    cleanWs()
                    checkout scm
                }
                stage('Set Python V Environment') {
                    // Get Python dependencies
                    sh "echo set up virtual env and pip install nose and other app dependencies"
                }
                dir("src") {

                    stage('Tests') {
                        sh 'ls'
                        sh 'python -m unittest discover -s ../test'
                    }
                }
                stage('Run Script') {
                    sh 'python src/system_inventory.py'

                }
                stage('Archival') {
                    archiveArtifacts 'Inventory_store/*.json'
                }
                stage('Deploy') {
                    sh 'echo package up distribution of app'
                }
            }catch(err) {
                notify("Error ${err}")
                currentBuild.result == 'Failure'

            }
            finally {
                echo 'junit **/target/*.xml'
                rtp parserName: 'HTML', stableText: '${FILE:Inventory_Store/*.json}'
            }
        }
    },
            Windows: {
                node('windows') {
                    try {
                        stage('SCM checkout') {
                            cleanWs()
                            checkout scm
                        }
                        stage('Set Environment') {
                            // Get Python dependencies
                            bat "echo Set up virutal env and pip install nose and other app dependencies"
                        }
                        dir("src") {
                            stage('Tests') {
                                bat 'ls'
                                bat 'python -m unittest discover -s ../test'
                            }
                        }
                        stage('Run Script') {
                            bat 'python src/system_inventory.py'

                        }
                        stage('Archival') {
                            archiveArtifacts 'Inventory_store/*.json'
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
                        rtp parserName: 'HTML', stableText: '${FILE:Inventory_Store/*.json}'
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