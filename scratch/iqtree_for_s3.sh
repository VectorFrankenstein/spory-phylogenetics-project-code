#!/bin/bash

# Specify the jobs names and metadata here

#PBS -N broad_iaa_data

# the directory before the last / needs to exist for it to work

#PBS -e /shares/baxter/users/rdhakal/errors/pbs/error/
#PBS -o /shares/baxter/users/rdhakal/errors/pbs/output/

#PBS -q normal
#PBS -P baxter
#PBS -l system_metrics=true

# specify the instance type and size here.

#PBS -l nodes=1,instance_type=r5a.8xlarge

# what should be the size of the scratch directory

#PBS -l scratch_size=200

# specify the tasks that will be executed

source ~/.bash_profile

# paths for easy access later

aws_s3_source_loc="s3://ddpsc-baxterlab-data/rijan_backups/data/explore/spores/incomplete/"

aws_s3_destination_loc="s3://ddpsc-baxterlab-data/rijan_backups/data/explore/spores/complete/"

incomplete_path="/shares/baxter/users/rdhakal/s3_drive/rijan_backups/data/explore/spores/incomplete"

# mountpoint 
mount-s3 ddpsc-baxterlab-data s3_drive/

cd /scratch/

for file in "$incomplete_path"
do
    
  base_name="$(basename -- $file)"
  
  base_name_ext="${base_name%.*}"

  aws s3 cp "$aws_s3_source_loc/$base_name" .

  # run iqtree
  iqtree2 -s $base_name -m MFP -nt auto

  #move the file from its original bucket to done bucket

  aws s3 mv "$aws_s3_source_loc/$base_name" "$aws_s3_destination_loc"

  aws s3 mv . "$aws_s3_destination_loc" --exclude "*" --include "$base_name.*" --recursive

done
