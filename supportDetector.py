
import numpy as np
import os
import time

class SupportDetector:
    @staticmethod
    def findSupportLines(data, minTouches=3, maxViolation=0.05):
        closes = [candle[4] for candle in data]
        lows = [candle[3] for candle in data]
        n = len(closes)
        bestLine = None
        for i in range(n - minTouches):
            for j in range(i + minTouches, n):
                x1, x2 = i, j
                y1, y2 = lows[i], lows[j]
                if x2 == x1:
                    continue
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - slope * x1
                line = [slope * k + intercept for k in range(n)]
                touches = sum(abs(lows[k] - line[k]) < 1e-6 for k in range(n))
                violations = sum(closes[k] > line[k] for k in range(n)) / n
                if touches >= minTouches and violations <= maxViolation:
                    if not bestLine or touches > bestLine['touches']:
                        bestLine = {
                            'slope': slope,
                            'intercept': intercept,
                            'touches': touches,
                            'line': line
                        }
        return bestLine

    @staticmethod
    def plotSupportLine(symbol, data, supportLine, plotsPath):
        import matplotlib.pyplot as plt
        timestamps = [candle[0] for candle in data]
        closes = [candle[4] for candle in data]
        lows = [candle[3] for candle in data]
        line = supportLine['line']
        plt.figure(figsize=(12,5))
        plt.plot(timestamps, closes, label='Close')
        plt.plot(timestamps, lows, label='Low')
        plt.plot(timestamps, line, color='yellow', label='Support Line')
        plt.legend()
        plt.title(f"Support Line for {symbol}")
        plt.xlabel('Timestamp')
        plt.ylabel('Price')
        plotPath = os.path.join(plotsPath, f"{symbol.replace('/', '_')}_{int(time.time())}.png")
        plt.savefig(plotPath)
        plt.close()
        print(f"Plot saved: {plotPath}")
