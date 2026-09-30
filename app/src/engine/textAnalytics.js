/**
 * Text Analytics Engine
 * JS Port of src/text_analysis/metrics.py
 */

export function countSyllables(word) {
  const w = word.toLowerCase().replace(/[^a-z]/g, '');
  if (!w) return 0;
  if (w.length <= 3) return 1;
  const matches = w.match(/[aeiouy]{1,2}/g);
  let count = matches ? matches.length : 1;
  if (w.endsWith('e') && !w.endsWith('le') && !w.endsWith('ee')) {
    count = Math.max(1, count - 1);
  }
  return Math.max(1, count);
}

export function computeTextMetrics(rawText) {
  if (!rawText || !rawText.trim()) {
    return {
      word_count: 0,
      unique_word_count: 0,
      sentence_count: 0,
      paragraph_count: 0,
      avg_word_length: 0.0,
      avg_sentence_length: 0.0,
      dialogue_percentage: 0.0,
      readability_score: 0.0,
      grade_level: 0.0,
      syllable_count: 0,
      lexical_diversity: 0.0
    };
  }

  // Strip common Gutenberg header boilerplate if present
  let cleaned = rawText.replace(/\*\*\* START OF THE PROJECT GUTENBERG EBOOK [\s\S]*?\*\*\*/i, '');
  cleaned = cleaned.replace(/\*\*\* END OF THE PROJECT GUTENBERG EBOOK [\s\S]*?\*\*\*/i, '');

  const words = (cleaned.toLowerCase().match(/\b[a-z0-9']+\b/g) || []);
  const sentences = cleaned.split(/[.!?]+/).map(s => s.trim()).filter(Boolean);
  const paragraphs = cleaned.split(/\n\s*\n/).map(p => p.trim()).filter(Boolean);

  const word_count = words.length;
  const unique_word_count = new Set(words).size;
  const sentence_count = Math.max(1, sentences.length);
  const paragraph_count = Math.max(1, paragraphs.length);

  const totalChars = words.reduce((acc, w) => acc + w.length, 0);
  const avg_word_length = word_count > 0 ? parseFloat((totalChars / word_count).toFixed(2)) : 0;
  const avg_sentence_length = word_count > 0 ? parseFloat((word_count / sentence_count).toFixed(2)) : 0;

  // Dialogue ratio calculation
  const dialogueMatches = cleaned.match(/"([^"]*)"|“([^”]* logic)”/g) || [];
  let dialogueWordCount = 0;
  dialogueMatches.forEach(quote => {
    const qWords = quote.match(/\b[a-z0-9']+\b/gi);
    if (qWords) dialogueWordCount += qWords.length;
  });
  const dialogue_percentage = word_count > 0 ? parseFloat(((dialogueWordCount / word_count) * 100).toFixed(2)) : 0;

  // Syllables and Flesch Reading Ease / Kincaid Grade Level
  const syllable_count = words.reduce((acc, w) => acc + countSyllables(w), 0);
  const avg_syllables_per_word = word_count > 0 ? syllable_count / word_count : 0;

  let readability_score = 0;
  let grade_level = 0;

  if (word_count > 0 && sentence_count > 0) {
    const flesch = 206.835 - (1.015 * (word_count / sentence_count)) - (84.6 * avg_syllables_per_word);
    readability_score = parseFloat(Math.max(0, Math.min(100, flesch)).toFixed(2));

    const grade = (0.39 * (word_count / sentence_count)) + (11.8 * avg_syllables_per_word) - 15.59;
    grade_level = parseFloat(Math.max(0, grade).toFixed(1));
  }

  const lexical_diversity = word_count > 0 ? parseFloat(((unique_word_count / word_count) * 100).toFixed(1)) : 0;

  return {
    word_count,
    unique_word_count,
    sentence_count,
    paragraph_count,
    avg_word_length,
    avg_sentence_length,
    dialogue_percentage,
    readability_score,
    grade_level,
    syllable_count,
    lexical_diversity
  };
}
