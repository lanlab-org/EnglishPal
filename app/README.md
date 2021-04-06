How to run EnglishPal
===========================



Hui Lan <hui.lan@cantab.net>
1 November 2019





Run it on a local machine
-------------------------

python3 main.py






Run it within Docker
--------------------

Assuming that docker has been installed...


ssh to ubuntu@118.25.96.118
cd to /home/lanhui/englishpal

# Stop service
sudo service docker restart

# Rebuild container. Run this after modifying the source code.
sudo docker build -t englishpal .

# Run the application
sudo docker run -d -p 90:80 -v /home/lanhui/englishpal/app/static/frequency:/app/static/frequency -t englishpal  # for permanently saving data
sudo docker run -d -p 90:80 -t englishpal # data will be lost after existing

# Save space.  Run it after sudo docker run
sudo docker system prune -a -f


# Other commands
sudo docker ps -a

sudo docker logs image_name, where image name could be obtained from sudo docker ps.

build.sh contains all the above commands.  Run "sudo ./build.sh" to rebuild the web application.



Update articles
---------------

pscp wordfreqapp.db lanhui@118.25.96.118:/home/lanhui/englishpal/app/static



Feedback
---------

Tianhua people
~~~~~~~~~~~~~~~~

Need a smart phone app.  I use phone a lot.

Can take a picture for text.  Automatic translation.

You cannot ask students to use computers.


Usability testing
~~~~~~~~~~~~~~~~~~~~~~

Respondent 1 --- Paid 10 yuan

“成为会员”改成“注册”

“登出”改成“退出”

“收集生词吧”改成“生词收集栏”

***不要自动显示下一篇

需要有“上一篇”、“下一篇”

Internal server error when register using an email address.
