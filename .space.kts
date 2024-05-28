/**
* JetBrains Space Automation
* This Kotlin script file lets you automate build activities
* For more info, see https://www.jetbrains.com/help/space/automation.html
*/

job("Build and push Docker") {
    // both 'host.shellScript' and 'host.dockerBuildPush' run on the same host
    host("Build artifacts and a Docker image") {

        dockerBuildPush {
            // Note that if Dockerfile is in the project root, we don't specify its path.
            // We also imply that Dockerfile takes artifacts from ./build and puts them to image
            // e.g. with 'ADD /build/app.jar /root/home/app.jar'

            val spaceRepo = "docker pull lightny.registry.jetbrains.space/p/main/tg-gpt-bot/gpt-bot:latest"
            tags {
                +"$spaceRepo:0.${"$"}JB_SPACE_EXECUTION_NUMBER"
                +"$spaceRepo:lts"
            }
        }
    }
}