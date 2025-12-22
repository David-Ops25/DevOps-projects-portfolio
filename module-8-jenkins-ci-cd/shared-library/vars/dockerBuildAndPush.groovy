def call(Map config = [:]) {

    if (!config.imageName) {
        error "imageName is required"
    }
    if (!config.tag) {
        error "tag is required"
    }
    if (!config.registry) {
        error "registry is required"
    }

    def imageName = config.imageName
    def tag       = config.tag
    def registry  = config.registry
    def workDir   = config.workDir ?: '.'

    echo "🚀 Docker Build & Push Started"
    echo "📦 Image: ${imageName}:${tag}"
    echo "📍 Registry: ${registry}"

    dir(workDir) {
        sh """
          set -e
          docker build -t ${imageName}:${tag} .
          docker tag ${imageName}:${tag} ${registry}/${imageName}:${tag}
          docker push ${registry}/${imageName}:${tag}
        """
    }
}

