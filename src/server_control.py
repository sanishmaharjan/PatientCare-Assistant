#!/usr/bin/env python3
"""
Utility script to control the PatientCare Assistant servers (API and Frontend)
"""

import os
import sys
import argparse
import subprocess
import signal
import time
import psutil
import socket
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("server_control")

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import API_HOST, API_PORT, FRONTEND_PORT


def is_port_in_use(host, port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except socket.error:
            return True


def free_port(port):
    """Free up a port by killing any process using it"""
    try:
        if sys.platform == 'win32':
            # Windows command
            os.system(f'for /f "tokens=5" %a in (\'netstat -ano ^| find ":{port}"\') do taskkill /f /pid %a')
        else:
            # Unix/Mac command
            os.system(f"lsof -t -i:{port} | xargs -r kill -9")
        time.sleep(1)  # Give time for the process to be killed
        return True
    except Exception as e:
        logger.error(f"Error freeing port {port}: {e}")
        return False


def find_server_processes():
    """Find running API and Frontend server processes"""
    api_processes = []
    frontend_processes = []
    
    # Get absolute paths for more reliable detection
    api_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api", "app.py")
    frontend_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "app.py")
    
    # Normalize paths for comparison
    api_script_path = os.path.normpath(api_script_path)
    frontend_script_path = os.path.normpath(frontend_script_path)
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmd = proc.info['cmdline']
            if not cmd:
                continue
            cmd_str = ' '.join(cmd)
            
            # More robust API server detection
            # Check for both uvicorn processes and direct Python execution of app.py
            if (
                ('uvicorn' in cmd_str.lower() and 'app:app' in cmd_str) or
                ('uvicorn' in cmd_str.lower() and ('app.py' in cmd_str or 'api/app.py' in cmd_str)) or
                ('python' in cmd_str.lower() and 'uvicorn' in cmd_str.lower()) or
                ('python' in cmd_str.lower() and ('api/app.py' in cmd_str or api_script_path in cmd_str))
            ):
                api_processes.append(proc)
            
            # Improved Streamlit frontend detection
            if (
                'streamlit' in cmd_str and ('frontend/app.py' in cmd_str or 'app.py' in cmd_str or
                                          frontend_script_path in cmd_str)
            ):
                frontend_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return api_processes, frontend_processes


def start_servers(api=True, frontend=True):
    """Start the API and/or Frontend servers"""
    success = True
    
    if api:
        try:
            # First check if port is in use and kill any process using it
            if is_port_in_use(API_HOST, API_PORT):
                logger.info(f"Port {API_PORT} is already in use. Attempting to free it...")
                if not free_port(API_PORT):
                    logger.error(f"Failed to free port {API_PORT}. Aborting API server start.")
                    success = False
            
            if success:
                # Start the API server using uvicorn directly to ensure it stays running
                api_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api")
                if not os.path.exists(api_dir):
                    logger.error(f"API directory not found: {api_dir}")
                    success = False
                else:
                    # Run the app.py directly to enable advanced logging
                    api_process = subprocess.Popen([
                        sys.executable, "app.py",
                        "--log-level", "debug" if logger.level <= logging.DEBUG else "info"
                    ], cwd=api_dir)
                    
                    # Check if process started successfully
                    if api_process.poll() is None:
                        logger.info(f"API server started at http://{API_HOST}:{API_PORT}")
                    else:
                        logger.error("Failed to start API server. Process exited immediately.")
                        success = False
        except Exception as e:
            logger.error(f"Error starting API server: {e}")
            success = False
    
    if frontend:
        try:
            # First check if port is in use and kill any process using it
            if is_port_in_use("localhost", FRONTEND_PORT):
                logger.info(f"Port {FRONTEND_PORT} is already in use. Attempting to free it...")
                if not free_port(FRONTEND_PORT):
                    logger.error(f"Failed to free port {FRONTEND_PORT}. Aborting Frontend server start.")
                    if api:  # Only return failure if we're not also starting API
                        success = False
            
            frontend_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "app.py")
            if not os.path.exists(frontend_script):
                logger.error(f"Frontend script not found: {frontend_script}")
                success = False
            else:
                frontend_process = subprocess.Popen([
                    sys.executable, "-m", "streamlit", "run", frontend_script,
                    "--server.port", str(FRONTEND_PORT),
                    "--server.address", "localhost"
                ])
                
                # Check if process started successfully
                if frontend_process.poll() is None:
                    logger.info(f"Frontend server started at http://localhost:{FRONTEND_PORT}")
                else:
                    logger.error("Failed to start Frontend server. Process exited immediately.")
                    success = False
        except Exception as e:
            logger.error(f"Error starting Frontend server: {e}")
            success = False
            
    return success


