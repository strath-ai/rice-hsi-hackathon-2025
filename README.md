# hsi-hackathon

Welcome

This is an open ended Hackathon.
We have proviced you with a dataset: https://zenodo.org/records/3241923

**RGB and VIS/NIR Hyperspectral Imaging Data for 90 Rice Seed Varieties**


This dataset has been predownloaded onto Maxwell into a shared folder that you can all access.

The dataset can be found on maxwell at: /uoa/scratch/shared/2025_hackathon/RGB_and_VIS-NIR_HSI_data_for_90_rice_seed_varieties/RGB_and_VIS-NIR_HSI_data_for_90_rice_seed_varieties




Attached is an example slurm script "runScript.sh"

#SBATCH --nodelist=agpu004 <---- This line will run the job on gpu4 change the number so you can run on different cards and avoid queueing for the same card.



Running this will then run the hsipy.py file which will store its ouputs inthe "output" folder.

The job should take a few seconds to run.

