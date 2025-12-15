export interface Country {
  'country-id': number;
  'country-name': string;
  url: string; // Ülke bayrak URL'si
  info: string;
}

// API'den dönen liste yapısı
export interface CountryListResponse extends Array<Country> {}