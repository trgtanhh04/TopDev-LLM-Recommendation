/* eslint-disable */
export function parseStringToArray(input) {
  try {
    return input.replace(/[\[\]']/g, '').split(',').map(item => item.trim());
  } catch (error) {
    console.error('Error parsing string to array:', error);
    return [];
  }
}