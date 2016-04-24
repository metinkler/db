rm /scratch/421/ncowen/galactic-data/gosearch/2016-03-13T22-00-00Z/*
cd /scratch/421/ncowen/galactic-data/gosearch/2016-03-13T22-00-00Z
git commit -am "removed data"
git push origin gh-pages
cd /scratch/421/ncowen/db/app/graph_workspace/families
cp links.bin /scratch/421/ncowen/galactic-data/gosearch/2016-03-13T22-00-00Z/
cp labels.json /scratch/421/ncowen/galactic-data/gosearch/2016-03-13T22-00-00Z/
cp data/positions.bin /scratch/421/ncowen/galactic-data/gosearch/2016-03-13T22-00-00Z/
cd /scratch/421/ncowen/galactic-data/gosearch/2016-03-13T22-00-00Z
git add .
git commit -am "updated data"
git push origin gh-pages
git push origin --delete gh-pages ; git push origin gh-pages
cd /scratch/421/ncowen/db/app/graph_workspace/families
