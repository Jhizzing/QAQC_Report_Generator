/**
 * Validation utilities for form inputs and data.
 * Provides validation functions with clear error messages.
 */

export interface ValidationResult {
    valid: boolean;
    error?: string;
}

export interface ValidationRule<T = any> {
    validate: (value: T) => ValidationResult;
    message?: string;
}

/**
 * Validate that a value is not empty
 */
export function validateRequired(value: any): ValidationResult {
    if (value === null || value === undefined || value === '') {
        return { valid: false, error: 'This field is required' };
    }
    if (typeof value === 'string' && value.trim() === '') {
        return { valid: false, error: 'This field cannot be empty' };
    }
    return { valid: true };
}

/**
 * Validate that a value is a number
 */
export function validateNumber(value: any): ValidationResult {
    if (value === null || value === undefined || value === '') {
        return { valid: false, error: 'A number is required' };
    }
    const num = typeof value === 'string' ? parseFloat(value) : Number(value);
    if (isNaN(num)) {
        return { valid: false, error: 'Must be a valid number' };
    }
    return { valid: true };
}

/**
 * Validate that a number is within a range
 */
export function validateNumberRange(
    value: any,
    min?: number,
    max?: number
): ValidationResult {
    const numResult = validateNumber(value);
    if (!numResult.valid) {
        return numResult;
    }

    const num = typeof value === 'string' ? parseFloat(value) : Number(value);

    if (min !== undefined && num < min) {
        return { valid: false, error: `Must be at least ${min}` };
    }
    if (max !== undefined && num > max) {
        return { valid: false, error: `Must be at most ${max}` };
    }
    return { valid: true };
}

/**
 * Validate that a number is positive
 */
export function validatePositive(value: any): ValidationResult {
    return validateNumberRange(value, 0, undefined);
}

/**
 * Validate that a value is a valid percentage (0-100)
 */
export function validatePercentage(value: any): ValidationResult {
    return validateNumberRange(value, 0, 100);
}

/**
 * Validate that a value matches a pattern
 */
export function validatePattern(value: any, pattern: RegExp, message?: string): ValidationResult {
    if (value === null || value === undefined || value === '') {
        return { valid: false, error: message || 'Invalid format' };
    }
    const str = String(value);
    if (!pattern.test(str)) {
        return { valid: false, error: message || 'Invalid format' };
    }
    return { valid: true };
}

/**
 * Validate email format
 */
export function validateEmail(value: any): ValidationResult {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return validatePattern(value, emailPattern, 'Must be a valid email address');
}

/**
 * Validate file extension
 */
export function validateFileExtension(
    file: File | null,
    allowedExtensions: string[]
): ValidationResult {
    if (!file) {
        return { valid: false, error: 'File is required' };
    }

    const extension = file.name.split('.').pop()?.toLowerCase();
    if (!extension || !allowedExtensions.includes(extension)) {
        return {
            valid: false,
            error: `File must be one of: ${allowedExtensions.join(', ')}`,
        };
    }
    return { valid: true };
}

/**
 * Validate file size
 */
export function validateFileSize(
    file: File | null,
    maxSizeMB: number
): ValidationResult {
    if (!file) {
        return { valid: false, error: 'File is required' };
    }

    const maxSizeBytes = maxSizeMB * 1024 * 1024;
    if (file.size > maxSizeBytes) {
        return {
            valid: false,
            error: `File size must be less than ${maxSizeMB}MB`,
        };
    }
    return { valid: true };
}

/**
 * Validate that a value is in a list of allowed values
 */
export function validateOneOf<T>(value: T, allowedValues: T[]): ValidationResult {
    if (!allowedValues.includes(value)) {
        return {
            valid: false,
            error: `Must be one of: ${allowedValues.join(', ')}`,
        };
    }
    return { valid: true };
}

/**
 * Validate that an array has at least one item
 */
export function validateArrayNotEmpty(value: any[]): ValidationResult {
    if (!Array.isArray(value)) {
        return { valid: false, error: 'Must be an array' };
    }
    if (value.length === 0) {
        return { valid: false, error: 'At least one item is required' };
    }
    return { valid: true };
}

/**
 * Validate multiple rules
 */
export function validateAll<T>(
    value: T,
    rules: Array<(val: T) => ValidationResult>
): ValidationResult {
    for (const rule of rules) {
        const result = rule(value);
        if (!result.valid) {
            return result;
        }
    }
    return { valid: true };
}

/**
 * Validate at least one rule passes
 */
export function validateAny<T>(
    value: T,
    rules: Array<(val: T) => ValidationResult>
): ValidationResult {
    for (const rule of rules) {
        const result = rule(value);
        if (result.valid) {
            return { valid: true };
        }
    }
    return {
        valid: false,
        error: 'Value does not meet any validation requirements',
    };
}

/**
 * Validate sample ID format
 */
export function validateSampleID(value: any): ValidationResult {
    if (value === null || value === undefined || value === '') {
        return { valid: false, error: 'Sample ID is required' };
    }
    const str = String(value).trim();
    if (str.length === 0) {
        return { valid: false, error: 'Sample ID cannot be empty' };
    }
    if (str.length > 100) {
        return { valid: false, error: 'Sample ID is too long (max 100 characters)' };
    }
    return { valid: true };
}

/**
 * Validate sample type
 */
export function validateSampleType(value: any): ValidationResult {
    const validTypes = ['STD', 'BLK', 'UNK', 'DUP', 'Standard', 'Blank', 'Unknown', 'Duplicate'];
    return validateOneOf(value, validTypes);
}

/**
 * Validate tolerance value (percentage)
 */
export function validateTolerance(value: any): ValidationResult {
    return validateAll(value, [
        validateRequired,
        validateNumber,
        validatePercentage,
    ]);
}

/**
 * Validate detection limit
 */
export function validateDetectionLimit(value: any): ValidationResult {
    return validateAll(value, [
        validateRequired,
        validateNumber,
        validatePositive,
    ]);
}

/**
 * Create a validator function from rules
 */
export function createValidator<T>(
    rules: Array<(val: T) => ValidationResult>
): (value: T) => ValidationResult {
    return (value: T) => validateAll(value, rules);
}
