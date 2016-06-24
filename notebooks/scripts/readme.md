<h1>Swarm batch script howto</h1>


How to run:
python run_all_swarms.py "path_to_mat_folder"

The script processes all .mat files from the folder and stores results in ./swarms/ directory.

To view results of the script open 'Swarm results viewer' notebook. Make sure that 'mat folder' contains unique EXO 'strategy_xxxxx.mat' files to avoid duplication.

To change template settings edit the 'settings.py' file variables:<br>
STRATEGY_CONTEXT_COMMON – to change common settings for all swarms<br>
BATCH_CONTEXT – to change particular swarm preset settings