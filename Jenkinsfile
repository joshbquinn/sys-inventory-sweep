node {
    parallel Linux: {
        node('ubuntu') {
            try {
                stage('SCM checkout') {
                    cleanWs()
                    checkout scm
                }
                stage('Python Environment Setup') {
                    withPythonEnv('python') {
                        sh 'python -m pip install --upgrade pip'
                        sh 'pip install nose'
                        sh 'pip install coverage'
                    }
                }

                stage('Env'){
                    withPythonEnv('python') {

                    }
                }

                stage('Unit Tests') {
                    withPythonEnv('python') {
                        sh 'python -m nose -v'
                    }
                }

                stage ('Coverage Tests') {
                    withPythonEnv('python') {
                        sh 'coverage run src/dict_factory.py'
                        sh 'coverage run src/directory_management.py'
                        sh 'coverage run src/file_management.py'
                        sh 'coverage run src/linux_system.py'
                        sh 'coverage run src/time_stamper.py'
                        sh 'coverage run src/windows_system.py'
                        sh 'coverage html'
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
                junit '**/htmlcov/index.html'
                rtp parserName: 'HTML', stableText: '${FILE:htmlcov/index.html}'
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

                        stage('Virtual Python Env') {
                            withPythonEnv('python') {
                                bat 'python -m pip install --upgrade pip'
                                bat 'pip install nose'
                                bat 'pip install coverage'
                            }
                        }

                        stage('Unit Tests') {
                            withPythonEnv('python') {
                                bat 'python -m nose -v'
                            }
                        }

                        stage('Coverage Tests') {
                            withPythonEnv('python') {
                                bat 'coverage run src/dict_factory.py'
                                bat 'coverage run src/directory_management.py'
                                bat 'coverage run src/file_management.py'
                                bat 'coverage run src/linux_system.py'
                                bat 'coverage run src/time_stamper.py'
                                bat 'coverage run src/windows_system.py'
                                bat 'coverage html'
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
                        junit '**/htmlcov/index.html'
                        rtp parserName: 'HTML', stableText: '${FILE:htmlcov/index.html}'
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
