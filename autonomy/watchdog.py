#!/usr/bin/env python3
"""
🐕 Watchdog - страж стабильности Claude
Следит за критическими сбоями и перезапускает систему
"""

import time
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(
    filename='logs/watchdog.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Watchdog:
    def __init__(self):
        self.last_success_file = Path("state/last_success.txt")
        self.crash_count_file = Path("state/crash_count.txt")
        self.max_crashes = 3
        self.reset_period = 3600  # Сброс счетчика через час
        
    def check_last_success(self):
        """Проверяет время последней успешной операции"""
        if not self.last_success_file.exists():
            return None
            
        try:
            with open(self.last_success_file, 'r') as f:
                last_time = datetime.fromisoformat(f.read().strip())
                return last_time
        except:
            return None
    
    def update_success_time(self):
        """Обновляет время последней успешной операции"""
        self.last_success_file.parent.mkdir(exist_ok=True)
        with open(self.last_success_file, 'w') as f:
            f.write(datetime.now().isoformat())
    
    def get_crash_count(self):
        """Получает счетчик сбоев"""
        if not self.crash_count_file.exists():
            return 0
        
        try:
            with open(self.crash_count_file, 'r') as f:
                data = f.read().strip().split('\n')
                count = int(data[0])
                first_crash = datetime.fromisoformat(data[1])
                
                # Сбрасываем счетчик если прошло много времени
                if datetime.now() - first_crash > timedelta(seconds=self.reset_period):
                    self.reset_crash_count()
                    return 0
                    
                return count
        except:
            return 0
    
    def increment_crash_count(self):
        """Увеличивает счетчик сбоев"""
        count = self.get_crash_count()
        
        with open(self.crash_count_file, 'w') as f:
            if count == 0:
                # Первый сбой - записываем время
                f.write(f"1\n{datetime.now().isoformat()}")
            else:
                # Увеличиваем счетчик, сохраняем время первого сбоя
                with open(self.crash_count_file, 'r') as rf:
                    lines = rf.read().strip().split('\n')
                    first_crash = lines[1] if len(lines) > 1 else datetime.now().isoformat()
                f.write(f"{count + 1}\n{first_crash}")
    
    def reset_crash_count(self):
        """Сбрасывает счетчик сбоев"""
        if self.crash_count_file.exists():
            self.crash_count_file.unlink()
    
    def perform_recovery(self):
        """Выполняет восстановление системы"""
        crash_count = self.get_crash_count()
        
        if crash_count >= self.max_crashes:
            logging.error(f"Слишком много сбоев ({crash_count}), требуется вмешательство")
            # Можно отправить уведомление через Telegram
            return False
        
        logging.info(f"Попытка восстановления #{crash_count + 1}")
        self.increment_crash_count()
        
        try:
            # Жесткий перезапуск
            subprocess.run(['pkill', '-9', '-f', 'claude'], capture_output=True)
            time.sleep(3)
            
            # Запускаем заново
            result = subprocess.run(
                ['./start', '--force', '--quiet'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                logging.info("Система восстановлена")
                self.update_success_time()
                return True
            else:
                logging.error(f"Не удалось восстановить: {result.stderr}")
                return False
                
        except Exception as e:
            logging.error(f"Ошибка восстановления: {str(e)}")
            return False
    
    def monitor(self):
        """Основной цикл мониторинга"""
        last_success = self.check_last_success()
        
        if last_success:
            time_since = datetime.now() - last_success
            
            # Если больше 15 минут без успеха - проблема
            if time_since > timedelta(minutes=15):
                logging.warning(f"Нет активности {time_since.total_seconds()/60:.1f} минут")
                
                # Проверяем здоровье через health monitor
                health_check = subprocess.run(
                    ['python3', 'health_monitor.py'],
                    capture_output=True,
                    text=True
                )
                
                # Если health monitor не справился - восстанавливаем
                if health_check.returncode != 0:
                    self.perform_recovery()
        else:
            # Первый запуск
            self.update_success_time()
            logging.info("Watchdog запущен")

if __name__ == "__main__":
    watchdog = Watchdog()
    watchdog.monitor()