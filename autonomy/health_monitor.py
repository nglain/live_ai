#!/usr/bin/env python3
"""
🏥 Health Monitor - мониторинг здоровья Claude сессии
"""

import subprocess
import time
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    filename='health_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class HealthMonitor:
    def __init__(self):
        self.health_file = Path("state/claude_health.txt")
        self.health_file.parent.mkdir(exist_ok=True)
        
    def check_claude_health(self):
        """Проверяет здоровье Claude сессии"""
        try:
            # Пробуем простую команду
            result = subprocess.run(
                ['claude', '--no-markdown'],
                input="echo 'health check'",
                text=True,
                capture_output=True,
                timeout=10
            )
            
            # Проверяем признаки живой сессии
            output = result.stdout.lower()
            stderr = result.stderr.lower()
            
            healthy_signs = [
                "? for shortcuts",
                "auto-accept edits on",
                "health check",
                "claude>"
            ]
            
            unhealthy_signs = [
                "command not found",
                "session expired",
                "error",
                "failed"
            ]
            
            # Анализируем здоровье
            is_healthy = any(sign in output for sign in healthy_signs)
            is_unhealthy = any(sign in stderr for sign in unhealthy_signs)
            
            if is_healthy and not is_unhealthy:
                self._update_health_status("HEALTHY")
                return True
            else:
                self._update_health_status("UNHEALTHY")
                return False
                
        except subprocess.TimeoutExpired:
            logging.error("Claude health check timeout")
            self._update_health_status("TIMEOUT")
            return False
        except Exception as e:
            logging.error(f"Health check error: {str(e)}")
            self._update_health_status("ERROR")
            return False
    
    def _update_health_status(self, status):
        """Обновляет файл статуса здоровья"""
        with open(self.health_file, 'w') as f:
            f.write(f"{status}\n{datetime.now().isoformat()}")
        logging.info(f"Health status: {status}")
    
    def restart_if_needed(self):
        """Перезапускает Claude если нужно"""
        if not self.check_claude_health():
            logging.warning("Claude unhealthy, attempting restart...")
            
            # Используем скрипт start для перезапуска
            try:
                # Определяем путь к скрипту
                script_dir = Path(__file__).parent
                start_script = script_dir / 'start'
                
                result = subprocess.run(
                    [str(start_script), '--force', '--quiet'],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=script_dir
                )
                
                if result.returncode == 0:
                    logging.info("Claude restarted successfully via start script")
                    self._update_health_status("RESTARTED")
                    return True
                else:
                    logging.error(f"Failed to restart Claude: {result.stderr}")
                    return False
                    
            except subprocess.TimeoutExpired:
                logging.error("Restart timeout")
                return False
            except Exception as e:
                logging.error(f"Restart error: {str(e)}")
                return False
        
        return True

if __name__ == "__main__":
    monitor = HealthMonitor()
    monitor.restart_if_needed()