from criminal_offence_segmentation.utils import list_all_files
from criminal_offence_segmentation.plot_extraction import PlotExtraction

import os

root = "/home/tangxuan/data/law"
res_hit_dir = '/home/tangxuan/data/confession3.0/hit'
res_miss_dir = '/home/tangxuan/data/confession3.0/miss'


def extract_judgement_and_plot(fname):
    extractor = PlotExtraction(fname)
    return extractor.extract_confession_plot(), extractor.judgement


if __name__ == '__main__':
    filenames = []
    list_all_files(root, filenames)

    cnt = 0
    for fname in filenames:
        plot, judgement = extract_judgement_and_plot(fname)

        if judgement is None:  # no judgement in the legal instrument.
            continue
        fname = os.path.split(fname)[1]
        res_dir = res_miss_dir
        if plot:
            res_dir = res_hit_dir
        fname = os.path.join(res_dir, fname)
        out = open(fname, 'a', encoding='utf-8')
        if plot:
            out.write('坦白情节：\n')
            out.write('\t')
            out.write(plot)
            out.write('\n\n')

        out.write('判决结果：\n')
        out.write('\t')
        out.write(judgement)
        out.close()

        cnt += 1
        if cnt > 100000:
            break
