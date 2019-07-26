node {
    stage('Parallel Run') {
        parallel linux: {
            node('ubuntu') {
                try {
                    stage('U: SCM') {
                        cleanWs()
                        checkout scm
                    }
                    withPythonEnv('python3') {

                        stage('U: PyEnv Setup') {
                            sh 'pip install nose'
                            sh 'pip install coverage'
                        }


                        stage('U: Unit Tests'){
                            sh 'python -m nose -v'
                        }


                        stage('U: Coverage') {
                                sh 'coverage run src/dict_factory.py'
                                sh 'coverage run src/directory_management.py'
                                sh 'coverage run src/file_management.py'
                                sh 'coverage run src/linux_system.py'
                                sh 'coverage run src/time_stamper.py'
                                sh 'coverage html'
                            }

                        stage('U: Run Script') {
                            sh 'python src/check_os.py'
                        }

                        stage('U: Archival') {
                            publishHTML(target: [allowMissing         : true,
                                                 alwaysLinkToLastBuild: false,
                                                 keepAll              : true,
                                                 reportDir            : 'htmlcov/',
                                                 reportFiles          : 'index.html',
                                                 reportName           : 'Ubuntu Code Coverage',
                                                 reportTitles         : ''])
                            archiveArtifacts 'Inventory_store/*.json'
                        }
                    }
                    stage('U: Deploy') {
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
                            stage('W: SCM') {
                                echo 'cloning code'
                                cleanWs()
                                checkout scm
                            }
                            withPythonEnv('python3') {


                                stage('W: PyEnv Setup') {
                                    echo 'Setting up virtual environment and install dependencies'
                                    bat 'python -m pip install --upgrade pip'
                                    bat 'pip install nose'
                                    bat 'pip install coverage'
                                }


                                stage('W: Unit Tests') {
                                    echo 'Running unittests'
                                    bat 'python -m nose -v'
                                }


                                stage('W: Coverage Tests') {
                                    echo 'Running Code Coverage Tests'
                                        bat 'coverage run src/dict_factory.py'
                                        bat 'coverage run src/directory_management.py'
                                        bat 'coverage run src/file_management.py'
                                        bat 'coverage run src/time_stamper.py'
                                        bat 'coverage run src/windows_system.py'
                                        bat 'coverage html'

                                }


                                stage('W: Run Script') {
                                    echo 'Running the Script'
                                    bat 'python src/check_os.py'
                                }


                                stage('W: Archival') {
                                    publishHTML(target: [allowMissing         : true,
                                                         alwaysLinkToLastBuild: false,
                                                         keepAll              : true,
                                                         reportDir            : 'htmlcov/',
                                                         reportFiles          : 'index.html',
                                                         reportName           : 'Windows Code Coverage',
                                                         reportTitles         : ''])
                                    archiveArtifacts 'Inventory_store/*.json'
                                }
                            }

                            stage('W: Deploy') {
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
