def call(Map config = [:]) {

    // ---- Input validation ----
    if (!config.imageName) {
        error "imageName is required"
    }
    if (!config.tag) {
        error "tag is required"
    }
    if (!config.registry) {
        error " registry is required"
    }

    def imageName = config.imageName
    def tag       = config.tag
    def registry  = config.registry
    def workDir   = config.workDir ?: '.'

    echo "Starting Docker build & push"
    echo "Image      : ${imageName}"
    echo "Tag        : ${tag}"
    echo "Registry   : ${registry}"
    echo "Working dir: ${workDir}"

    dir(workDir) {
        sh """
          set -e

          echo "Building Docker image..."
          docker build -t ${imageName}:${tag} .

          echo "  Tagging image for registry..."
          docker tag ${imageName}:${tag} ${registry}/${imageName}:${tag}

          echo " Pushing image to registry..."
          docker push ${registry}/${imageName}:${tag}

          echo " Docker image successfully pushed"
        """
    }
}
