# hsi-hackathon


Attached is an example slurm script "runScript.sh"

#SBATCH --nodelist=agpu004 <---- This line will run the job on gpu4 change the number so you can run on different cards and avoid queueing for the same card.



Running this will then run the hsipy.py file which will store its ouputs inthe "output" folder.

The job should take a few seconds to run.

