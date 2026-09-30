/**
 * Entity Resolution Algorithm Engine
 * Performs Jaro-Winkler title matching & Levenshtein author reconciliation
 */

export function levenshteinDistance(a, b) {
  if (a.length === 0) return b.length;
  if (b.length === 0) return a.length;

  const matrix = [];
  for (let i = 0; i <= b.length; i++) {
    matrix[i] = [i];
  }
  for (let j = 0; j <= a.length; j++) {
    matrix[0][j] = j;
  }

  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1,
          Math.min(matrix[i][j - 1] + 1, matrix[i - 1][j] + 1)
        );
      }
    }
  }

  return matrix[b.length][a.length];
}

export function levenshteinSimilarity(str1, str2) {
  const s1 = (str1 || '').toLowerCase().trim();
  const s2 = (str2 || '').toLowerCase().trim();
  if (s1 === s2) return 1.0;
  const dist = levenshteinDistance(s1, s2);
  const maxLen = Math.max(s1.length, s2.length);
  if (maxLen === 0) return 1.0;
  return parseFloat((1 - dist / maxLen).toFixed(4));
}

export function jaroDistance(s1, s2) {
  if (s1 === s2) return 1.0;
  const len1 = s1.length;
  const len2 = s2.length;
  if (len1 === 0 || len2 === 0) return 0.0;

  const matchDistance = Math.floor(Math.max(len1, len2) / 2) - 1;
  const s1Matches = new Array(len1).fill(false);
  const s2Matches = new Array(len2).fill(false);

  let matches = 0;
  let transpositions = 0;

  for (let i = 0; i < len1; i++) {
    const start = Math.max(0, i - matchDistance);
    const end = Math.min(i + matchDistance + 1, len2);
    for (let j = start; j < end; j++) {
      if (s2Matches[j]) continue;
      if (s1[i] !== s2[j]) continue;
      s1Matches[i] = true;
      s2Matches[j] = true;
      matches++;
      break;
    }
  }

  if (matches === 0) return 0.0;

  let k = 0;
  for (let i = 0; i < len1; i++) {
    if (!s1Matches[i]) continue;
    while (!s2Matches[k]) k++;
    if (s1[i] !== s2[k]) transpositions++;
    k++;
  }

  return (
    (matches / len1 +
      matches / len2 +
      (matches - transpositions / 2) / matches) /
    3.0
  );
}

export function jaroWinklerSimilarity(str1, str2, p = 0.1) {
  const s1 = (str1 || '').toLowerCase().trim();
  const s2 = (str2 || '').toLowerCase().trim();
  const jaro = jaroDistance(s1, s2);

  if (jaro < 0.7) return parseFloat(jaro.toFixed(4));

  let prefix = 0;
  const maxPrefix = 4;
  for (let i = 0; i < Math.min(s1.length, s2.length, maxPrefix); i++) {
    if (s1[i] === s2[i]) prefix++;
    else break;
  }

  const jw = jaro + prefix * p * (1 - jaro);
  return parseFloat(jw.toFixed(4));
}

export function reconcileEntities(recordA, recordB, config = { titleWeight: 0.55, authorWeight: 0.35, isbnWeight: 0.10, threshold: 0.82 }) {
  const titleScore = jaroWinklerSimilarity(recordA.title, recordB.title);
  const authorScore = levenshteinSimilarity(recordA.author, recordB.author);
  
  const isbnExact = (recordA.isbn && recordB.isbn && recordA.isbn === recordB.isbn) ? 1.0 : 0.0;

  const totalScore = parseFloat(
    (
      titleScore * config.titleWeight +
      authorScore * config.authorWeight +
      isbnExact * config.isbnWeight
    ).toFixed(4)
  );

  const isMatch = totalScore >= config.threshold;

  let matchTier = 'REJECTED';
  if (totalScore >= 0.92) matchTier = 'EXACT_MATCH';
  else if (totalScore >= config.threshold) matchTier = 'FUZZY_MATCH';
  else if (totalScore >= 0.60) matchTier = 'REVIEW_REQUIRED';

  return {
    recordA,
    recordB,
    titleScore,
    authorScore,
    isbnExact,
    totalScore,
    isMatch,
    matchTier,
    thresholdUsed: config.threshold
  };
}
