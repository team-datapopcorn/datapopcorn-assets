# -*- coding: utf-8 -*-
"""국가데이터처 「2025년 기업생멸행정통계(잠정)」 표19 재현 스크립트.

python reproduce_table19.py            # 같은 폴더의 data/ 를 읽어 파싱·검증하고 fig_out/ 에 차트 4개 저장
python reproduce_table19.py --pdf 파일.pdf  # (선택) 원문 PDF 27쪽을 pypdf로 다시 읽어 같은 파서로 대조

원문 PDF와 기사 본문은 이 패키지에 없습니다. data/table19_raw_lines.csv 는 표19 영역의 행 텍스트(숫자표)만 담고 있습니다.
"""
import os, re, sys, json, hashlib
import pandas as pd

SOURCE_PDF_PAGE = 27        # PDF 파일 기준 쪽 번호 (인쇄 쪽 번호 21)
SOURCE_PRINTED_PAGE = 21
COLUMNS = ['scope', 'observation_year', 'horizon_years', 'birth_year', 'rate_pct', 'pdf_page']
NUM7 = r'((?:-?\d+\.\d\s+){6}-?\d+\.\d)'
ROW_RE = re.compile(r'^(?:(부동산업\s*제외)\s+)?(\d{4})년(p?)\s+' + NUM7 + r'\s*$')
CHG_RE = re.compile(r'^증감\s+' + NUM7 + r'\s*$')

# 원문 표19의 값을 손으로 옮긴 것이 아니라, 파싱 결과가 맞는지 대조만 하는 기대값
EXPECTED = {
    ('전체', 2024, 1): 63.9, ('전체', 2024, 5): 36.5, ('전체', 2023, 1): 64.4, ('전체', 2023, 5): 36.4,
    ('전체', 2021, 2): 54.2, ('전체', 2022, 3): 46.9, ('전체', 2023, 4): 41.0,
    ('부동산업 제외', 2024, 1): 63.7, ('부동산업 제외', 2024, 5): 36.0,
    ('부동산업 제외', 2023, 1): 64.0, ('부동산업 제외', 2023, 5): 35.3,
}


def table19_block(page_text):
    """PDF 27쪽 텍스트에서 '표 19>' 줄부터 '그림 1>' 직전 줄까지를 잘라낸다.
    추출 도구에 따라 '<'가 다른 줄로 떨어지거나 '부동산업제외'처럼 띄어쓰기가 사라지므로 느슨하게 찾는다."""
    lines = page_text.splitlines()
    start = next(i for i, l in enumerate(lines) if '표 19>' in l)
    end = next(i for i, l in enumerate(lines) if i > start and '그림 1>' in l)
    return [l.rstrip() for l in lines[start:end]]


def parse_table19(lines, pdf_page=SOURCE_PDF_PAGE):
    """표19 행 텍스트 → (생존율 긴 표, 공식 증감 행, 잠정 표시 연도).

    잠정 표시 'p'는 위첨자라 추출 도구에 따라 다른 연도 줄에 붙기도 한다(pdftotext -layout은 2023년 줄에 붙음).
    그래서 잠정 연도는 참고로만 돌려주고, 숫자 대조에는 쓰지 않는다.
    '부동산업 제외' 라벨이 처음 나오기 전 행은 전체 산업(원문 표에는 라벨 없음)으로 본다.
    신생 연도 = 관측 연도 - 생존 기간 (원문 정의: n년 생존율 = t-n년 신생기업 중 t년까지 생존 기업 수 / t-n년 신생기업 수)."""
    scope, rates, changes, provisional = '전체', [], [], set()
    for ln in lines:
        s = ' '.join(ln.split())
        m = ROW_RE.match(s)
        if m:
            if m.group(1):
                scope = '부동산업 제외'
            year = int(m.group(2))
            if m.group(3) == 'p':
                provisional.add(year)
            for h, v in enumerate(m.group(4).split(), 1):
                rates.append({'scope': scope, 'observation_year': year, 'horizon_years': h,
                              'birth_year': year - h, 'rate_pct': float(v), 'pdf_page': pdf_page})
            continue
        m = CHG_RE.match(s)
        if m:
            for h, v in enumerate(m.group(1).split(), 1):
                changes.append({'scope': scope, 'horizon_years': h, 'change_pp': float(v), 'pdf_page': pdf_page})
    return pd.DataFrame(rates, columns=COLUMNS), pd.DataFrame(changes), sorted(provisional)


def validate(rates, changes):
    """행 수, 키 중복, 기대값, 공식 증감 행과 계산 차이를 대조한다. 실패하면 AssertionError."""
    assert len(rates) == 56, len(rates)                       # 2 범위 x 4 관측연도 x 7 기간
    assert not rates.duplicated(['scope', 'observation_year', 'horizon_years']).any()
    assert set(rates.scope) == {'전체', '부동산업 제외'}
    assert sorted(rates.observation_year.unique()) == [2021, 2022, 2023, 2024]
    assert (rates.birth_year == rates.observation_year - rates.horizon_years).all()
    key = rates.set_index(['scope', 'observation_year', 'horizon_years']).rate_pct
    for k, v in EXPECTED.items():
        assert key[k] == v, (k, key[k], v)
    assert len(changes) == 14
    w = rates.pivot_table(index=['scope', 'horizon_years'], columns='observation_year', values='rate_pct')
    diff = (w[2024] - w[2023]).round(1)
    off = changes.set_index(['scope', 'horizon_years']).change_pp
    mism = (diff - off.reindex(diff.index)).abs().round(1)
    assert (mism == 0).all(), mism[mism != 0]
    return diff