def stop_servers(api=True, frontend=True):
    """Stop the API and/or Frontend servers"""
    api_processes, frontend_processes = find_server_processes()
    success = True
    
    if api:
        if api_processes:
            api_stopped_count = 0
            api_failed_count = 0
            for proc in api_processes:
                try:
                    pid = proc.info['pid']
                    logger.info(f"Stopping API server (PID: {pid})...")
                    proc.kill()
                    
                    # Check if process is really killed
                    try:
                        # Wait for up to 5 seconds for process to terminate
                        for _ in range(10):
                            if not psutil.pid_exists(pid):
                                break
                            time.sleep(0.5)
                        
                        if psutil.pid_exists(pid):
                            logger.warning(f"API server process (PID: {pid}) still exists after kill command")
                            # Try more forceful termination
                            os.kill(pid, signal.SIGKILL)
                            api_failed_count += 1
                        else:
                            api_stopped_count += 1
                    except Exception as e:
                        logger.error(f"Error while verifying process termination: {e}")
                        api_failed_count += 1
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, Exception) as e:
                    logger.error(f"Failed to stop API server process (PID: {proc.info['pid']}): {e}")
                    api_failed_count += 1
            
            if api_failed_count == 0:
                logger.info(f"API server stopped successfully ({api_stopped_count} processes)")
            else:
                logger.warning(f"Some API processes could not be stopped ({api_failed_count} failed, {api_stopped_count} succeeded)")
                success = False
        else:
            logger.info("No running API server found")
    
    if frontend:
        if frontend_processes:
            frontend_stopped_count = 0
            frontend_failed_count = 0
            for proc in frontend_processes:
                try:
                    pid = proc.info['pid']
                    logger.info(f"Stopping Frontend server (PID: {pid})...")
                    proc.kill()
                    
                    # Check if process is really killed
                    try:
                        # Wait for up to 5 seconds for process to terminate
                        for _ in range(10):
                            if not psutil.pid_exists(pid):
                                break
                            time.sleep(0.5)
                        
                        if psutil.pid_exists(pid):
                            logger.warning(f"Frontend server process (PID: {pid}) still exists after kill command")
                            # Try more forceful termination
                            os.kill(pid, signal.SIGKILL)
                            frontend_failed_count += 1
                        else:
                            frontend_stopped_count += 1
                    except Exception as e:
                        logger.error(f"Error while verifying process termination: {e}")
                        frontend_failed_count += 1
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, Exception) as e:
                    logger.error(f"Failed to stop Frontend server process (PID: {proc.info['pid']}): {e}")
                    frontend_failed_count += 1
            
            if frontend_failed_count == 0:
                logger.info(f"Frontend server stopped successfully ({frontend_stopped_count} processes)")
            else:
                logger.warning(f"Some Frontend processes could not be stopped ({frontend_failed_count} failed, {frontend_stopped_count} succeeded)")
                success = False
        else:
            logger.info("No running Frontend server found")
            
    return success


def restart_servers(api=True, frontend=True):
    """Restart the API and/or Frontend servers"""
    logger.info("Restarting servers...")
    
    # Stop the servers
    stop_success = stop_servers(api=api, frontend=frontend)
    if not stop_success:
        logger.warning("Some servers may not have stopped cleanly. Continuing with restart...")
    
    # Give more time for processes to fully terminate
    logger.info("Waiting for processes to terminate completely...")
    time.sleep(3)
    
    # Check if any processes are still running
    api_processes, frontend_processes = find_server_processes()
    if (api and api_processes) or (frontend and frontend_processes):
        logger.warning("Some server processes are still running after stop command")
        
        # Try to force kill again
        if api and api_processes:
            logger.info("Attempting to force kill remaining API processes...")
            for proc in api_processes:
                try:
                    os.kill(proc.info['pid'], signal.SIGKILL)
                except Exception as e:
                    logger.error(f"Failed to force kill API process: {e}")
                    
        if frontend and frontend_processes:
            logger.info("Attempting to force kill remaining Frontend processes...")
            for proc in frontend_processes:
                try:
                    os.kill(proc.info['pid'], signal.SIGKILL)
                except Exception as e:
                    logger.error(f"Failed to force kill Frontend process: {e}")
        
        # Wait a bit more
        time.sleep(2)
    
    # Start the servers
    start_success = start_servers(api=api, frontend=frontend)
    
    if start_success:
        logger.info("Servers restarted successfully")
        return True
    else:
        logger.error("Failed to restart some servers")
        return False


