/**
 * Education content data for the QAQC Report Generator.
 * Contains info cards for graphs, assay methods, commodities, and QAQC concepts.
 */

export type TopicCategory = 'graphs' | 'methods' | 'commodities' | 'qaqc';

export interface EducationTopic {
  id: string;
  category: TopicCategory;
  title: string;
  icon: string;           // Lucide icon name
  summary: string;        // 1-2 sentences
  keyPoints: string[];    // 3-5 bullet points
  whenToUse?: string;     // Practical guidance
  example?: string;       // Brief example
  relatedTopics?: string[];
}

export const CATEGORY_INFO: Record<TopicCategory, { label: string; description: string }> = {
  graphs: {
    label: 'Graphs & Charts',
    description: 'Visual tools for analyzing and presenting QAQC data'
  },
  methods: {
    label: 'Assay Methods',
    description: 'Laboratory techniques for determining element concentrations'
  },
  commodities: {
    label: 'Commodities',
    description: 'Common minerals and elements analyzed in exploration'
  },
  qaqc: {
    label: 'QAQC Concepts',
    description: 'Quality assurance and quality control fundamentals'
  }
};

export const EDUCATION_TOPICS: EducationTopic[] = [
  // ===== GRAPHS =====
  {
    id: 'control-chart',
    category: 'graphs',
    title: 'Control Chart (Shewhart)',
    icon: 'LineChart',
    summary: 'A time-series plot showing measurements against control limits to detect out-of-control processes.',
    keyPoints: [
      'Center line represents the target or mean value',
      'Upper and Lower Control Limits (UCL/LCL) are typically set at ±3 standard deviations',
      'Points outside control limits indicate potential problems',
      'Used primarily for monitoring CRM/standards performance',
      'Can detect trends, shifts, and cycles in data'
    ],
    whenToUse: 'Use when monitoring laboratory performance over time with certified reference materials.',
    relatedTopics: ['cusum-chart', 'standards-crms']
  },
  {
    id: 'bland-altman',
    category: 'graphs',
    title: 'Bland-Altman Plot',
    icon: 'ScatterChart',
    summary: 'Compares two measurement methods by plotting the mean of pairs against their difference to reveal systematic bias.',
    keyPoints: [
      'X-axis shows the mean of original and duplicate values',
      'Y-axis shows the difference between measurements',
      'Horizontal line at mean difference reveals systematic bias',
      'Limits of agreement (±1.96 SD) show 95% of differences',
      'Superior to correlation for detecting bias'
    ],
    whenToUse: 'Use when comparing duplicate analyses or different laboratories to detect systematic bias.',
    example: 'If the mean difference line is at +0.05 g/t, the original measurements are consistently 0.05 g/t higher than duplicates.',
    relatedTopics: ['duplicates', 'rpd-scatter']
  },
  {
    id: 'cusum-chart',
    category: 'graphs',
    title: 'CUSUM Chart',
    icon: 'TrendingUp',
    summary: 'Cumulative sum chart that detects small, persistent drift in process mean that control charts might miss.',
    keyPoints: [
      'Plots cumulative sum of deviations from target value',
      'Horizontal trend indicates stable process',
      'Upward slope indicates positive drift (values above target)',
      'Downward slope indicates negative drift',
      'More sensitive to small shifts than Shewhart charts'
    ],
    whenToUse: 'Use for early detection of laboratory drift before individual values fail control limits.',
    relatedTopics: ['control-chart', 'standards-crms']
  },
  {
    id: 'rpd-scatter',
    category: 'graphs',
    title: 'RPD Scatter Plot',
    icon: 'GitBranch',
    summary: 'Plots Relative Percent Difference against grade with a hyperbolic precision envelope.',
    keyPoints: [
      'Shows duplicate precision across the grade range',
      'Hyperbolic envelope accounts for higher RPD at low grades',
      'Fixed RPD limit applies at higher grades (typically 20%)',
      'Green points pass, red points fail the precision criteria',
      'Industry-standard visualization for duplicate QA'
    ],
    whenToUse: 'Use when assessing field or pulp duplicate precision across varying grades.',
    example: 'At 0.01 g/t Au, 50% RPD may be acceptable due to detection limits. At 10 g/t Au, only 10% RPD is expected.',
    relatedTopics: ['duplicates', 'bland-altman']
  },
  {
    id: 'histogram',
    category: 'graphs',
    title: 'Histogram',
    icon: 'BarChart3',
    summary: 'Distribution plot showing the frequency of values across bins to understand data spread and normality.',
    keyPoints: [
      'Reveals data distribution shape (normal, skewed, bimodal)',
      'Mean and standard deviation lines help assess centrality',
      'Useful for identifying outliers and data quality issues',
      'Can compare expected vs actual distributions',
      'Essential for statistical assumption checking'
    ],
    whenToUse: 'Use when understanding the distribution of assay results or QAQC measurements.',
    relatedTopics: ['control-chart']
  },
  {
    id: 'scatter-plot',
    category: 'graphs',
    title: 'Scatter Plot',
    icon: 'CircleDot',
    summary: 'Plots two variables against each other to visualize correlation and identify the 1:1 relationship.',
    keyPoints: [
      '1:1 line shows perfect agreement between measurements',
      'R² value quantifies correlation strength',
      'Useful for comparing original vs duplicate or lab vs lab',
      'Outliers are easily identified as points far from the line',
      'Does not reveal systematic bias as well as Bland-Altman'
    ],
    whenToUse: 'Use for quick visual assessment of duplicate agreement or multi-element correlations.',
    relatedTopics: ['bland-altman', 'duplicates']
  },

  // ===== ASSAY METHODS =====
  {
    id: 'fire-assay',
    category: 'methods',
    title: 'Fire Assay',
    icon: 'Flame',
    summary: 'The gold standard for precious metals analysis using high-temperature fusion with lead collection.',
    keyPoints: [
      'Most accurate method for gold and PGE analysis',
      'Uses lead oxide flux to collect precious metals',
      'Typical sample size: 30-50 grams',
      'Detection limits: ~0.005 ppm for Au',
      'Gravimetric finish for high-grade samples'
    ],
    whenToUse: 'Use for all gold exploration and resource definition. Required for JORC-compliant reporting.',
    example: 'A 50g fire assay with AAS finish provides detection to 0.01 ppm Au, suitable for most exploration.',
    relatedTopics: ['gold', 'standards-crms']
  },
  {
    id: 'pxrf',
    category: 'methods',
    title: 'pXRF (Portable XRF)',
    icon: 'Zap',
    summary: 'Handheld X-ray fluorescence for rapid, non-destructive multi-element analysis in the field.',
    keyPoints: [
      'Instant results in 30-120 seconds per sample',
      'Non-destructive - sample can be re-analyzed',
      'Best for elements with atomic number >20 (Ca and heavier)',
      'Limited for light elements and low concentrations',
      'Requires matrix-matched calibration'
    ],
    whenToUse: 'Use for field screening, grade control, and rapid decision-making. Always validate with laboratory assays.',
    example: 'pXRF can detect Cu >50 ppm accurately, useful for mapping copper mineralization in real-time.',
    relatedTopics: ['copper', 'zinc-lead']
  },
  {
    id: 'photon-assay',
    category: 'methods',
    title: 'PhotonAssay',
    icon: 'Sun',
    summary: 'Gamma-ray activation analysis providing rapid, non-destructive bulk gold analysis.',
    keyPoints: [
      'Analyzes 500g to 3kg samples for better representation',
      'Results in 2 minutes per sample',
      'Non-destructive - entire sample measured',
      'Reduces nugget effect issues with large sample mass',
      'Detection limit ~0.02 ppm Au'
    ],
    whenToUse: 'Use for coarse gold deposits where nugget effect is a concern, or when rapid turnaround is critical.',
    relatedTopics: ['gold', 'fire-assay']
  },
  {
    id: 'icp-oes',
    category: 'methods',
    title: 'ICP-OES',
    icon: 'Sparkles',
    summary: 'Inductively Coupled Plasma Optical Emission Spectrometry for multi-element analysis.',
    keyPoints: [
      'Analyzes 30+ elements simultaneously',
      'Requires sample digestion (4-acid or aqua regia)',
      'Detection limits typically 0.1-10 ppm',
      'Cost-effective for multi-element suites',
      'May not achieve total digestion of refractory minerals'
    ],
    whenToUse: 'Use for base metals exploration and pathfinder element analysis.',
    relatedTopics: ['copper', 'zinc-lead', 'nickel']
  },
  {
    id: 'aas',
    category: 'methods',
    title: 'AAS (Atomic Absorption)',
    icon: 'Atom',
    summary: 'Atomic Absorption Spectrometry for single-element analysis with excellent sensitivity.',
    keyPoints: [
      'Measures one element at a time',
      'Excellent precision and accuracy',
      'Common finish for fire assay (Au, Pt, Pd)',
      'Graphite furnace AAS for ultra-low detection',
      'Being replaced by ICP methods in many labs'
    ],
    whenToUse: 'Use as the finish method for fire assay or when specific single-element precision is required.',
    relatedTopics: ['fire-assay', 'gold']
  },

  // ===== COMMODITIES =====
  {
    id: 'gold',
    category: 'commodities',
    title: 'Gold (Au)',
    icon: 'Gem',
    summary: 'Precious metal requiring specialized sampling and assay methods due to nugget effect.',
    keyPoints: [
      'Fire assay is the industry standard method',
      'Nugget effect requires larger sample sizes',
      'Screen fire assay for coarse gold',
      'Typical detection limit: 0.005-0.01 ppm',
      'JORC requires rigorous QAQC protocols'
    ],
    whenToUse: 'Understanding gold-specific challenges is essential for any Au exploration program.',
    relatedTopics: ['fire-assay', 'photon-assay', 'duplicates']
  },
  {
    id: 'copper',
    category: 'commodities',
    title: 'Copper (Cu)',
    icon: 'CircleDollarSign',
    summary: 'Base metal analyzed by various methods depending on grade and deposit type.',
    keyPoints: [
      'ICP-OES/MS after 4-acid digestion is standard',
      'pXRF effective for grades >100 ppm',
      'Consider copper speciation for oxide vs sulfide',
      'Acid-soluble copper may require specific methods',
      'Check for incomplete digestion in refractory ores'
    ],
    whenToUse: 'Copper projects require attention to mineralogy and appropriate digestion methods.',
    relatedTopics: ['icp-oes', 'pxrf']
  },
  {
    id: 'silver',
    category: 'commodities',
    title: 'Silver (Ag)',
    icon: 'Star',
    summary: 'Precious metal often co-occurring with gold, lead-zinc, or copper deposits.',
    keyPoints: [
      'Fire assay with gravimetric finish for high grades',
      'ICP-OES/MS for lower concentrations',
      'Can be lost in sample preparation if not careful',
      'Consider Ag:Au ratios for deposit characterization',
      'Important by-product credit in many deposits'
    ],
    whenToUse: 'Silver analysis protocols depend on grade range and associated commodities.',
    relatedTopics: ['gold', 'zinc-lead', 'fire-assay']
  },
  {
    id: 'zinc-lead',
    category: 'commodities',
    title: 'Zinc-Lead (Zn-Pb)',
    icon: 'Layers',
    summary: 'Base metals commonly occurring together in sediment-hosted and VMS deposits.',
    keyPoints: [
      'ICP-OES after 4-acid digestion is standard',
      'pXRF effective for grade control',
      'Often analyzed with Ag, Cu, and pathfinders',
      'High grades may require dilution',
      'Consider sulfide vs oxide mineralogy'
    ],
    whenToUse: 'Zn-Pb projects benefit from multi-element analysis to understand metal zonation.',
    relatedTopics: ['icp-oes', 'pxrf', 'silver']
  },
  {
    id: 'nickel',
    category: 'commodities',
    title: 'Nickel (Ni)',
    icon: 'Hexagon',
    summary: 'Battery metal with different analytical requirements for sulfide vs laterite deposits.',
    keyPoints: [
      'Sulfide Ni: 4-acid digest with ICP finish',
      'Laterite Ni: May require fusion for complete recovery',
      'Consider Ni speciation (sulfide vs silicate)',
      'MgO, Fe, Co are key associated elements',
      'Class 1 vs Class 2 nickel distinction important'
    ],
    whenToUse: 'Nickel deposit type determines optimal analytical approach.',
    relatedTopics: ['icp-oes', 'copper']
  },
  {
    id: 'iron-ore',
    category: 'commodities',
    title: 'Iron Ore (Fe)',
    icon: 'Mountain',
    summary: 'Bulk commodity requiring high-precision analysis for product specification.',
    keyPoints: [
      'XRF is primary method for Fe and impurities',
      'Tight specifications for SiO2, Al2O3, P, S',
      'LOI (Loss on Ignite) is critical specification',
      'Consider Fe²⁺ vs Fe³⁺ for some products',
      'Sample preparation homogeneity is crucial'
    ],
    whenToUse: 'Iron ore analysis focuses on product quality parameters as much as grade.',
    relatedTopics: ['pxrf']
  },
  {
    id: 'lithium',
    category: 'commodities',
    title: 'Lithium (Li)',
    icon: 'Battery',
    summary: 'Critical battery metal requiring specialized analysis due to its light atomic mass.',
    keyPoints: [
      'ICP-OES/MS after 4-acid or fusion digest',
      'pXRF cannot detect Li (too light)',
      'Consider Li in spodumene vs brine chemistry',
      'Associated elements: Cs, Ta, Sn, Be',
      'Li2O conversion factor: Li × 2.153'
    ],
    whenToUse: 'Lithium projects require laboratory analysis; field methods have limitations.',
    relatedTopics: ['icp-oes']
  },

  // ===== QAQC CONCEPTS =====
  {
    id: 'standards-crms',
    category: 'qaqc',
    title: 'Standards (CRMs)',
    icon: 'Award',
    summary: 'Certified Reference Materials with known values used to monitor laboratory accuracy.',
    keyPoints: [
      'Use matrix-matched CRMs (similar to your samples)',
      'Insert at 1:20 to 1:50 ratio (2-5%)',
      'Monitor on control charts with ±2SD limits',
      'Investigate failures immediately',
      'Use multiple CRMs covering your grade range'
    ],
    whenToUse: 'CRMs are essential for every assay batch to verify laboratory accuracy.',
    example: 'If a 1.0 g/t Au CRM returns 1.15 g/t consistently, the lab may have a +15% bias.',
    relatedTopics: ['control-chart', 'cusum-chart', 'insertion-rates']
  },
  {
    id: 'blanks',
    category: 'qaqc',
    title: 'Blanks',
    icon: 'Square',
    summary: 'Barren material inserted to detect contamination during sample preparation and analysis.',
    keyPoints: [
      'Coarse blanks detect prep contamination',
      'Fine blanks (pulp) detect lab contamination',
      'Insert after high-grade samples',
      'Failure threshold typically 3-5× detection limit',
      'Critical for gold due to smearing risk'
    ],
    whenToUse: 'Insert blanks after every high-grade sample and randomly at 2-5% rate.',
    example: 'A blank returning 0.5 g/t Au after a 50 g/t sample indicates serious contamination.',
    relatedTopics: ['insertion-rates']
  },
  {
    id: 'duplicates',
    category: 'qaqc',
    title: 'Duplicates',
    icon: 'Copy',
    summary: 'Repeat samples measuring precision at different stages of the sampling process.',
    keyPoints: [
      'Field duplicates: measure geological variability',
      'Coarse duplicates: measure prep precision',
      'Pulp duplicates: measure analytical precision',
      'RPD <20% typically acceptable for most elements',
      'Lower grades tolerate higher RPD'
    ],
    whenToUse: 'Use different duplicate types to identify where variability is introduced.',
    example: 'Poor field duplicate precision may indicate nugget effect or sampling issues, not lab problems.',
    relatedTopics: ['rpd-scatter', 'bland-altman']
  },
  {
    id: 'insertion-rates',
    category: 'qaqc',
    title: 'Insertion Rates',
    icon: 'Percent',
    summary: 'The frequency of QAQC samples inserted into the sample stream.',
    keyPoints: [
      'JORC typically requires 5% each: standards, blanks, duplicates',
      'Total QAQC: 15-20% of all samples',
      'Higher rates for critical programs',
      'Must be representative across all batches',
      'Track and report actual vs target rates'
    ],
    whenToUse: 'Plan QAQC insertion before sampling begins and monitor compliance throughout.',
    relatedTopics: ['standards-crms', 'blanks', 'duplicates']
  },
  {
    id: 'jorc-compliance',
    category: 'qaqc',
    title: 'JORC Compliance',
    icon: 'ShieldCheck',
    summary: 'Australasian code for reporting Exploration Results, Mineral Resources, and Ore Reserves.',
    keyPoints: [
      'Table 1 requires QAQC documentation',
      'Competent Person must sign off on data quality',
      'Requires documented sampling and assay methods',
      'QAQC results must be discussed and interpreted',
      'Similar codes: NI 43-101 (Canada), SAMREC (South Africa)'
    ],
    whenToUse: 'All public reporting of exploration results must follow JORC or equivalent codes.',
    relatedTopics: ['insertion-rates', 'standards-crms']
  },
  {
    id: 'accuracy-precision',
    category: 'qaqc',
    title: 'Accuracy vs Precision',
    icon: 'Target',
    summary: 'Two distinct measures of data quality: accuracy measures closeness to true value, precision measures reproducibility.',
    keyPoints: [
      'Accuracy = how close results are to the true value (measured by standards/CRMs)',
      'Precision = how reproducible results are (measured by duplicates)',
      'High accuracy + low precision = scattered around the bullseye',
      'Low accuracy + high precision = tight cluster off-center (systematic bias)',
      'Both are required for reliable QAQC data'
    ],
    whenToUse: 'Understanding the difference helps diagnose whether issues are bias (accuracy) or variability (precision).',
    example: 'A lab returning 1.05 g/t ± 0.02 for a 1.00 g/t CRM has good precision but poor accuracy (5% positive bias).',
    relatedTopics: ['standards-crms', 'duplicates', 'bland-altman']
  }
];

// Helper function to get topics by category
export function getTopicsByCategory(category: TopicCategory): EducationTopic[] {
  return EDUCATION_TOPICS.filter(topic => topic.category === category);
}

// Helper function to get a topic by ID
export function getTopicById(id: string): EducationTopic | undefined {
  return EDUCATION_TOPICS.find(topic => topic.id === id);
}

// Helper function to search topics
export function searchTopics(query: string): EducationTopic[] {
  const lowerQuery = query.toLowerCase();
  return EDUCATION_TOPICS.filter(topic =>
    topic.title.toLowerCase().includes(lowerQuery) ||
    topic.summary.toLowerCase().includes(lowerQuery) ||
    topic.keyPoints.some(point => point.toLowerCase().includes(lowerQuery))
  );
}
