import { parseStringToArray } from './parseStringToArray';

const HEADERS = [
  "About us",
  "Sứ mệnh",
  "Tầm nhìn",
  "Giá trị cốt lõi",
  "Cam kết",
  "Đối tác chiến lược",
  "Hoạt động cộng đồng"
];

function cleanLine(line) {
  return line
    .replace(/\\xa0/g, ' ')
    .replace(/\u00A0/g, ' ')
    .trim();
}

export function parseCompanyProfileToSections(profile) {
  const arr = parseStringToArray(profile).map(cleanLine);
  const sections = [];
  let current = null;

  arr.forEach(line => {
    const header = HEADERS.find(h => line.toLowerCase() === h.toLowerCase());
    if (header) {
      if (current) sections.push(current);
      current = { header, content: [] };
    } else if (current) {
      current.content.push(line);
    } else {
      // If no header yet, treat as "About us"
      current = { header: "About us", content: [line] };
    }
  });
  if (current) sections.push(current);

  // Join content lines into a single paragraph for each section
  return sections.map(section => ({
    header: section.header,
    content: section.content.join(' ')
  }));
}