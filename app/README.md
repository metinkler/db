# BoardGame Galaxies

This repository combines visualizations of board games, card games, and domino games.

All visualizations are abridged versions of the Software Galaxies project, available here: http://anvaka.github.io/pm/#/

Please read [operating manual](https://github.com/anvaka/pm/tree/master/about#software-galaxies-documentation) -
it is short and describes basic navigation principles.



# local development on W&M lab computers
First, log into `db` with your William and Mary account. Then type the following commands.
```
cd /scratch/421/
mkdir *personalusername*
cd *personalusername*
git clone https://github.com/metinkler/db.git #or clone using ssh, or just download the zip, up to you
cd db/app
npm i
npm start
```

This will start local development sever with auto-rebuild. To access the application itself, from a different terminal, you will want to hook up the port that the server is talking to on `db` to the same port on your own computer. To do so, type:
```
ssh -L 8081:localhost:8081 userid@db.cs.wm.edu
```

Then, finally navigate to `127.0.0.1:8081` in your browser to see the app!

