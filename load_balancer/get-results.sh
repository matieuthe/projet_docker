cd ~/CLIFspace/CLient/stats/

#Change here the path to your results folder
# (ls -t | tail -1) is for the last directory created
cp -rf $(ls -t | tail -1) /home/strebern/Stage/DockerizedRubis/load_balancer/results

