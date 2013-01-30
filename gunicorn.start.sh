#!/bin/bash                                                                                                                                                                                  
if [ -f logs/gunicorn.pid ]
then
  source ../envs/leave_env/bin/activate
  hup_out=$(kill -HUP `cat logs/gunicorn.pid` 2>&1)
  echo $hup_out
  if [[ $hup_out =~ .*`echo No such process`*. ]]
  then 
      source ../envs/leave_env/bin/activate
      gunicorn_django -c $(pwd)/gunicorn.conf.py -D
  fi
else
  source ../envs/leave_env/bin/activate
  gunicorn_django -c $(pwd)/gunicorn.conf.py -D
fi