def setup_font():
    import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    for f in ['/usr/share/fonts/truetype/nanum/NanumGothic.ttf', '/System/Library/Fonts/AppleSDGothicNeo.ttc',
              'C:/Windows/Fonts/malgun.ttf']:
        if os.path.exists(f):
            fm.fontManager.addfont(f)
            plt.rcParams['font.family'] = fm.FontProperties(fname=f).get_name()
            break
    plt.rcParams.update({'axes.unicode_minus': False, 'figure.dpi': 150, 'axes.spines.top': False,
                         'axes.spines.right': False, 'font.size': 11})


C = {'main': '#E8590C', 'sub': '#1C7ED6', 'gray': '#868E96', 'ink': '#212529'}
SOURCE_NOTE = ('자료: 국가데이터처 「2025년 기업생멸행정통계(잠정)」 보도자료 <표 19> (PDF 27쪽, 2026-10-22 발표), '
               '2026-10-24 조회. 2024년 값은 잠정(p).')


def _foot(fig, extra=''):
    fig.text(0.01, -0.02, SOURCE_NOTE + (('\n' + extra) if extra else ''), fontsize=8, color=C['gray'], va='top')


def chart_latest_changes(rates, scope='전체'):
    import matplotlib.pyplot as plt
    k = rates[rates.scope == scope].set_index(['observation_year', 'horizon_years']).rate_pct
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True)
    d1, d5 = k[(2024, 1)] - k[(2023, 1)], k[(2024, 5)] - k[(2023, 5)]
    for ax, h, col in [(axes[0], 1, C['main']), (axes[1], 5, C['sub'])]:
        a, b = k[(2023, h)], k[(2024, h)]
        labels = [f'2023년 관측\n({2023 - h}년 신생)', f'2024년p 관측\n({2024 - h}년 신생)']
        ax.bar(labels, [a, b], color=[C['gray'], col], width=0.55)
        for i, v in enumerate([a, b]):
            ax.text(i, v + 1.2, f'{v:.1f}%', ha='center', fontsize=13, fontweight='bold')
        ax.set_title(f'{h}년 생존율  {b - a:+.1f}%p', loc='left', fontsize=13, color=col)
        ax.set_ylim(0, 80)
    axes[0].set_ylabel('생존율 (%)')
    fig.suptitle(f'1년 생존율은 {abs(d1):.1f}%p 내리고 5년은 {d5:.1f}%p 올랐지만, 네 막대는 모두 다른 해에 생긴 기업이다\n'
                 '전체 산업 · 관측 2023년 → 2024년(p) · 괄호 = 그 비율의 분모가 된 신생 연도',
                 x=0.01, ha='left', fontsize=12)
    plt.tight_layout(rect=(0, 0, 1, 0.93))
    _foot(fig)
    return fig


def chart_cross_section(rates, scope='전체', year=2024):
    import matplotlib.pyplot as plt
    r = rates[(rates.scope == scope) & (rates.observation_year == year)].sort_values('horizon_years')
    fig, ax = plt.subplots(figsize=(11, 4.9))
    colors = [C['main'] if h == 1 else C['sub'] if h == 5 else C['gray'] for h in r.horizon_years]
    labels = [f'{h}년\n({b}년 신생)' for h, b in zip(r.horizon_years, r.birth_year)]
    ax.bar(labels, r.rate_pct, color=colors, width=0.62)
    for i, v in enumerate(r.rate_pct):
        ax.text(i, v + 1.0, f'{v:.1f}', ha='center', fontsize=11)
    ax.set_ylim(0, 75); ax.set_ylabel('생존율 (%)')
    ax.text(6.4, 68, '막대 7개 = 신생 연도가 다른 7개 집단\n한 집단을 7년 따라간 곡선이 아닙니다', ha='right',
            fontsize=10, color=C['ink'])
    ax.set_title(f'{year}년에 한꺼번에 잰 1~7년 생존율: {r.rate_pct.iloc[0]:.1f}%에서 {r.rate_pct.iloc[-1]:.1f}%까지, 막대마다 신생 연도가 다르다\n'
                 f'전체 산업 · 관측 {year}년(p) 한 해의 단면', loc='left', fontsize=12)
    plt.tight_layout(); _foot(fig)
    return fig


def cohort_path(rates, birth_year=2019, scope='전체', horizons=(2, 3, 4, 5)):
    p = rates[(rates.scope == scope) & (rates.birth_year == birth_year) & rates.horizon_years.isin(horizons)]
    return p.sort_values('observation_year').reset_index(drop=True)


