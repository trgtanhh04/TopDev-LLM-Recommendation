import { parseStringToArray } from './parseStringToArray';

export function parseCompanyProfile(profile) {
  const arr = parseStringToArray(profile);
  return arr
    .map(line =>
      line
        .replace(/\\xa0/g, ' ')
        .replace(/\u00A0/g, ' ')
        .trim()
    )
    .filter(line => line.length > 0)
    .join(' ');
}