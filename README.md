# hsi-hackathon

Welcome

This is an open ended Hackathon.
We have proviced you with a dataset: https://zenodo.org/records/3241923

This dataset has bene predownloaded onto Maxwell into a shared folder that you can all access.




Attached is an example slurm script "runScript.sh"

#SBATCH --nodelist=agpu004 <---- This line will run the job on gpu4 change the number so you can run on different cards and avoid queueing for the same card.



Running this will then run the hsipy.py file which will store its ouputs inthe "output" folder.

The job should take a few seconds to run.

