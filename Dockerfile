# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT

##### IMPORTANT #####
# This Dockerfile requires several build arguments to be defined through --build-arg
# See utils/devel/build_dockerfile.sh for an example of how to build this Dockerfile
#####################

FROM curlimages/curl:latest AS downloader

ARG TEST_DATASET_URL='https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/genes/hg38.refGene.gtf.gz'

RUN curl -L "$TEST_DATASET_URL" | gzip -dc > /tmp/test_dataset.txt


FROM python:3.10-bullseye AS builder

ARG src_dir='/tmp/cryptonite'

RUN mkdir -p "$src_dir"
COPY . "$src_dir"

RUN python3 -m pip install --upgrade pip build   \
&& python3 -m build "$src_dir" --outdir /tmp/pkg

FROM python:3.10-slim-bullseye AS tester

COPY --from=downloader /tmp/test_dataset.txt /tmp/
COPY --from=builder /tmp/pkg /tmp/pkg

RUN python3 -m pip install /tmp/pkg/*.whl

RUN python3 -m cryptonite encrypt -k 5 --no-validate < /tmp/test_dataset.txt | \
    python3 -m cryptonite decrypt -k 5 --no-validate | \
    diff -s -q - /tmp/test_dataset.txt

FROM python:3.10-slim-bullseye AS final
COPY --from=tester /tmp/pkg/*.whl /tmp/

RUN python3 -m pip install /tmp/*.whl --no-cache-dir

RUN cryptonite --help
RUN cryptonite --version

CMD [ "cryptonite" ]

# https://github.com/opencontainers/image-spec/blob/main/annotations.md#pre-defined-annotation-keys
LABEL org.opencontainers.image.authors='Roberto Rossini <roberros@uio.no>'
LABEL org.opencontainers.image.url='https://github.com/robomics/2022-sbi-ci-workshop'
LABEL org.opencontainers.image.documentation='https://github.com/robomics/2022-sbi-ci-workshop'
LABEL org.opencontainers.image.source='https://github.com/robomics/2022-sbi-ci-workshop'
LABEL org.opencontainers.image.licenses='MIT'
LABEL org.opencontainers.image.title='2022-sbi-ci-workflow-cryptonite'
