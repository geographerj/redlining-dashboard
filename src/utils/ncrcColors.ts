/**
 * NCRC Brand Colors
 * Based on: Updated NCRC_Brand Guidelines_V19b.pdf
 * Official NCRC Color Palette
 */

export const NCRC_COLORS = {
  // Official NCRC Brand Colors (from Brand Guidelines V19b)
  SKY_BLUE: '#2fade3',            // RGB: 47, 173, 227 - Primary brand color
  DARK_BLUE: '#034ea0',           // RGB: 3, 78, 160 - Secondary blue
  RED: '#e82e2e',                 // RGB: 232, 46, 46 - Accent/warning color
  PURPLE: '#552d87',              // RGB: 85, 45, 135 - Accent color
  PINK: '#eb2f89',                // RGB: 235, 47, 137 - Accent color
  GOLD: '#ffc23a',                // RGB: 255, 194, 58 - Accent/warning color
  GRAY: '#818390',                // RGB: 129, 131, 144 - Neutral gray
  BLACK: '#000000',               // RGB: 0, 0, 0 - Black
  
  // Neutral Colors
  WHITE: '#FFFFFF',
  
  // Gap Analysis Colors (for performance indicators)
  GAP_GREEN: '#C6EFCE',           // Positive gap - Outperforms peers (> 0 pp)
  GAP_YELLOW: '#ffc23a',          // Minor negative gap (0 to -2.0 pp) - Using brand gold
  GAP_ORANGE: '#ffc23a',          // Moderate negative gap (-2.0 to -5.0 pp) - Using brand gold
  GAP_LIGHT_RED: '#e82e2e',      // Large negative gap (-5.0 to -10.0 pp) - Using brand red
  GAP_RED: '#e82e2e',             // Severe negative gap (<-10.0 pp) - Using brand red
  
  // Ratio Colors (for peer comparison)
  RATIO_EXCELLENT: '#C6EFCE',     // Ratio < 1.0 (bank outperforms peers)
  RATIO_GOOD: '#ffc23a',          // Ratio 1.0-1.5 (similar performance) - Brand gold
  RATIO_WARNING: '#ffc23a',       // Ratio 1.5-2.0 (moderate underperformance) - Brand gold
  RATIO_POOR: '#e82e2e',          // Ratio 2.0-3.0 (significant underperformance) - Brand red
  RATIO_SEVERE: '#e82e2e',        // Ratio >= 3.0 (severe underperformance) - Brand red
};

/**
 * Get color for gap value (percentage points)
 * Uses NCRC brand colors where appropriate
 */
export function getGapColor(gap: number | null | undefined): string {
  if (gap === null || gap === undefined) return NCRC_COLORS.WHITE;
  if (gap > 0) return NCRC_COLORS.GAP_GREEN;
  if (gap >= -2.0) return NCRC_COLORS.GAP_YELLOW;  // Brand gold
  if (gap >= -5.0) return NCRC_COLORS.GAP_ORANGE;   // Brand gold
  if (gap >= -10.0) return NCRC_COLORS.GAP_LIGHT_RED; // Brand red
  return NCRC_COLORS.GAP_RED;  // Brand red
}

/**
 * Get color for ratio value (Peer Rate / Bank Rate)
 * Uses NCRC brand colors where appropriate
 */
export function getRatioColor(ratio: number | null | undefined): string {
  if (ratio === null || ratio === undefined) return NCRC_COLORS.WHITE;
  if (ratio < 1.0) return NCRC_COLORS.RATIO_EXCELLENT;
  if (ratio < 1.5) return NCRC_COLORS.RATIO_GOOD;  // Brand gold
  if (ratio < 2.0) return NCRC_COLORS.RATIO_WARNING; // Brand gold
  if (ratio < 3.0) return NCRC_COLORS.RATIO_POOR; // Brand red
  return NCRC_COLORS.RATIO_SEVERE; // Brand red
}

/**
 * Get text color for ratio/gap cells (white for dark backgrounds)
 */
export function getTextColor(backgroundColor: string): string {
  const darkColors = [NCRC_COLORS.GAP_RED, NCRC_COLORS.RATIO_SEVERE];
  return darkColors.includes(backgroundColor) ? NCRC_COLORS.WHITE : NCRC_COLORS.BLACK;
}

