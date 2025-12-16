export interface Question {
  'question-id': number;
  'question-title': string;
  'question-body': string;
  'username': string;
  'creation-time': string;
  'city-id': number;
  'answer-count'?: number; // Opsiyonel olarak ekleyebiliriz
  'vote-count'?: number;
}