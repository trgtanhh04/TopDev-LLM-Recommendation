export function parseJobDescription(desc) {
  // Remove brackets and quotes, then split by \n
  let arr = [];
  try {
    arr = JSON.parse(desc.replace(/'/g, '"'));
  } catch {
    arr = [desc];
  }
  // Join all lines, split by \n, trim, and filter empty
  return arr
    .join('\n')
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0);
}