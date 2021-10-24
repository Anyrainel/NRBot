import os, shutil
import json


def readStats():
    if not os.path.exists('stats.json'):
        return {}
    with open('stats.json', 'r') as f:
        return json.load(f)


def writeStats(stats):
    with open('stats.json', 'w') as f:
        json.dump(stats, f,sort_keys=True, indent=2)
    return


def main():
    stats = readStats()
    for root, dirs, files in os.walk('screenshots'):
        for file in files:
            if not file.endswith('.jpg') or 'result' in file:
                continue
            ts, category = file.split('_', 1)
            ts = ts[:8]
            category = category.replace('.jpg', '')
            if ts not in stats:
                stats[ts] = {category : 1}
            elif category not in stats[ts]:
                stats[ts][category] = 1
            else:
                stats[ts][category] += 1
            os.remove(os.path.join(root, file))
    writeStats(stats)
    q = 0
    p = 0
    w = 0
    l = 0
    for x in stats.values():
        for k, v in x.items():
            if 'pass' in k:
                p += v
            elif 'quit' in k:
                q += v
            elif 'win' in k:
                w += v
            elif 'lose' in k:
                l += v
    if p + q > 0:
        print('Overall drop rate in dark lair quests is %.3f%%' % (p / (p+q) * 100))
    if w + l > 0:
        print('Overall win rate in arena is %.3f%%' % (w / (w+l) * 100))
    return


if __name__ == "__main__":
    main()