def chart_2019_cohort(rates):
    import matplotlib.pyplot as plt
    p = cohort_path(rates)
    fig, ax = plt.subplots(figsize=(11, 4.9))
    x = [f'{o}년 관측\n{h}년 생존율' for o, h in zip(p.observation_year, p.horizon_years)]
    ax.plot(x, p.rate_pct, color=C['main'], lw=2.8, marker='o', ms=9)
    for i, v in enumerate(p.rate_pct):
        ax.text(i, v + 1.6, f'{v:.1f}%', ha='center', fontsize=13, fontweight='bold')
    ax.set_ylim(0, 65); ax.set_ylabel('2019년 신생기업 중 생존 비율 (%)')
    path = ' → '.join(f'{h}년 {v:.1f}%' for h, v in zip(p.horizon_years, p.rate_pct))
    ax.set_title(f'같은 2019년 신생기업을 따라가면 {path}\n'
                 '전체 산업 · 관측 2021~2024년(p)의 각 행에서 신생 연도가 2019인 칸만 선택', loc='left', fontsize=12)
    plt.tight_layout()
    _foot(fig, '표19의 관측 범위는 2021~2024년이라 2019년 신생의 1년 생존율(2020년 관측)은 이 차트에 넣지 않았습니다. '
          '모든 값은 이번 발표본 기준이며 과거 수치는 갱신될 수 있습니다.')
    return fig


def chart_scope_sensitivity(rates):
    import matplotlib.pyplot as plt
    import numpy as np
    w = rates.pivot_table(index=['scope', 'horizon_years'], columns='observation_year', values='rate_pct')
    d = (w[2024] - w[2023]).round(1)
    groups = [(1, '1년 생존율 변화\n(2022년 신생 → 2023년 신생)'), (5, '5년 생존율 변화\n(2018년 신생 → 2019년 신생)')]
    fig, ax = plt.subplots(figsize=(11, 4.9))
    xs = np.arange(2); bw = 0.34
    for j, (sc, col) in enumerate([('전체', C['main']), ('부동산업 제외', C['sub'])]):
        vals = [d[(sc, h)] for h, _ in groups]
        ax.bar(xs + (j - 0.5) * bw, vals, bw, color=col, label=sc)
        for x, v in zip(xs + (j - 0.5) * bw, vals):
            ax.text(x, v + (0.05 if v >= 0 else -0.05), f'{v:+.1f}%p', ha='center',
                    va='bottom' if v >= 0 else 'top', fontsize=12, fontweight='bold')
    ax.axhline(0, color=C['ink'], lw=0.8)
    ax.set_xticks(xs); ax.set_xticklabels([g for _, g in groups])
    ax.set_ylim(-0.9, 1.0); ax.set_ylabel('관측 2023 → 2024년(p) 변화 (%p)')
    ax.legend(frameon=False, loc='upper left')
    ax.set_title('부동산업을 빼도 방향은 같다: 1년은 하락, 5년은 상승. 폭은 범위에 따라 달라진다\n'
                 '전체 산업 vs 부동산업 제외 · 관측 2023년 → 2024년(p)', loc='left', fontsize=12)
    plt.tight_layout()
    _foot(fig, '범위에 따른 폭 차이의 원인(업종 구성 등)은 이 표만으로 판단할 수 없습니다.')
    return fig


CHARTS = [('fig1_latest_changes', chart_latest_changes), ('fig2_cross_section', chart_cross_section),
          ('fig3_2019_cohort', chart_2019_cohort), ('fig4_scope_sensitivity', chart_scope_sensitivity)]


def save_charts(rates, out_dir):
    import matplotlib.pyplot as plt
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for name, fn in CHARTS:
        fig = fn(rates)
        p = os.path.join(out_dir, name + '.webp')
        fig.savefig(p, bbox_inches='tight', pil_kwargs={'quality': 88}, facecolor='white')
        plt.close(fig); paths.append(p)
    return paths


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main(argv):
    import matplotlib
    matplotlib.use('Agg')
    here = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(here, 'data')
    if '--pdf' in argv:
        from pypdf import PdfReader   # pip install pypdf
        pdf = argv[argv.index('--pdf') + 1]
        meta = json.load(open(os.path.join(data, 'source_metadata.json'), encoding='utf-8'))
        print('sha256 일치:', sha256(pdf) == meta['pdf']['sha256'])
        lines = table19_block(PdfReader(pdf).pages[SOURCE_PDF_PAGE - 1].extract_text())
    else:
        lines = pd.read_csv(os.path.join(data, 'table19_raw_lines.csv'), encoding='utf-8-sig').text.tolist()
    rates, changes, prov = parse_table19(lines)
    validate(rates, changes)
    published = pd.read_csv(os.path.join(data, 'survival_rates.csv'), encoding='utf-8-sig')
    same = published[COLUMNS].reset_index(drop=True).equals(rates[COLUMNS].reset_index(drop=True))
    print(f'파싱 {len(rates)}행, 잠정 연도 {prov}, 공개 CSV와 동일: {same}')
    setup_font()
    for p in save_charts(rates, os.path.join(here, 'fig_out')):
        print('saved', p)
    return 0 if same else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
