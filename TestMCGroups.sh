# Automate MC Group testing
# Here, you:
#   - provide list of MC Groups
#   - for each interface on this box, for each MC Groups
#       -- Subscribe for 2 secs
#       -- Unsubscribe
# e.g. TestMCGroups.sh '233.0.0.1 10000' '233.0.0.1 10001' '233.0.0.1 10002'

# Get arguement list
# use 'shift' if you want to skip a few
GROUPS=("$@")

INTF_PREFIX='intf'
# assuming i have 2 interfaces and they are appropriately named
for i in 1 2; do
    # get IP addtress for this interface
    ip=`ifconfig | grep -A1 ${INTF_PREFIX}${i} | sed -r 's/^.+ inet ([^ ]+) .+$/\1/'`

    # try and subscribe to each multicast group
    for g in "${GROUPS[@]}"; do \
        echo '#******************************************************************************************'
        echo "# Trying ${INTF_PREFIX}${i} on ${g}"
        echo '#******************************************************************************************'
        cmd="./TestMulticastGroupSubscription.py ${ip} ${g}"
        echo "Doing ${cmd}"

        # run in background
        ${cmd} &

        # get PID of this backgroupd command
        PID=$!
        wcho "    PID is ${PID}"

        # sleep for a bit and let it run, then kill it
        sleep 2
        kill -9 ${PID}
    done
done

        
