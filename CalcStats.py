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
            if not file.endswith('.png'):
                continue
            ts, category = file.split('_', 1)
            ts = ts[:8]
            category = category.replace('.png', '')
            if ts not in stats:
                stats[ts] = {category : 1}
            elif category not in stats[ts]:
                stats[ts][category] = 1
            else:
                stats[ts][category] += 1
            os.remove(os.path.join(root, file))
    writeStats(stats)
    f = 0
    p = 0
    for x in stats.values():
        if 'easy_pass' in x:
            p += x['easy_pass']
        if 'easy_quit' in x:
            f += x['easy_quit']
    print('Overall drop rate in Easy is %.3f%%' % (p / (p+f) * 100))
    return


if __name__ == "__main__":
    main()
