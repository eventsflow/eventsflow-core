
DOCKER_IMAGE ?= 'eventsflow-dev:0.1.1-ubuntu'

.PHONY: console
console:
	@ docker run -ti --rm --name eventsflow-console \
		-v $(shell pwd):/app ${DOCKER_IMAGE} \
		-c bash

.PHONY: pre-cleanup
pre-cleanup:
	@ $(shell pwd)/scripts/pre-cleanup.sh

.PHONY: pre-cleanup
post-cleanup:
	@ $(shell pwd)/scripts/post-cleanup.sh

.PHONY: test
test: 
	@ drone exec --event test

# .PHONY: deploy
# deploy:
# 	@ echo "[INFO] Deploy build to Nexus Snapshots" && \
# 		drone exec --build-event deploy

# .PHONY: release
# release:
# 	@ echo "[INFO] Release component and deploy to Nexus Releases" && \
# 		drone exec --event release
# 	git push origin master
# 	git push origin --tags

