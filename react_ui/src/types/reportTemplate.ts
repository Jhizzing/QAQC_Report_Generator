/**
 * TypeScript types for Report Template System
 * Based on JSON Schema for LogiQore QAQC Report Templates
 */

export type BlockType =
    | 'text_auto'      // Auto-generated narrative
    | 'text_user'      // User input text
    | 'text_mixed'     // Combination of auto + user
    | 'table_auto'     // Auto-generated data table
    | 'table_user'     // User-defined table
    | 'figure_auto'    // Auto-generated chart/figure
    | 'meta';          // Metadata field

export type TemplateType = 'full_report' | 'figure_pack';

export interface TemplateBlock {
    id: string;
    type: BlockType;
    label: string;
    description?: string;
    key?: string;              // Data binding key
    placeholder?: string;      // For user input blocks
    required?: boolean;
    order: number;
}

export interface TemplateSection {
    id: string;
    label: string;
    order: number;
    optional?: boolean;
    blocks: TemplateBlock[];
}

export interface ReportTemplate {
    template_id: string;
    template_type: TemplateType;
    title: string;
    description?: string;
    sections: TemplateSection[];
}

/**
 * User-provided values for template blocks
 */
export interface TemplateUserInput {
    [blockId: string]: string | number | boolean;
}

/**
 * Template validation result
 */
export interface TemplateValidation {
    valid: boolean;
    errors: string[];
    warnings: string[];
}

/**
 * Available data keys for binding
 */
export const DATA_KEYS = {
    // Project metadata
    'project_name': 'Project Name',
    'date_range': 'Date Range',
    'generated_date': 'Generated Date',
    'app_version': 'Application Version',

    // JORC metadata
    'jorc_config.competentPerson': 'Competent Person',
    'jorc_config.companyName': 'Company Name',
    'jorc_config.laboratory': 'Laboratory',
    'jorc_config.drillingCompany': 'Drilling Company',
    'jorc_config.sampleType': 'Sample Type',

    // Report narratives
    'report_purpose': 'Report Purpose',
    'key_findings': 'Key Findings',
    'intro_background': 'Introduction Background',
    'intro_data_summary': 'Data Summary',
    'intro_objectives': 'QAQC Objectives',

    // QAQC Program Overview
    'overview_crms': 'CRM Types and Ranges',
    'overview_blanks': 'Blank Material Description',
    'overview_duplicates': 'Duplicate Types',
    'overview_lab_repeats': 'Lab Repeats',

    // Summary data
    'results.summary.totalSamples': 'Total Samples',
    'results.summary.totalStandards': 'Total Standards',
    'results.summary.totalBlanks': 'Total Blanks',
    'results.summary.totalDuplicates': 'Total Duplicates',
    'results.summary.overallPassRate': 'Overall Pass Rate',

    // Standards
    'table_crm_summary': 'CRM Summary Table',
    'figure_crm_bias': 'CRM Bias Plot',
    'figure_crm_timeseries': 'CRM Time Series',
    'results.standards.statistics': 'Standards Statistics',
    'results.standards.flaggedBatches': 'Flagged Batches',

    // Blanks
    'table_blanks_summary': 'Blanks Summary Table',
    'figure_blanks': 'Blanks Plot',
    'results.blanks.statistics': 'Blanks Statistics',
    'results.blanks.flaggedBlanks': 'Flagged Blanks',

    // Duplicates
    'table_duplicates_summary': 'Duplicates Summary Table',
    'figure_duplicates_scatter': 'Duplicate Scatter Plot',
    'figure_duplicates_precision': 'Precision Envelope Plot',
    'results.duplicates.statistics': 'Duplicates Statistics',
    'results.duplicates.flaggedPairs': 'Flagged Pairs',

    // Lab Performance
    'table_internal_lab': 'Internal Lab Comparison',
    'figure_internal_lab': 'Internal Lab Figure',
    'table_umpire_lab': 'Umpire Lab Comparison',
    'figure_umpire_lab': 'Umpire Lab Figure',

    // JORC & Verification
    'data_verification_summary': 'Data Verification Summary',
    'jorc_mapping': 'JORC 2012 Mapping',
    'auto_recommendations': 'Automated Recommendations',

    // Appendices
    'appendix_crm': 'Full CRM Data',
    'appendix_blanks': 'Full Blank Data',
    'appendix_duplicates': 'Full Duplicate Data',
    'processing_log': 'Processing Log'
} as const;

export type DataKey = keyof typeof DATA_KEYS;
