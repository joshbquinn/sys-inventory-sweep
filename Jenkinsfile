node {
    stage('Build') {
        parallel linux: {
            node('ubuntu') {
                try {
                    stage('Ubuntu: SCM') {
                        cleanWs()
                        checkout scm
                    }

                    stage('Ubuntu: Pyenv Setup') {
                        withPythonEnv('python3') {

                            sh 'pip install nose'
                            sh 'pip install coverage'
                        }
                    }


                    stage('Ubuntu: Unit Tests'){
                        withPythonEnv('python3') {
                            sh 'python -m nose -v'

                        }
                    }


                    stage('Ubuntu: Coverage Tests') {
                        withPythonEnv('python3') {
                            sh 'coverage run src/dict_factory.py'
                            sh 'coverage run src/directory_management.py'
                            sh 'coverage run src/file_management.py'
                            sh 'coverage run src/linux_system.py'
                            sh 'coverage run src/time_stamper.py'
                            sh 'coverage run src/windows_system.py'
                            sh 'coverage html'
                        }
                    }


                    stage('Ubuntu: Run Script') {
                        withPythonEnv('python3') {
                            sh 'python src/system_inventory.py'
                        }
                    }
                    stage('Archival') {
                        publishHTML(target: [allowMissing         : true,
                                             alwaysLinkToLastBuild: false,
                                             keepAll              : true,
                                             reportDir            : 'htmlcov/',
                                             reportFiles          : 'index.html',
                                             reportName           : 'Code Coverage',
                                             reportTitles         : ''])
                        archiveArtifacts 'Inventory_store/*.json'
                    }
                    stage('Deploy') {
                        sh 'echo package up distribution of app'
                    }

                } catch (err) {
                    notify("Error ${err}")
                    currentBuild.result == 'Failure'

                }
                finally {
                    // rtp parserName: 'HTML', stableText: '${FILE:htmlcov/index.html}'
                }
            }
        },
                windows:{
                    node('windows') {
                        try {
                            stage('Win: SCM') {
                                echo 'cloning code'
                                cleanWs()
                                checkout scm
                            }

                            stage('Win: Pyenv') {
                                echo 'Setting up virtual environment and install dependencies'
                                withPythonEnv('python3') {
                                    bat 'python -m pip install --upgrade pip'
                                    bat 'pip install nose'
                                    bat 'pip install coverage'
                                }
                            }

                            stage('Win: Unit Tests') {
                                echo 'Running unittests'
                                withPythonEnv('python3') {
                                    bat 'python -m nose -v'
                                }
                            }

                            stage('Win: Coverage Tests') {
                                echo 'Running Code Coverage Tests'
                                withPythonEnv('python3') {
                                    bat 'coverage run src/dict_factory.py'
                                    bat 'coverage run src/directory_management.py'
                                    bat 'coverage run src/file_management.py'
                                    bat 'coverage run src/linux_system.py'
                                    bat 'coverage run src/time_stamper.py'
                                    bat 'coverage run src/windows_system.py'
                                    bat 'coverage html'
                                }
                            }


                            stage('Win: Run Script') {
                                withPythonEnv('python3') {
                                    bat 'python src/system_inventory.py'
                                }
                            }

                            stage('Win: Archival') {
                                publishHTML(target: [allowMissing         : true,
                                                     alwaysLinkToLastBuild: false,
                                                     keepAll              : true,
                                                     reportDir            : 'htmlcov/',
                                                     reportFiles          : 'index.html',
                                                     reportName           : 'Code Coverage',
                                                     reportTitles         : ''])
                                archiveArtifacts 'Inventory_store/*.json'
                            }

                            stage('Win: Deploy') {
                                bat 'echo package up distribution of app'
                            }

                        } catch (err) {
                            notify("Error ${err}")
                            currentBuild.result == 'Failure'

                        }
                        finally {

                            // rtp parserName: 'HTML', stableText: '${FILE:htmlcov/index.html}'
                        }
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
