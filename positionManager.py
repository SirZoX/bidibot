import json
import os
import time

class PositionManager:
    def __init__(self, positionsPath):
        self.positionsPath = positionsPath
        self.positions = self.loadPositions()

    def loadPositions(self):
        if os.path.exists(self.positionsPath):
            with open(self.positionsPath, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}

    def savePositions(self):
        with open(self.positionsPath, "w", encoding="utf-8") as f:
            json.dump(self.positions, f, indent=2)

    def syncWithExchange(self, remotePositions):
        toRemove = []
        for posId, pos in self.positions.items():
            found = any(rp['symbol'] == pos['symbol'] and rp['side'] == pos['side'] for rp in remotePositions)
            if not found:
                print(f"Position {pos['symbol']} ({pos['side']}) not found in exchange, removing from JSON.")
                toRemove.append(posId)
        for posId in toRemove:
            self.positions.pop(posId)
        for rp in remotePositions:
            posId = f"bdbot_{rp['symbol']}_{rp['side']}_{int(time.time())}"
            if not any(pos['symbol'] == rp['symbol'] and pos['side'] == rp['side'] for pos in self.positions.values()):
                self.positions[posId] = {
                    "symbol": rp['symbol'],
                    "side": rp['side'],
                    "entry": rp.get('entryPrice'),
                    "tp": rp.get('takeProfit'),
                    "sl": rp.get('stopLoss'),
                    "oco": rp.get('ocoOrders', {}),
                    "timestamp": int(time.time())
                }
                print(f"Added missing position from exchange: {rp['symbol']} ({rp['side']})")
        self.savePositions()

    def addPosition(self, posId, posData):
        self.positions[posId] = posData
        self.savePositions()

    def removePosition(self, posId):
        if posId in self.positions:
            self.positions.pop(posId)
            self.savePositions()
