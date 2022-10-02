const shell = require('shelljs')

const docker_username = 'artronics'
const docker_image_name = 'pipeline'

module.exports = function (grunt) {
  const getTags = () => {
    const tags = grunt.option('tags')
    if (!tags) {
      grunt.fail.fatal('--tags option is required. It must be a comma separated list of tags')
    }

    return tags.split(',')
  }

  grunt.registerTask('docker-build', 'build docker imag. pass --tags as csv', () => {
    const tags = getTags()
    const tags_opt = tags.map(t => `-t ${docker_username}/${docker_image_name}:${t}`).join(' ')
    shell.exec(`docker build ${tags_opt} .`)
  })
  grunt.registerTask('docker-login', 'login to docker using token from DOCKERHUB_TOKEN environment variable', () => {
    const token = process.env.DOCKERHUB_TOKEN
    if (!token) {
      grunt.fail.fatal('DOCKERHUB_TOKEN environment variable is not set')
    }
    shell.exec(`docker login -u ${docker_username} -p ${token}`)
  })
  grunt.registerTask('docker-push', 'push docker image', () => {
    const tags = getTags()
    const tags_opt = tags.map(t => `-t ${docker_username}/${docker_image_name}:${t}`).join(' ')
    shell.exec(`docker buildx build --push ${tags_opt} .`)
  })
  grunt.registerTask('docker-push-multi', 'build and push for both amd64 and arm64 arch', () => {
    const tags = getTags()
    const tags_opt = tags.map(t => `-t ${docker_username}/${docker_image_name}:${t}`).join(' ')
    shell.exec(`docker buildx build --platform linux/amd64,linux/arm64 --push ${tags_opt} .`)
  })
  grunt.registerTask('docker-deploy', 'login to docker and then build and push docker image',
    ['docker-login', 'docker-build', 'docker-push'])

}