def status_servers():
    """Check the status of API and Frontend servers"""
    api_processes, frontend_processes = find_server_processes()
    
    # Check if ports are actually in use
    api_port_in_use = is_port_in_use(API_HOST, API_PORT)
    frontend_port_in_use = is_port_in_use("localhost", FRONTEND_PORT)
    
    if api_processes:
        if len(api_processes) > 1:
            logger.info(f"✅ API server is running at http://{API_HOST}:{API_PORT} with {len(api_processes)} processes")
        else:
            logger.info(f"✅ API server is running at http://{API_HOST}:{API_PORT}")
            
        for proc in api_processes:
            pid = proc.info['pid']
            try:
                # Get process status, memory usage and running time
                p = psutil.Process(pid)
                process_info = p.as_dict(attrs=['create_time', 'memory_info', 'status'])
                
                # Calculate uptime
                uptime_seconds = time.time() - process_info['create_time']
                hours, remainder = divmod(uptime_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                uptime_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
                
                # Get memory usage in MB
                memory_mb = process_info['memory_info'].rss / 1024 / 1024
                
                # Show extended info
                logger.info(f"   Process ID: {pid} | Status: {process_info['status']} | Memory: {memory_mb:.1f} MB | Uptime: {uptime_str}")
            except Exception:
                logger.info(f"   Process ID: {pid}")
        
        if not api_port_in_use:
            logger.warning(f"   ⚠️ API process detected, but port {API_PORT} is not in use! Server might not be functioning correctly.")
    else:
        logger.info("❌ API server is not running")
        if api_port_in_use:
            logger.warning(f"   ⚠️ Port {API_PORT} is in use but no API server process was detected!")
    
    if frontend_processes:
        if len(frontend_processes) > 1:
            logger.info(f"✅ Frontend server is running at http://localhost:{FRONTEND_PORT} with {len(frontend_processes)} processes")
        else:
            logger.info(f"✅ Frontend server is running at http://localhost:{FRONTEND_PORT}")
            
        for proc in frontend_processes:
            pid = proc.info['pid']
            try:
                # Get process status, memory usage and running time
                p = psutil.Process(pid)
                process_info = p.as_dict(attrs=['create_time', 'memory_info', 'status'])
                
                # Calculate uptime
                uptime_seconds = time.time() - process_info['create_time']
                hours, remainder = divmod(uptime_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                uptime_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
                
                # Get memory usage in MB
                memory_mb = process_info['memory_info'].rss / 1024 / 1024
                
                # Show extended info
                logger.info(f"   Process ID: {pid} | Status: {process_info['status']} | Memory: {memory_mb:.1f} MB | Uptime: {uptime_str}")
            except Exception:
                logger.info(f"   Process ID: {pid}")
                
        if not frontend_port_in_use:
            logger.warning(f"   ⚠️ Frontend process detected, but port {FRONTEND_PORT} is not in use! Server might not be functioning correctly.")
    else:
        logger.info("❌ Frontend server is not running")
        if frontend_port_in_use:
            logger.warning(f"   ⚠️ Port {FRONTEND_PORT} is in use but no Frontend server process was detected!")
            
    # Return status so other functions can use it
    return {
        'api_running': len(api_processes) > 0,
        'api_port_in_use': api_port_in_use,
        'api_processes': api_processes,
        'frontend_running': len(frontend_processes) > 0,
        'frontend_port_in_use': frontend_port_in_use,
        'frontend_processes': frontend_processes
    }


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Control PatientCare Assistant servers")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--start", action="store_true", help="Start servers")
        group.add_argument("--stop", action="store_true", help="Stop servers")
        group.add_argument("--restart", action="store_true", help="Restart servers")
        group.add_argument("--status", action="store_true", help="Check server status")
        
        parser.add_argument("--api", action="store_true", help="Only affect API server")
        parser.add_argument("--frontend", action="store_true", help="Only affect Frontend server")
        parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
        
        args = parser.parse_args()
        
        # Set logging level based on verbose flag
        if args.verbose:
            logger.setLevel(logging.DEBUG)
            logger.debug("Verbose logging enabled")
        
        # If neither --api nor --frontend is specified, affect both
        api = True
        frontend = True
        if args.api and not args.frontend:
            frontend = False
            logger.info("Running operation for API server only")
        elif args.frontend and not args.api:
            api = False
            logger.info("Running operation for Frontend server only")
        else:
            logger.info("Running operation for both API and Frontend servers")
        
        success = True
        if args.start:
            success = start_servers(api=api, frontend=frontend)
        elif args.stop:
            success = stop_servers(api=api, frontend=frontend)
        elif args.restart:
            success = restart_servers(api=api, frontend=frontend)
        elif args.status:
            status = status_servers()
            # Status doesn't return a success flag
            success = True
        
        # Exit with appropriate status code
        if not success:
            logger.error("Operation completed with errors")
            sys.exit(1)
        else:
            logger.debug("Operation completed successfully")
            sys.exit(0)
            
    except KeyboardInterrupt:
        logger.info("\nOperation interrupted by user")
        sys.exit(130)  # 128 + SIGINT value (2)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        if args and getattr(args, 'verbose', False):
            import traceback
            logger.error(traceback.format_exc())
        sys.exit(1)
