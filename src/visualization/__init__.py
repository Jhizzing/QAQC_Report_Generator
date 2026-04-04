"""
Visualization utilities for QAQC application.

Produces publication-quality plots styled with the LogiQore dark-on-white
report theme. Every chart is designed to be pasted directly into a
JORC-compliant QAQC report at 300 DPI.
"""

import numpy as np

# ── LogiQore Report Colour Palette ──────────────────────────────────────────
_COLORS = {
    'primary':    '#D97706',   # Amber-600  – data points, main series
    'accent':     '#0369A1',   # Sky-700    – secondary series
    'success':    '#059669',   # Emerald-600
    'danger':     '#DC2626',   # Red-600
    'warning':    '#D97706',   # Amber-600
    'info':       '#2563EB',   # Blue-600
    'muted':      '#64748B',   # Slate-500
    'grid':       '#E2E8F0',   # Slate-200
    'bg':         '#FFFFFF',   # White
    'text':       '#1E293B',   # Slate-800
    'text_light': '#64748B',   # Slate-500
    'sigma2':     '#F59E0B',   # Amber-500   ±2σ warning
    'sigma3':     '#EF4444',   # Red-500     ±3σ action
    'fill_pass':  '#D1FAE5',   # Emerald-100
    'fill_warn':  '#FEF3C7',   # Amber-100
    'fill_fail':  '#FEE2E2',   # Red-100
}

# Shared rcParams applied once per figure
_RC = {
    'font.family':      'sans-serif',
    'font.sans-serif':  ['Inter', 'Helvetica Neue', 'Arial', 'sans-serif'],
    'font.size':        10,
    'axes.titlesize':   13,
    'axes.titleweight': 'bold',
    'axes.labelsize':   11,
    'axes.labelweight': 'medium',
    'axes.linewidth':   0.8,
    'axes.edgecolor':   _COLORS['muted'],
    'axes.facecolor':   _COLORS['bg'],
    'figure.facecolor': _COLORS['bg'],
    'figure.dpi':       300,
    'xtick.labelsize':  9,
    'ytick.labelsize':  9,
    'xtick.color':      _COLORS['text'],
    'ytick.color':      _COLORS['text'],
    'legend.fontsize':  9,
    'legend.framealpha': 0.9,
    'legend.edgecolor': _COLORS['grid'],
    'grid.color':       _COLORS['grid'],
    'grid.linewidth':   0.6,
    'grid.alpha':       0.7,
    'savefig.dpi':      300,
    'savefig.bbox':     'tight',
    'savefig.pad_inches': 0.15,
}


