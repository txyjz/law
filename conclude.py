import os
import random
import shutil

res_hit_dir = '/home/tangxuan/data/confession3.0/hit'
res_miss_dir = '/home/tangxuan/data/confession3.0/miss'


if __name__ == '__main__':
    hits = os.listdir(res_hit_dir)
    misses = os.listdir(res_miss_dir)

    hit_samples = [random.randint(0, len(hits)) for _ in range(300)]
    miss_samples = [random.randint(0, len(misses)) for _ in range(300)]

    for idx in hit_samples:
        src = os.path.join(res_hit_dir, hits[idx])
        dst = os.path.join(res_hit_dir + 'c', hits[idx])
        shutil.copyfile(src, dst)

    for idx in miss_samples:
        src = os.path.join(res_miss_dir, misses[idx])
        dst = os.path.join(res_miss_dir + 'c', misses[idx])
        shutil.copyfile(src, dst)
