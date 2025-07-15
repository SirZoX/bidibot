
import time
import sys
from configManager import ConfigManager
from exchangeManager import ExchangeManager
from positionManager import PositionManager
from supportDetector import SupportDetector
from telegramManager import TelegramManager

configPath = "files/config/config.json"
positionsPath = "files/json/openedPositions.json"
plotsPath = "files/plots"


configManager = ConfigManager(configPath)

# Detect test mode
testMode = '-test' in sys.argv

exchangeManager = ExchangeManager(configManager.config, testMode)
positionManager = PositionManager(positionsPath)
telegramManager = TelegramManager(configManager.config.get("telegramToken"), configManager.config.get("telegramChatId"))


# Sync positions
remotePositions = exchangeManager.fetchPositions()
positionManager.syncWithExchange(remotePositions)

while True:
    for posId, pos in positionManager.positions.items():
        try:
            ticker = exchangeManager.fetchTicker(pos['symbol'])
            lastPrice = ticker['last']
            entry = pos['entry']
            side = pos['side']
            pnl = (lastPrice - entry) / entry if side == 'long' else (entry - lastPrice) / entry
            pnlPct = pnl * 100
            print(f"{pos['symbol']} | {side.upper()} | Entry: {entry:.4f} | Last: {lastPrice:.4f} | PnL: {pnlPct:.2f}% | TP: {pos['tp']:.4f} | SL: {pos['sl']:.4f}")
        except Exception as e:
            print(f"Error evaluating position {pos['symbol']}: {e}")
    time.sleep(10)