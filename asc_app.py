import os
import sys
import re
import csv
import xml.etree as ET
import py_helper as ph
from py_helper import MountHelper, Msg, DebugMode, DbgMsg, Touch, CmdLineMode
import shutil
import argparse
import configparser
import subprocess
import inspect, platform
from datetime import datetime, timedelta
from pathlib import Path
import time

#
# Variables/Constants
#

sim_mode = False

config_filename = "config.ini"

logs = list()

fpath = r"\\harrypotter.infosec.stonybrook.edu\srv"
uname = r"harrypotter\ejohnfelt"
drv = r"T:"
pw = None

src = f"G:\\f8a60fe2-38c7-4f59-a7cb-6cc011394019.AscVolume"
dst = f"{drv}\\array2\\asc"

missing_filename = r"missing.txt"
log_filename = r"log.txt"
debug_log = r"C:\Temp\debug.txt"
debug_file = None

flag_file = "stop.txt"
interactive = False

def logwrite(logfile, msg, send_to_console=False, callerframe=None):
    """Write message to Log(s)"""
    
    global interactive

    if callerframe is None:
        callerframe = inspect.currentframe().f_back

        module = callerframe.f_code.co_filename
        line = callerframe.f_lineno
        host = platform.node()

    timestamped_msg = f"{datetime.now()} [{host}/{line}/{module}] : {msg}"
    
    if interactive or send_to_console:
        Msg(f"{timestamped_msg}")

    try:
        if type(logfile) is list:
            for log in logfile:
                log.write(f"{timestamped_msg}\n")
                log.flush()
        else:
            logfile.write(f"{timestamped_msg}\n")
            logfile.flush()
    except Exception as err:
        DbgMsg(f"An error occurred - {err} - With log message {msg}")

def Connect(net_path, drv_letter, username, password):
    """Connect to SMB Share"""
    
    connect_command = [ "net", "use", drv_letter, net_path, r"/persistent:no", f"/user:{username}", password ]

    result = None

    try:
        result = subprocess.run(connect_command)
    except Exception as err:
        result = err

    return result

def Disconnect(drv_path):
    """Disconnect from SMB Share"""
    
    disconnect_command = [ "net", "use", drv_path, "/del" ]

    result = None

    try:
        result = subprocess.run(drv_path)
    except Exception as err:
        result = err

    return result

def CheckPath(path_to_check):
    """Check a path"""

    global fpath, uname, pw

    usable = False

    retry_count = 0
    max_retry = 9
    error = None

    while not usable and retry_count < max_retry:
        try:
            if os.path.exists(path_to_check):
                DbgMsg(f"{path_to_check} available")
                usable = True
            else:
                DbgMsg(f"{path_to_check} unavailable, waiting...")
                time.sleep(60)
        except Exception as exp:
            DbgMsg(f"An error occurred during path check for {path_to_check}, not available, {retry_count}")
            error = exp
            break
            
        retry_count += 1
            
    return usable, (retry_count >= max_retry), error

def periodic(logfile, msg, delta, last_done):
    """Write Provided Message Periodically"""

    if (last_done + delta) <= datetime.now():
        logwrite(logfile,msg)
        last_done = datetime.now()

    return last_done

def chkflag(src, dst):
    """Check for early terminate flag"""

    sflag = f"{src}/{flag_file}"
    dflag = f"{dst}/{flag_file}"

    flag_exists = False

    if os.path.exists(sflag):
        os.remove(sflag)
        flag_exists = True
    elif os.path.exists(dflag):
        os.remove(dflag)
        flag_exists = True

    return flag_exists

def add_index(entry, dst):
    """Add Entry to index"""

    try:
        index_file = os.path.join(dst,"index.csv")

        guid = None

        if type(entry) is str:
            guid = os.path.basename(os.path.splitext(entry)[0])
        else:
            guid = os.path.basename(os.path.splitext(entry.name)[0])

        mode = "a"

        xml_file = os.path.join(guid,".xml")

        if not os.path.exists(index_file):
            mode = "w"

        with open(index_file,mode,newline="") as csvfile:
            writer = csv.writer(csvfile)

            date_folder = None

            row = [ guid, date_folder ]

            writer.writerow(row)
    except Exception as err:
        DbgMsg(f"Could not add {dst} to index : {err}")

