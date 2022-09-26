FROM alpine:latest
LABEL maintainer="Jalal Hosseini - @artronics"

RUN apk add --update bash py3-pip terraform
RUN pip install invoke

CMD /bin/bash
