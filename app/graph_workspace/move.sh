rm ~/workspace/galactic-data/cran/2016-04-20T14-30-00Z/*
cd ~/workspace/galactic-data/cran/2016-04-20T14-30-00Z
git commit -am "removed data"
git push origin gh-pages
cd ~/workspace/db/app/
cp links.bin ~/workspace/galactic-data/cran/2016-04-20T14-30-00Z
cp labels.json ~/workspace/galactic-data/cran/2016-04-20T14-30-00Z
cp data/positions.bin ~/workspace/galactic-data/cran/2016-04-20T14-30-00Z
cd ~/workspace/galactic-data/cran/2016-04-20T14-30-00Z
git add .
git commit -am "updated data"
git push origin gh-pages
cd ~/workspace/db/app/
