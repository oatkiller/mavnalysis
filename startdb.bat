call set MAVNAL_DB_HOME=.\data
call pg_ctl start -D %MAVNAL_DB_HOME% &
