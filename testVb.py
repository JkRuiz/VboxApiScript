import VBApi as vb

START_EXECUTION = 'startExecution'  # Done
SHOW_INFO = 'showInfo'  # Done
STOP_EXECUTION = 'stopExecution'  # Done
UNREGISTER_VM = 'unregisterVm'  # Done
REGISTER_VM = 'registerVm'  # Done
RESTART_EXECUTION = 'restartExecution'  # Done
CONFIGURE_EXECUTION_HARDWARE = 'configureExecutionHardware'  # Done
COPY_FILE_ON_EXECUTION = 'copyFileOnExecution'  # Done
TAKE_EXECUTION_SNAPSHOT = 'takeExecutionSnapshot'  # Done
DELETE_EXECUTION_SNAPSHOT = 'deleteExecutionSnapshot'  # Done
CHANGE_EXECUTION_MAC = 'changeExecutionMac'  # Done (missing a test with a real network interface)
RESTORE_EXECUTION_SNAPSHOT = 'restoreExecutionSnapshot'  # Done
LIST_VMS = 'listVms'  # Done
CLONE_IMAGE = 'cloneImage'  # Done
CHECK_EXECUTIONS = 'checkExecutions'  # Done
SET_UUID = 'sethduuid'

# Constant with the vm name
VM_NAME = 'testVm'
vbClass = vb.VBoxApi()


# Start and stop execution tests
def test_start_stop_test():
    print(vbClass.runCommand(VM_NAME, START_EXECUTION))
    print(vbClass.runCommand(VM_NAME, STOP_EXECUTION))


def clone_image():
    # [VmName, dest.getName() , basefolder(where is gonna be saved)]
    VM_ARR = [VM_NAME, 'cloneVm', '/Users/JuanCamiloRuiz/Downloads/cloneVm']
    print(vbClass.runCommand(VM_NAME, START_EXECUTION))
    print(vbClass.runCommand(VM_ARR, CLONE_IMAGE))


def change_mac():
    def_net = 'eth0'
    # [VmName, networkInterface.getDisplayName()]
    VM_ARR = [VM_NAME, def_net]
    print(vbClass.runCommand(VM_NAME, SHOW_INFO))
    print(vbClass.runCommand(VM_ARR, CHANGE_EXECUTION_MAC))
    print(vbClass.runCommand(VM_NAME, SHOW_INFO))


def configure_hardware():
    # [VmName, VmNewMemory, VmNewCpus]
    VM_CONF = [VM_NAME, '2000', '1']
    print(vbClass.runCommand(VM_NAME, SHOW_INFO))
    print(vbClass.runCommand(VM_CONF, CONFIGURE_EXECUTION_HARDWARE))
    print(vbClass.runCommand(VM_NAME, SHOW_INFO))


# Register and unregister a VM tests
def registerVm_unregisterVm():
    # The image has to be in the virtualBox path Users/JuanCamiloRuiz/Library/VirtualBox/testVm.vbox
    VM_IMAGE = 'testVm.vbox'
    print(vbClass.runCommand(VM_IMAGE, REGISTER_VM))
    print(vbClass.runCommand(VM_NAME, LIST_VMS))
    print(vbClass.runCommand(VM_NAME, UNREGISTER_VM))
    print(vbClass.runCommand(VM_NAME, LIST_VMS))


def registerVm():
    # The image has to be in the virtualBox path Users/JuanCamiloRuiz/Library/VirtualBox/testVm.vbox
    VM_IMAGE = 'testVm.vbox'
    print(vbClass.runCommand(VM_IMAGE, REGISTER_VM))
    print(vbClass.runCommand(VM_NAME, LIST_VMS))


# Start, showinfo, restart, listvms, chechvmsrunning tests | The lock should be share, because the machine can be started and all of the others process should run without having any error
def basics_share_lock_test():
    print(vbClass.runCommand(VM_NAME, START_EXECUTION))
    print(vbClass.runCommand(VM_NAME, SHOW_INFO))
    print(vbClass.runCommand(VM_NAME, RESTART_EXECUTION))
    print(vbClass.runCommand(VM_NAME, LIST_VMS))
    print(vbClass.runCommand(VM_NAME, CHECK_EXECUTIONS))
    print(vbClass.runCommand(VM_NAME, STOP_EXECUTION))
    print(vbClass.runCommand(VM_NAME, CHECK_EXECUTIONS))


# Snapshots test | Taking and deleting a snapshot should have share lock (the can run while machine is ON) but restoring a snapshot is a write lock, so it shouldn't run until the machine is power off
def snapshots_tests():
    # List with parameters of spanshot methods
    VM_ARR = []
    VM_ARR.append(VM_NAME)
    VM_ARR.append('sp1')
    print(vbClass.runCommand(VM_NAME, START_EXECUTION))
    print(vbClass.runCommand(VM_ARR, TAKE_EXECUTION_SNAPSHOT))
    print(vbClass.runCommand(VM_ARR, DELETE_EXECUTION_SNAPSHOT))
    print(vbClass.runCommand(VM_ARR, TAKE_EXECUTION_SNAPSHOT))
    print(vbClass.runCommand(VM_NAME, RESTORE_EXECUTION_SNAPSHOT))


# Copy file test
def copy_file_test():
    # List with parameters of spanshot methods, it has to be [VmName, username, password, host-source, vm-destination]
    VM_ARR = []
    VM_ARR.append(VM_NAME)
    VM_ARR.append('juan')
    VM_ARR.append('juan123')
    VM_ARR.append('home/juan/documents/testLinux.txt')
    VM_ARR.append('/Users/JuanCamiloRuiz/Downloads/test.txt')
    print(vbClass.runCommand(VM_NAME, START_EXECUTION))
    print(vbClass.runCommand(VM_ARR, COPY_FILE_ON_EXECUTION))


if __name__ == '__main__':
    basics_share_lock_test()