def indexed(entry,dst):
    """Check to see if source was indexed"""

    is_indexed = False

    index_file = os.path.join(dst,"index.csv")
    guid = os.path.basename(os.path.splitext(entry.name)[0])

    if os.path.exists(index_file):
        with open(index_file,"r",newline="") as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                if row[0] == guid:
                    is_indexed = True

                    break

    return is_indexed

def get_missing(logfile, data, source, destination):
    """Getting source files missing from destination"""

    completed = True
    existing = 0
    missing_dest = 0
    processed = 0
    delta = timedelta(minutes=10)
    last_logged = datetime.now()

    try:
        with os.scandir(src) as srcfldr:
            with open(data,"w",newline="") as csvfile:
                writer = csv.writer(csvfile)
                
                logwrite(logfile, f"Processing {source} items")

                for entry in srcfldr:
                    if entry.is_file():
                        processed += 1
                        dstfile = os.path.join(dst,entry.name)

                        path_ok, timeout, error = CheckPath(dst)

                        if path_ok:
                            if not os.path.exists(dstfile):
                                DbgMsg(f"{entry.name} does not exist in {dst}")
                            
                                row = [ entry.path, dstfile ]

                                writer.writerow(row)
                                missing_dest += 1
                            elif not indexed(entry,destination):
                                # In the event the file was copied but preceded the index
                                add_index(entry, destinations)
                            else:
                                DbgMsg(f"{entry.name} exists in {dst}")
                                existing += 1
                        elif timeout:
                            raise FileNotFoundException(f"{dst} check timed out")
                        elif error is not None:
                            raise FileNotFoundException(f"{dst} is unavailable, an error has occurred")

                    if chkflag(source, destination):
                        logwrite(logfile,"Encountered early terminate flag, terminating")
                        completed = False
                            
                        break

                    last_logged = periodic(logfile, f"Scanning source, processed {processed} files, {missing_dest} missing so far...", delta, last_logged)

                    time.sleep(0.001)
    except Exception as err:
        msg = f"An error occurred with : {err}"
        logwrite(logfile, msg)
        DbgMsg(msg)
        
        completed = False

    if not completed:
        os.remove(data)

    return missing_dest, existing, processed, completed

def copy_known_missing(logfile, missing, srv, dst):
    """
    Copy known missing files destination folder.
    List of missing files supplied in 'missing' list
    """

    DbgMsg("Entering copy_known_missing")
    
    completed = True
    copied_count = 0
    ignore_debug = False
    missing_count = ph.LineCount(missing)

    delta = timedelta(minutes=10)
    last_logged = datetime.now()

    with open(missing,"r",newline='') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            source, destination = row

            if not os.path.exists(destination):
                DbgMsg(f"Copying {source} to {destination}")

                try:
                    path_ok,timeout,error = CheckPath(dst)

                    if path_ok:
                        logwrite(logfile, f"Copying {source} to {destination} @ {datetime.now()}")
                        shutil.copy(source, destination)
                        copied_count += 1
                        add_index(source,destination)
                    elif timeout:
                        raise FileNotFoundError(f"{dst} retries timeout")
                    elif error is not None:
                        raise FileNotFoundError(f"{dst} is not available")
                except Exception as err:
                    msg = f"An error occurred with : {err}"
                    DbgMsg(msg)
                    logwrite(logfile, msg)
                        
                    completed = False

                    break
            else:
                DbgMsg(f"{destination} appears to already exist")
                logwrite(logfile,f"{source} appears to exist in {destination}")

            if chkflag(src,dst):
                logwrite(logfile,"Encountered early terminate flag, terminating")
                completed = False

                break

            last_logged = periodic(logfile, f"Copied {copied_count} of {missing_count} so far...", delta, last_logged)

    os.remove(missing)

    return copied_count, completed

