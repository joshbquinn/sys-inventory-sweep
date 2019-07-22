node windows {

    os = checkOs()

    try {

        stage('Checkout') {
            echo "-=- Cloning sourcecode from Git -=-"
            checkout scm
        }

        stage('Environment preparation') {
            steps {
                echo "-=- preparing project environment -=-"
                // Python dependencies
                echo "Set up virutal env and pip install nose and other app dependencies"
            }
        }

        stage('Run Script') {
            echo "-=- Running Script -=-"
            if (os == "Windows") {
                bat 'python src/system_inventory.py'
            } else {
                sh 'python src/system_inventory.py'
            }

        }

        stage('Archive'){
            archiveArtifacts 'Inventory_store/*/*.json'
        }

    } catch (err){
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

def checkOs(){
    if (isUnix()) {
        def uname = sh script: 'uname', returnStdout: true
        if (uname.startsWith("Darwin")) {
            return "Macos"
        }

        else {
            return "Linux"
        }
    }
    else {
        return "Windows"
    }
}
