import vboxapi
import time
import subprocess


class VBoxApi:

    # Global variables
    vboxMgr = None
    vbox = None
    needWriteLock = None

    def __init__(self):
        global vboxMgr, vbox, needWriteLock
        # Create the vbox manager, an get a virtual box
        vboxMgr = vboxapi.VirtualBoxManager(None, None)
        vbox = vboxMgr.getVirtualBox()
        needWriteLock = False

    def runCommand(self, Vm, command):
        global vboxMgr, vbox, needWriteLock

        # All the constants that represent the commands that can be requested
        START_EXECUTION = 'startExecution'
        UNREGISTER_VM = 'unregisterVm'
        CONFIGURE_EXECUTION_HARDWARE = 'configureExecutionHardware'
        CHANGE_EXECUTION_MAC = 'changeExecutionMac'
        RESTORE_EXECUTION_SNAPSHOT = 'restoreExecutionSnapshot'
        SET_UUID = 'sethduuid'

        # List with the commands that lock for write, so they can't run at the same time
        list_excluyent_lock = [START_EXECUTION, UNREGISTER_VM, CONFIGURE_EXECUTION_HARDWARE, RESTORE_EXECUTION_SNAPSHOT, SET_UUID, CHANGE_EXECUTION_MAC]

        needWriteLock = True if command in list_excluyent_lock else False
        if (needWriteLock):
            # Find the machine with the name VmName
            if (isinstance(Vm, list)):
                vm = vbox.findMachine(str(Vm[0]))
            else:
                vm = vbox.findMachine(Vm)
            session = vboxMgr.getSessionObject(vbox)
            # Boolean for knowing if the vm is available or not
            available = not needWriteLock
            # While the machine is not available, keep trying until it is available
            while (not available):
                try:
                    # Try to lock the machine, if its already locked it will throw an exception
                    vm.lockMachine(session, vboxMgr.constants.LockType_Write)
                    # If the line above doesn't throw an exception, the machine is available because it wasn't locked
                    available = True
                    # At the end it have to unlock the machine for letting the agent use it
                    session.unlockMachine()
                except Exception as err:
                    print ('The machine is not available for running the command ' + str(command) + ' , waiting...')
                    # If the machine was locked and it threw an exception, wait five seconds and try again
                    time.sleep(5)
        return self.run_command_in_terminal(Vm, command)

    def run_command_in_terminal(self, Vm, command):
        START_EXECUTION = 'startExecution'
        SHOW_INFO = 'showInfo'
        STOP_EXECUTION = 'stopExecution'
        UNREGISTER_VM = 'unregisterVm'
        REGISTER_VM = 'registerVm'
        RESTART_EXECUTION = 'restartExecution'
        CONFIGURE_EXECUTION_HARDWARE = 'configureExecutionHardware'
        COPY_FILE_ON_EXECUTION = 'copyFileOnExecution'
        TAKE_EXECUTION_SNAPSHOT = 'takeExecutionSnapshot'
        DELETE_EXECUTION_SNAPSHOT = 'deleteExecutionSnapshot'
        CHANGE_EXECUTION_MAC = 'changeExecutionMac'
        COPY_FILE_ON_EXECUTION = 'copyFileOnExecution'
        RESTORE_EXECUTION_SNAPSHOT = 'restoreExecutionSnapshot'
        LIST_VMS = 'listVms'
        CLONE_IMAGE = 'cloneImage'
        CHECK_EXECUTIONS = 'checkExecutions'
        SET_UUID = 'sethduuid'
        EXECUTE_COMMAND = 'executeCommandInVm'
        SUCCESS = 'Task done successfully'
        ERROR = 'The task couldn\'t be done, error: '

        # Now that you know that the machine is available, run the command
        if command == START_EXECUTION:
            proc = subprocess.Popen(['VBoxManage startvm ' + Vm + ' --type headless'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == SHOW_INFO:
            proc = subprocess.Popen(['VBoxManage showvminfo ' + Vm], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed, Result: ' + str(stdout) + '\n'))
        elif command == STOP_EXECUTION:
            proc = subprocess.Popen(['VBoxManage controlvm ' + Vm + ' poweroff'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == REGISTER_VM:
            # In this case Vm can't be the image name, have to be the 'image.getMainFile().getExecutableFile().getPath()'
            proc = subprocess.Popen(['VBoxManage registervm ' + Vm], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == UNREGISTER_VM:
            proc = subprocess.Popen(['VBoxManage unregistervm ' + Vm], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == RESTART_EXECUTION:
            proc = subprocess.Popen(['VBoxManage controlvm ' + Vm + ' reset'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == CONFIGURE_EXECUTION_HARDWARE:
            # In this case Vm can't be the image name, it have to be an array with [VmName, VmNewMemory, VmNewCpus]
            proc = subprocess.Popen(['VBoxManage modifyvm ' + Vm[0] + ' --memory ' + Vm[1] + ' --cpus ' + Vm[2]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == COPY_FILE_ON_EXECUTION:
            # In this case Vm can't be the image name, it have to be an array with [VmName, username, password, vm-destination, host-source]
            print(str('VBoxManage guestcontrol ' + Vm[0] + ' --username ' + Vm[1] + ' --password ' + Vm[2] + ' copyto --target-directory ' + Vm[3] + ' ' + Vm[4]))
            proc = subprocess.Popen(['VBoxManage guestcontrol ' + Vm[0] + ' --username ' + Vm[1] + ' --password ' + Vm[2] + ' copyto --target-directory ' + Vm[3] + ' ' + Vm[4]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + ' unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == TAKE_EXECUTION_SNAPSHOT:
            # In this case Vm can't be the image name, it have to be an array with [VmName, SnapshotName]
            proc = subprocess.Popen(['VBoxManage snapshot ' + Vm[0] + ' take ' + Vm[1]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == DELETE_EXECUTION_SNAPSHOT:
            # In this case Vm can't be the image name, it have to be an array with [VmName, SnapshotName]
            proc = subprocess.Popen(['VBoxManage snapshot ' + Vm[0] + ' delete ' + Vm[1]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == CHANGE_EXECUTION_MAC:
            # In this case Vm can't be the image name, it have to be an array with [VmName, networkInterface.getDisplayName()]
            proc = subprocess.Popen(['VBoxManage modifyvm ' + Vm[0] + ' --bridgeadapter1 ' + Vm[1] + ' --macaddress1 auto'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == RESTORE_EXECUTION_SNAPSHOT:
            proc = subprocess.Popen(['VBoxManage snapshot ' + Vm + ' restorecurrent'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == LIST_VMS:
            proc = subprocess.Popen(['VBoxManage list vms'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed, Result: ' + str(stdout) + str('\n')))
        elif command == CLONE_IMAGE:
            # In this case Vm can't be the image name, it have to be an array with [VmName, dest.getImageName(), dest.getMainFile().getExecutableFile().getParentFile().getParentFile().getAbsolutePath()]
            proc = subprocess.Popen(['VBoxManage clonevm ' + Vm[0] + ' --snapshot unacloudbase --name ' + Vm[1] + ' --basefolder ' + Vm[2] + ' --register'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == CHECK_EXECUTIONS:
            proc = subprocess.Popen(['VBoxManage list runningvms'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed, Result: ' + str(stdout) + str('\n')))
        elif command == SET_UUID:
            # In this case Vm can't be the image name, it have to be like image.getMainFile().getFilePath().replaceAll(".vbox", ".vdi")).split(":")[1].trim()
            proc = subprocess.Popen(['VBoxManage internalcommands sethduuid ' + Vm], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
        elif command == EXECUTE_COMMAND:
            # In this case Vm can't be the image name, it have to be like [VmName, command, username, password]
            proc = subprocess.Popen(['VBoxManage guestcontrol ' + Vm[0] + ' ' + Vm[1] + ' --username ' + Vm[2] + ' --password ' + Vm[3]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                if stderr is not None:
                    return (ERROR + stderr)
                else:
                    return (ERROR + 'unkown')
            else:
                return (SUCCESS + str(': Command ' + command + ' executed \n'))
