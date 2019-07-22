node{

    notify('CI')
    try {

        stage('Checkout'){
            checkout scm
        }

        stage('Run'){
            bat 'python /src/system_inventory.py'
        }

        stage('Archive'){
            archiveArtifacts 'Inventory_store/*/*.json'
        }

    } catch(err){
        notify("Error ${err}")
        currentBuild.result = 'Failure'
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
