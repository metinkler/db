rm /scratch/421/ncowen/galactic-data/rubygems/2015-12-26T23-00-00Z/*
cd /scratch/421/ncowen/galactic-data/rubygems/2015-12-26T23-00-00Z
git commit -am "removed data"
git push origin gh-pages
cd /scratch/421/ncowen/db/app/graph_workspace/designers
cp links.bin /scratch/421/ncowen/galactic-data/rubygems/2015-12-26T23-00-00Z/
cp labels.json /scratch/421/ncowen/galactic-data/rubygems/2015-12-26T23-00-00Z/
cp data/positions.bin /scratch/421/ncowen/galactic-data/rubygems/2015-12-26T23-00-00Z/
cd /scratch/421/ncowen/galactic-data/rubygems/2015-12-26T23-00-00Z
git add .
git commit -am "updated data"
git push origin gh-pages
git push origin --delete gh-pages ; git push origin gh-pages
cd /scratch/421/ncowen/db/app/graph_workspace/designers