def _apply_style(fig, ax):
    """Apply consistent report styling to an axes object."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(_COLORS['muted'])
    ax.spines['bottom'].set_color(_COLORS['muted'])
    ax.tick_params(axis='both', which='both', length=4, width=0.8,
                   colors=_COLORS['text'])
    ax.grid(True, which='major', axis='both', linewidth=0.5,
            color=_COLORS['grid'], alpha=0.7)
    ax.set_axisbelow(True)
    fig.tight_layout()


def _stat_box(ax, text, loc='upper left'):
    """Add a small statistics text-box."""
    props = dict(boxstyle='round,pad=0.4', facecolor='#F8FAFC',
                 edgecolor=_COLORS['grid'], alpha=0.95)
    xy = {'upper left': (0.03, 0.97), 'upper right': (0.97, 0.97),
          'lower right': (0.97, 0.03)}
    x, y = xy.get(loc, (0.03, 0.97))
    ha = 'right' if 'right' in loc else 'left'
    va = 'bottom' if 'lower' in loc else 'top'
    ax.text(x, y, text, transform=ax.transAxes, fontsize=8.5,
            verticalalignment=va, horizontalalignment=ha, bbox=props,
            color=_COLORS['text'], family='monospace')


class PlotGenerator:
    """
    Generates publication-quality QAQC plots.

    Key plot types:
    - Control charts (Shewhart with ±2σ/±3σ, CUSUM)
    - Scatter plots for duplicates
    - Histograms for distributions
    - Bland-Altman bias plots
    - RPD scatter with hyperbolic envelope
    """

    def __init__(self, config: dict = None) -> None:
        self.config = config or {}
        self.figure_size = self.config.get('figure_size', (8, 5))
        self.dpi = self.config.get('dpi', 300)
        self.style = self.config.get('style', 'seaborn-v0_8')

    # ── Control Chart ───────────────────────────────────────────────────────

    def create_control_chart(self, data: list, limits: dict = None,
                             title: str = "Control Chart") -> dict:
        """
        Shewhart control chart with ±2σ (warning) and ±3σ (action) limits.
        """
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        with plt.rc_context(_RC):
            fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

            data_arr = np.array(data, dtype=float)
            n = len(data_arr)
            x = np.arange(1, n + 1)

            # Derive limits
            center = limits.get('center', np.mean(data_arr)) if limits else np.mean(data_arr)
            sigma = np.std(data_arr, ddof=1) if n > 1 else np.std(data_arr)

            ucl_2 = center + 2 * sigma
            lcl_2 = center - 2 * sigma
            ucl_3 = center + 3 * sigma
            lcl_3 = center - 3 * sigma

            if limits:
                ucl_3 = limits.get('ucl', ucl_3)
                lcl_3 = limits.get('lcl', lcl_3)

            # Shaded bands
            ax.fill_between(x, lcl_3, lcl_2, color=_COLORS['fill_fail'], alpha=0.5, zorder=0)
            ax.fill_between(x, ucl_2, ucl_3, color=_COLORS['fill_fail'], alpha=0.5, zorder=0)
            ax.fill_between(x, lcl_2, ucl_2, color=_COLORS['fill_warn'], alpha=0.35, zorder=0)
            inner_hi = min(ucl_2, center + 1 * sigma)
            inner_lo = max(lcl_2, center - 1 * sigma)
            ax.fill_between(x, inner_lo, inner_hi, color=_COLORS['fill_pass'], alpha=0.4, zorder=0)

            # Limit lines
            ax.axhline(center, color=_COLORS['success'], ls='-', lw=1.8,
                       label=f'Certified Value ({center:.3f})', zorder=2)
            ax.axhline(ucl_2, color=_COLORS['sigma2'], ls='--', lw=1.2,
                       label=f'+2σ ({ucl_2:.3f})', zorder=2)
            ax.axhline(lcl_2, color=_COLORS['sigma2'], ls='--', lw=1.2,
                       label=f'−2σ ({lcl_2:.3f})', zorder=2)
            ax.axhline(ucl_3, color=_COLORS['sigma3'], ls='-.', lw=1.4,
                       label=f'+3σ ({ucl_3:.3f})', zorder=2)
            ax.axhline(lcl_3, color=_COLORS['sigma3'], ls='-.', lw=1.4,
                       label=f'−3σ ({lcl_3:.3f})', zorder=2)

            # Classify points
            ok_mask = (data_arr >= lcl_2) & (data_arr <= ucl_2)
            warn_mask = ((data_arr < lcl_2) | (data_arr > ucl_2)) & \
                        (data_arr >= lcl_3) & (data_arr <= ucl_3)
            fail_mask = (data_arr < lcl_3) | (data_arr > ucl_3)

            # Connecting line
            ax.plot(x, data_arr, color=_COLORS['muted'], lw=1.0, zorder=3, alpha=0.6)

            # Data points
            ax.scatter(x[ok_mask], data_arr[ok_mask], s=48, color=_COLORS['success'],
                       edgecolors='white', linewidths=0.8, zorder=4, label=f'Pass ({ok_mask.sum()})')
            if warn_mask.any():
                ax.scatter(x[warn_mask], data_arr[warn_mask], s=64, color=_COLORS['sigma2'],
                           edgecolors='white', linewidths=0.8, zorder=5, marker='D',
                           label=f'Warning ({warn_mask.sum()})')
            if fail_mask.any():
                ax.scatter(x[fail_mask], data_arr[fail_mask], s=80, color=_COLORS['sigma3'],
                           edgecolors='white', linewidths=0.8, zorder=5, marker='X',
                           label=f'Fail ({fail_mask.sum()})')

            ax.set_xlabel('Sample Number')
            ax.set_ylabel('Measured Value')
            ax.set_title(title, pad=12)
            ax.set_xlim(0.5, n + 0.5)
            ax.legend(loc='upper right', fontsize=8, ncol=2, framealpha=0.9)

            # Stats box
            rsd = (sigma / center * 100) if center != 0 else 0
            _stat_box(ax, (f'n = {n}\n'
                           f'Mean = {np.mean(data_arr):.4f}\n'
                           f'SD = {sigma:.4f}\n'
                           f'RSD = {rsd:.1f}%'))

            _apply_style(fig, ax)

        return {'figure': fig, 'axes': ax, 'data': data, 'limits': limits}

    # ── Scatter Plot (Duplicates) ───────────────────────────────────────────

    def create_scatter_plot(self, x_data: list, y_data: list,
                            title: str = "Scatter Plot") -> dict:
        """Duplicates scatter plot with 1:1 line and ±10%/±20% tolerance bands."""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        with plt.rc_context(_RC):
            fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

            x_arr = np.array(x_data, dtype=float)
            y_arr = np.array(y_data, dtype=float)

            pad = 0.08
            lo = min(x_arr.min(), y_arr.min())
            hi = max(x_arr.max(), y_arr.max())
            span = hi - lo if hi != lo else 1.0
            lo -= span * pad
            hi += span * pad
            diag = np.array([lo, hi])

            # Tolerance bands
            ax.fill_between(diag, diag * 0.8, diag * 1.2, color=_COLORS['fill_warn'],
                            alpha=0.35, label='±20% RPD zone', zorder=0)
            ax.fill_between(diag, diag * 0.9, diag * 1.1, color=_COLORS['fill_pass'],
                            alpha=0.45, label='±10% RPD zone', zorder=0)

            # 1:1 line
            ax.plot(diag, diag, color=_COLORS['text'], ls='-', lw=1.2,
                    label='1:1 Line', zorder=2)

            # Data points
            ax.scatter(x_arr, y_arr, s=52, color=_COLORS['primary'],
                       edgecolors='white', linewidths=0.8, zorder=4, alpha=0.85)

            # R²
            corr = np.corrcoef(x_arr, y_arr)[0, 1]
            r_sq = corr ** 2

            ax.set_xlabel('Original Analysis')
            ax.set_ylabel('Duplicate Analysis')
            ax.set_title(title, pad=12)
            ax.set_xlim(lo, hi)
            ax.set_ylim(lo, hi)
            ax.set_aspect('equal', adjustable='box')
            ax.legend(loc='lower right', fontsize=8, framealpha=0.9)

            # Calculate mean RPD
            means = (x_arr + y_arr) / 2.0
            rpd_vals = np.where(means > 0,
                                np.abs(x_arr - y_arr) / means * 100, 0)

            _stat_box(ax, (f'n = {len(x_arr)} pairs\n'
                           f'R² = {r_sq:.4f}\n'
                           f'Mean RPD = {rpd_vals.mean():.1f}%'))

            _apply_style(fig, ax)

        return {'figure': fig, 'axes': ax, 'x_data': x_data,
                'y_data': y_data, 'r_squared': r_sq}

    # ── Histogram ───────────────────────────────────────────────────────────

    def create_histogram(self, data: list, bins: int = 25,
                         title: str = "Histogram") -> dict:
        """Distribution histogram with mean, median, and ±1σ overlays."""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        with plt.rc_context(_RC):
            fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

            data_arr = np.array(data, dtype=float)
            mean_v = np.mean(data_arr)
            median_v = np.median(data_arr)
            std_v = np.std(data_arr, ddof=1)
            p95 = np.percentile(data_arr, 95)

            n, edges, patches = ax.hist(
                data_arr, bins=bins, color=_COLORS['primary'], alpha=0.75,
                edgecolor='white', linewidth=0.6, zorder=3,
            )

            ax.axvline(mean_v, color=_COLORS['danger'], ls='-', lw=1.6,
                       label=f'Mean: {mean_v:.3f}', zorder=4)
            ax.axvline(median_v, color=_COLORS['accent'], ls='--', lw=1.4,
                       label=f'Median: {median_v:.3f}', zorder=4)
            ax.axvline(mean_v + std_v, color=_COLORS['muted'], ls=':', lw=1.2,
                       label=f'+1σ: {mean_v + std_v:.3f}', zorder=4)
            ax.axvline(mean_v - std_v, color=_COLORS['muted'], ls=':', lw=1.2,
                       label=f'−1σ: {max(0, mean_v - std_v):.3f}', zorder=4)
            ax.axvline(p95, color=_COLORS['sigma2'], ls='-.', lw=1.2,
                       label=f'P95: {p95:.3f}', zorder=4)

            ax.set_xlabel('Concentration')
            ax.set_ylabel('Frequency')
            ax.set_title(title, pad=12)
            ax.legend(loc='upper right', fontsize=8, framealpha=0.9)

            _stat_box(ax, (f'n = {len(data_arr)}\n'
                           f'Mean = {mean_v:.4f}\n'
                           f'SD = {std_v:.4f}\n'
                           f'CV = {std_v / mean_v * 100:.1f}%' if mean_v else ''))

            _apply_style(fig, ax)

        return {'figure': fig, 'axes': ax, 'data': data,
                'mean': mean_v, 'std': std_v, 'bins': edges}

    # ── Time Series ─────────────────────────────────────────────────────────

    def create_time_series(self, data: list, timestamps: list = None,
                           title: str = "Time Series") -> dict:
        """Time-series line plot."""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from datetime import datetime, timedelta

        with plt.rc_context(_RC):
            fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

            if timestamps is None:
                timestamps = [datetime.now() + timedelta(hours=i)
                              for i in range(len(data))]

            ax.plot(timestamps, data, color=_COLORS['primary'], lw=1.4,
                    marker='o', markersize=4, markerfacecolor=_COLORS['primary'],
                    markeredgecolor='white', markeredgewidth=0.6)

            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

            ax.set_xlabel('Time')
            ax.set_ylabel('Value')
            ax.set_title(title, pad=12)

            _apply_style(fig, ax)

        return {'figure': fig, 'axes': ax, 'data': data,
                'timestamps': timestamps}

    # ── RPD Scatter (Hyperbolic Envelope) ───────────────────────────────────

    def create_rpd_scatter(self, original: list, duplicate: list,
                           rpd_limit: float = 20.0,
                           absolute_precision: float = 0.01,
                           title: str = "RPD vs Grade") -> dict:
        """RPD scatter with hyperbolic precision envelope."""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        if len(original) != len(duplicate):
            raise ValueError("Original and duplicate lists must have same length")

        with plt.rc_context(_RC):
            fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

            orig = np.array(original, dtype=float)
            dupl = np.array(duplicate, dtype=float)
            grades = (orig + dupl) / 2.0
            rpd = np.zeros_like(grades)
            nz = grades > 0
            rpd[nz] = np.abs(orig[nz] - dupl[nz]) / grades[nz] * 100

            g_range = np.linspace(max(0.001, grades.min() * 0.5),
                                  grades.max() * 1.2, 300)
            hyp = 100 * np.sqrt(2) * (absolute_precision / g_range)
            envelope = np.maximum(hyp, rpd_limit)

            point_lim = np.maximum(
                100 * np.sqrt(2) * (absolute_precision / np.maximum(grades, 0.001)),
                rpd_limit)
            passed = rpd <= point_lim
            failed = ~passed
            pass_rate = passed.sum() / len(passed) * 100

            ax.fill_between(g_range, 0, envelope, color=_COLORS['fill_pass'],
                            alpha=0.5, zorder=0)
            ax.plot(g_range, envelope, color=_COLORS['text'], lw=1.6,
                    label='Precision Envelope', zorder=2)
            ax.axhline(rpd_limit, color=_COLORS['muted'], ls=':', lw=1.2,
                       label=f'Fixed RPD Limit ({rpd_limit}%)', zorder=2)

            if passed.any():
                ax.scatter(grades[passed], rpd[passed], s=48,
                           color=_COLORS['success'], edgecolors='white',
                           lw=0.6, zorder=4, label=f'Pass ({passed.sum()})')
            if failed.any():
                ax.scatter(grades[failed], rpd[failed], s=60,
                           color=_COLORS['danger'], edgecolors='white',
                           lw=0.6, zorder=5, marker='X',
                           label=f'Fail ({failed.sum()})')

            ax.set_xlabel('Grade (Mean of Pair)')
            ax.set_ylabel('Relative Percent Difference (%)')
            ax.set_title(title, pad=12)
            ax.set_ylim(bottom=0)
            ax.legend(loc='upper right', fontsize=8, framealpha=0.9)

            if grades.max() / max(grades.min(), 0.001) > 100:
                ax.set_xscale('log')

            _stat_box(ax, (f'n = {len(orig)}\n'
                           f'Pass Rate = {pass_rate:.1f}%\n'
                           f'Mean RPD = {rpd.mean():.1f}%'))

            _apply_style(fig, ax)

        return {'figure': fig, 'axes': ax,
                'grades': grades.tolist(), 'rpd_values': rpd.tolist(),
                'passed': passed.tolist(), 'failed': failed.tolist(),
                'pass_rate': pass_rate, 'mean_rpd': rpd.mean(),
                'rpd_limit': rpd_limit,
                'absolute_precision': absolute_precision,
                'n': len(orig)}

    # ── CUSUM Chart ─────────────────────────────────────────────────────────

    def create_cusum_chart(self, values: list, target: float,
                           title: str = "CUSUM Chart") -> dict:
        """Cumulative Sum chart for drift detection."""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        with plt.rc_context(_RC):
            vals = np.array(values, dtype=float)
            n = len(vals)
            devs = vals - target
            cusum = np.cumsum(devs)
            sd = np.std(devs, ddof=1) if n > 1 else 0
            h, k = 4 * sd, 0.5 * sd

            cu, cl = np.zeros(n), np.zeros(n)
            for i in range(n):
                prev_u = cu[i - 1] if i else 0
                prev_l = cl[i - 1] if i else 0
                cu[i] = max(0, prev_u + devs[i] - k)
                cl[i] = max(0, prev_l - devs[i] - k)

            uv = np.where(cu > h)[0]
            lv = np.where(cl > h)[0]

            fig, (ax1, ax2) = plt.subplots(
                2, 1, figsize=(self.figure_size[0], self.figure_size[1] * 1.2),
                dpi=self.dpi, sharex=True)

            x = np.arange(1, n + 1)

            # Top: raw CUSUM
            ax1.fill_between(x, cusum, 0, color=_COLORS['primary'], alpha=0.15, zorder=0)
            ax1.plot(x, cusum, color=_COLORS['primary'], lw=1.6, marker='o',
                     markersize=4, markerfacecolor=_COLORS['primary'],
                     markeredgecolor='white', markeredgewidth=0.6, zorder=3,
                     label='Cumulative Sum')
            ax1.axhline(0, color=_COLORS['success'], ls='-', lw=1.4,
                        label='Target (0)', zorder=2)

            ax1.set_ylabel('Cumulative Sum')
            ax1.set_title(title, pad=12)
            ax1.legend(loc='upper left', fontsize=8)

            if n > 1:
                slope = np.polyfit(range(n), cusum, 1)[0]
                trend = 'Stable' if abs(slope) < 0.1 * sd else \
                        ('Positive Drift' if slope > 0 else 'Negative Drift')
                tc = _COLORS['success'] if trend == 'Stable' else _COLORS['sigma2']
                _stat_box(ax1, f'Trend: {trend}', loc='upper right')

            _apply_style(fig, ax1)

            # Bottom: two-sided CUSUM
            ax2.plot(x, cu, color=_COLORS['danger'], lw=1.4, marker='^',
                     markersize=4, label='Upper CUSUM', zorder=3)
            ax2.plot(x, -cl, color=_COLORS['accent'], lw=1.4, marker='v',
                     markersize=4, label='Lower CUSUM', zorder=3)
            ax2.axhline(h, color=_COLORS['danger'], ls='--', lw=1.2,
                        label=f'UCL (+{h:.3f})', zorder=2)
            ax2.axhline(-h, color=_COLORS['accent'], ls='--', lw=1.2,
                        label=f'LCL (−{h:.3f})', zorder=2)
            ax2.axhline(0, color=_COLORS['muted'], ls=':', lw=0.8, zorder=1)

            if len(uv):
                ax2.scatter([v + 1 for v in uv], [cu[v] for v in uv],
                            color=_COLORS['danger'], s=80, marker='X', zorder=5)
            if len(lv):
                ax2.scatter([v + 1 for v in lv], [-cl[v] for v in lv],
                            color=_COLORS['accent'], s=80, marker='X', zorder=5)

            ax2.set_xlabel('Sample Number')
            ax2.set_ylabel('Two-Sided CUSUM')
            ax2.legend(loc='upper left', fontsize=7, ncol=2)

            _apply_style(fig, ax2)

        return {'figure': fig, 'axes': (ax1, ax2),
                'values': vals.tolist(), 'target': target,
                'cusum': cusum.tolist(),
                'cusum_upper': cu.tolist(), 'cusum_lower': cl.tolist(),
                'decision_interval': h,
                'upper_violations': uv.tolist(),
                'lower_violations': lv.tolist(), 'n': n}

    # ── Bland-Altman ────────────────────────────────────────────────────────

    def create_bland_altman(self, original: list, duplicate: list,
                            title: str = "Bland-Altman Plot") -> dict:
        """Bland-Altman bias plot with limits of agreement."""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        if len(original) != len(duplicate):
            raise ValueError("Original and duplicate lists must have same length")

        with plt.rc_context(_RC):
            fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

            orig = np.array(original, dtype=float)
            dupl = np.array(duplicate, dtype=float)
            means = (orig + dupl) / 2.0
            diffs = orig - dupl
            bias = np.mean(diffs)
            sd = np.std(diffs, ddof=1)
            loa_hi = bias + 1.96 * sd
            loa_lo = bias - 1.96 * sd

            ax.fill_between([means.min() * 0.95, means.max() * 1.05],
                            loa_lo, loa_hi,
                            color=_COLORS['fill_warn'], alpha=0.4, zorder=0)
            ax.axhline(bias, color=_COLORS['danger'], ls='-', lw=1.6,
                       label=f'Mean Diff (Bias): {bias:.4f}', zorder=2)
            ax.axhline(loa_hi, color=_COLORS['sigma2'], ls='--', lw=1.2,
                       label=f'+1.96 SD: {loa_hi:.4f}', zorder=2)
            ax.axhline(loa_lo, color=_COLORS['sigma2'], ls='--', lw=1.2,
                       label=f'−1.96 SD: {loa_lo:.4f}', zorder=2)
            ax.axhline(0, color=_COLORS['muted'], ls=':', lw=0.8, zorder=1)

            ax.scatter(means, diffs, s=48, color=_COLORS['accent'],
                       edgecolors='white', lw=0.6, alpha=0.85, zorder=4)

            ax.set_xlabel('Mean of Original and Duplicate')
            ax.set_ylabel('Difference (Original − Duplicate)')
            ax.set_title(title, pad=12)
            ax.legend(loc='upper right', fontsize=8, framealpha=0.9)

            _stat_box(ax, (f'n = {len(orig)}\n'
                           f'Bias = {bias:.4f}\n'
                           f'SD = {sd:.4f}'))

            _apply_style(fig, ax)

        return {'figure': fig, 'axes': ax,
                'means': means.tolist(), 'differences': diffs.tolist(),
                'bias': bias, 'std': sd,
                'loa_upper': loa_hi, 'loa_lower': loa_lo,
                'n': len(orig)}

    # ── Save ────────────────────────────────────────────────────────────────

    def save_plot(self, plot_data: dict, filename: str,
                  format: str = 'png') -> str:
        """Save a plot to file at 300 DPI."""
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plot_data['figure'].savefig(filename, format=format, dpi=self.dpi,
                                    bbox_inches='tight', facecolor='white',
                                    pad_inches=0.15)
        return filename


class ReportVisualizer:
    """Stub report visualizer class."""
    def __init__(self) -> None:
        pass
