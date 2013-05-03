Ganeti High Availability
========================

Project to make use of pacemaker to HA Ganeti Master and related

Content:

	ganeti		init script that is cluster-aware (not autostart masterd)
	GanetiMaster	OCF resource agent for Ganeti Master role
	clumon.py	daemon to monitor CoroSync status and report it to
			Ganeti underlying cluster status (online/offline/drained)
			This is a temporary name until a useful state is reached


*WARNING* 
This is ALPHA software, proceed at your risk
