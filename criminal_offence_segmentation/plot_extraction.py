from pyltp import SentenceSplitter
from .legal_instrument_segmentation import InstrumentSegmentation

import synonyms
import re


class PlotExtraction(object):
    def __init__(self, instrument_path):
        self.instrument_path = instrument_path
        self.judgement = None
        self.confession_key = '如实 供述 供认 所犯罪行 犯罪事实 系坦白 主动坦白 具有坦白情节'
        self.confession_filter_keys = ['辩称', '辩护人', '自首']
        self.confession_legal_term = '第六十七条第三款'

    def extract_confession_plot(self):
        if self.judgement is None:
            inst_seg = InstrumentSegmentation()
            self.judgement = inst_seg.extract_judgement(self.instrument_path)
            if self.judgement is None:
                return None

        plots = SentenceSplitter.split(self.judgement)

        contain_confession_legal_term = False
        plot_with_confession_legal_term_only = None

        sims = [self._try(plot) for plot in plots]
        max_sim_idx = sims.index(max(sims))
        max_sim = sims[max_sim_idx]

        hit = max_sim > 0.5
        uncertain = 0.3 < max_sim <= 0.5
        miss = max_sim <= 0.3

        if hit:
            return plots[max_sim_idx]

        for plot in plots:
            if plot.find(self.confession_legal_term) != -1:
                contain_confession_legal_term = True
                plot_with_confession_legal_term_only = plot
                break

        if uncertain and contain_confession_legal_term:
            return plots[max_sim_idx]

        if miss and contain_confession_legal_term:
            return plot_with_confession_legal_term_only

        return None

    def _filter_confession(self, plot):
        match_obj = re.search('|'.join(self.confession_filter_keys), plot)
        return True if match_obj is None else False

    def _try(self, plot):
        if not self._filter_confession(plot):
            return 0
        max_sim = 0
        subs = plot.split('，')
        for sub in subs:
            if len(sub) < 1:
                continue
            sim = synonyms.compare(self.confession_key, plot, seg=True)
            if sim > max_sim:
                max_sim = sim

        return max_sim