def copy_missing(logfile, src, dst):
    """
    Copy missing files destination folder.

    Executes by reading the source folder and seeing if the file(s) are in the destination, and then copying the ones that are not.
    """

    completed = True
    copied_count = 0

    delta = timedelta(minutes=10)
    last_logged = datetime.now()

    existing = 0
    missing_dest = 0
    processed = 0

    try:
        with os.scandir(src) as srcfldr:
            logwrite(logfile, f"Processing {src} items")

            for entry in srcfldr:
                if entry.is_file():
                    processed += 1
                    dstfile = os.path.join(dst,entry.name)

                    # It is implied here that CheckPath will retry the connection for 10 minutes before giving up
                    path_ok, timeout, error = CheckPath(dst)

                    if path_ok:
                        if not os.path.exists(dstfile) or not indexed(entry,dst):
                            DbgMsg(f"{entry.name} does not exist in {dst}")
                            logwrite(logfile, f"Copying {entry.path} to {dst} @ {datetime.now()}")
                        
                            shutil.copy(entry.path, dstfile)

                            add_index(entry, dstfile)
                        
                            processed += 1
                        else:
                            DbgMsg(f"{entry.name} exists in {dst}")
                            existing += 1
                    elif timeout:
                        raise FileNotFoundError(f"{dst} is unavailable, timed out")
                    elif error is not None:
                        raise FileNotFoundError(f"Path, {dst}, is not accessible")

                if chkflag(src, dst):
                    logwrite(logfile,"Encountered early terminate flag, terminating")
                    completed = False
                            
                    break

                last_logged = periodic(logfile, f"Scanning source, processed {processed} files, {missing_dest} missing so far...", delta, last_logged)

                time.sleep(0.001)
    except Exception as err:
        msg = f"An error occurred with : {err}"
        logwrite(logfile, msg)
        DbgMsg(msg)
        
        completed = False

    #if not completed:
    #    os.remove(data)

    return missing_dest, existing, processed, completed

def BuildParser():
    """Build Cmd line Parser"""

    parser = argparse.ArgumentParser(prog="F-This", description="Dumb shit to deal with")
    parser.add_argument("-d","--debug", action="store_true", help="Enter Debug Mode")
    parser.add_argument("--test", action="store_true", help="Run Test function")
    parser.add_argument("-c","--check", action="store_true", help="Get stats on folders")
    parser.add_argument("--config", help="Config.ini Specification")
    parser.add_argument("-i","--interactive", action="store_true", help="Execute in interactive mode")
    parser.add_argument("-l","--local", help="Also write to local file")
    parser.add_argument("-p","--passover", action="store_true", help="Pass over missing file check, go directly to automatic copying")
    parser.add_argument("-m","--missing", action="store_true", help="If missing file list exists, skip the file scan and use it")
    #parser.add_argument("--src", help="Source Folder to copy from")
    #arser.add_argument("--dst", help="Folder to copy to")

    return parser

def ReadConfig(filename):
    """Read Config file"""

    global fpath, uname, drv, pw, sim_mode
    global interactive, src, dst

    cfg = None
    
    if os.path.exists(filename):
        cfg = configparser.ConfigParser()

        cfg.read(filename)

        config_section = cfg["config"]
        remote_section = cfg["remote"]
        source_section = cfg["source"]
        destination_section = cfg["destination"]

        # Config Stuff
        
        interactive = config_section.getboolean("interactive", False)
        sim_mode = config_section.getboolean("sim_mode", False)
        
        CmdLineMode(interactive)
        DebugMode(config_section.getboolean("debugmode",False))


        # Source Stuff
        src = source_section.get("src_path", src)

        # Dest Stuff
        dst = destination_section.get("dst_path", r"T:\array2\asc")

        # Remote Stuff

        uname = remote_section.get("username", r"harrypotter\ejohnfelt")
        pw = remote_section.get("password", None)

        drv = remote_section.get("drv_letter", r"T:")
        server = remote_section.get("server", r"\\harrypotter.infosec.stonybrook.edu")
        share = remote_section.get("share", r"srv")

        fpath = f"{server}\\{share}"
        
    return cfg

