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

export function parseJobDescriptionToSections(desc) {
  const sections = [
    {
      key: 'responsibility',
      title: 'Trách nhiệm công việc',
      icon: '📝',
      keywords: ['Trách nhiệm công việc'],
    },
    {
      key: 'skill',
      title: 'Kỹ năng & Chuyên môn',
      icon: '💡',
      keywords: ['Kỹ năng & Chuyên môn'],
    },
    {
      key: 'benefit',
      title: 'Phúc lợi dành cho bạn',
      icon: '🎁',
      keywords: ['Phúc lợi dành cho bạn'],
    },
    {
      key: 'interview',
      title: 'Quy trình phỏng vấn',
      icon: '🗂️',
      keywords: ['Quy trình phỏng vấn'],
    },
  ];
  const lines = parseJobDescription(desc);
  let current = null;
  const result = [];
  for (const line of lines) {
    const found = sections.find(s => s.keywords.some(k => line.includes(k)));
    if (found) {
      current = { ...found, items: [] };
      result.push(current);
    } else if (current) {
      current.items.push(line);
    }
  }
  return result;
}