import vboxapi
import time


def machineAvailable(VmName):
    # Create the vbox manager, an get a virtual box
    vboxMgr = vboxapi.VirtualBoxManager(None, None)
    vbox = vboxMgr.getVirtualBox()
    # Find the machine with the name VmName
    vm = vbox.findMachine(VmName)
    session = vboxMgr.getSessionObject(vbox)
    # Boolean for knowing if the vm is available or not
    available = False

    # While the machine is not available, keep trying until it is available
    while (not available):
        try:
            # Try to lock the machine, if its already locked it will throw an exception
            vm.lockMachine(session, vboxMgr.constants.LockType_Write)
            # If the line above doesn't throw an exception, the machine is available because it wasn't locked
            available = True
            print('The machine was successfully locked')
        except Exception as err:
            print (err)
            # If the machine was locked and it threw an exception, wait five seconds and try again
            time.sleep(5)
    # At the end it have to unlock the machine for letting the agent use it
    session.unlockMachine()
    print('The machine was successfully unlocked')
    return True