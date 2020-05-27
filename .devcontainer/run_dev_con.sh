#!/bin/bash
export INFS_DEV_CON='infs_dev'
export WORK_DIR='infs'
docker run -d -it -v $(pwd)/:/mnt/$WORK_DIR -v /var/run/docker.sock:/var/run/docker.sock -w /mnt/$WORK_DIR infs_dev bash