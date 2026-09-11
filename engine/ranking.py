from dataclasses import dataclass
from typing import List
@dataclass
class Candidate:
    start: float; end: float; hook: str; reason: str; category: str; score: float

def score_candidate(text: str, duration: float, brief: str='') -> float:
    words=len(text.split()); hook=min(100,35+len(text[:100])*0.45); density=min(100,40+words/max(duration,1)*12); standalone=85 if text.strip().endswith(('.', '?', '!')) else 68; relevance=90 if brief and any(w.lower() in text.lower() for w in brief.split() if len(w)>4) else 75
    return round(hook*.28+density*.22+standalone*.25+relevance*.25,1)

def refine_boundaries(segments, start, end):
    before=[s for s in segments if s['end']<=start][-1:]
    after=[s for s in segments if s['start']>=end][:1]
    return (max(0,before[0]['start'] if before else start-2), after[0]['end'] if after else end)

def rank_candidates(candidates: List[Candidate], count=5):
    return sorted(candidates,key=lambda x:x.score,reverse=True)[:count]