def PrintState():
    """Print Internal Variables State(s)"""

    Msg(f"Debugmode\t: {DebugMode()}")
    Msg(f"CmdLineMode\t: {CmdLineMode()}")
    Msg(f"Sim Mode\t: {sim_mode}")
    fex = os.path.exists(config_filename)
    Msg(f"Config Fname\t: {config_filename} exists {fex}")
    Msg(f"src\t\t: {src}")
    Msg(f"dst\t\t: {dst}")
    Msg(f"Drv\t\t: {drv}")
    Msg(f"fpath\t\t: {fpath}")
    Msg(f"uname\t\t: {uname}")
    status = "Empty" if pw is None else "Defined"
    Msg(f"pw\t\t: {status}")

def test():
    Msg("Test function invoked")

    cfg = ReadConfig(config_filename)

    tpath = r"\\ubuntucntr.infosec.stonybrook.edu\srv"
    tuname = r"WORKGROUP\ejohnfelt"
    tpw = input("Password for share: ")
    
    result = Connect(tpath,"S:",tuname,tpw)  # result.returncode == 0 completed successfully

    # boolean, true if timeout exceeded, Exception encountered
    path_ok, timeout, error = CheckPath(r"S:\storage")

    if path_ok:
        Msg("Path is good")
    else:
        Msg("Path is a problem")

    result = Disconnect("S:")
    
    PrintState()

    print("Done with test")

if __name__ == "__main__":
    CmdLineMode(True)
    
    parser = BuildParser()

    DbgMsg("About to parse")
    args = parser.parse_args()
    DbgMsg("After parse")

    interactive = args.interactive

    if args.config:
        config_filename = args.config

    if os.path.exists(config_filename):
        cfg = ReadConfig(config_filename)

    #if args.src is not None:
    #    src = args.src
    #if args.dst is not None:
    #    dst = args.dst

    if args.debug:
        DebugMode(args.debug)

    DbgMsg("Starting run")

    log=f"{dst}\\{log_filename}"
    missing_csv=f"{dst}\\{missing_filename}"

    copied = 0
    processed = 0
    completed = True
    alternative_log = None

    if args.test:
        test()
    else:
        result = Connect(fpath,drv,uname,pw)

        if result is Exception:
            # Failed hard
            pass
        elif result.returncode != 0:
            # Failed
            pass
    
        with open(log, "wt") as logfile:
            logs.append(logfile)

            if args.local is not None:
                alternative_log = open(args.local,"at")
                logs.append(alternative_log)

            if args.debug:
                debug_file = open(debug_log,"at")
                logs.append(debug_file)
                debug_mode = True
        
            started = datetime.now()

            if args.missing and os.path.exists(missing_csv):
                copied, completed = copy_known_missing(logs, missing_csv, src, dst)
            elif not args.passover:
                try:
                    logwrite(logfile, f"Starting scandir - {datetime.now()}")

                    missing_from_dest_count, existing, processed, completed = get_missing(logs, missing_csv, src, dst)
    
                    if args.check:
                        logwrite(logs, f"Processed\t: {processed}\nExisting\t: {existing}\nMissing\t: {missing_from_dest_count}")
                    elif completed:
                        logwrite(logs, f"Starting copy - {datetime.now()}")
                        copied, completed = copy_known_missing(logs, missing_csv, src, dst)
                    else:
                        msg = "get_missing() did not seem to complete"

                        logwrite(logs, msg)
                        DbgMsg(msg)
            
                    ended = datetime.now()
                    duration = ended - started
        
                    logwrite(logs, f"Ending copy : {ended} after {duration}\n{processed} files processed and {copied} copied")
                except Exception as err:
                    logwrite(logs, f"An error occurred with : {err}")
            else:
                copied, completed = copy_missing(logs, src, dst)

            if alternative_log is not None:
                alternative_log.close()

            if debug_mode:
                debug_file.close()

        result = Disconnect(drv)
            
