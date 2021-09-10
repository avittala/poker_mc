# poker_mc
Web app to find your chance of winning at Texas Hold 'Em

A working version of this project is deployed at [poker-mc.ue.r.appspot.com](poker-mc.ue.r.appspot.com). 
It's run on a small Google server, so please don't send too many requests or it'll break!

# How do I use it?
You put in the cards you have and any you see on the table. The app then runs hundreds of simulations of what the other cards could be to estimate your odds of winning. It makes sure to limit its thinking time to just a few seconds. Finally, it gives you the chance you'll win the round along with an estimate of its uncertainty. 

# What should I use this for?
Any poker related calculation you like! Because it's a web app, it'll work on your phone browser without any effort on your part. A sneaky person could pull out their phone in the middle of a round of betting and run this app to get an edge on the other players. The app is particularly helpful for newbies who don't have an intuitive grasp of how good their hand is. Of course, the fun in poker is tricking other people to under or overestimate your own hand. This app gives you a firm grasp on reality while you trick (and are tricked by) the others around you. 

# What if I want to customize this app?
If you want to have your own personal version of this app running, use and modify the code in the PokerApp folder. 
The easiest way to do this is to use Google Cloud Console:
1. Create a new project in Cloud Console
2. Set it up in App Engine
3. Download the Cloud SDK and make sure it works on your computer
4. Download the PokerApp folder to your computer
5. Go into that folder and type 'gcloud init' in your Terminal
6. When you're ready, type 'gcloud app deploy' to deploy the app!

If you don't want to go through this hassle, feel free to just use the website I've made. As long as not too many people use it, I don't think it'll have any problems. 

# I have suggestions!
If you have any suggestions for improvements, feel free to contact me at my email!


